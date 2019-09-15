from uuid import getnode as get_mac

# ================== Exceptions =================
class FakeMacError(Exception):
    def __init__(self):
        self.msg = "uuid.getnode[alias get_mac] returns fake mac"
    def __str__(self):
        return(repr(self.msg))

class UnknownOSError(Exception):
    def __init__(self):
        self.msg = 'unknown os'
    def __str__(self):
        return(repr(self.msg))
    
# ================================================

# ================================================    
def test_fake_mac_addr():
    """Returns True if uuid.getnode returns actual mac address
    else return False
    """
    return get_mac() == get_mac()

def get_mac_addr():
    """Returns None if uuid.getnode returns fake mac address
    else return mac addr in list of integers
    """
    if not test_fake_mac_addr():
        return None
    mac_addr = []
    for digit in range(40, -8, -8):
        mac_addr.append((get_mac() >> digit) & 0xff)
    return mac_addr

# =================================================

# =============== socket ==========================

import socket
import os
import platform

host = socket.gethostbyname(socket.gethostname())
port = 9

def sleep_command():
    plat_sys = platform.system()
    if plat_sys == 'Windows':
        os.system('shutdown /p')
    elif plat_sys == 'Linux':
        os.system('shutdown now')
    else:
        raise UnknownOSError()
    
def service_wasol(sock, data):
    try:
        if get_mac_addr() is None:
            raise FakeMacError()
        sleep_magic_packet = bytes([0x00]*6+get_mac_addr()*16)

        if data == sleep_magic_packet:
            sleep_command()
    except FakeMacError as e:
        print(e)
    except UnknownOSError as e:
        print(e)
        

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

while True:
    data, addr = sock.recvfrom(1024)
    print('received data from', data)
    service_wasol(sock, data)
    
# =================================================
