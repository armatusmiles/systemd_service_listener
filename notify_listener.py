#!/usr/bin/env python3

import os
import socket
import threading
import subprocess
from signal import SIGTERM


class SystemdNotifyListener(object):
    
    def __init__(self):
        self.socket_path = "/tmp/notify_socket_" + str(os.getpid())
        os.environ["NOTIFY_SOCKET"] = self.socket_path
        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.socket_path)
        self.listen_thread = threading.Thread(target=self.__listen)
        self.listen_thread.start()
    
    def __del__(self):
        self.server_socket.close()
        os.unlink(self.socket_path)
        self.listen_thread.join(timeout = 2)

    def __listen(self):
        while True:
            message = self.server_socket.recv(4096).decode()
            print("Received: {}".format(message))
            if message == "READY=1":
                proc.send_signal(SIGTERM)
            elif message == "STOPPING=1":
                return   

    def set_service_process(self, proc):
        self.service_process = proc

def compile_service():
    os.system('gcc -o service service.c -lsystemd')

if __name__ == '__main__':
    snl = SystemdNotifyListener()
    compile_service()
    proc = subprocess.Popen("./service")
    snl.set_service_process(proc)

