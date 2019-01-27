from SPARQLWrapper import SPARQLWrapper, JSON

def getEntityAttributes(url):
    attributes = []

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            select distinct ?o 
            where {
               %s ?o ?p .
            }
            """ % (url))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        attributes.append(result["o"]["value"])

    return attributes

listAttributes = getEntityAttributes('<https://en.wikipedia.org/wiki/Diego_Maradona>');
#listAttributes = getEntityAttributes("<http://dbpedia.org/resource/Diego_Maradona>");
#listAttributes = getEntityAttributes("<https://en.wikipedia.org/wiki/Golden_Gate_Cloning>");

for str in listAttributes:
    print(str)