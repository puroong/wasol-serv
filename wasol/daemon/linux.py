import sys
import os
import time
import atexit
import logging
from wasol import core
from signal import SIGTERM

logger = logging.getLogger('wasol_logger')

class WasolDaemon:
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        logger.debug('start init')
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self._wasol = core.Wasol()
        logger.debug('end init')
    
    def daemonize(self):
        logger.debug('start daemonize')
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            logger.error(f'fork #1 failed: {e.errno} {e.strerror}')
            sys.exit(1)
        
        os.chdir("/")
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            logger.error(f'fork #2 failed: {e.errno} {e.strerror}')
            sys.exit(1)
        
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write(f'{pid}')
        
        logger.debug('end daemonize')

    def delpid(self):
        logger.debug('start delpid')
        os.remove(self.pidfile)
        logger.debug('end delpid')
    
    def start(self):
        logger.debug('start start')
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        
        if pid:
            logger.error(f'pidfile {self.pidfile} already exists. Daemon already running')
            sys.exit(1)
        
        self.daemonize()
        self._wasol.open_socket()
        self._wasol.main()

        logger.debug('end start')
    
    def stop(self):
        logger.debug('start stop')
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        
        if not pid:
            logger.error(f'pidfile {self.pidfile} does not exist. Daemon not running.')
            return
        
        try:
            while True:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as e:
            e = str(e)
            if e.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    logger.error(e)
                    sys.exit(1)
        self._wasol.close_socket()
        logger.debug('end stop')
