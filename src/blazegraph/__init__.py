import requests
from xml.dom.minidom import parseString

import re

def fetch_url_data(url):
    response = requests.get(url)
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