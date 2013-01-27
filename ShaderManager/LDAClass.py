import pymel.core as pc
from functools import partial

class LDA():
    
    def __init__(self):
        
        # Dictionnary containing all the UI elements
        self.globalWidgets = {}
        # Dictionnary containing all the UI elements for the shaders list
        self.sListWidgets = {}
        # Dictionnary containing all the UI elements for the shaders attributes
        self.sAttrWidgets= {}
        
        # Check if MtoA is loaded
        pluginsRunning = pc.pluginInfo(query=True, listPlugins=True)
        if 'mtoa' not in pluginsRunning:
            raise Exception("MtoA is not loaded! Please load it first then restart the script.")
        
        # Build the UI
        self.buildUI()
        
        # Populate the shader list
        self.refreshList()
        
        # Displays main window
        pc.showWindow(self.globalWidgets['window'])
        
    def buildUI(self):
        """Self explanatory: Build the static UI"""
        
        # Delete windows if already existing
        if pc.window("lookdevAssistant", exists=True):
            pc.deleteUI("lookdevAssistant")
        
        # Main window
        self.globalWidgets['window'] = pc.window("lookdevAssistant", menuBar=True, title="Arnold Lookdev assistant", sizeable=False, h=360, w=500)
        
        # Menu bar
        self.globalWidgets['windowMenuCreate'] = pc.menu(label="Create")
        pc.menuItem(label='new aiStandard', parent=self.globalWidgets['windowMenuCreate'], c=partial(self.createNode, 'aiStandard'))
        pc.menuItem(label='new File', parent=self.globalWidgets['windowMenuCreate'], c=partial(self.createNode, 'file'))
        pc.menuItem(label='new ygColorCorrect', parent=self.globalWidgets['windowMenuCreate'], c=partial(self.createNode, 'ygColorCorrect'))
        self.globalWidgets['windowMenuSeeOnFlat'] = pc.menu(label="See on flat")
        pc.menuItem(label='Diffuse Color', parent=self.globalWidgets['windowMenuSeeOnFlat'], c=partial(self.displayInputOnFlat, 'color'))
        pc.menuItem(label='Specular Color', parent=self.globalWidgets['windowMenuSeeOnFlat'], c=partial(self.displayInputOnFlat, 'KsColor'))
        pc.menuItem(label='Specular Roughness', parent=self.globalWidgets['windowMenuSeeOnFlat'], c=partial(self.displayInputOnFlat, 'specularRoughness'))
        pc.menuItem(divider=True, parent=self.globalWidgets['windowMenuSeeOnFlat'])
        pc.menuItem(label='Revert to aiStandard', parent=self.globalWidgets['windowMenuSeeOnFlat'], c=self.revert)
        
#       import maya.cmds as mc
#       mc.ConnectionEditor()
        
        # Main layout : 2 columns / 1 for the list of the ai* shaders / 1 to access selected shader attributes
        self.globalWidgets['mainLayout'] = pc.rowColumnLayout(nc=2, cw=[(1,100), (2,350)])
        
        # Shaders list layout
        self.globalWidgets['sListLayout'] = pc.frameLayout( label='Shaders list', borderStyle='etchedIn', cll=True, h=360 ,parent=self.globalWidgets['mainLayout'])
        self.sListWidgets['layout'] = pc.columnLayout(parent=self.globalWidgets['sListLayout'])
        self.sListWidgets['list'] = pc.textScrollList(h=300, parent=self.sListWidgets['layout'])
        self.sListWidgets['listRefreshButton'] = pc.button(l='Refresh', w=95, c=self.refreshList)
        
        # Shaders attributes layout
        self.globalWidgets['sAttrLayout'] = pc.frameLayout( label='Shaders attributes', borderStyle='etchedIn', cll=True, h=360, parent=self.globalWidgets['mainLayout'] )
        
        # Setup all callbacks
        self.setupCallbacks()
        
    def refreshList(self, *args):
        """Populate the list in the UI with all aiStandard shaders currently present in the scene
        Raise an exception and abort if no shaders are present."""
        
        # We remove the UI for the attributes, just in case
        self.removeShaderAttributesUI()
        
        # Test if there is any aiStandard shader in the scene
        aiList = pc.ls(exactType='aiStandard')
        if len(aiList) == 0:
            pc.warning("No aiStandard shaders in the scene. Please create one before launching the lookdev assistant.")
        else:
            # Clear the list
            self.sListWidgets['list'].removeAll()
            # Append shaders to the list
            self.sListWidgets['list'].append(aiList)
            
            
    def setupCallbacks(self):
        
        # Refresh the UI with the selected shader
        self.sListWidgets['list'].doubleClickCommand(self.refreshShaderAttributes)
        
    def refreshShaderAttributes(self):
        
        # Set the current shader we're working on
        self.selectedShader = self.sListWidgets['list'].getSelectItem()[0]
        
        self.removeShaderAttributesUI()
   
        # Main layout for shader attributes
        self.sAttrWidgets['layout'] = pc.columnLayout(parent=self.globalWidgets['sAttrLayout'], cal="left")
        
        # Buttons for selecting shader in AA and assign material to current selection
        self.sAttrWidgets['miscButtonsLayout'] = pc.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,50), (2, 60), (3, 120)], parent=self.sAttrWidgets['layout'])
        pc.text(l="Selected: ", parent=self.sAttrWidgets['miscButtonsLayout'])
        pc.textField(enable=False, parent=self.sAttrWidgets['miscButtonsLayout'], text=self.selectedShader)
        # Empty text to complete this row
        pc.text(l="")
        pc.button(label="Select", parent=self.sAttrWidgets['miscButtonsLayout'], c=self.selectShader)
        pc.button(label="Rename", parent=self.sAttrWidgets['miscButtonsLayout'], c=self.renameShader)
        pc.button(label="Assign to selection", parent=self.sAttrWidgets['miscButtonsLayout'], c=self.assignToSelection)
    
        # DIFFUSE
        ###################
        # Label
        self.sAttrWidgets['diffuseLabelLayout'] = pc.rowColumnLayout(nc=2, columnAlign=(1, 'center'), columnAttach=(2, 'both', 0), columnWidth=[(1, 60),(2, 150)], parent=self.sAttrWidgets['layout'])
        pc.text(label='Diffuse ', fn='boldLabelFont', parent=self.sAttrWidgets['diffuseLabelLayout'])
        pc.separator(height=20, style='in', parent=self.sAttrWidgets['diffuseLabelLayout'])
        
        # Controls
        self.sAttrWidgets['diffuseControlsLayout'] = pc.columnLayout(parent=self.sAttrWidgets['layout'])
        pc.attrColorSliderGrp(label="Color", w=200, cw=[(1,50), (2,30)], at = '%s.color' % self.selectedShader, parent=self.sAttrWidgets['diffuseControlsLayout'])
        pc.attrFieldSliderGrp(label="Weight", w=200, cw=[(1,50), (2,50)], min=0, max=1.0, at='%s.Kd' % self.selectedShader, pre=3, parent=self.sAttrWidgets['diffuseControlsLayout'])
        pc.attrFieldSliderGrp(label="Rough", w=200, cw=[(1,50), (2,50)], min=0, max=1.0, at='%s.diffuseRoughness' % self.selectedShader, pre=3, parent=self.sAttrWidgets['diffuseControlsLayout'])
        
        # SPECULAR
        ###################
        # Label
        self.sAttrWidgets['specularLabelLayout'] = pc.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'center'), columnAttach=(2, 'both', 0), columnWidth=[(1, 60),(2, 150)], parent=self.sAttrWidgets['layout'])
        pc.text(label='Specular ', fn='boldLabelFont', parent=self.sAttrWidgets['specularLabelLayout'])
        pc.separator(height=20, style='in')
        
        # Controls
        self.sAttrWidgets['specularControlsLayout'] = pc.columnLayout(parent=self.sAttrWidgets['layout'])
        pc.attrColorSliderGrp(label="Color", w=200, cw=[(1,50), (2,30)], at = '%s.KsColor' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        pc.attrFieldSliderGrp(label="Weight", w=200, cw=[(1,50), (2,50)], pre=3, at = '%s.Ks' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        pc.attrEnumOptionMenuGrp(label="BRDF", w=200, cw=[(1,50)], ei=[(0,'stretched_phong'), (1,'ward_duer'), (2, 'cook_torrance')], at = '%s.specularBrdf' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        pc.attrFieldSliderGrp(label="Rough", w=200, cw=[(1,50), (2,50)], pre=4, at = '%s.specularRoughness' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        pc.attrEnumOptionMenuGrp(label="Fresnel", w=200, cw=[(1,50)], ei=[(0,'No'), (1,'Yes')], at = '%s.specularFresnel' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        pc.attrFieldSliderGrp(label="% at N", w=200, cw=[(1,50), (2,50)], pre=3, at = '%s.Ksn' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
    
        # BUMP MAPPING
        ###################
        # Label
        self.sAttrWidgets['bumpLabelLayout'] = pc.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'center'), columnAttach=(2, 'both', 0), columnWidth=[(1, 60),(2, 150)], parent=self.sAttrWidgets['layout'])
        pc.text(label='Bump ', fn='boldLabelFont', parent=self.sAttrWidgets['bumpLabelLayout'])
        pc.separator( height=20, style='in')
        
        # Controls
        pc.attrNavigationControlGrp(label="Map", cw=[(1,50), (2,120)], at = '%s.normalCamera' % self.selectedShader, parent=self.sAttrWidgets['layout'])

        # Test
        #pc.columnLayout(self.sAttrWidgets['diffuseControlsLayout'], edit=True, enable=False)
        
    def removeShaderAttributesUI(self):
        
        # Remove current UI if it already exists
        if 'layout' in self.sAttrWidgets:
            pc.deleteUI(self.sAttrWidgets['layout'])
            del self.sAttrWidgets['layout']
            
    def assignToSelection(self, *args):
        
        # Controls if selection is not null
        test = pc.ls(sl=1)
        if len(test) == 0:
            raise Exception("Tried to assign '%s' to the current selection but nothing is selected." % self.selectedShader)
        
        # If everything is ok, assign current shader to selection
        pc.hyperShade(assign=self.selectedShader)
        
    def selectShader(self, *args):
        pc.select(self.selectedShader, r=True)
        
    def createNode(self, nodeType, *args):
        
        if nodeType == 'aiStandard':
            # Ask for name
            name = self.inputDialog("Create aiStandard", "Enter a name for the node: ")
            
            # Create and assign shader
            aiStd = pc.shadingNode('aiStandard', asShader = True, name=name)
            aiStdSg = pc.sets(renderable=True, noSurfaceShader=True, empty=True, name=name+'SG')
            aiStd.outColor >> aiStdSg.surfaceShader 
            
            self.refreshList()

        if nodeType == 'file':
            # Ask for name
            name = self.inputDialog("Create file", "Enter a name for the node: ")
            # Ask for location of the file
            location = pc.fileDialog2(fm=1, dialogStyle=2)
            myTex = pc.shadingNode('file', asTexture=True, name=name)     
            myTex.fileTextureName.set(location) 
            
        if nodeType == 'ygColorCorrect':
            # Ask for name
            name = self.inputDialog("Create ygColorCorrect", "Enter a name for the node: ")
            aiStd = pc.shadingNode('ygColorCorrect', asShader = True, name=name)
    
    def inputDialog(self, title, message):
        
        result = pc.promptDialog(title=title, message=message, button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
        if result == 'OK':
            text = pc.promptDialog(query=True, text=True)
            return text
        
    def renameShader(self, *args):
        
        result = self.inputDialog("Rename shader", "Enter new name: ")
        shader = pc.PyNode(self.selectedShader)
        pc.rename(shader, result)
        self.refreshList()
        
    def connectedTo(self, attribute):
        """
        Return the attribute from where the connection originated
        This is useful to know if RGB->RGB or alpha->RGB
        """
        # TODO: Pour le cas du outAlpha, il faut tester si il y a des connections sur colorR, colorB, etc car
        # c'est different de color tout court...
        myShader = pc.PyNode(self.selectedShader)
        connectionOrigin = myShader.attr(attribute).listConnections(c=True, p=True)
        
        if len(connectionOrigin) == 0:
            pc.confirmDialog(title="toto", message="Nothing is connected to %s" % self.selectedShader+'.'+attribute)
            return None, None
        else:
            conType = connectionOrigin[0][1].split('.')[1]
            nodeName = connectionOrigin[0][1].split('.')[0]
        
            return nodeName, conType
                 
    def displayInputOnFlat(self, attribute, *args):
        """Displays attribute input on a aiUtility flat surface"""
        
        # Check if dummy shader exists, create it if not
        if len(pc.ls('dummySHD')) == 0:
            print("#INFO# '{0}' // Dummy shader not present. Creating.".format(self.selectedShader))
            # ShadingGroup creation
            sg = pc.sets(renderable=True, noSurfaceShader=True, empty=True, name="aiUtilitySG")
            # aiUtility creation
            aiUtility = pc.shadingNode("aiUtility", asShader=True, name="dummySHD")
            aiUtility.outColor >> sg.surfaceShader
            # Set shade mode to flat
            aiUtility.shadeMode.set('flat')
        
        # Get the aiUtility node    
        aiUtility = pc.PyNode('dummySHD')
        
        # Clear connections if they exist
        connections = aiUtility.listConnections(d=False, c=True, p=True)
        for con in connections:
            pc.disconnectAttr(con[1],con[0])
            
        # Return input node
        inputNode = self.connectedTo(attribute)
        
        if inputNode != (None, None):
            # Make the connections    
            myNode = pc.PyNode(inputNode[0])
                
            if inputNode[1] == 'outAlpha':
                myNode.attr(inputNode[1]).connect(aiUtility.color.colorR)
                myNode.attr(inputNode[1]).connect(aiUtility.color.colorG)
                myNode.attr(inputNode[1]).connect(aiUtility.color.colorB)
            elif inputNode[1] == 'outColor':
                myNode.attr(inputNode[1]).connect(aiUtility.color)
                
            # Select all objets with current shader and assign dummySHD
            self.replaceMaterial(self.selectedShader, 'dummySHD')
            
    def replaceMaterial(self, mat1, mat2, *args):
        """Replace current material mat1 by another material mat2"""
        pc.hyperShade(o=mat1)
        test = pc.ls(sl=1)
        
        if len(test) > 0:
            pc.hyperShade(assign=mat2)
            
    def revert(self, *args):
        """Revert back to the aiStandard"""
        self.replaceMaterial('dummySHD', self.selectedShader)
    
        

        
        