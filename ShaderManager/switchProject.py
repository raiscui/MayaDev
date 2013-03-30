import pymel.core as pc
import re
import os

# Global locations for shots and assets. Must be modified depending on your configuration
assetLocation = '/mnt/Data/Runaway/Assets'
shotsLocation = '/home/student/Runaway_local/02_Plans'

def User_inputDialog(title, message):
        
    result = pc.promptDialog(title=title, message=message, button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':
        text = pc.promptDialog(query=True, text=True)
        return text
    elif result == 'Cancel':
        exit('User abort.')

# Asks the user for input
result = User_inputDialog("Switch project", "Enter a shot ID or an asset name: ")

# Check what the user entered
userInput = {}

# If he entered 0, abort
if len(result) == 0:
    exit('You did not enter anything.')
# If he entered 3 characters
elif len(result) == 3:
    # We check if they are digits
    prog = re.compile('^[0-9]{3}$')
    test = prog.match(result)
    
    print test
    # If not, abort
    if test:
        print "Probably a shot"
        userInput['type'] = 'shot'
        userInput['value'] = result
    elif test is None:
        exit("Incorrect shot ID. Aborting.")
# If he entered more than 3
elif len(result) > 3:
    # We check if the string only contains alphabetical characters
    prog2 = re.compile('^[A-Za-z]+$')
    test2 = prog2.match(result)
    
    if test2:
        print "Probably an asset."
        userInput['type'] = 'asset'
        userInput['value'] = result
    elif test2 is None:
        exit('Incorrect asset name (only alphabetical characters are allowed). Aborting.')

else:
    exit("Incorrect input. Must be at leats 3 characters longs for a Shot ID or more than 3 characters long for an Asset. Aborting")
    
# From now on, we assume that the input is valid. 
# Now we gotta look in the filesystem if the folder exists or not.

if userInput['type'] == 'shot':
    shotExists = os.path.isdir(shotsLocation+'/01_'+userInput['value'])
    
    # Check if the shot folder exists
    if not shotExists:
        exit("Shot folder '01_"+userInput['value']+"' doesn't seem to exist. Please try again after creating the folder there manually.")
    
    # Check if the folder '01_Maya' exists inside the shot folder
    mayaFolderExists = os.path.isdir(shotsLocation+'/01_'+userInput['value']+'/01_Maya')
    
    if not mayaFolderExists:
        exit("The Maya folder inside shot folder '01_"+userInput['value']+"' doesn't seem to exist. Please try again or create the project there manually.")
    
    projectLocation = shotsLocation+'/01_'+userInput['value']+'/01_Maya'
    
elif userInput['type'] == 'asset':
    assetExists = os.path.isdir(assetLocation+'/'+userInput['value'])
    
    # Check if the asset folder exists
    if not assetExists:
        exit("Asset folder '"+userInput['value']+"' doesn't seem to exist. Please try again after creating the folder there manually.")
    
    # Check if there is at least the folder "scenes" inside the asset folder, so that we can assume there is a maya project there
    sceneFolderExists = os.path.isdir(assetLocation+'/'+userInput['value']+'/scenes')
    
    if not sceneFolderExists:
        exit("Asset folder '"+userInput['value']+"' doesn't seem to be a valid Maya project. Please try again or create the project there manually.")

    projectLocation = assetLocation+'/'+userInput['value']

# From now we assume that the folders exists and we can set the maya project to
# the location

print projectLocation
pc.mel.eval('setProject "'+projectLocation+'"')
pc.mel.eval('OpenScene')

