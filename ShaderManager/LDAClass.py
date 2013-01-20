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
        self.globalWidgets['windowMenuConnect'] = pc.menu(label="Connect")
        pc.menuItem(label='File to ygColorCorrect to shader', parent=self.globalWidgets['windowMenuCreate'], c=partial(self.connectNodes, 'fileToYgToShd'))
        pc.menuItem(label='File to ygColorCorrect', parent=self.globalWidgets['windowMenuCreate'], c=partial(self.connectNodes, 'fileToYgToShd'))
        pc.menuItem(label='Node to node', parent=self.globalWidgets['windowMenuCreate'], c=partial(self.connectNodes, 'fileToYgToShd'))
        
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
        self.sAttrWidgets['miscButtonsLayout'] = pc.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'right'), parent=self.sAttrWidgets['layout'])
        pc.text(l="Selected: ", parent=self.sAttrWidgets['miscButtonsLayout'])
        pc.textField(enable=False, parent=self.sAttrWidgets['miscButtonsLayout'], text=self.selectedShader)
        #pc.button(label="Rename", parent=self.sAttrWidgets['miscButtonsLayout'], c=self.renameShader)
        #pc.button(label="Delete", parent=self.sAttrWidgets['miscButtonsLayout'])
        pc.button(label="Select", parent=self.sAttrWidgets['miscButtonsLayout'], c=self.selectShader)
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
        
#    def connectTo(self, outNode, outAttr, inNode, inAttr):
#        
#        outN = pc.PyNode(outNode)
#        inN = pc.PyNode(inNode)
#        outOp = outNode + '.' + outAttr
#        inOp = inNode + '.' + inAttr
        
    def createNode(self, nodeType, *args):
        
        if nodeType == 'aiStandard':
            # Ask for name
            name = self.inputDialog("Create aiStandard", "Enter a name for the node: ")
            
            # Create and assign shader
            aiStd = pc.shadingNode('aiStandard', asShader = True, name=name)
            aiStdSg = pc.sets(renderable=True, noSurfaceShader=True, empty=True, name=name+'SG')
            aiStd.outColor >> aiStdSg.surfaceShader 

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
        

        
        