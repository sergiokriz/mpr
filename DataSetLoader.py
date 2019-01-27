from Entity import Entity
import csv
import sys

class DataSetLoader:

  def normalizeDomainName(self,oldDomainName):

        result = oldDomainName.lower()
        result = result.replace(" ", "-")

        return result

  def loadFromFile(self, path):

    sys.stdout.write('Loading entities and domains from: [%s] [' % path)

    entityItemList=[]
    domainItemList=[]

    with open(path, 'r') as f:
        reader = csv.reader(f, quotechar='"', delimiter=',')

        for row in reader:

            domainName = self.normalizeDomainName(row[0])
            entityName = row[1]

            #Create a new entity.
            newEntity = Entity(entityName, domainName)
            newEntity.loadAttributes()
            entityItemList .append(newEntity)

            #Populate the list of domains that will be returned.
            if domainName not in domainItemList:
              domainItemList.append(domainName)

            sys.stdout.write('.')
            sys.stdout.flush()

    sys.stdout.write(']\n')

    return entityItemList , domainItemList