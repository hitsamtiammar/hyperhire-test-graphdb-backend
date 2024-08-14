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
    print('Hello 12345 44444')
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    dir = "blazegraph-servers/9000"
    #dir = os.path.join(os.getcwd(), dir) 
    print('hehe: ' +os.path.join(parent_dir, dir))
    dir = os.path.join(parent_dir, dir)
    if not os.path.exists(dir):
        os.mkdir(dir)

    process_result = subprocess.Popen(['python', parent_dir + '/../test.py' ])
    print('this is dir ' + dir)
    print('This is output')
    print(process_result.stdout)

    # target_dir = os.path.join(parent_dir, 'blazegraph-servers', '8787')
    
    # if not os.path.exists(target_dir):
    #     os.mkdir(target_dir)
    #     shutil.copy(os.path.join(parent_dir, 'blazegraph.jar'), os.path.join(target_dir, 'blazegraph.jar') )


    str_command = 'java -server -Xmx10g -Djetty.port=<port> -jar <blazegraph>'

    str_command = str_command.replace('<port>', '8787')\
        .replace('<blazegraph>', os.path.join(parent_dir, 'blazegraph.jar'))

    print(str_command)

    print(str_command.split(' '))

    process_result = subprocess.Popen(['python', parent_dir + '/../test.py' ])

    process_result_blaze = subprocess.Popen(str_command.split(' '))

    print('pid:')
    #print(process_result_blaze.pid)
  
    # print(output) 
    # print(error) 
    return {'Data': 'This is post example', 'all': request.json}