import requests
from xml.dom.minidom import parseString

def get_namespace(url):
    response = requests.get(f"{url}/blazegraph/namespace?describe-each-named-graph=true")
    text_response = response.text
    root = parseString(text_response)

    elements = root.getElementsByTagName('rdf:Description')
    namespaces = []
    for child in elements:
        title = child.getElementsByTagName('Namespace')[0].firstChild.nodeValue
        sparqlEndpoint = child.getElementsByTagName('sparqlEndpoint')[0].attributes.get('rdf:resource')
        namespaces.append({
            'title': title,
            'sparqlEndpoint': sparqlEndpoint.nodeValue
        })

    return namespaces