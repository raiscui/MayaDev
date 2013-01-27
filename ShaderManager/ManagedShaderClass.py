# This class is meant to represent an aiStandard shader
# with its attributes stored in attributesDict
# along with several methods allowing to manipulate the shader
# and its incoming connections

import pymel.core as pc

class LookdevAssistant:
    
    def __init__(self, shaderName):
        # Shader name is retrieved from Maya
        self.shaderName = str(shaderName)
        # Along with a dictionnaire containing all shader attributes and their associated values
        self.attributesDict = {}
        
    def getInfosFromMaya(self):
        """Populate a LookdevAssistant objet with the informations from its real counterpart in Maya"""
        print("#INFO# '{0}' // Retrieving attributes and values from Maya.".format(self.shaderName))
        myShader = pc.PyNode(self.shaderName)
        attributes = myShader.listAttr()

        for attribute in attributes:
            splittedAttribute = str(attribute.split(".")[1])
            value = str(myShader.getAttr(splittedAttribute))
            self.attributesDict[splittedAttribute] = value
            
        print("#INFO# '{1}' // Found {0} attributes inside shader.".format(len(attributes), self.shaderName))
        
    def hasIncomingConnections(self, attribute):
        """Test if a specific attribute has incoming connection or not"""
        myShader = pc.PyNode(self.shaderName)
        hasConnections = myShader.attr(attribute).listConnections(d=False, s=True, c=True)
    
        if hasConnections:
            return True
        else:
            return False
        
    def incomingNodeName(self,attribute):
        """Return the name of the node connected to the specified attribute"""
        if self.hasIncomingConnections(attribute):
            myShader = pc.PyNode(self.shaderName)
            nodeName = myShader.attr(attribute).listConnections(d=False, s=True)[0].name()
            return nodeName
        else:
            raise Exception("#ERROR# '{0}' // Attribute '{1}' has no input connections.".format(self.shaderName, attribute))
        
    
    def reflectance(self, ior, k=0):
        """Return a reflectance at 0 degrees from a given IOR"""
        result = ((float(ior) - 1)**2 + float(k)**2)/((float(ior) + 1)**2 + float(k)**2)
        return result
    
    def selectAttributeInput(self, attribute):
        """Select an attribute input connection"""
        if self.hasIncomingConnections(attribute):
            inputCon = self.incomingNodeName(attribute)
            pc.select(inputCon[0])
        else:
            raise Exception("#ERROR# '{0}' // Attribute '{1}' has no input connections.".format(self.shaderName, attribute))
        
    def incomingNodeOrigin(self, attribute):
        """
        Return the attribute from where the connection originated
        This is useful to know if RGB->RGB or alpha->RGB
        """
        
        # TODO: Pour le cas du outAlpha, il faut tester si il y a des connections sur colorR, colorB, etc car
        # c'est different de color tout court...
        nodeName = self.incomingNodeName(attribute)
        myShader = pc.PyNode(nodeName)
        
        
         
        connectionOrigin = myShader.attr('outColor').listConnections(c=True)
        conOrig = ""  
        
        for origin in connectionOrigin:
            if origin[1] == self.shaderName:
                conOrig = origin[0].split('.')[1]
                break
        
        # If outColor has no output connection to our shader, we try outAlpha      
        if conOrig == "": 
            connectionOrigin = myShader.attr('outAlpha').listConnections(c=True)
            
            for origin in connectionOrigin:
                if origin[1] == self.shaderName:
                    conOrig = origin[0].split('.')[1]
                    break
        
        if conOrig == "":
            raise Exception("#ERROR# '{0}' // Connection from the incoming node '{1}' has not been retrieved successfully.".format(self.shaderName, nodeName))
            
        print("#INFO# '{0}' // Connection found : {0}.{1} >> {2}".format(nodeName,conOrig, self.shaderName + "." + attribute))
        return conOrig   
                 
    def Maya_focusOn(self, attribute):
        """Displays attribute input on a aiUtility flat surface"""
        
        # Check if dummy shader exists
        if len(pc.ls('dummySHD')) == 0:
            print("#INFO# '{0}' // Dummy shader not present. Creating.".format(self.shaderName))
            # ShadingGroup creation
            sg = pc.sets(renderable=True, noSurfaceShader=True, empty=True, name="aiUtilitySG")
            # aiUtility creation
            aiUtility = pc.shadingNode("aiUtility", asShader=True, name="dummySHD")
            aiUtility.outColor >> sg.surfaceShader
            # Set shade mode to flat
            aiUtility.shadeMode.set('flat')
            
            # Connect attribute input to the aiUtility
            origin = self.incomingNodeName(attribute)
            conType = self.incomingNodeOrigin(attribute)
            
            myNode = pc.PyNode(origin)
            myNode.attr(conType).connect(aiUtility.color)
            
            # Select all objets with current shader and assign dummySHD
            self.Maya_replaceMaterial(self.shaderName, 'dummySHD')
        else:
            self.Maya_replaceMaterial('dummySHD', self.shaderName)
            print("#INFO# '{0}' // Deleting dummy shader.".format(self.shaderName))
            pc.delete('dummySHD')
            pc.delete('aiUtilitySG')
            
    def Maya_replaceMaterial(self, mat1, mat2):
        """Replace current material mat1 by another material mat2"""
        pc.hyperShade(o=mat1)
        test = pc.ls(sl=1)
        
        if len(test) == 0:
            raise Exception("Tried to replace '{0}' by '{1}' but '{0}' is not assigned to any object in the scene.".format(mat1, mat2))
        
        pc.hyperShade(assign=mat2)
        print("Successfully replaced '{0}' by '{1}' on meshes :".format(mat1, mat2))
        
        for testObject in test:
            print("- {0}".format(testObject.name()))
        
        
        
    
            
            
        
        

