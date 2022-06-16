import paramiko
import time



def ssh_connection(host):
    """подулючение к SSH"""
    user = 'root'
    port = 22
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, port=port)
    return client


def ssh_command(host, command) -> list:
    """выполнение комманд на узле"""
    client = ssh_connection(host)
    stdin, stdout, stderr = client.exec_command(command)
    result = stdout.read().decode('utf-8').split()
    client.close()
    return result


def ssh_session_commands(host, commands: list) -> dict:
     """
     сессия SSH внутри котороый можно
     выполнять последовательность комманд
     """
     result = {'host': host,
               'commands': [],
               'state': True,
               }
     with ssh_connection(host) as client:
         device_access = client.invoke_shell()
         for command in commands:
             device_access.send(f'{command}\n')
             time.sleep(.5)
             output = device_access.recv(65000).decode()
             if 'InvalidRequest' in output:
                 result.update({'state': False})
                 return result
             #result['commands'].append({command: output})
             result['commands'].append(command)
     return result

