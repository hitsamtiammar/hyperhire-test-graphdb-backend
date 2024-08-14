from server import app
from flask import request
import os
import subprocess
import shutil

@app.route('/')
def index():
    return {"Data": "12345"}

@app.route('/create-database', methods=['POST'])
def create_database():
    working_directory = os.getcwd()
    os.chdir(working_directory)
    parent_dir = os.path.dirname(os.path.realpath(__file__))

    blazegraph_dir = os.path.join(parent_dir, 'blazegraph-servers')

    if not os.path.exists(blazegraph_dir):
        os.mkdir(blazegraph_dir)

    print('blazegraph_dir: ' + blazegraph_dir)
    print('working_directory: ' + parent_dir)
    port = request.json['port']
    target_dir = os.path.join(blazegraph_dir, str(port))

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    blazegraph_target_dir =os.path.join(target_dir, 'blazegraph.jar')

    if not os.path.exists(blazegraph_target_dir):
        shutil.copy(os.path.join(parent_dir, 'blazegraph.jar'), blazegraph_target_dir)

    maximum_usage = request.json['minimumUsage'] if 'minimumUsage' in request.json else None 
    minimum_usage = request.json['minimumUsage'] if 'minimumUsage' in request.json else None 

    maximum_usage_cmd = f"-Xmx{maximum_usage}g" if maximum_usage is not None else ''
    minimum_usage_cmd = f"-Xms{minimum_usage}g" if minimum_usage is not None else ''


    str_command = f"java -server {maximum_usage_cmd} {minimum_usage_cmd} -Djetty.port={port} -jar <blazegraph>"
    str_command = str_command.replace('<blazegraph>', os.path.join(target_dir, 'blazegraph.jar'))

    os.chdir(os.path.join(target_dir))

    log_file = os.path.join(target_dir, 'file.log')
    flag = 'w'

    if os.path.exists(log_file):
        flag = 'a'

    out_file = open(log_file, flag)

    subprocess.Popen(str_command.split(' '), stdout=out_file)

    return {
        'status': 'Success',
        'message': 'Wait for a while before the server is ready to connect'
    }