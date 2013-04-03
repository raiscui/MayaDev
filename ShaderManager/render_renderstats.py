import pymel.core as pc
from functools import partial

# Dictionnary that contains all UI elements
uiWidgets = {}

# Global variable 
elements = ['primaryVisibility', 'visibleInReflections', 'visibleInRefractions', 'castsShadows', 'receiveShadows', 'aiOpaque']

# Explore recursively
def exploreFurther(selected, elements):
    relatives = pc.listRelatives(selected)
    
    # Dig deeper in the hierarchy to find the shapes 
    for relative in relatives:
        if len(pc.listRelatives(relative)) != 0:
            exploreFurther(relative, elements)
        elif relative.type() == 'mesh':
            
            for element in elements.keys():
                pc.setAttr(relative+'.'+element, elements[element])

            
def applyToSelected(*args):
    
    elementsUnlocked = {}
    
    for element in elements:
        # Check if controls are enabled and if so, append them to the list
        state = pc.checkBox(uiWidgets[element], q=1, enable=1)
        if (state):
            elementsUnlocked[element] =  pc.checkBox(uiWidgets[element], q=1, value=1)
            
    print "Setting select objects to these render stats : %s" % elementsUnlocked
    
    # If everything is locked, we interrupt execution
    if len(elementsUnlocked) == 0:
        pc.confirmDialog(icon='critical', message="You have to unlock at least one render stat.")
        exit('Please unlock at least one render stat.')
    
    # Saves what's selected and call the recursive dig & assign
    selected = pc.ls(sl=1)
    exploreFurther(selected, elementsUnlocked)

def toggleEnable(control, *args):
    
    # Get the state of the control
    state = pc.checkBox(uiWidgets[control], q=1, enable=1)
    
    if (state):
        # If enabled, we grey it
        state = pc.checkBox(uiWidgets[control], edit=1, enable=0)
        # Button update
        pc.button(uiWidgets[control+'Button'], edit=1, label='Unlock')
        
    else:
        state = pc.checkBox(uiWidgets[control], edit=1, enable=1)
        pc.button(uiWidgets[control+'Button'], edit=1, label='Lock')
        

def showUI():
    # Delete windows if already existing
    if pc.window("batchVisibility", exists=True):
        pc.deleteUI("batchVisibility")
    
    # Main window
    uiWidgets['window'] = pc.window("batchVisibility", menuBar=True, title="Render Stats", sizeable=False, h=430, w=300)
    
    uiWidgets['layout'] = pc.rowColumnLayout(nc=2)
    
    uiWidgets['primaryVisibility'] = pc.checkBox(label='Primary visibility', value=1)
    uiWidgets['primaryVisibilityButton'] = pc.button(l='Lock', c=partial(toggleEnable, 'primaryVisibility'))
    
    uiWidgets['visibleInReflections'] = pc.checkBox(label='Visible in Reflections', value=1)
    uiWidgets['visibleInReflectionsButton'] = pc.button(l='Lock', c=partial(toggleEnable, 'visibleInReflections'))
    
    uiWidgets['visibleInRefractions'] = pc.checkBox(label='Visible in Refractions', value=1)
    uiWidgets['visibleInRefractionsButton'] = pc.button(l='Lock', c=partial(toggleEnable, 'visibleInRefractions'))
    
    uiWidgets['castsShadows'] = pc.checkBox(label='Cast shadows', value=1)
    uiWidgets['castsShadowsButton'] = pc.button(l='Lock', c=partial(toggleEnable, 'castsShadows'))
    
    uiWidgets['receiveShadows'] = pc.checkBox(label='Receive shadows', value=1)
    uiWidgets['receiveShadowsButton'] = pc.button(l='Lock', c=partial(toggleEnable, 'receiveShadows'))

    pc.separator(h=10)
    pc.separator(h=10)

    uiWidgets['aiOpaque'] = pc.checkBox(label='Opaque', value=1)
    uiWidgets['aiOpaqueButton'] = pc.button(l='Lock', c=partial(toggleEnable, 'aiOpaque'))
    
    uiWidgets['layout'] = pc.columnLayout()
    pc.separator(h=10)
    pc.button(l='Set all', c=applyToSelected)
    
    pc.showWindow(uiWidgets['window'])
    
showUI()

