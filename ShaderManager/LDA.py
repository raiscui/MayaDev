import pymel.core as pc

class LDA():
    
    def __init__(self):
        
        # Dictionnary containing all the UI elements
        widgets = {}
        
        # Build the UI
        self.buildUI()
        
        # Populate the shader list
        self.populateList()
        
    
    def buildUI(self):
        """Self explanatory: Build the UI"""
        
        # Delete windows if already existing
        if pc.window("lookdevAssistant", exists=True):
            pc.deleteUI("lookdevAssistant")
        
        # Main window
        self.widgets['mainWindow'] = pc.window("lookdevAssistant", title="Arnold - Lookdev assistant", sizeable=False, h=400, w=600)
        
        # Main layout : 2 columns / 1 for the list of the ai* shaders / 1 to access selected shader attributes
        self.widgets['mainLayout'] = pc.rowColumnLayout(nc=2, cw=[(1,150), (2,450)])
        
        # Shaders list layout
        self.widgets['shadersListLayout'] = pc.frameLayout( label='Shaders list', borderStyle='etchedIn', cll=True, h=400 ,parent=self.widgets['mainLayout'])
        self.widgets['shadersListInternalLayout'] = pc.columnLayout(parent=self.widgets['shadersListLayout'])
        
        self.widgets['shaderListTextField'] = pc.textField(text="test", parent=self.widgets['shadersListInternalLayout'])
        self.widgets['shadersList'] = pc.textScrollList(parent=self.widgets['shadersListInternalLayout'])
        
        # Shaders attributes layout
        self.widgets['shadersAttrLayout'] = pc.frameLayout( label='Shaders attributes', borderStyle='etchedIn', cll=True, h=400, parent=self.widgets['mainLayout'] )
        self.widgets['shadersAttrInternalLayout'] = pc.columnLayout(parent=self.widgets['shadersAttrLayout'], cal="left")
        
        # Displays main window
        pc.showWindow(self.widgets['mainWindow'])
        
    def populateList(self):
        """Populate the list in the UI with all aiStandard shaders currently present in the scene
        Raise an exception and abort if no shaders are present."""
        
        # Test if there is any aiStandard shader in the scene
        aiList = pc.ls(exactType='aiStandard')
        if len(aiList) == 0:
            raise Exception("No aiStandard shaders in the scene. Please create one before launching the lookdev assistant.")
        else:
        # Append shaders to the list
            self.widgets['shadersList'].append(aiList)