from pprint import pprint

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

from time import time
from multiprocessing.dummy import Pool as ThreadPool

#------------------------------------------------------------------------------
def read_file( devices_filename ):
    with open( devices_filename ) as f:
        lines = f.read().splitlines()
    return lines

#------------------------------------------------------------------------------
def config_worker (device):
    isok = True
    try:
        net_connect = ConnectHandler(**device)
    except (AuthenticationException):
        print ('Authentication failure: ' + device["ip"])
        isok = False
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + device["ip"])
        isok = False
    except (EOFError):
        print ('End of file while attempting device ' + device["ip"])
        isok = False
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + device["ip"])
        isok = False
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        isok = False
    
    if (isok == True):
        output = net_connect.send_config_set(commands)
        print (output)

#------------------------------------------------------------------------------

addresses = read_file("devices-file")
commands = read_file("config-file")

num_threads = 4
config_params_list = []

for items in addresses:
    device = {
        'device_type': 'cisco_ios',
        'ip': items,
        'username': '',
        'password': '',
    }
    config_params_list.append( ( device ) )
    
starting_time = time()

threads = ThreadPool( num_threads )
results = threads.map( config_worker, config_params_list )

threads.close()
threads.join()

print ("\nConfiguración finalizada, tiempo demorado:", round(time()-starting_time, 2), "segundos")