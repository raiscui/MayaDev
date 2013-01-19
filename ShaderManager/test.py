import pymel.core as pc
from functools import partial

# Dictionnary containing existing UI widgets
widgets = {}
attrList = ['attrColor', 'attrKd']
iconsPath = pc.internalVar(upd=True) + "icons/"

def removeUI(*args):
    for attr in attrList: 
        # If attribute UI exists, delete
        if widgets[attr] != "":
            pc.deleteUI(widgets[attr], control=True)
            widgets[attr] = ""
   
def UI():
    
    # Delete windows if already existing
    if pc.window("lookdevAssistant", exists=True):
        pc.deleteUI("lookdevAssistant")
    
    # Main window
    widgets['mainWindow'] = pc.window("lookdevAssistant", title="Arnold - Lookdev assistant", sizeable=False, h=400, w=600)
    
    # Main layout : 2 columns / 1 for the list of the ai* shaders / 1 to access selected shader attributes
    widgets['mainLayout'] = pc.rowColumnLayout(nc=2, cw=[(1,150), (2,450)])
    
    # Shaders list layout
    widgets['shadersListLayout'] = pc.frameLayout( label='Shaders list', borderStyle='etchedIn', cll=True, h=400 ,parent=widgets['mainLayout'])
    widgets['shadersListInternalLayout'] = pc.columnLayout(parent=widgets['shadersListLayout'])
    
    widgets['shaderListTextField'] = pc.textField(text="test", parent=widgets['shadersListInternalLayout'])
    widgets['shadersList'] = pc.textScrollList(parent=widgets['shadersListInternalLayout'])
    
    # Shaders attributes layout
    widgets['shadersAttrLayout'] = pc.frameLayout( label='Shaders attributes', borderStyle='etchedIn', cll=True, h=400, parent=widgets['mainLayout'] )
    widgets['shadersAttrInternalLayout'] = pc.columnLayout(parent=widgets['shadersAttrLayout'], cal="left")
    
    #test
    widgets['removeUIButton'] = pc.button(label="Remove UI", command=removeUI, parent=widgets['mainLayout'])
    
    # Displays main window
    pc.showWindow(widgets['mainWindow'])
    




UI()



def refreshUI():
    # Get selected shader name
    widgets['miscButtonsLayout'] = pc.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'right'), parent=widgets['shadersAttrInternalLayout'])
    pc.button(label="Select", parent=widgets['miscButtonsLayout'])
    pc.button(label="Assign to selection", parent=widgets['miscButtonsLayout'])

    
    widgets['diffuseLabelLayout'] = pc.rowColumnLayout(nc=3, columnSpacing=[(1,5), (2,5), (3,5)], columnAlign=(1, 'right'), columnAttach=(2, 'both', 0), columnWidth=(2, 150), parent=widgets['shadersAttrInternalLayout'])
    pc.text( label='Diffuse ' , parent=widgets['diffuseLabelLayout'])
    pc.separator( height=20, style='in', parent=widgets['diffuseLabelLayout'])
    
    selected = widgets['shadersList'].getSelectItem()[0]
    
    widgets['diffuseSoloMode'] = pc.symbolButton(bgc=[ 0.5, 0.5, 0.5], w=20, h=20, image=(iconsPath + "eye.png"), parent=widgets['diffuseLabelLayout'])
    widgets['diffuseLayout'] = pc.rowLayout(nc=4, parent=widgets['shadersAttrInternalLayout'])

    widgets['diffuseColor'] = pc.attrColorSliderGrp(label="Color", w=200, cw=[(1,50), (2,30)], at = '%s.color' % selected, parent=widgets['diffuseLayout'])
    widgets['diffuseWeight'] = pc.attrFieldSliderGrp(label="Weight", w=200, cw=[(1,50), (2,50)], min=0, max=1.0, at='%s.Kd' % selected, pre=3, parent=widgets['shadersAttrInternalLayout'])
    widgets['diffuseRoughness'] = pc.attrFieldSliderGrp(label="Rough", w=200, cw=[(1,50), (2,50)], min=0, max=1.0, at='%s.diffuseRoughness' % selected, pre=3, parent=widgets['shadersAttrInternalLayout'])
    
    pc.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'right'), columnAttach=(2, 'both', 0), columnWidth=(2, 200), parent=widgets['shadersAttrInternalLayout'])
    pc.text( label='Specular ' )
    pc.separator( height=20, style='in')
    widgets['specularColor'] = pc.attrColorSliderGrp(label="Color", w=200, cw=[(1,50), (2,30)], at = '%s.KsColor' % selected, parent=widgets['shadersAttrInternalLayout'])
    widgets['specularWeight'] = pc.attrFieldSliderGrp(label="Weight", w=200, cw=[(1,50), (2,50)], pre=3, at = '%s.Ks' % selected, parent=widgets['shadersAttrInternalLayout'])
    widgets['specularBrdf'] = pc.attrEnumOptionMenuGrp(label="BRDF", w=200, cw=[(1,50)], ei=[(0,'stretched_phong'), (1,'ward_duer'), (2, 'cook_torrance')], at = '%s.specularBrdf' % selected, parent=widgets['shadersAttrInternalLayout'])
    widgets['specularRoughness'] = pc.attrFieldSliderGrp(label="Rough", w=200, cw=[(1,50), (2,50)], pre=4, at = '%s.specularRoughness' % selected, parent=widgets['shadersAttrInternalLayout'])
    widgets['specularUseFresnel'] = pc.attrEnumOptionMenuGrp(label="Fresnel", w=200, cw=[(1,50)], ei=[(0,'No'), (1,'Yes')], at = '%s.specularFresnel' % selected, parent=widgets['shadersAttrInternalLayout'])
    widgets['specularFresnel'] = pc.attrFieldSliderGrp(label="% at N", w=200, cw=[(1,50), (2,50)], pre=3, at = '%s.Ksn' % selected, parent=widgets['shadersAttrInternalLayout'])

    pc.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'right'), columnAttach=(2, 'both', 0), columnWidth=(2, 200), parent=widgets['shadersAttrInternalLayout'])
    pc.text( label='Bump Mapping ' )
    pc.separator( height=20, style='in')
    widgets['bump'] = pc.attrNavigationControlGrp(label="Bump", cw=[(1,50), (2,120)], at = '%s.normalCamera' % selected, parent=widgets['shadersAttrInternalLayout'])
    
widgets['shadersList'].doubleClickCommand(refreshUI)
pc.showWindow(widgets['mainWindow'])


