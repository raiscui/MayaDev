import pymel.core as pc
import mtoa.aovs as aovs

# Contains the list of the passes with the first letter in capital
passesList = ['Dust', 'Decals', 'Burn', 'Dots']

for element in passesList:
    
    print "Processing '%s'" % element
    # Creation of the layered texture node
    lyrNode = pc.shadingNode('layeredTexture', asTexture=1, name=element+"_LyrTx")
    
    # We get the shader
    shdNode = pc.PyNode(element+"_SHD")
    
    # We make the connection
    pc.connectAttr(element+"_SHD.outColor", element+"_LyrTx.inputs[0].color")
    pc.connectAttr(element+"_File.outAlpha", element+"_LyrTx.inputs[0].alpha")
    
    # We create the aov
    aovs.AOVInterface().addAOV(element.lower())
    aov = pc.PyNode('aiAOV_'+element.lower())
    
    # Connect the lyrtx to the AOV default value
    lyrNode.outAlpha >>  aov.defaultValue