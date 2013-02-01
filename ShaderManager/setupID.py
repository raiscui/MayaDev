import pymel.core as pc
from functools import partial

uiWidgets = {}

def createRgbConstant(*args):
    listSel = pc.ls(sl=1)
    
    for sel in listSel:
        shape = sel.getShape()
        
        
        if shape.hasAttr('mtoa_constant_rgbMask'):
            print "Attribute exists."
        else:
            print "No attribute.. Creating"
            shape.addAttr('mtoa_constant_rgbMask', at='double3')
            shape.addAttr('mtoa_constant_rgbMaskX', at='double', p='mtoa_constant_rgbMask')
            shape.addAttr('mtoa_constant_rgbMaskY', at='double', p='mtoa_constant_rgbMask')
            shape.addAttr('mtoa_constant_rgbMaskZ', at='double', p='mtoa_constant_rgbMask')
            shape.setAttr('mtoa_constant_rgbMask', [0, 0, 0])
            
            shape.setAttr('mtoa_constant_rgbMask', k=True)
            shape.setAttr('mtoa_constant_rgbMaskX', k=True)
            shape.setAttr('mtoa_constant_rgbMaskY', k=True)
            shape.setAttr('mtoa_constant_rgbMaskZ', k=True)
            
def removeRgbConstant(*args):
    
    listSel = pc.ls(sl=1)
    
    for sel in listSel:
        shape = sel.getShape()
        
        if shape.hasAttr('mtoa_constant_rgbMask'):
            shape.deleteAttr('mtoa_constant_rgbMask')
        else:
            print "Attribute does not exist."
            
def setIdColor(color, *args):
    
    listSel = pc.ls(sl=1)
    
    for sel in listSel:
        shape = sel.getShape()
        
        if shape.hasAttr('mtoa_constant_rgbMask'):
            shape.setAttr('mtoa_constant_rgbMaskX', color[0])
            shape.setAttr('mtoa_constant_rgbMaskY', color[1])
            shape.setAttr('mtoa_constant_rgbMaskZ', color[2])
        else:
            print "Attribute does not exist."

def setupNetwork(*args):
    
    # aiUserDataColor
    dataColor = pc.shadingNode('aiUserDataColor', asShader=True, name='rgbMaskDataColor')
    dataColor.setAttr('colorAttrName', 'rgbMask', type='string')
    # aiWriteColor
    writeColor = pc.shadingNode('aiWriteColor', asShader=True, name='rgbMaskWriteColor')
    # Target aiStandard
    aiStd = pc.shadingNode('surfaceShader', asShader = True, name='rgbMask_SHD')
    
    # Make connections
    dataColor.outColor >> writeColor.beauty
    writeColor.outColor >> aiStd.outColor

def close(*args):
    
    pc.deleteUI("IDsetup")

# Delete windows if already existing
if pc.window("IDsetup", exists=True):
    pc.deleteUI("IDsetup") 
    
uiWidgets['window'] = pc.window("IDsetup", menuBar=True, title="Setup Attributes for ID AOV", sizeable=False, h=200, w=200)

# Main layout
uiWidgets['mainLayout'] = pc.columnLayout()


uiWidgets['sub1'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l="1) Select objects and create/remove attributes needed", p=uiWidgets['sub1'])
pc.separator(h=10, p=uiWidgets['sub1'])

uiWidgets['sub1_rc'] = pc.rowColumnLayout(w=220, nc=2, cw=[(1,100), (2,100)], parent=uiWidgets['sub1'])
pc.button(l="Create attribute", c=createRgbConstant, parent=uiWidgets['sub1_rc'])
pc.button(l="Delete attribute", c=removeRgbConstant, parent=uiWidgets['sub1_rc'])

pc.separator(h=10, p=uiWidgets['sub1'])

uiWidgets['sub2'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='2) Set desired color for selected objects.', parent=uiWidgets['sub2'])
pc.separator(h=10, p=uiWidgets['sub2'])

uiWidgets['sub2_rc'] = pc.rowColumnLayout(w=220, nc=2, cw=[(1,100), (2,100)], parent=uiWidgets['sub2'])
pc.button(l="Red", ebg=True, bgc=[1, 0, 0], c=partial(setIdColor, [1, 0, 0]), p=uiWidgets['sub2_rc'])
pc.button(l="Green", ebg=True, bgc=[0, 1, 0], c=partial(setIdColor, [0, 1, 0]), p=uiWidgets['sub2_rc'])
pc.button(l="Blue", ebg=True, bgc=[0, 0, 1], c=partial(setIdColor, [0, 0, 1]), p=uiWidgets['sub2_rc'])
pc.button(l="Cyan", ebg=True, bgc=[0, 1, 1], c=partial(setIdColor, [0, 1, 1]), p=uiWidgets['sub2_rc'])
pc.button(l="Yellow", ebg=True, bgc=[1, 1, 0], c=partial(setIdColor, [1, 1, 0]), p=uiWidgets['sub2_rc'])
pc.button(l="Magenta", ebg=True, bgc=[1, 0, 1], c=partial(setIdColor, [1, 0, 1]), p=uiWidgets['sub2_rc'])
pc.button(l="Black", ebg=True, bgc=[0, 0, 0], c=partial(setIdColor, [0, 0, 0]), p=uiWidgets['sub2_rc'])
pc.button(l="White", ebg=True, bgc=[1, 1, 1], c=partial(setIdColor, [1, 1, 1]), p=uiWidgets['sub2_rc'])

pc.separator(h=10, p=uiWidgets['sub2'])

uiWidgets['sub3'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='3) Create nodes to output to a custom AOV', parent=uiWidgets['sub3'])
pc.separator(h=10, p=uiWidgets['sub3'])

pc.button(l="Setup nodes network", c=setupNetwork, p=uiWidgets['sub3'])

pc.separator(h=10, p=uiWidgets['sub3'])

pc.text(l="4) Finally, do not forget to create a custom AOV \n and plug rgbMask_SHD.color to the AOV default\nshader. Thanks for using this awesome script.", align='left')

pc.separator(h=10, p=uiWidgets['sub3'])

pc.button(l="Close", c=close)

pc.showWindow(uiWidgets['window'])
