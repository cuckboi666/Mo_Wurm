import socket
from urllib.request import urlopen 
import urllib 

def get_priv_ip():
    """
    steals IP addy
    """
    ip = socket.gethostbyname(socket.gethostname())
    return ip
    

def get_pub_ip():
    import re
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+.\d+.\d+.\d+)').search(data).group(1)