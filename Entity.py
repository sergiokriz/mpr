from SparqlUtil import getEntityAttributes

class Entity:

    def __init__(self, entityName, domainName):
        self.entityName = entityName
        self.domainName = domainName
        self.attributes ={}

    def getEntityName(self):
        return self.entityName

    def getDomainName(self):
        return self.domainName

    def getAttributes(self):
        return self.attributes

    def loadAttributes(self):
        for attribute in getEntityAttributes("<" + self.entityName + ">"):
            self.attributes[attribute] = 0

    def initializeAttributeDeclarionList(self, globalNumberAttributes):

        self.attributeDeclarationList = [0] * globalNumberAttributes

    def setAttributeDeclarationByIndex(self, globalAttributeIndex, attributeName):

        if attributeName in self.attributes:
            self.attributes[attributeName] = globalAttributeIndex

    def getAttributeDeclararionEntityList(self, totalNumberOfAttributes):

        result = [0] * totalNumberOfAttributes

        for idxAttribute in self.attributes.values():
            result[idxAttribute] = 1

        return result

    def totalNumberOfAttributeDeclaration(self):

        result = 0;

        for key in self.attributes:
            if self.attributes[key] != 0:
                result += 1

        return result

