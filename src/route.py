from server import app
from flask import request
import os
import subprocess
import shutil
from src.blazegraph\
    import connect_to_db, create_database_redirection, delete_namespace, execute_ttl, get_namespace, get_status_list, create_namespace

@app.route('/')
def index():
    return {"Data": "12345"}

@app.route('/get-status')
def get_status_list_local():
    url = request.args.get('url')
    if url is None:
        return {'message': 'URL is required'}, 400
    try:
        namespaces = get_status_list(url)
        return {'message': 'success', 'status_list': namespaces}
    except Exception as err:
        print(err)
        return {'message': 'An error occured', 'err': str(err)}
    
@app.route('/connect', methods=['POST'])
def connect_to_db_local():
    url = request.json['url']
    port = request.json['port']
    result, code = connect_to_db(url, port)

    if code != 200:
        return { 'status': False }, code
    return result, code

@app.route('/get-namespace')
def get_namespace_local():
    url = request.args.get('url')
    if url is None:
        return {'message': 'URL is required'}, 400
    try:
        namespaces = get_namespace(url)
        return {'message': 'success', 'namespace': namespaces}
    except Exception:
        return {'message': 'An error occured'}, 500

@app.route('/create-namespace', methods=['POST'])
def create_namespace_local():
    name = request.json['name']
    url = request.json['url']
    result, status_code = create_namespace(url, name)

    return result, status_code

@app.route('/delete-namespace', methods=['POST'])
def delete_namespace_local():
    name = request.json['name']
    url = request.json['url']
    response, code = delete_namespace(url, name)

    return response, code

@app.route('/upload-ttl', methods=['POST'])
def upload_ttl_local():
    files = request.files

    contents = []

    for file in files.values():
        content = file.read().decode('utf-8')
        contents.append(content)
    
    url = request.form['url']
    namespace = request.form['namespace']
    result = execute_ttl(url, namespace, contents)

    return result

@app.route('/create-database-redirection', methods=['POST'])
def create_database_redirection_local():
    port = request.json['port']
    url = request.json['url']
    maximum_usage = request.json['minimumUsage'] if 'minimumUsage' in request.json else None 
    minimum_usage = request.json['minimumUsage'] if 'minimumUsage' in request.json else None
    result, status_code = create_database_redirection(url, port, maximum_usage, minimum_usage)

    return result, status_code
    

@app.route('/create-database', methods=['POST'])
def create_database():
    working_directory = os.getcwd()
    os.chdir(working_directory)
    parent_dir = os.path.dirname(os.path.realpath(__file__))

    blazegraph_dir = os.path.join(parent_dir, 'blazegraph-servers')

    if not os.path.exists(blazegraph_dir):
        os.mkdir(blazegraph_dir)

    port = request.json['port']
    target_dir = os.path.join(blazegraph_dir, str(port))

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    blazegraph_target_dir =os.path.join(target_dir, 'blazegraph.jar')

    if not os.path.exists(blazegraph_target_dir):
        shutil.copy(os.path.join(parent_dir, 'blazegraph.jar'), blazegraph_target_dir)

    maximum_usage = request.json['minimumUsage'] if 'minimumUsage' in request.json and request.json['minimumUsage'] > 0 else 1 
    minimum_usage = request.json['minimumUsage'] if 'minimumUsage' in request.json and request.json['minimumUsage'] > 0 else 1 

    maximum_usage_cmd = f"-Xmx{maximum_usage}g" if maximum_usage is not None else ''
    minimum_usage_cmd = f"-Xms{minimum_usage}g" if minimum_usage is not None else ''


    str_command = f"java -server {maximum_usage_cmd} {minimum_usage_cmd} -Djetty.port={port} -jar <blazegraph>"
    str_command = str_command.replace('<blazegraph>', os.path.join(target_dir, 'blazegraph.jar'))

    os.chdir(os.path.join(target_dir))

    log_file = os.path.join(target_dir, 'file.log')
    flag = 'w'

    if os.path.exists(log_file):
        flag = 'a'

    with open(log_file, flag) as out_file:
        subprocess.Popen(str_command.split(' '), stdout=out_file)

    return {
        'status': 'Success',
        'message': 'Wait for a while before the server is ready to connect'
    }