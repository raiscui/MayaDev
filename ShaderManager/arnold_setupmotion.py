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
            
def recursiveAssign(attribute, selected, state):
    
    # List relatives
    relatives = pc.listRelatives(selected)
    
    # We scan if any relative is a group, if so we dig deeper
    for relative in relatives:
        if relative.type() == 'transform':
            recursiveAssign(attribute, relative, state)
            
        # We assign color if everything is ok
        elif relative.type() == 'mesh':
            
            # If the custom attribute is not in place already, we create it
            if not relative.hasAttr(attribute):
                print "No attribute.. Creating"
                relative.addAttr(attribute, at='double')
                relative.setAttr(attribute, 0)
                
                relative.setAttr(attribute, k=True)
            
            # We then set the color
            print "Setting state '{0}' for mesh {1} ".format(state, relative)
            relative.setAttr(attribute, state)

def setState(state, *args):
    
    # Get current AOV name
    aov = pc.radioButtonGrp(uiWidgets['aovs'], q=1, select=1)
    
    if aov == 1:
        aovName = 'mtoa_constant_motion1'
    elif aov == 2:
        aovName = 'mtoa_constant_motion2'
    elif aov == 3:
        aovName = 'mtoa_constant_motion3'
        
    if aovName is None:
        raise Exception('Error while determining which AOV to focus on.')
    
    print "AOV Name: %s" % aovName
    
    listSel = pc.ls(sl=1)
    
    if len(listSel) == 0:
        pc.confirmDialog(t="Error", message="Nothing selected.", icon='critical')
    else:
        for sel in listSel:
            recursiveAssign(aovName, sel, state)
            

def setupNetwork(aovName, *args):
    
    # If already existing, do nothing
    listShd = pc.ls('aiAOV_'+aovName)
    if len(listShd) == 0:
        # aiUserDataColor
        dataFloat = pc.shadingNode('aiUserDataFloat', asShader=True, name=aovName+'DataFloat')
        dataFloat.setAttr('floatAttrName', aovName, type='string')
        # aiWriteColor
        motionVector = pc.shadingNode('aiMotionVector', asShader=True, name=aovName+'MotionNode')
        motionVector.raw.set(1)
        
        # Make connections
        dataFloat.outValue >> motionVector.time1
        
        # Creates AOV
        aovs.AOVInterface().addAOV(aovName)
        motionAov = pc.PyNode('aiAOV_'+aovName)
        
        # Connect the shader previously created to the default shader input of the AOV
        motionVector.outColor >> motionAov.defaultValue
    else:
        pc.warning("Network already in place. Skipping setup.")


def close(*args):
    
    pc.deleteUI("IDsetup")

# Delete windows if already existing
if pc.window("IDsetup", exists=True):
    pc.deleteUI("IDsetup") 
    
uiWidgets['window'] = pc.window("IDsetup", menuBar=True, title="Setup Attributes for motion AOV", sizeable=False, h=200, w=200)

# Main layout
uiWidgets['mainLayout'] = pc.columnLayout()

uiWidgets['sub1'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='0) Select motion AOV where colors will be set.', parent=uiWidgets['sub1'])
pc.separator(h=10, p=uiWidgets['sub1'])

uiWidgets['aovs'] = pc.radioButtonGrp(nrb=3, labelArray3=['motion1', 'motion2', 'motion3'], sl=1, cw3=[75,75,75])

pc.separator(h=10, p=uiWidgets['sub1'])

uiWidgets['sub2'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='1) Set desired state for selected objects.', parent=uiWidgets['sub2'])
pc.separator(h=10, p=uiWidgets['sub2'])

uiWidgets['sub2_rc'] = pc.rowColumnLayout(w=220, nc=2, cw=[(1,100), (2,100)], parent=uiWidgets['sub2'])
pc.button(l="On", ebg=True, bgc=[1, 0, 0], c=partial(setState, 1), p=uiWidgets['sub2_rc'])
pc.button(l="Off", ebg=True, bgc=[0, 1, 0], c=partial(setState, 0), p=uiWidgets['sub2_rc'])

pc.separator(h=10, p=uiWidgets['sub2'])

uiWidgets['sub3'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='2) Create nodes to output to a custom AOV', parent=uiWidgets['sub3'])
pc.separator(h=10, p=uiWidgets['sub3'])

pc.button(l="Setup motion1 AOV", c=partial(setupNetwork, 'motion1'), p=uiWidgets['sub3'])
pc.button(l="Setup motion2 AOV", c=partial(setupNetwork, 'motion2'), p=uiWidgets['sub3'])
pc.button(l="Setup motion3 AOV", c=partial(setupNetwork, 'motion3'), p=uiWidgets['sub3'])

pc.separator(h=10, p=uiWidgets['sub3'])

pc.button(l="Close", c=close)

pc.showWindow(uiWidgets['window'])
