import requests
from xml.dom.minidom import parseString

import re

def fetch_url_data(url):
    response = requests.get(url)
    requests.post('aa')
    text_response = response.text
    return text_response

def get_status_list(url):
    text_response = fetch_url_data(f"{url}/blazegraph/status")
    result = {}
    print('status', text_response)
    listValues = ['runningQueriesCount', 'queryStartCount', 'queryErrorCount', 'queryPerSecond', 'operatorTasksPerQuery', 'operatorStartCount', 'operatorHaltCount','operatorActiveCount','deadlineQueueSize']
    for value in listValues:
         reg_result = re.findall(f"{value}=([0-9a-zA-Z]+)", text_response)
         print('reg_result', reg_result)
         result[value] = int(reg_result[0]) if len(reg_result) > 0 else None
    
    return result

def create_namespace(url, name):
    prepare_text = f"""
    com.bigdata.rdf.sail.namespace={name}
    com.bigdata.rdf.store.AbstractTripleStore.textIndex=false
    com.bigdata.rdf.sail.truthMaintenance=false
    com.bigdata.rdf.store.AbstractTripleStore.quads=false
    com.bigdata.rdf.store.AbstractTripleStore.statementIdentifiers=false
    com.bigdata.rdf.store.AbstractTripleStore.axiomsClass=com.bigdata.rdf.axioms.NoAxioms
    com.bigdata.rdf.store.AbstractTripleStore.justify=false
    com.bigdata.rdf.sail.isolatableIndices=false
    com.bigdata.rdf.store.AbstractTripleStore.geoSpatial=false
    """

    prepared_response = requests.post(f"{url}/blazegraph/namespace/prepareProperties", 
                                    data=prepare_text, 
                                    headers={'Content-Type': 'text/plain'})
    prepared_result = prepared_response.text

    root_result = parseString(prepared_result)
    elements = root_result.getElementsByTagName('entry')
    dict_result = {}
    for child in elements:
        key = child.attributes.get('key').nodeValue
        value = child.firstChild.nodeValue
        dict_result[key] = value

    text_request = ''

    for key, value in dict_result.items():
        text_request += f"{key}={value}\n"
    
    namespace_response = requests.post(f"{url}/blazegraph/namespace",
                                       data=text_request,
                                        headers={'Content-Type': 'text/plain'}
                                       )
    return namespace_response.text, namespace_response.status_code
    

def get_namespace(url):
    text_response = fetch_url_data(f"{url}/blazegraph/namespace?describe-each-named-graph=true")
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