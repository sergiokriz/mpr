from SPARQLWrapper import SPARQLWrapper, JSON

def getEntityAttributes(url):
    attributes = []

    sparql = SPARQLWrapper("http://dbpedia.org/sparql/")
    sparql.addDefaultGraph("http://dbpedia.org")
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