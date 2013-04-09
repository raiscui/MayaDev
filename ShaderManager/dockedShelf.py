import pymel.core as pc
import os
import fnmatch
from functools import partial

class DockableShelf():
    
    def __init__(self):
        
        # Folder stuff
        self.scanFolder = 'ygShelf'
        
        # UI
        self.windowName = 'ygShelf'
        self.windowHeight = 400
        self.windowWidth = 109
        
        self.uiWidgets = {}
        
        self.buildUI()
        
    def buildUI(self):
        
        # Make sure there are no duplicated UI
        if pc.window(self.windowName, exists=True):
            pc.deleteUI(self.windowName)
        if pc.dockControl(self.windowName+'_dock', exists=True):
            pc.deleteUI(self.windowName+'_dock')
        
        # Dock window
        self.uiWidgets['window'] = pc.window(self.windowName, title=self.windowName, h=self.windowHeight, w=self.windowWidth, mnb=False, mxb=False, sizeable=False)
        
        # Layout and dock
        self.uiWidgets['layout'] = pc.columnLayout(p=self.uiWidgets['window'])
        pc.dockControl(self.windowName+'_dock', label=self.windowName, area='right', content=self.uiWidgets['window'])
        
        #### Tabs and buttons creation
        # Categories list
        categories = {}
        
        # Check for file that has to be ignored
        ignoreFile = open(pc.internalVar(upd=True)+'scripts/'+self.scanFolder+'/ignore.txt')
        ignoredFiles = []
        for line in ignoreFile:
            ignoredFiles.append(line.replace('\n',''))
        
        # Check for existing *.py files in the script/self.scanFolder folder
        for pyscript in os.listdir(pc.internalVar(upd=True)+'scripts/'+self.scanFolder):
            if fnmatch.fnmatch(pyscript, '*.py') and pyscript not in ignoredFiles:
                # Get the category for later use
                category = pyscript.partition('_')[0]
                # If category is not empty
                if category != '':
                    if category not in categories.keys():
                        categories[category] = []
                    # Append the icon path associated to the script
                    print "Adding script '%s' to shelf." % pyscript
                    categories[category].append(pyscript.partition('.')[0]+'.png')
                    
        print categories
        
        for category in categories.keys():
            self.uiWidgets[category+'_frameLayout'] = pc.frameLayout(label=category.capitalize(), borderStyle='etchedIn', cll=True, w=self.windowWidth, parent=self.uiWidgets['layout'])
            
            self.uiWidgets[category+'_rcLayout']= pc.rowColumnLayout(nc=3, p=self.uiWidgets[category+'_frameLayout'])
            
            for icon in categories[category]:
                iconPath = pc.internalVar(upd=True)+'icons/'+self.scanFolder+'/'+icon
                # If icon exists, we use it
                if os.path.exists(iconPath):
                    pc.iconTextButton(w=35, h=35, i1=iconPath,c=partial(self.loadScript, icon.partition('.')[0]))
                else:
                    pc.iconTextButton(iol=icon.partition('.')[0].partition('_')[2], w=35, h=35, i1=pc.internalVar(upd=True)+'icons/'+self.scanFolder+'/missing.png',c=partial(self.loadScript, icon.partition('.')[0]))
                    
    def loadScript(self, script, *args):
        
        scriptName = script.partition('_')[2]
        
        exec 'import ygShelf.'+script+' as '+scriptName[0:3]+''+scriptName[-1]
        exec 'reload('+scriptName[0:3]+''+scriptName[-1]+')'
    
    
toto = DockableShelf()