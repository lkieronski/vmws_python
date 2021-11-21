# vmws_python

Deploy fast lab_env in VMWare Workstation Pro

Requirements:
    - import python requests module:
        pip install requests
    
You need to turn on rest api on host server:
    vmrest.exe in your vmware workstation directory, please look into vmware documentation. 

-----------------------------------
Example:
config.json

{
    "host":"192.168.0.101",
    "connection":"https_noverify",
    "login":"workstation",
    "password":"P@$$w0rd"
}

----------------------------------

connection types:
    - http
    - https
    - https_noverify