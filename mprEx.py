import sys, getopt
import sklearn
from builtins import enumerate
from AttributeBuilder import AttributeBuilder
from ModelObjectFactory import ModelObjectFactory
from sklearn import tree

def generateAttributeDeclarationAllEntities(listAttributes, listEntities):

    for idx, attribute in enumerate(listAttributes):
        for entity in listEntities:
            entity.setAttributeDeclarationByIndex(idx, attribute)

def printListAttributeDeclarationsByEntity(fileName, listEntities):

    text_file = open(fileName, "w")

    for entity in listEntities:
        text_file.write("Entiry name [%s]\n" % entity.getEntityName())
        text_file.write("Number of attributes %d " % len(entity.getAttributes()))
        text_file.write(str(entity.getAttributes().values()) + "\n")

    text_file.close()

def generateArffFile(fileName, listEntities, listDomains, listAttributes, minPercentageAttributesMapped):

    arff_file = open(fileName, "w")

    arff_file.write("@relation entity-domain\n\n")

    #header
    for attribute in listAttributes:
        arff_file.write("@attribute %s numeric\n" % attribute)

    arff_file.write("\n@attribute class {")
    arff_file.write("%s" % ','.join(e for e in listDomains))

    arff_file.write("}\n\n")
    #end of header.

    #Data segment.
    arff_file.write("@data\n\n")
    for entity in listEntities:

        percentageAttributesMapped = entity.totalNumberOfAttributeDeclaration() / len(listAttributes) * 100

        if percentageAttributesMapped >= minPercentageAttributesMapped:
            arff_file.write( ','.join(str(e) for e in entity.getAttributeDeclararionEntityList(len(listAttributes))))
            arff_file.write(",%s\n" % entity.getDomainName())

    #end of the data segment.

    arff_file.close()

def printPotentiallyWeakEntities(listNotFilteredAttributes, listEntities):

    print("Number of Unique Not Filtered Attributes [%d]." % len(listNotFilteredAttributes))

    listEntities.sort(key=lambda x: x.totalNumberOfAttributeDeclaration(), reverse=False)

    for entity in listEntities:
        print("Entity Name [%s] Total Attribute Declaration [%d] Percentage Mapped [%f]" %
              (entity.getEntityName(),
               entity.totalNumberOfAttributeDeclaration(),
               (entity.totalNumberOfAttributeDeclaration() / len(listNotFilteredAttributes) * 100)))

class mprEx:

    def __init__(self):
        self.inputTrainingFile = ''
        self.inputPredictionFile = ''
        self.outputWeka = False
        self.outputDomainList = False
        self.modelObjectFactoryTraining = ModelObjectFactory()
        self.modelObjectFactoryPrediction= ModelObjectFactory()
        self.uniqueAttributes = AttributeBuilder()

    def parseCmdArgs(self, argv):

        try:
            opts, args = getopt.getopt(argv[1:], "ht:p:wd")

            for opt, arg in opts:

                if arg == '-h':
                    print('%s -i <inputfile> -o <outputfile>' % argv[0])
                    sys.exit()
                elif opt in ("-t"):
                    self.inputTrainingFile = arg.strip()
                elif opt in ("-p"):
                    self.inputPredictionFile = arg.strip()
                elif opt in ("-w"):
                    self.outputWeka = True
                elif opt in ("-d"):
                    self.outputDomainList = True

        except getopt.GetoptError:
            print('%s -t <trainingfile> -o <predictionfile>' % argv[0])
            sys.exit(2)

    def printDomainList(self):

        print("Printing the Domain List")
        self.modelObjectFactoryTraining.loadObjectsFromFile(self.inputTrainingFile)
        domains = self.modelObjectFactoryTraining.getDomains()
        for domain in domains:
            print(domain)

        return

    def runNewEncodingFeatures(self):

        if self.outputDomainList:
            self.printDomainList()
            return

        # Training Part.
        self.modelObjectFactoryTraining.loadObjectsFromFile(self.inputTrainingFile)

        self.uniqueAttributes = AttributeBuilder()
        self.uniqueAttributes.generateListUniqueAttributes(self.modelObjectFactoryTraining.listEntities)
        self.uniqueAttributes.filterMostCommomAttributes(100)

        generateAttributeDeclarationAllEntities(self.uniqueAttributes.listNotFilteredAttributes(),
                                                self.modelObjectFactoryTraining.listEntities)

        featuresList = []
        labelsList = []

        for entity in self.modelObjectFactoryTraining.listEntities:

            percentageAttributesMapped = entity.totalNumberOfAttributeDeclaration() / len(self.uniqueAttributes.listNotFilteredAttributes()) * 100

            if percentageAttributesMapped >= 0.001:
                featuresList.append(entity.getAttributeDeclararionEntityList(len(self.uniqueAttributes.listNotFilteredAttributes())))
                labelsList.append(self.modelObjectFactoryTraining.listDomains.index(entity.domainName))

                print(entity.getAttributeDeclararionEntityList(len(self.uniqueAttributes.listNotFilteredAttributes())))
                print("Domain %d " % self.modelObjectFactoryTraining.listDomains.index(entity.domainName))

        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(featuresList, labelsList)

        print("Training is done.")

        # Prediction.
        self.modelObjectFactoryPrediction.loadObjectsFromFile(self.inputPredictionFile)

        generateAttributeDeclarationAllEntities(self.uniqueAttributes.listNotFilteredAttributes(),
                                                self.modelObjectFactoryPrediction.listEntities)

        predictionAttributList = self.createAttributeListForPrediction()

        print("Predictions result:")
        entityIndex=0
        for entity in self.modelObjectFactoryPrediction.listEntities:

            print("Entity name for prediction: [{0} Predicted Domain {1}. ".format(entity.entityName,
                                                                                   self.predictedDomain(clf.predict(predictionAttributList)[entityIndex])))
            entityIndex+=1

    def createAttributeListForPrediction(self):

        attributeListForPrediction = []

        for entity in self.modelObjectFactoryPrediction.listEntities:

            percentageAttributesMapped = entity.totalNumberOfAttributeDeclaration() / len(
                self.uniqueAttributes.listNotFilteredAttributes()) * 100

            if percentageAttributesMapped >= 0.001:
                attributesForPrediction = entity.getAttributeDeclararionEntityList(
                    len(self.uniqueAttributes.listNotFilteredAttributes()))
                attributeListForPrediction.append(attributesForPrediction)

        return attributeListForPrediction

    def predictedDomain(self, indexReturnedPrediction):

        if indexReturnedPrediction < len(self.modelObjectFactoryTraining.getDomains()):
           result = self.modelObjectFactoryTraining.getDomains()[indexReturnedPrediction]
        else:
           result = "can't predict the domain."
        return result

        #if (clf.predict(predict)[0]) == int(0):
        #    print('you are describing orange')
        #elif (clf.predict(predict)[0]) == int(1):
        #    print('you are describing apple')
        #else:
        #    print('Can\'t Guess')

    def run(self):

        # Training Part.
        entitiesTraining = ModelObjectFactory()
        entitiesTraining.loadObjectsFromFile(self.inputTrainingFile)

        uniqueAttributes = AttributeBuilder()
        uniqueAttributes.generateListUniqueAttributes(entitiesTraining.listEntities)
        uniqueAttributes.filterMostCommomAttributes(100)

        generateAttributeDeclarationAllEntities(uniqueAttributes.listNotFilteredAttributes(),
                                               entitiesTraining.listEntities)

        if(self.outputWeka):

            generateArffFile("entity-domain-training.arff",
                             entitiesTraining.listEntities,
                             entitiesTraining.listDomains,
                             uniqueAttributes.listNotFilteredAttributes(),
                             0.001)

        # Predicition Part.
        entitiesPrediction = ModelObjectFactory()
        entitiesPrediction.loadEntities(self.inputPredictionFile)

        generateAttributeDeclarationAllEntities(uniqueAttributes.listNotFilteredAttributes(),
                                               entitiesPrediction.listEntities)

        if(self.outputWeka):

            generateArffFile("entity-domain-prediction.arff",
                             entitiesPrediction.listEntities,
                             entitiesTraining.listDomains,
                             uniqueAttributes.listNotFilteredAttributes(), 0.001)

        printPotentiallyWeakEntities(uniqueAttributes.listNotFilteredAttributes(),
                                     entitiesPrediction.listEntities)

        # Stats.
        # uniqueAttributes.printNotFilteredAttributes(uniqueAttributes.listNotFilteredAttributes())
        # uniqueAttributes.printStatUniqueAttributes()
        # uniqueAttributes.printlistFilteredAttributes(0)
        # uniqueAttributes.printlistFilteredAttributes(1)
        # printPotentiallyWeakEntities(uniqueAttributes.listNotFilteredAttributes(), entitiesTraining.listEntities)
        # printListAttributeDeclarationsByEntity("EntitiesAttributeDeclarations.txt", entities.listEntities)


if __name__ == "__main__":

    mprEx = mprEx()
    mprEx.parseCmdArgs(sys.argv)
    #mprEx.run()
    mprEx.runNewEncodingFeatures()

    print("Done!")