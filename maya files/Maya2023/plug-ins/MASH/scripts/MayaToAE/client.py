from maya.app.flux.imports import *
import socket
import threading
import traceback
import select
import time

# ==============
# STRING RESOURCES
def getResource(name):
    return mel.eval('getPluginResource("MASH", "' + name + '")')

_SR = {
    'Connecting to Adobe(R) After Effects(R)': getResource('kM2AE_Connecting_To_AAE'),
    'Live link established.': getResource('kM2AE_Link_Established'),
    'Connection established': getResource('kM2AE_Conn_Established'),
    'Sending message failed.': getResource('kM2AE_SMessage_Failed'),
    'Connection closed': getResource('kM2AE_Connection_Closed'),
    'Live link failed': getResource('kM2AE_Link_Failed'),
    'Closing connection failed.': getResource('kM2AE_ClosingC_Failed'),
    'Live link disconnected.': getResource('kM2AE_Link_Disconnected')
}

class AEClient(qt.QObject):
    # SIGNALS
    receiver = qt.Signal(str)
    
    host = 'localhost'
    port = 8883

    def __init__(self):
        super(AEClient, self).__init__()
        self.socket = None
        self.isRunning = False
        self.isSocketConnected = False

    def run(self):
        if not self.isRunning:
            self.isRunning = True
            nom.MGlobal.displayInfo(_SR['Connecting to Adobe(R) After Effects(R)'])
            listener = threading.Thread(target=self.tryConnectUntilConnected)
            listener.start()

    def tryConnectUntilConnected(self):
        while self.isRunning and not self.isSocketConnected:
            if self.establishConnection():
                break
            time.sleep(1)

        if self.isRunning:
            nom.MGlobal.displayInfo('# ' + _SR['Live link established.'] + ' #')
            self.receiver.emit(_SR['Connection established'])
            self.listenForMsg()
        
    def establishConnection(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.host, self.port))
            self.isSocketConnected = True
            return True
        except Exception as e:
            self.isSocketConnected = False
            return False

    def sendMsg(self, msg):
        try:
            self.socket.send(str(len(msg)) + '>' + msg)
            return True
        except Exception as e:
            cmds.warning(_SR['Sending message failed.'])
            self.isSocketConnected = False
            return False

    def listenForMsg(self):
        try:
            msg = ''
            while self.isSocketConnected and self.isRunning:
                try:
                    resp = self.socket.recv(1024)
                    if len(resp) == 0:
                        self.receiver.emit(_SR['Connection closed'])
                        self.closeConnection()
                        return
                    msg += resp
                    index = msg.find('>')
                    if index > 0:
                        length = int(msg[:index])
                        if len(msg) > index + length:
                            self.receiver.emit(msg[index + 1: index + 1 + length])
                            msg = ''
                except socket.timeout:
                    pass


        except Exception as e:
            cmds.warning(_SR['Live link failed'])
            self.isConnected = False

    def isConnected(self):
        return self.isSocketConnected and self.isRunning

    def closeConnection(self):
        if self.isRunning:
            self.isRunning = False
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except Exception as e:
                cmds.warning(_SR['Closing connection failed.'])

            self.socket = None
            self.isSocketConnected = False
            nom.MGlobal.displayInfo(_SR['Live link disconnected.'])# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
