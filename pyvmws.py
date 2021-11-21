import json
import requests
from time import sleep
from requests.models import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

class pyvmws:
    def __init__(self, host, type, user, passwd):
        if (type == 'https'):
            protocol = 'https://'
            self.cert_verify = True
        elif (type == 'https_noverify'):
            protocol = 'https://'
            self.cert_verify = False
        elif (type == 'http'):
            protocol= 'http://'
            self.cert_verify = False

        self.base_url = '{}{}:8697/api/'.format(protocol, host)
        self.api_auth = HTTPBasicAuth(user,passwd)

    def make_request(self, type, api_req, api_data=''):
        req_url = self.base_url+api_req
        api_headers={"Content-Type": "application/vnd.vmware.vmw.rest-v1+json", "Accept": "application/vnd.vmware.vmw.rest-v1+json"}

        if (type == 'get'):
            r = requests.get(url=req_url,auth=self.api_auth ,headers=api_headers,data=api_data,verify=self.cert_verify)
            return r.json()
        elif (type == 'put'):
            r = requests.put(url=req_url,auth=self.api_auth ,headers=api_headers,data=api_data,verify=self.cert_verify)
            return r.json()
        elif (type == 'post'):
            r = requests.post(url=req_url,auth=self.api_auth ,headers=api_headers,data=api_data,verify=self.cert_verify)
            return r.json()
        elif (type == 'delete'):
            requests.delete(url=req_url,auth=self.api_auth ,headers=api_headers,data=api_data,verify=self.cert_verify)
        

    def get_vms(self):
         return self.make_request('get','vms')

    def get_vms_details(self):
        vms = self.get_vms()
        vm_list = []
        for vm in vms:
            tmp = self.get_vm_info(vm['id'])
            processors = tmp['cpu']['processors']
            memory = tmp['memory']
            tmp = self.get_vm_power(vm['id'])
            powerstate = tmp['power_state']
            vminfo = {'id' : vm['id'], 'path': vm['path'], 'processors' : processors, 'memory' : memory, 'powerstate' : powerstate}
            if (powerstate == 'poweredOn'):
                tmp = self.get_vm_ip(vm['id'])
                vminfo['ip'] = tmp['ip']
            vm_list.append(vminfo)
        return vm_list

    def get_vm_info(self, id):
        req = 'vms/{}'.format(id)
        return self.make_request('get',req)

    def get_vm_power(self, id):
        req = 'vms/{}/power'.format(id)
        return self.make_request('get',req)

    def get_vm_ip(self, id):
        req = 'vms/{}/ip'.format(id)
        return self.make_request('get',req)

    def set_vm_power(self, id, state):
        req = 'vms/{}/power'.format(id)
        return self.make_request('put', req , state)

    def set_vm_params(self, id, processors='', memory=''):
        params = dict()
        if (processors != ''):
            params['processors'] = processors
        if (memory != ''):
            params['memory'] = memory
        req = 'vms/{}'.format(id)
        p = json.dumps(params)
        return self.make_request('put', req, p)

    def duplicate_vm(self, id, name):
        req = 'vms'
        data = {'name': name, 'parentId': id}
        data_json = json.dumps(data)
        return self.make_request('post', req, data_json)

    def duplicate_vm_x_times(self, id, name, number):
        vm_id_list = []
        #vm_ip_list = []
        vm_list = []
        for i in range(number):
            vm_name='{}_{}'.format(name,i)
            r = self.duplicate_vm(id, vm_name)
            new_vm_id = r['id']
            vm_id_list.append(new_vm_id)
            self.set_vm_power(new_vm_id, 'on')
        sleep(120)
        i = 0
        for vm_id in vm_id_list:
            r = self.get_vm_ip(vm_id)
            vm_ip = r['ip']
            #vm_ip_list.append(vm_ip)
            vm_info = {'id': vm_id_list[i], 'ip': vm_ip}
            vm_list.append(vm_info)
            i+=1
        return vm_list

    def duplicate_and_delete_vm(self, id, name):
        req = 'vms'
        data = {'name': name, 'parentId': id}
        data_json = json.dumps(data)
        r = self.make_request('post', req, data_json)
        vm_id = r['id']
        self.set_vm_power(vm_id, 'on')
        sleep(120)
        r = self.get_vm_ip(vm_id)
        vm_ip = r['ip']
        print('VM: {}\nip: {}'.format(vm_id, vm_ip))
        input('After key press the VM will be deleted')
        print('Turning off VM...')
        self.set_vm_power(vm_id, 'off')
        print('Deleting VM...')
        self.delete_vm(vm_id)

    def duplicate_and_delete_vm_x_times(self, id, name, number):
        r = self.duplicate_vm_x_times(id, name, number)
        print('VM ips:')
        for vm in r:
            print('- {}'.format(vm['ip']))
        input('After key press the VM\'s will be deleted')
        for vm in r:
            self.set_vm_power(vm['id'], 'off')
            self.delete_vm(vm['id'])


    def delete_vm(self, id):
        req = 'vms/{}'.format(id)
        self.make_request('delete', req)

