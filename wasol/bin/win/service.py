import socket
import win32serviceutil
import servicemanager
import win32event
import win32service
import logging
import os
from wasol import core

logger = logging.getLogger('wasol_logger')

class WasolService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'wasolService'
    _svc_display_name_ = 'Wasol Service'
    _svc_description_ = 'Wake and Sleep on Lan Service'

    @classmethod
    def parse_command_line(cls, argv=[]):
        # argv is sys.argv
        logger.debug('\n\n\n===============================')
        logger.debug(f'begin parse commad line')
        if len(argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(cls)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(cls)
        logger.debug(f'end parse command line')
        logger.debug('\n===============================')
    
    def __init__(self, args):
        logger.debug('begin init')
        win32serviceutil.ServiceFramework.__init__(self, args)
        self._hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self._wasol = core.Wasol()
        logger.debug('end init')
    
    def SvcStop(self):
        logger.debug('start svcstop')
        logger.debug('stopping wasolservice...')
        self._wasol.close_socket()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self._hWaitStop)
        logger.debug('end svcstop')
    
    def SvcDoRun(self):
        logger.debug('start svcdorun')
        logger.debug('starting wasolservice...')
        self._wasol.open_socket()
        self._wasol.main()
        win32event.WaitForSingleObject(self._hWaitStop, win32event.INFINITE)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                servicemanager.PYS_SERVICE_STARTED,
                                (self._svc_name_, ''))
        logger.debug('end svcdorun')