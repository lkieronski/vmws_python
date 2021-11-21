from pyvmws import pyvmws
import json
import os.path

if not os.path.exists('./config.json'):
    print('Please create config.json file')
    print('''
    ### config.json example
    {
        "host":"<host>",
        "connection":"<connection type>",
        "login":"<login>",
        "password":"<password>"
    }
     ''')
else:
    f=open("./config.json","r")
    content = f.read()
    f.close
    conf = json.loads(content)
    


    # Creating new pyvmws class with credentials
    vmware = pyvmws(conf['host'], conf['connection'], conf['login'], conf['password'])
    
    # Defining templates
    centos_template_id = '3QO9EUNG80LLU7BR362VSREFB9HDA3MV'

    # Listing all VM's
    for vm in vmware.get_vms():
        print('id: {}\tpath: {}'.format(vm['id'],vm['path']))

    # Making simple lab env
    vmware.duplicate_and_delete_vm(centos_template_id, 'testlab_01')