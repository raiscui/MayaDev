import pymel.core as pc

# Main dictionnary
infos = {}

def saveShaders():
    # Prompt user with a string to search shader by names
    dialog = pc.promptDialog(title='Search joker',
                    message='Enter joker to find specific shaders :',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')
    
    joker = pc.promptDialog(query=True, text=True)
    
    # List shaders named that way
    listShaders = pc.ls(joker, exactType='aiStandard')
    
    
    for shader in listShaders:
         
        # This variable will contain all shape that have the current shader assigned
        shapeList = []
        
        # Select shapes with the current shader
        pc.hyperShade(o=shader)
        selectedShapes = pc.ls(sl=1)
        
        # Clear selection, just for clarity
        pc.select(cl=1)
        
        # Append the shape to the list
        for shape in selectedShapes:
            shapeList.append(str(shape))
        
        # Assign the list to the dictionnary with the key set to the shader name
        infos[str(shader)] = shapeList
        
    print "Saved informations :\n %s" % infos
    
def loadShaders():
    
    print "Following shaders will be loaded and assigned to their saved shape :\n %s" % infos
    
    confirm = pc.confirmDialog( title='Confirm', message='Are you sure?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    
    # We proceed
    if confirm == "Yes":
        
        # We loop over the different shaders
        for shaderName in infos.keys():
            
            exists = pc.ls(shaderName)
            print "Shader found: %s" % exists
            
            if len(exists) == 1:
                "Shader %s found, proceeding..." % shaderName
                
                # We clear the selection
                pc.select(cl=1)
                
                # We loop over the different shapes
                for shape in infos[str(shaderName)]:
                    pc.select(shape, add=True)
                    
                # Assign shader
                pc.hyperShade(assign=shaderName)
                
                # We clear the selection
                pc.select(cl=1)
            