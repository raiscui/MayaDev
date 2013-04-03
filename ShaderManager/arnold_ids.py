import pymel.core as pc
from functools import partial
import mtoa.aovs as aovs

uiWidgets = {}
            
#def removeRgbConstant(*args):
#    
#    listSel = pc.ls(sl=1)
#    
#    for sel in listSel:
#        shape = sel.getShape()
#        
#        if shape.hasAttr('mtoa_constant_rgbMask'):
#            shape.deleteAttr('mtoa_constant_rgbMask')
#        else:
#            print "Attribute does not exist."
            
def recursiveAssign(attribute, selected, color):
    
    # List relatives
    relatives = pc.listRelatives(selected)
    
    # Case where only shapes are selected
    if (len(relatives) == 0 and selected.type() == 'mesh'):
        relatives = []
        relatives.append(selected)
    
    # We scan if any relative is a group, if so we dig deeper
    for relative in relatives:
        if relative.type() == 'transform':
            recursiveAssign(attribute, relative, color)
            
        # We assign color if everything is ok
        elif relative.type() == 'mesh':
            
            # If the custom attribute is not in place already, we create it
            if not relative.hasAttr(attribute):
                print "No attribute.. Creating"
                relative.addAttr(attribute, at='double3')
                relative.addAttr(attribute+'X', at='double', p=attribute)
                relative.addAttr(attribute+'Y', at='double', p=attribute)
                relative.addAttr(attribute+'Z', at='double', p=attribute)
                relative.setAttr(attribute, [0, 0, 0])
                
                relative.setAttr(attribute, k=True)
                relative.setAttr(attribute+'X', k=True)
                relative.setAttr(attribute+'Y', k=True)
                relative.setAttr(attribute+'Z', k=True)
            
            # We then set the color
            print "Setting color '{0}' for mesh {1} ".format(color, relative)
            relative.setAttr(attribute+'X', color[0])
            relative.setAttr(attribute+'Y', color[1])
            relative.setAttr(attribute+'Z', color[2])

def setColor(color, *args):
    
    # Get current AOV name
    aov = pc.radioButtonGrp(uiWidgets['aovs'], q=1, select=1)
    
    if aov == 1:
        aovName = 'mtoa_constant_rgbMask'
    elif aov == 2:
        aovName = 'mtoa_constant_rgbMask1'
    elif aov == 3:
        aovName = 'mtoa_constant_rgbMask2'
    elif aov == 4:
        aovName = 'mtoa_constant_rgbMask3'
        
    if aovName is None:
        raise Exception('Error while determining which AOV to focus on.')
    
    print "AOV Name: %s" % aovName
    
    listSel = pc.ls(sl=1)
    
    if len(listSel) == 0:
        pc.confirmDialog(t="Error", message="Nothing selected.", icon='critical')
    else:
        for sel in listSel:
            recursiveAssign(aovName, sel, color)
            

def setupNetwork(aovName, *args):
    
    # If already existing, do nothing
    listShd = pc.ls(aovName+'_SHD')
    if len(listShd) == 0:
        # aiUserDataColor
        dataColor = pc.shadingNode('aiUserDataColor', asShader=True, name=aovName+'DataColor')
        dataColor.setAttr('colorAttrName', aovName, type='string')
        # aiWriteColor
        writeColor = pc.shadingNode('aiWriteColor', asShader=True, name=aovName+'WriteColor')
        # Target aiStandard
        aiStd = pc.shadingNode('surfaceShader', asShader = True, name=aovName+'_SHD')
        
        # Make connections
        dataColor.outColor >> writeColor.beauty
        writeColor.outColor >> aiStd.outColor
        
        # Creates AOV
        aovs.AOVInterface().addAOV('id_'+aovName)
        idAov = pc.PyNode('aiAOV_id_'+aovName)
        
        # Connect the shader previously created to the default shader input of the AOV
        aiStd.outColor >> idAov.defaultValue
    else:
        print "Network already in place. Skipping setup."


def close(*args):
    
    pc.deleteUI("IDsetup")

# Delete windows if already existing
if pc.window("IDsetup", exists=True):
    pc.deleteUI("IDsetup") 
    
uiWidgets['window'] = pc.window("IDsetup", menuBar=True, title="Setup Attributes for ID AOV", sizeable=False, h=200, w=300)

# Main layout
uiWidgets['mainLayout'] = pc.columnLayout()

uiWidgets['sub1'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='0) Select ID AOV where colors will be set.', parent=uiWidgets['sub1'])
pc.separator(h=10, p=uiWidgets['sub1'])

uiWidgets['aovs'] = pc.radioButtonGrp(nrb=4, labelArray4=['rgbMask', 'rgbMask1', 'rgbMask2', 'rgbMask3'], sl=1, cw4=[75,75,75,75])

pc.separator(h=10, p=uiWidgets['sub1'])

uiWidgets['sub2'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='1) Set desired color for selected objects.', parent=uiWidgets['sub2'])
pc.separator(h=10, p=uiWidgets['sub2'])

uiWidgets['sub2_rc'] = pc.rowColumnLayout(w=220, nc=2, cw=[(1,100), (2,100)], parent=uiWidgets['sub2'])
pc.button(l="Red", ebg=True, bgc=[1, 0, 0], c=partial(setColor, [1, 0, 0]), p=uiWidgets['sub2_rc'])
pc.button(l="Green", ebg=True, bgc=[0, 1, 0], c=partial(setColor, [0, 1, 0]), p=uiWidgets['sub2_rc'])
pc.button(l="Blue", ebg=True, bgc=[0, 0, 1], c=partial(setColor, [0, 0, 1]), p=uiWidgets['sub2_rc'])
pc.button(l="Cyan", ebg=True, bgc=[0, 1, 1], c=partial(setColor, [0, 1, 1]), p=uiWidgets['sub2_rc'])
pc.button(l="Yellow", ebg=True, bgc=[1, 1, 0], c=partial(setColor, [1, 1, 0]), p=uiWidgets['sub2_rc'])
pc.button(l="Magenta", ebg=True, bgc=[1, 0, 1], c=partial(setColor, [1, 0, 1]), p=uiWidgets['sub2_rc'])
pc.button(l="Black", ebg=True, bgc=[0, 0, 0], c=partial(setColor, [0, 0, 0]), p=uiWidgets['sub2_rc'])
pc.button(l="White", ebg=True, bgc=[1, 1, 1], c=partial(setColor, [1, 1, 1]), p=uiWidgets['sub2_rc'])

pc.separator(h=10, p=uiWidgets['sub2'])

uiWidgets['sub3'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='2) Create nodes to output to a custom AOV', parent=uiWidgets['sub3'])
pc.separator(h=10, p=uiWidgets['sub3'])

pc.button(l="Setup rgbMask AOV", c=partial(setupNetwork, 'rgbMask'), p=uiWidgets['sub3'])
pc.button(l="Setup rgbMask1 AOV", c=partial(setupNetwork, 'rgbMask1'), p=uiWidgets['sub3'])
pc.button(l="Setup rgbMask2 AOV", c=partial(setupNetwork, 'rgbMask2'), p=uiWidgets['sub3'])
pc.button(l="Setup rgbMask3 AOV", c=partial(setupNetwork, 'rgbMask3'), p=uiWidgets['sub3'])

pc.separator(h=10, p=uiWidgets['sub3'])

pc.button(l="Close", c=close)

pc.showWindow(uiWidgets['window'])
