import pymel.core as pc

def applyToSelected(*args):
    
    selectedObjects = pc.ls(sl=1)
    
    subdivType = pc.radioButtonGrp(uiWidgets['subdivType'], q=1, sl=1)
    subdivIt = pc.intSliderGrp(uiWidgets['subdivIterations'], q=1, value=1)
    autobump = pc.checkBox(uiWidgets['autobump'],q=1, value=1)
    
    for object in selectedObjects:
        
        shape = object.getShape()
        
        shape.setAttr('aiSubdivType', subdivType-1)
        shape.setAttr('aiSubdivIterations', subdivIt)
        shape.setAttr('aiDispAutobump', autobump)

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
pc.button(l='Apply to selected', c=applyToSelected)

pc.setParent('..')

pc.separator(h=5, style='none', parent=uiWidgets['layout'])
pc.showWindow(uiWidgets['window'])