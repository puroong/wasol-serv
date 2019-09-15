from uuid import getnode as get_mac
import logging

logger = logging.getLogger('wasol_logger')

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
    try:
        logger.debug(f'using sleep command in [platform : {plat_sys}]...')
        if plat_sys == 'Windows':
            os.system('shutdown /p')
        elif plat_sys == 'Linux':
            os.system('shutdown now')
        else:
            raise UnknownOSError()
    except:
        logger.error('unexpected error', exc_info=True)
    
def service_wasol(sock, data):
    try:
        if get_mac_addr() is None:
            raise FakeMacError()
        sleep_magic_packet = bytes([0x00]*6+get_mac_addr()*16)

        if data == sleep_magic_packet:
            logger.debug('received sleep magic packet.')
            sleep_command()
    except FakeMacError as e:
        logger.error(e.msg, exc_info=True)
    except UnknownOSError as e:
        logger.error(e.msg, exc_info=True)
        

def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    while True:
        logger.debug(f'listening on {host}:{port}...')
        data, addr = sock.recvfrom(1024)
        logger.debug(f'received [data : {data}] from [addr : {addr}]')
        service_wasol(sock, data)
    
# =================================================
