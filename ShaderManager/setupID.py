import pymel.core as pc

uiWidgets = {}

def process():
    listSel = pc.ls(sl=1)
    
    for sel in listSel:
        shape = sel.getShape()
        
        print "Shape selected: %s" % shape
        
        if shape.hasAttr('mtoa_constant_rgbMask'):
            print "Attribute exists"
            shape.deleteAttr('mtoa_constant_rgbMaskX')
            shape.deleteAttr('mtoa_constant_rgbMaskY')
            shape.deleteAttr('mtoa_constant_rgbMaskZ')
            shape.deleteAttr('mtoa_constant_rgbMask')
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
# Delete windows if already existing
if pc.window("IDsetup", exists=True):
    pc.deleteUI("IDsetup") 
    
uiWidgets['window'] = pc.window("IDsetup", menuBar=True, title="Setup Attributes for ID AOV", sizeable=False, h=200, w=200)

uiWidgets['mainLayout'] = pc.columnLayout()    

pc.showWindow(uiWidgets['window'])
