import pymel.core as pc
from functools import partial

class LookDevAssistant():
    
    def __init__(self):
        """Global constructor"""
        
        # Dictionnary containing all the UI elements
        self.globalWidgets = {}
        # Dictionnary containing all the UI elements for the shaders list
        self.sListWidgets = {}
        # Dictionnary containing all the UI elements for the shaders attributes
        self.sAttrWidgets = {}
        
        # Dictionnary containing all dynamic buttons
        self.dynamicButtons = {}
        
        # Dictionnary containing all secondary UI
        # - List existing nodes UI
        self.listNodesWidgets = {}
        
        # Check if MtoA is loaded
        pluginsRunning = pc.pluginInfo(query=True, listPlugins=True)
        if 'mtoa' not in pluginsRunning:
            raise Exception("MtoA is not loaded! Please load it first then restart the script.")
        
        # Build the UI
        self.UI_Build()
        
        # Populate the shader list
        self.UI_refreshShaders()
        
        # Displays main window
        pc.showWindow(self.globalWidgets['window'])
      
######################################## UI FUNCTIONS ########################################
# > Specific function to help manage the UI
        
    def UI_Build(self):
        """Build the static UI and define the main layouts.
        
        Keyword arguments:
        none
        """
        
        # Delete windows if already existing
        if pc.window("lookdevAssistant", exists=True):
            pc.deleteUI("lookdevAssistant")
        
        # Main window
        self.globalWidgets['window'] = pc.window("lookdevAssistant", menuBar=True, title="Arnold Lookdev assistant", sizeable=False, h=360, w=500)
        
        # Menu bar
        # |-- Creation Menu
        self.globalWidgets['windowMenuCreate'] = pc.menu(label="Create")
        pc.menuItem(label='new aiStandard', parent=self.globalWidgets['windowMenuCreate'], c=partial(self.Maya_createNode, 'aiStandard'))
        pc.menuItem(label='new File', parent=self.globalWidgets['windowMenuCreate'], c=partial(self.Maya_createNode, 'file'))
        pc.menuItem(label='new ygColorCorrect', parent=self.globalWidgets['windowMenuCreate'], c=partial(self.Maya_createNode, 'ygColorCorrect'))
        #pc.menuItem(divider=True)
        #pc.menuItem(label='Complete network', parent=self.globalWidgets['windowMenuCreate'], subMenu=True)
        #pc.menuItem(l="use existing File...", c=partial(self.Maya_createFullNetwork, True))
        #pc.menuItem(l="use new File", c=partial(self.Maya_createFullNetwork, False))
        # |-- See on flat Menu
        self.globalWidgets['windowMenuSeeOnFlat'] = pc.menu(label="See on flat")
        pc.menuItem(label='Diffuse Color', parent=self.globalWidgets['windowMenuSeeOnFlat'], c=partial(self.Maya_focusOn, 'color'))
        pc.menuItem(label='Specular Color', parent=self.globalWidgets['windowMenuSeeOnFlat'], c=partial(self.Maya_focusOn, 'KsColor'))
        pc.menuItem(label='Specular Roughness', parent=self.globalWidgets['windowMenuSeeOnFlat'], c=partial(self.Maya_focusOn, 'specularRoughness'))
        pc.menuItem(divider=True, parent=self.globalWidgets['windowMenuSeeOnFlat'])
        pc.menuItem(label='Revert to aiStandard', parent=self.globalWidgets['windowMenuSeeOnFlat'], c=self.Maya_revertToAiStd)
        
        # Main layout : 2 columns / 1 for the list of the ai* shaders / 1 to access selected shader attributes
        self.globalWidgets['mainLayout'] = pc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 240)])
        
        # Shaders list layout
        self.globalWidgets['sListLayout'] = pc.frameLayout(label='Shaders list', borderStyle='etchedIn', cll=True, h=360 , parent=self.globalWidgets['mainLayout'])
        self.sListWidgets['layout'] = pc.columnLayout(parent=self.globalWidgets['sListLayout'])
        self.sListWidgets['list'] = pc.textScrollList(h=300, parent=self.sListWidgets['layout'])
        self.sListWidgets['listRefreshButton'] = pc.button(l='Refresh', w=95, c=self.UI_refreshShaders)
        
        # Shaders attributes layout
        self.globalWidgets['sAttrLayout'] = pc.frameLayout(label='Shaders attributes', borderStyle='etchedIn', cll=True, h=300, parent=self.globalWidgets['mainLayout'])
        
        # Setup all callbacks
        self.UI_Callbacks()
        
    def UI_refreshShaders(self, *args):
        """Populate the list in the UI with all aiStandard shaders present in the scene.
        
        Keyword arguments:
        none
        
        Return:
        none
        
        Misc:
        Warn if no shaders are present and advise to create one."""
        
        # We remove the UI for the attributes, just in case
        self.UI_removeAttributes()
        
        # Test if there is any aiStandard shader in the scene
        aiList = pc.ls(exactType='aiStandard')
        if len(aiList) == 0:
            pc.warning("No aiStandard shaders in the scene. To get started, please create one and hit refresh.")
        else:
            # Clear the list
            self.sListWidgets['list'].removeAll()
            # Append shaders to the list
            self.sListWidgets['list'].append(aiList)
            
            
    def UI_Callbacks(self):
        """Specific rules when UI events happen.
        
        Keyword arguments:
        none
        
        Return:
        none
        """
        
        # Refresh the UI with the selected shader
        self.sListWidgets['list'].doubleClickCommand(self.UI_refreshAttributes)
        
    def UI_refreshAttributes(self):
        """Display the attributes of the shader that has been selected in the list
        
        Keyword arguments:
        none
        
        Return:
        none
        """
        
        # Set the current shader we're working on
        self.selectedShader = self.sListWidgets['list'].getSelectItem()[0]
        
        # Remove previous shader attributes
        self.UI_removeAttributes()
   
        # Main layout for shader attributes
        self.sAttrWidgets['layout'] = pc.columnLayout(parent=self.globalWidgets['sAttrLayout'], cal="left")
        
        # Buttons for selecting shader in AA and assign material to current selection
        self.sAttrWidgets['selectedShaderLayout'] = pc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 50), (2, 170)], parent=self.sAttrWidgets['layout'])
        pc.text(l="Selected: ", parent=self.sAttrWidgets['selectedShaderLayout'])
        pc.textField(enable=False, parent=self.sAttrWidgets['selectedShaderLayout'], text=self.selectedShader)

        self.sAttrWidgets['miscButtonsLayout'] = pc.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 50), (2, 60), (3, 120)], parent=self.sAttrWidgets['layout'])
        pc.button(label="Select", parent=self.sAttrWidgets['miscButtonsLayout'], c=self.Maya_selectShader)
        pc.button(label="Rename", parent=self.sAttrWidgets['miscButtonsLayout'], c=self.Maya_renameShader)
        pc.button(label="Assign to selection", parent=self.sAttrWidgets['miscButtonsLayout'], c=self.Maya_assignToSelection)
    
        # DIFFUSE
        ###################
        # Label
        self.sAttrWidgets['diffuseLabelLayout'] = pc.rowColumnLayout(nc=2, columnAlign=(1, 'center'), columnAttach=(2, 'both', 0), columnWidth=[(1, 60), (2, 150)], parent=self.sAttrWidgets['layout'])
        pc.text(label='Diffuse ', fn='boldLabelFont', parent=self.sAttrWidgets['diffuseLabelLayout'])
        pc.separator(height=20, style='in', parent=self.sAttrWidgets['diffuseLabelLayout'])
        
        # Controls
        self.sAttrWidgets['diffuseControlsLayout'] = pc.rowColumnLayout(nc=2, cw=[(1, 200), (2, 30)], parent=self.sAttrWidgets['layout'])
        pc.attrColorSliderGrp(label="Color", w=200, cw=[(1, 50), (2, 30)], at='%s.color' % self.selectedShader, parent=self.sAttrWidgets['diffuseControlsLayout'])
        self.dynamicButtons['colorToggle'] = pc.iconTextButton(style='iconOnly', h=20, image1="disableForRendering.png", c=partial(self.Maya_toggleConnection, 'color'))
        pc.attrFieldSliderGrp(label="Weight", w=200, cw=[(1, 50), (2, 50)], min=0, max=1.0, at='%s.Kd' % self.selectedShader, pre=3, parent=self.sAttrWidgets['diffuseControlsLayout'])
        pc.text(l="")
        pc.attrFieldSliderGrp(label="Rough", w=200, cw=[(1, 50), (2, 50)], min=0, max=1.0, at='%s.diffuseRoughness' % self.selectedShader, pre=3, parent=self.sAttrWidgets['diffuseControlsLayout'])
        pc.text(l="")
        
        # SPECULAR
        ###################
        # Label
        self.sAttrWidgets['specularLabelLayout'] = pc.rowColumnLayout(numberOfColumns=2, columnAlign=(1, 'center'), columnAttach=(2, 'both', 0), columnWidth=[(1, 60), (2, 150)], parent=self.sAttrWidgets['layout'])
        pc.text(label='Specular ', fn='boldLabelFont', parent=self.sAttrWidgets['specularLabelLayout'])
        pc.separator(height=20, style='in')
        
        # Controls
        self.sAttrWidgets['specularControlsLayout'] = pc.rowColumnLayout(nc=2, cw=[(1, 200), (2, 30)], parent=self.sAttrWidgets['layout'])
        pc.attrColorSliderGrp(label="Color", w=200, cw=[(1, 50), (2, 30)], at='%s.KsColor' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        self.dynamicButtons['KsColorToggle'] = pc.iconTextButton(style='iconOnly', h=20, image1="disableForRendering.png", c=partial(self.Maya_toggleConnection, 'KsColor'))
        pc.attrFieldSliderGrp(label="Weight", w=200, cw=[(1, 50), (2, 50)], pre=3, at='%s.Ks' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        pc.text(l="")
        pc.attrEnumOptionMenuGrp(label="BRDF", w=200, cw=[(1, 50)], ei=[(0, 'stretched_phong'), (1, 'ward_duer'), (2, 'cook_torrance')], at='%s.specularBrdf' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        pc.text(l="")
        pc.attrFieldSliderGrp(label="Rough", w=200, cw=[(1, 50), (2, 50)], pre=4, at='%s.specularRoughness' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        self.dynamicButtons['specularRoughnessToggle'] = pc.iconTextButton(style='iconOnly', h=20, image1="disableForRendering.png", c=partial(self.Maya_toggleConnection, 'specularRoughness'))
        pc.attrEnumOptionMenuGrp(label="Fresnel", w=200, cw=[(1, 50)], ei=[(0, 'No'), (1, 'Yes')], at='%s.specularFresnel' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        pc.text(l="")
        pc.attrFieldSliderGrp(label="% at N", w=200, cw=[(1, 50), (2, 50)], pre=3, at='%s.Ksn' % self.selectedShader, parent=self.sAttrWidgets['specularControlsLayout'])
        self.dynamicButtons['reflectance'] = pc.iconTextButton(style='iconOnly', h=20, image1="calculator.png", c=self.Maya_calculateReflectance)
        # BUMP MAPPING
        ###################
        # Label
        self.sAttrWidgets['bumpLabelLayout'] = pc.rowColumnLayout(numberOfColumns=2, columnAlign=(1, 'center'), columnAttach=(2, 'both', 0), columnWidth=[(1, 60), (2, 150)], parent=self.sAttrWidgets['layout'])
        pc.text(label='Bump ', fn='boldLabelFont', parent=self.sAttrWidgets['bumpLabelLayout'])
        pc.separator(height=20, style='in')
        
        # Controls
        self.sAttrWidgets['bumpControlsLayout'] = pc.rowColumnLayout(nc=2, cw=[(1, 200), (2, 30)], parent=self.sAttrWidgets['layout'])
        pc.attrNavigationControlGrp(label="Map", cw=[(1, 50), (2, 120)], at='%s.normalCamera' % self.selectedShader, parent=self.sAttrWidgets['bumpControlsLayout'])
        self.dynamicButtons['normalCameraToggle'] = pc.iconTextButton(style='iconOnly', h=20, image1="disableForRendering.png", c=partial(self.Maya_toggleConnection, 'normalCamera'))

        # Refresh connection state icons
        self.UI_refreshIcons()
        
    def UI_refreshIcons(self):
        """Refresh connection state icons
        
        Keyword arguments:
        none
        
        Return:
        none
        """
        
        # Given specific attributes, we look for their state
        for attribute in ('color', 'KsColor', 'specularRoughness', 'normalCamera'):
            
            # Connection state
            connectionState = pc.shadingConnection(self.selectedShader + '.' + attribute, q=True, cs=True)
            
            # If the connection is OK, we display the correct icon to disable it 
            if (connectionState):
                pc.iconTextButton(self.dynamicButtons[attribute + 'Toggle'], edit=True, image="disableForRendering.png")
            else:
                pc.iconTextButton(self.dynamicButtons[attribute + 'Toggle'], edit=True, image="enableForRendering.png")
                
    def UI_removeAttributes(self):
        
        # Remove current UI if it already exists
        if 'layout' in self.sAttrWidgets:
            pc.deleteUI(self.sAttrWidgets['layout'])
            del self.sAttrWidgets['layout']
            
    
######################################## MAYA FUNCTIONS ########################################
# > Functions that manipulate nodes in Maya 

    def Maya_createFullNetwork(self, withFile, *args):
        
        if withFile:
            print 'titi'
            fileNode = self.Maya_listExistingNode('file')
        else:
            fileNode = self.Maya_createNode('file')
            
        #aiNode = self.Maya_createNode('aiStandard')
        
        # DiffCC
        #diffCC = pc.shadingNode('ygColorCorrect', asShader=True, name='diffCC_' + aiNode)
        # specCC
        #specCC = pc.shadingNode('ygColorCorrect', asShader=True, name='specCC_' + aiNode)
        # roughCC
        #roughCC = pc.shadingNode('ygColorCorrect', asShader=True, name='roughCC_' + aiNode)
        # bumpCC
        #bumpCC = pc.shadingNode('ygColorCorrect', asShader=True, name='bumpCC_' + aiNode)
        
        # Bump node
        #bumpNode = pc.shadingNode('bump2d', asUtility=True, name='bump_' + aiNode)
        
    def Maya_listExistingNode(self, type, *args):
        
        # Delete windows if already existing
        if pc.window("listExistingNode", exists=True):
            pc.deleteUI("listExistingNode")
            
        self.listNodesWidgets['window'] = pc.window("listExistingNode", title="Select a node", sizeable=False, h=150, w=150)
        
        self.listNodesWidgets['mainLayout'] = pc.columnLayout()
        
        listNodes = pc.ls(exactType=type)
        print listNodes
        self.listNodesWidgets['nodeCollection'] = pc.radioCollection()
        
        for node in listNodes:
            pc.radioButton(l=node)
            
        pc.button(l="OK", c="selected = pc.radioCollection(self.listNodesWidgets['nodeCollection'], edit=True, select=True) ; print selected")  
            
        pc.showWindow(self.listNodesWidgets['window'])
        
    def Maya_createNode(self, nodeType, *args):
        
        if nodeType == 'aiStandard':
            # Ask for name
            name = self.User_inputDialog("Create aiStandard", "Enter a name for the node: ")
            
            # Create and assign shader
            aiStd = pc.shadingNode('aiStandard', asShader=True, name=name)
            aiStdSg = pc.sets(renderable=True, noSurfaceShader=True, empty=True, name=name + 'SG')
            aiStd.outColor >> aiStdSg.surfaceShader 
            
            self.UI_refreshShaders()
            
            return(str(aiStd))

        if nodeType == 'file':
            # Ask for name
            name = self.User_inputDialog("Create file", "Enter a name for the node: ")
            # Ask for location of the file
            location = pc.fileDialog2(fm=1, dialogStyle=2)
            myTex = pc.shadingNode('file', asTexture=True, name=name)  
            myTex.fileTextureName.set(location)
            
            return(str(myTex))
            
        if nodeType == 'ygColorCorrect':
            # Ask for name
            name = self.User_inputDialog("Create ygColorCorrect", "Enter a name for the node: ")
            ygC = pc.shadingNode('ygColorCorrect', asShader=True, name=name)
            
            return(str(ygC))
        
    def Maya_assignToSelection(self, *args):
        """Assign current shader to selected objects"""
        # Controls if selection is not null
        test = pc.ls(sl=1)
        if len(test) == 0:
            raise Exception("Tried to assign '%s' to the current selection but nothing is selected." % self.selectedShader)
        
        # If everything is ok, assign current shader to selection
        pc.hyperShade(assign=self.selectedShader)
        
    def Maya_selectShader(self, *args):
        """Select the shader in the AA"""
        pc.select(self.selectedShader, r=True)
        
    def Maya_renameShader(self, *args):
        
        result = self.User_inputDialog("Rename shader", "Enter new name: ")
        shader = pc.PyNode(self.selectedShader)
        pc.rename(shader, result)
        self.UI_refreshShaders()
        
    def Maya_toggleConnection(self, attribute, *args):
        """Toggle on and off the connection state of specific attributes.
        
        Keyword arguments:
        attribute
        
        Return:
        none
        """
        
        if (self.Maya_getInput(attribute) == (None, None)):
            self.User_warningDialog("Error", "Nothing is connected to %s" % self.selectedShader + '.' + attribute)
        else:
            connectionState = pc.shadingConnection(self.selectedShader + '.' + attribute, q=True, cs=True)
            
            if (connectionState):
                pc.shadingConnection(self.selectedShader + '.' + attribute, e=True, cs=False)
            else:
                pc.shadingConnection(self.selectedShader + '.' + attribute, e=True, cs=True)
                
            self.UI_refreshIcons()
    
    def Maya_getInput(self, attribute):
        """
        Return the attribute from where the connection originated
        This is useful to know if RGB->RGB or alpha->RGB
        """
        # TODO: Pour le cas du outAlpha, il faut tester si il y a des connections sur colorR, colorB, etc car
        # c'est different de color tout court...
        myShader = pc.PyNode(self.selectedShader)
        connectionOrigin = myShader.attr(attribute).listConnections(c=True, p=True)
        
        if len(connectionOrigin) == 0:
            return None, None
        else:
            conType = connectionOrigin[0][1].split('.')[1]
            nodeName = connectionOrigin[0][1].split('.')[0]
        
            return nodeName, conType
        
    def Maya_calculateReflectance(self, *args):
        """Calculate reflectance at normal from a given IOR and extinction coefficient
        
        Keyword arguments:
        none
        
        Return:
        reflectance at normal
        
        Misc:
        display a warning if the result is not correct.
        """
        
        # IOR input
        ior = self.User_inputDialog("IOR", "Enter the IOR: ")
        # K input
        k = self.User_inputDialog("Extinction coefficient", "Enter the coefficient of extinction (k) or 0 if the material is an insulator: ")
    
        result = ((float(ior) - 1) ** 2 + float(k) ** 2) / ((float(ior) + 1) ** 2 + float(k) ** 2)
        
        # If result is between 0 and 1
        if (result >= 0 and result <= 1):
            # We set it in the shader
            myShader = pc.PyNode(self.selectedShader)
            myShader.Ksn.set(result)
        else:
            # An error is provided
            self.User_warningDialog("Error", "Result is not correct. Please ensure you provided valid inputs.")
    
    def Maya_revertToAiStd(self, *args):
        """Revert back to the aiStandard"""
        self.Maya_replaceMaterial('dummySHD', self.selectedShader)
        
    def Maya_replaceMaterial(self, mat1, mat2, *args):
        """Replace current material mat1 by another material mat2"""
        pc.hyperShade(o=mat1)
        test = pc.ls(sl=1)
        
        if len(test) > 0:
            pc.hyperShade(assign=mat2)
            
    def Maya_focusOn(self, attribute, *args):
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
            pc.disconnectAttr(con[1], con[0])
            
        # Return input node
        inputNode = self.Maya_getInput(attribute)
        
        print inputNode
        
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
            self.Maya_replaceMaterial(self.selectedShader, 'dummySHD')
        else:
            self.User_warningDialog("Error", "Nothing is connected to %s" % self.selectedShader + '.' + attribute)

######################################## USER FUNCTIONS ########################################
# > Functions that communicate with the user    
    
    def User_inputDialog(self, title, message):
        
        result = pc.promptDialog(title=title, message=message, button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
        if result == 'OK':
            text = pc.promptDialog(query=True, text=True)
            return text
        
    def User_warningDialog(self, title, message):
        pc.confirmDialog(title=title, message=message)     
