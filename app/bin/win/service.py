import socket
import win32serviceutil
import servicemanager
import win32event
import win32service
from app import core

class WasolService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'wasolService'
    _svc_display_name_ = 'Wasol Service'
    _svc_description_ = 'Wake and Sleep on Lan Service'

    @classmethod
    def parse_command_line(cls, argv=[]):
        # argv is sys.argv
        if len(argv) == 1:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(cls)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(cls)
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self._hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self._wasol = core.Wasol()
    
    def SvcStop(self):
        self._wasol.close_socket()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self._hWaitStop)
    
    def SvcDoRun(self):
        self._wasol.open_socket()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                servicemanager.PYS_SERVICE_STARTED,
                                (self._svc_name_, ''))
        self._wasol.main()