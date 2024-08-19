import requests
from xml.dom.minidom import parseString
from urllib.parse import urlparse
import json
import re

def connect_to_db(url, port):
    db_url = f"{url}:{port}/blazegraph"
    response = requests.get(db_url)

    print('db_url: ' + db_url)
    
    if response.status_code != 200:
        return {'message': 'Failed to connect'}, 500

    base_url = f"{url}:{port}"
    status_list = get_status_list(base_url)
    namespaces = get_namespace(base_url)
    return {
        'status_list': status_list,
        'namespaces': namespaces,
        'status': True
    }, 200

def fetch_url_data(url):
    response = requests.get(url)
    text_response = response.text
    return text_response

def get_status_list(url):
    url_send = f"{url}/blazegraph/status"
    url_detail = urlparse(url_send)
    text_response = fetch_url_data(url_send)
    result = {}
    result['hostname'] = url_detail.hostname
    result['port'] = url_detail.port
    result['scheme'] = url_detail.scheme
    result['databasetype'] = 'blazegraph'

    listValues = ['runningQueriesCount', 'queryStartCount', 'queryErrorCount', 'queryPerSecond', 'operatorTasksPerQuery', 'operatorStartCount', 'operatorHaltCount','operatorActiveCount','deadlineQueueSize', 'queryDoneCount']
    for value in listValues:
         reg_result = re.findall(f"{value}=([0-9a-zA-Z]+)", text_response)
         result[value] = int(reg_result[0]) if len(reg_result) > 0 else None
    
    return result

def execute_ttl(url, namespace, contents):
    sparql_url = f"{url}/blazegraph/namespace/{namespace}/sparql"
    results = []
    for content in contents:
        response = requests.post(sparql_url, data=content, headers={
            'Content-Type': 'application/x-turtle'
        })
        results.append({
            'text': response.text,
            'code': response.status_code
        })
    return results

def delete_namespace(url, name):
    new_url = f"{url}/blazegraph/namespace/{name}"
    response = requests.delete(new_url)

    if response.status_code == 200:
        return 'Success', 200
    return 'Failed', 500

def create_database_redirection(url, port, maximum_usage, minimum_usage):
    url_redirection = f"{url}/create-database"
    print('url: ' + url_redirection)
    request_data = {
        'port': port
    }

    request_data['maximumUsage']

    if maximum_usage > 0:
        request_data['maximumUsage'] = maximum_usage
    else:
        request_data['maximumUsage'] = 1

    if minimum_usage > 0:
        request_data['minimumUsage'] = minimum_usage
    else:
        request_data['minimumUsage'] = 1

    response = requests.post(url_redirection, data=json.dumps(request_data), headers= { 'Content-Type': 'application/json' })

    print('text response')
    print(response.text)
    if response.status_code == 200:
        return 'Success', 200
    return 'Failed', response.status_code

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