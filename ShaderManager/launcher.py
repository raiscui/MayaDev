
import pymel.core as pc
import LDAClass as ld

reload(ld)

#file(newFile=None, force=None)
'''pc.newFile

testSphere = pc.polySphere(n='mySphere', sx=20, sy=20, r=50)[0]


# Creation du SG
sg = pc.sets(renderable=True, noSurfaceShader=True, empty=True, name="aiStandardSG")
print "sg="+sg
# Creation du aiStandard
aiStandard = pc.shadingNode("aiStandard", asShader=True, name="toto")

print aiStandard
# Modification de la couleur de diffuse
aiStandard.color.set(0.5, 0.6, 0.8)maya

# On connecte l'un a l'autre
aiStandard.outColor >> sg.surfaceShader

# On assigne le shader
pc.sets(sg, edit=True, forceElement=testSphere)

toto = at.Aton()'''

#mayaShadersList = pc.ls(exactType="aiStandard")
#
#if len(mayaShadersList) == 0:
#    raise TypeError("No AiStandard shader in the scene")
#
#aiStandardsList = {}
#
#for shader in mayaShadersList:
#    print("~~~ Shader(s) found : {0} ~~~".format(shader))
#    mgShader = ms.LookdevAssistant(shader)
#    mgShader.getInfosFromMaya()
#    aiStandardsList[shader] = mgShader
#    
#def buttonPressed():
#    print('titi')
#    
#def refreshAttributes():
#    selectedAttribute = pc.textScrollList(scrollTest, query=True, selectItem=True)
#    textField.setText(str(selectedAttribute[0]))
#
#win = pc.window(title="My Window")
#layout = pc.columnLayout()
#
#textField = pc.textField()
#
#scrollTest = pc.textScrollList()
#scrollTest.extend(aiStandardsList)
#
#scrollTest.selectCommand("refreshAttributes()")
#
#pc.showWindow()

test = ld.LDA()

# test tototo

# BONJOUR CA MARCHE
# En effet




    
    
    
    
    








