from DataSetLoader import DataSetLoader

class ModelObjectFactory:

    def __init__(self):
        self.listEntities = []
        self.listDomains = []

    def loadObjectsFromFile(self, fileName):
        self.listEntities, self.listDomains = DataSetLoader().loadFromFile(fileName)

    def getDomains(self):
        return self.listDomains

    def getEntities(self):
        return self.listEntities

    def printEntities(self):

        for entity in self.listEntities:

            print("Entity name [%s] Domain name [%s]" % (entity.getEntityName(), entity.getDomainName()))

            print("List of Properties:")
            for property in entity.getProperties():
                print("\tProperty name [%s]" % (property))

