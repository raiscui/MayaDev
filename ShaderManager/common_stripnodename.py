## Import pymel
import pymel.core as pc

dialog = pc.promptDialog(title='Search joker',
                    message='Enter the characters you want removed from matching nodes:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')

joker = pc.promptDialog(query=True, text=True)

## Stores a list of all objects starting with joker
objects = pc.ls(joker+"*")

for obj in objects:
    ## The new name is the objects name without pasted__
    newName = obj.replace(joker, '')
    ## Rename the object with the new name
    pc.rename(obj, newName)