import pymel.core as pc
from functools import partial

uiWidgets = {}

            
def displayShading(relative):
    relative.overrideEnabled.set(1)
    relative.overrideTexturing.set(0)
    
def removeOverrides(relative):
    relative.overrideEnabled.set(0)
    relative.overrideTexturing.set(1)
    
methods = {'displayShading': displayShading, 
           'removeOverrides': removeOverrides
           }

def recursiveAssign(selected, function):
    
    # List relatives
    relatives = pc.listRelatives(selected)
    
    # Case where only shapes are selected
    if (len(relatives) == 0 and selected.type() == 'mesh'):
        relatives = []
        relatives.append(selected)
    
    # We scan if any relative is a group, if so we dig deeper
    for relative in relatives:
        if relative.type() == 'transform':
            recursiveAssign(relative, function)
            
        # We assign color if everything is ok
        elif relative.type() == 'mesh':
            
            # If the custom attribute is not in place already, we create it
            if function in methods:
                methods[function](relative)
            else:
                raise Exception("Method %s is not implemented" % function)


def setOverrides(function, *args):
    
    listSel = pc.ls(sl=1)
    
    if len(listSel) == 0:
        pc.confirmDialog(t="Error", message="Nothing selected.", icon='critical')
    else:
        for sel in listSel:
            recursiveAssign(sel, function)

def close(*args):
    
    pc.deleteUI("IDsetup")

# Delete windows if already existing
if pc.window("IDsetup", exists=True):
    pc.deleteUI("IDsetup") 
    
uiWidgets['window'] = pc.window("IDsetup", menuBar=True, title="Setup Attributes for ID AOV", sizeable=False, h=200, w=300)

# Main layout
uiWidgets['mainLayout'] = pc.columnLayout()

uiWidgets['sub3'] = pc.columnLayout(p=uiWidgets['mainLayout'])

pc.button(l="Display shaded", c=partial(setOverrides, 'displayShading'), p=uiWidgets['sub3'])
pc.button(l="Remove overrides", c=partial(setOverrides, 'removeOverrides'), p=uiWidgets['sub3'])


pc.separator(h=10, p=uiWidgets['sub3'])

pc.button(l="Close", c=close)

pc.showWindow(uiWidgets['window'])
