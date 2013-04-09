import pymel.core as pc
import re

# UI Elements
uiWidgets = {}

def replaceString(*args):
    
    fileNodes = pc.ls(exactType='file')
    
    # Get the search string
    searchString = pc.textField(uiWidgets['searchField'], q=1, text=1)
    
    # Get the replace string
    replaceString = pc.textField(uiWidgets['replaceField'], q=1, text=1)
    
    if len(searchString) == 0 or len(replaceString) == 0:
        pc.confirmDialog(t="Error", message="Either the search or the replace string is empty. Try again.", icon='critical')
        exit(1)
    
    fileModified = 0
        
    for node in fileNodes:
    
        filePath = str(node.fileTextureName.get())
        print "Found a file node: %s" % node
        print "Current path is: %s" % filePath
        
        if str(searchString) in filePath:
            print "Found an occurence of the search string."
            print type(filePath)
            newFilePath = filePath.replace(searchString,replaceString)
            print "Setting new path to: %s" % newFilePath
            
            node.fileTextureName.set(newFilePath)
            fileModified += 1
    
    pc.confirmDialog(t="Success", message=str(fileModified)+" file(s) has been modified.")


# Delete windows if already existing
if pc.window("txSearchReplace", exists=True):
    pc.deleteUI("txSearchReplace") 
    
uiWidgets['window'] = pc.window("txSearchReplace", menuBar=True, title="Texture Search & Replace", sizeable=False, h=200, w=300)

# Main layout
uiWidgets['mainLayout'] = pc.columnLayout()

uiWidgets['sub1'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='+ Search string: ', parent=uiWidgets['sub1'])

pc.separator(h=5, p=uiWidgets['sub1'])
uiWidgets['searchField'] = pc.textField(w=300)

uiWidgets['sub2'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.text(l='+ Replace with: ', parent=uiWidgets['sub2'])
pc.separator(h=5, p=uiWidgets['sub2'])

uiWidgets['replaceField'] = pc.textField(w=300)

uiWidgets['sub3'] = pc.columnLayout(p=uiWidgets['mainLayout'])
pc.separator(h=5, p=uiWidgets['sub3'])

pc.button(l='Replace', c=replaceString)

pc.showWindow(uiWidgets['window'])