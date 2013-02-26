import pymel.core as pc
from functools import partial

def prepareBatch(transfert, *args):
    
    # Retrieving values from UI
    subdivType = pc.radioButtonGrp(uiWidgets['subdivType'], q=1, sl=1)
    subdivIt = pc.intSliderGrp(uiWidgets['subdivIterations'], q=1, value=1)
    autobump = pc.checkBox(uiWidgets['autobump'],q=1, value=1)
    
    # Get the selected objects
    selections = pc.ls(sl=1)
    
    # If none, execution stops here
    if len(selections) == 0:
        pc.confirmDialog(t="Error", message="Nothing selected.", icon='critical')
    # Else, we batch set the primary visibility 
    else:
        print "BATCH SET SMOOTH"
        
        for sel in selections:
            applySmooth(sel, subdivType, subdivIt, autobump, transfert)

def applySmooth(selected, subdivType, subdivIt, autobump, transfert):
    
    # List relatives
    relatives = pc.listRelatives(selected)
    
    # We scan if any relative is a group, if so we dig deeper
    for relative in relatives:
        if relative.type() == 'transform':
            applySmooth(relative, subdivType, subdivIt, autobump, transfert)
            
        # We assign values if everything is ok
        elif relative.type() == 'mesh':
                
            if not transfert:
                relative.setAttr('aiSubdivType', subdivType-1)
                relative.setAttr('aiSubdivIterations', subdivIt)
            else:
                relative.setAttr('aiSubdivType', 1)
                relative.setAttr('aiSubdivIterations', relative.getAttr('smoothLevel'))
                
            relative.setAttr('aiDispAutobump', autobump)
# Dictionnary that contains all UI elements
uiWidgets = {}

# Delete windows if already existing
if pc.window("batchSmooth", exists=True):
    pc.deleteUI("batchSmooth")

# Main window
uiWidgets['window'] = pc.window("batchSmooth", menuBar=True, title="Arnold Smooth Buddy", sizeable=False, h=430, w=300)

uiWidgets['layout'] = pc.columnLayout()

uiWidgets['subdivType'] = pc.radioButtonGrp(l='Subdiv type: ', w=300, cw=[(1,100),(2,50),(3,70), (4,70)], labelArray3=['none', 'catclark', 'linear'], sl=1, nrb=3)

pc.separator(h=5, style='none')

uiWidgets['subdivIterations'] = pc.intSliderGrp(field=True, w=280, cw=[(1,100),(2,50),(3,70)], l="Subdiv iterations: ", minValue=0, maxValue=10, value=0)

pc.separator(h=5, style='none')

uiWidgets['autobumpLayout'] = pc.rowColumnLayout(nc=2, cw=[(1,100),(2, 100)])
pc.text(l='')
uiWidgets['autobump'] = pc.checkBox(label='Autobump')

pc.setParent('..')

pc.separator(h=5, style='none', parent=uiWidgets['layout'])

uiWidgets['applyButtonLayout'] = pc.rowColumnLayout(nc=2, cw=[(1,100),(2, 100)])

pc.text(l='')
pc.button(l='Apply to selected', c=partial(prepareBatch, False))

pc.setParent('..')

uiWidgets['copyLayout'] = pc.rowColumnLayout(nc=2, cw=[(1,100),(2, 150)])

pc.text(l='')
pc.button(l='Copy from smooth preview', c=partial(prepareBatch, True))

pc.setParent('..')

pc.separator(h=5, style='none', parent=uiWidgets['layout'])
pc.showWindow(uiWidgets['window'])