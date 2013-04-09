import maya.cmds as cmds

if cmds.commandPort(':7720', q=True) !=1:

    cmds.commandPort(n=':7720', eo = False, nr = True)