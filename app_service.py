import time

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys

from flask import request

from test import app


class FlaskAppService:
    """Silly little application stub"""

    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        self.running = True
        app.run(host='0.0.0.0', port=5000)
        while self.running:
            time.sleep(10)  # Important work
            servicemanager.LogInfoMsg("Service running...")


class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskAppService"
    _svc_display_name_ = "Flask App Service"
    _svc_description_ = "This service runs a Flask app."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.timeout = 30000
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = FlaskAppService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.service_impl.run()


if __name__ == '__main__':

    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AppServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
