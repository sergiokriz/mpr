from AttributeDetails import AttributeDetails

class AttributeBuilder:

    def __init__(self):
        self.listUniqueAttributes = {}

    def generateListUniqueAttributes(self, listEntities):

        self.listUniqueAttributes = {}

        for entity in listEntities:
            for attribute in entity.getAttributes():
                if not attribute in self.listUniqueAttributes:
                    self.listUniqueAttributes[attribute] = AttributeDetails()
                else:
                    self.listUniqueAttributes[attribute].numberOfOccurences = self.listUniqueAttributes[attribute].numberOfOccurences + 1

    def filterMostCommomAttributes(self, maxOccurrences):

        for key in self.listUniqueAttributes:
            if self.listUniqueAttributes[key].numberOfOccurences >= maxOccurrences:
                self.listUniqueAttributes[key].filtered = 1

    def listNotFilteredAttributes(self):

        listNotFilteredAttributes = []

        for key in self.listUniqueAttributes:
            if self.listUniqueAttributes[key].filtered == 0:
                listNotFilteredAttributes.append(key)

        return listNotFilteredAttributes

    def printNotFilteredAttributes(self, listAttributes):

        print("List of no filtered attributes:")

        for attribute in listAttributes:
            print("\t%s" % attribute)

        print("Total of attributes in the list [%d]" % len(listAttributes))

    def printStatUniqueAttributes(self):

        text_file = open("UniqueAttributes.txt", "w")

        print("Number of unique attributes: [%d]" % (len(self.listUniqueAttributes)))

        for idx, str in enumerate(self.listUniqueAttributes):
            text_file.write("Unique Attribute [%d] [%s]\n" % (idx, str))

        text_file.close()

    def printlistFilteredAttributes(self, filtered):

        numberInstances = 0

        print("List of %s attributes:" % (("no filtered", "filtered")[filtered == 1]))

        for key in self.listUniqueAttributes:
            if self.listUniqueAttributes[key].filtered == filtered:
                print("\t%s" % key)
                numberInstances += 1

        print("Number of attributes [%d]." % numberInstances)


