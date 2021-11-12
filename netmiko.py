import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

username = input('insert username ====> : ')
password = getpass.getpass('insert pssword ===> :')


#in this step you have to create files contain config   
#and read the content file

with open('biglabcommandSwitch') as fileswitch:
    filswitch = fileswitch.read().splitlines()

with open('biglabCommandrouter') as fileRouter:
    filerouter = fileRouter.read().splitlines()

    #contain ip of devices
    
with open('biglabip') as fielIp:  
    file_ip = fielIp.read().splitlines()

    
for ip_address in file_ip:
    print('in_start_is_'+ip_address)

    ip_all_device = ip_address

    cisco_type = {
        'device_type': 'ios',
        'ip': ip_all_device,
        'username': username,
        'password': password
    }
    
# function create connection
        
    try:
        connect_device = ConnectHandler(**cisco_type)
    except(AuthenticationException):
        print('authentication failure'+ip_all_device)
        continue
    except(NetmikoTimeoutException):
        print('time out to device'+ip_all_device)
        continue
    except(EOFError):
        print('end of file attempting device'+ip_all_device)
        continue
    except(SSHException):
        print('ssh issue'+ip_all_device)
        continue
    except Exception as unknow_error:
        print("strange error"+ unknow_error)
        continue

        # here need to erite your ios versios .. is depends you!!
lisl_version_ios = {
    'vios-adventerprisek9-m',
    'VIOS-adventerprisek9',
    'C1900-UNIVERSALK9-M',
    'C3570-ADVIPSERVICESK9-M',
}
out_find = 0
for check_ver_software in lisl_version_ios:
    print('llist_version'+check_ver_software)

    output_command = connect_device.send_command('show version')
    out_find = output_command.find(check_ver_software)

    if out_find > 0:
        print('software version found '+check_ver_software)
        break
    else:
        print('softawre version not found'+check_ver_software)

    if check_ver_software == 'vios-adventerprisek9-m':

        print('running' + check_ver_software + 'commands')
        output = connect_device.send_config_set(fileswitch)

    elif check_ver_software == 'VIOS-adventerprisek9':

        print('running'+check_ver_software+'commands')
        output = connect_device.send_config_set(fileRouter)

        print(output)












