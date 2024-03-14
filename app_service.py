import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import sys
from test import app
# from gunicorn.app.base import BaseApplication
# from gunicorn.workers.sync import SyncWorker
#
# class StandaloneApplication(BaseApplication):
#     def __init__(self, app, options=None):
#         self.options = options or {}
#         self.application = app
#         super().__init__()
#
#     def load_config(self):
#         config = {key: value for key, value in self.options.items()
#                   if key in self.cfg.settings and value is not None}
#         for key, value in config.items():
#             self.cfg.set(key.lower(), value)
#
#     def load(self):
#         return self.application
class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskAppService"
    _svc_display_name_ = "Flask App Service"
    _svc_description_ = "This service runs a Flask app."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.timeout = 3000
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.timeout = 10000
        # self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))

        self.main()

    def main(self):
        app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    # app.run(debug=True)
    # win32serviceutil.HandleCommandLine(AppServerSvc)
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AppServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
