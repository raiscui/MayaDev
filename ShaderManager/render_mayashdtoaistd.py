import pymel.core as pc

# Main dictionnary
infos = {}
uiWidgets = {}


def populateList():    
    # Get shader type
    shaderSel = pc.radioButtonGrp(uiWidgets['shaderType'], q=1, select=1)
    
    if shaderSel == 1:
        shaderType = 'lambert'
    elif shaderSel == 2:
        shaderType = 'blinn'
    elif shaderSel == 3:
        shaderType = 'phong'
        
    # Get shader prefix
    shaderPrefix = pc.textField(uiWidgets['shadersPrefix'], q=1, text=1)
    
    if len(shaderPrefix) == 0:
        listShaders = pc.ls(exactType=shaderType)
    else:
        listShaders = pc.ls(shaderPrefix+'*', exactType=shaderType)

    if len(listShaders) == 0:
        pc.confirmDialog(t="Error", message="No shaders fitting the given paramaters has been found.", icon='critical')
        exit(1)
    elif len(listShaders) > 0:
        pc.confirmDialog(t="Shaders found", message=str(len(listShaders))+" shader(s) found. Click confirm to continue.")
    else:
        exit("Unknown error.")
    
#    for info in infos.keys():
#        print "#######################"
#        print "### Shader: '%s'" % info
#        print " - Found %s shape(s)" % len(infos[info])
#        print "Shapes list: %s " % infos[info]
        
    return listShaders
    
def convertShaders(shdList):
    
    # List all file nodes in the scene
    fileNodes = pc.ls(exactType='file')
    
    for shd in shdList:
        
        fileNodeName = ''
        
        # For each shader in the list, get his file node
        connections = pc.listConnections(shd)
        
        for filenode in fileNodes:
            if filenode in connections:
                fileNodeName = filenode
                break
            
        # If we can find any file node, we continue to the next shader
        if fileNodeName == '':
            print "Shader '%s' has no file node associated. It won't be converted to aiStandard." % shd
            continue
        else:
            print "Shader '%s' has a file node '%s'" % (shd,fileNodeName)
            pc.rename(fileNodeName, shd+"_File")

        # Create an aiStandard
        aiStd = pc.shadingNode('aiStandard', asShader=True, name=str(shd)+"_std")
        aiStdSg = pc.sets(renderable=True, noSurfaceShader=True, empty=True, name=str(shd) + 'SG')
        aiStd.outColor >> aiStdSg.surfaceShader 

        # Creates associated ygColorCorrect nodes
        # DiffCC
        diffCC = pc.shadingNode('ygColorCorrect', asTexture=True, name='diffCC_' + aiStd)
        # specCC
        specCC = pc.shadingNode('ygColorCorrect', asTexture=True, name='specCC_' + aiStd)
        # roughCC
        roughCC = pc.shadingNode('ygColorCorrect', asTexture=True, name='roughCC_' + aiStd)
        # bumpCC
        bumpCC = pc.shadingNode('ygColorCorrect', asTexture=True, name='bumpCC_' + aiStd)
        
        # Bump node
        bumpNode = pc.shadingNode('bump2d', asUtility=True, name='bump_' + aiStd)
        
        # Connect everything
        fileNodeName.outColor >> diffCC.image
        fileNodeName.outColor >> specCC.image
        fileNodeName.outColor >> roughCC.image
        fileNodeName.outColor >> bumpCC.image
        
        bumpCC.outAlpha >> bumpNode.bumpValue
        bumpNode.outNormal >> aiStd.normalCamera
        
        # Set bump depth value
        bumpNode.bumpDepth.set(0.5)
        
        diffCC.outColor >> aiStd.color
        specCC.outColor >> aiStd.KsColor
        roughCC.outAlpha >> aiStd.specularRoughness
        
        # Replace "old" shaders with the new ones
        pc.hyperShade(o=shd)
        pc.hyperShade(assign=shd+"_std")
        
        removeOldShd = pc.checkBox(uiWidgets['removeOldShaders'], q=1, value=1)
        if removeOldShd:
            pc.delete(shd)
        

def processShaders(*args):
    
    # Populates a list of the shaders found and their associated shapes
    shdList = populateList()
    
    # Convert shaders
    convertShaders(shdList)

                
# Delete windows if already existing
if pc.window("ConvertShaders", exists=True):
    pc.deleteUI("ConvertShaders") 
    
uiWidgets['window'] = pc.window("ConvertShaders", menuBar=True, title="Convert shaders for Arnold", sizeable=False, h=200, w=250)

# Main layout
uiWidgets['mainLayout'] = pc.columnLayout()

uiWidgets['sub1'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='+ Source shaders type:', parent=uiWidgets['sub1'])
pc.separator(h=5, p=uiWidgets['sub1'])

uiWidgets['shaderType'] = pc.radioButtonGrp(nrb=3, labelArray3=['lambert', 'blinn', 'phong'], sl=1, cw3=[75,50,75])

pc.separator(h=10, p=uiWidgets['sub1'])

uiWidgets['sub2'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='+ Look for shaders prefix: ', parent=uiWidgets['sub2'])
pc.separator(h=5, p=uiWidgets['sub2'])

uiWidgets['sub2_rc'] = pc.rowColumnLayout(w=220, nc=2, cw=[(1,100), (2,100)], parent=uiWidgets['sub2'])
uiWidgets['shadersPrefix'] = pc.textField(text='SE_')

uiWidgets['sub3'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.separator(h=5, p=uiWidgets['sub3'])

uiWidgets['removeOldShaders'] = pc.checkBox(l='Remove old shaders', value=0)
pc.separator(h=5, p=uiWidgets['sub3'])

pc.button(l='Convert to aiStandard', c=processShaders)

pc.showWindow(uiWidgets['window'])
            