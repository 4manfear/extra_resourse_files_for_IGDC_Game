### Example Usage:
###
###
### import sheetsapi
### sheetsapi.loadSheet(name='type1', url='https://docs.google.com/spreadsheets/d/1qY_plOYw.../edit#gid=0', rangeFrames='A1:D1', rangeText='A2:D2')
###
### Note: type1 must be an existing Polygonal Type node

from builtins import object
from future import standard_library
standard_library.install_aliases()
import httplib2

import apiclient
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import socket
import sys

from six.moves import BaseHTTPServer
from six.moves import http_client
from six.moves import input
from six.moves import urllib

from oauth2client import _helpers

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

import re
import threading
import webbrowser

import json
import maya.cmds as cmds

class ClientRedirectServer(BaseHTTPServer.HTTPServer):
    query_params = {}

class ClientRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle a GET request.

        Parses the query parameters and prints a message
        if the flow has completed. Note that we can't detect
        if an error occurred.
        """
        self.send_response(http_client.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        parts = urllib.parse.urlparse(self.path)
        query = _helpers.parse_unique_urlencoded(parts.query)
        self.server.query_params = query
        self.wfile.write(
b'''
<!Doctype HTML>
<html>
<head><title>Maya Type Tool Authentication</title></head>
<style>
html, body{
    background-color: rgba(52,52,52,255)
}
#wrapper{
    text-align:center;
    padding: 0;
    margin:0;
}
#message{
    padding: 10px 20px;
    background-color: rgba(75,75,75,255);
    color:rgba(234,234,234,255);
    margin: 20px auto;
    display:inline-block;
    border-radius:4px;
}
</style>
<body>
<div id="wrapper">
<div id="message">''')
        if 'code' in query:
            self.wfile.write(
                b'<p style="text-align:center;">The authentication was successful.<br>Feel free to close this page.</p>')
        else:
            self.wfile.write(
                b'<p style="text-align:center;">The authentication was rejected.<br>'
                b'Maya Type Tool has no permission to access the spreadsheet.<br>'
                b'Please try again.<br>'
                b'Feel free to close this page.</p>')
        self.wfile.write(
b'''</div>
</div>
</body>
</html>''')

# If modifying these scopes, delete your previously saved credentials
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CREDENTIALS_FILENAME = 'sheets.googleapis.com-python-maya-type-tool2.json'
APPLICATION_NAME = 'Maya Type Tool'

class AuthenticationServer(object):
    def __init__(self, reader):
        self.reader = reader
        self.flags = flags
        self.isRunning = False
        self.httpd = None
        self.port_number = 0
        self.flow = None

    def startServer(self):
        if self.flags is None:
            self.flags = tools.argparser.parse_args()

        success = False
        for port in flags.auth_host_port:
            self.port_number = port
            try:
                self.httpd = ClientRedirectServer((flags.auth_host_name, port),
                                             ClientRedirectHandler)
            except socket.error:
                print('Error starting Authentication Server.')
            else:
                success = True
                break
        if success:
            print('Starting server')
            self.isRunning = True
            self.httpd.timeout = 1
            t1 = threading.Thread(target = self.serve)
            t1.start()
        else:
            print('Could not start server')      

    def serve(self):
        while self.isRunning:
            self.handleRequest()
        self.httpd.server_close()

    def stopServer(self):
        self.isRunning = False
        print('Stopped Server')

    def handleRequest(self):
        self.httpd.handle_request()
        if 'error' in self.httpd.query_params:
            print('Authentication request was rejected.')
            self.stopServer()
        elif 'code' in self.httpd.query_params:
            code = self.httpd.query_params['code']
            credential = None
            try:
                credential = self.flow.step2_exchange(code)
            except client.FlowExchangeError as e:
                print('Authentication has failed: {0}'.format(e))
            if credential is None:
                print('Authentication has failed.')
                return
            storeCredentials(credential)
            print('Authentication successful.')
            self.stopServer()
            self.reader.getSheetData(credential)

class SpreadSheetReader(object):
    def __init__(self, node, url, rangeFrames, rangeText, func=None):
        self.server = AuthenticationServer(self)
        self.sheetUrl = url
        self.readyFunc = func
        self.node = node
        self.rangeFrames = rangeFrames
        self.rangeText = rangeText

    def __del__(self):
        self.server.stopServer()

    def renewCredentials(self):
        if not self.server.isRunning:
            self.server.flow = client.OAuth2WebServerFlow(
                client_id='930050415317-v8a1kmdorb4s82il0hbmgvorp54qf959.apps.googleusercontent.com',
                               client_secret='sBEZ74vWNB_cTAhzbE1O1qFu',
                               scope=SCOPES,
                               auth_uri="https://accounts.google.com/o/oauth2/auth",
                               token_uri="https://accounts.google.com/o/oauth2/token",
                               redirect_uri = "urn:ietf:wg:oauth:2.0:oob")
            self.server.startServer()

        oauth_callback = 'http://{host}:{port}/'.format(host=flags.auth_host_name, 
            port=self.server.port_number)
        self.server.flow.redirect_uri = oauth_callback
        authorize_url = self.server.flow.step1_get_authorize_url()
        webbrowser.open(authorize_url, new=1, autoraise=True)

    def getSheetData(self, credentials):
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('sheets', 'v4', http=http)
        spreadsheetId = re.search('/d/(\w+)/', self.sheetUrl)
        if spreadsheetId is not None:
            spreadsheetId = spreadsheetId.group(1)
        sheetId = re.search('#gid=([0-9]+)', self.sheetUrl)
        if sheetId is not None:
            sheetId = sheetId.group(1)

        sheets = None
        try:
            sheets = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
        except:
            print('No permission to access spreadsheet.')
            store = getCredentialsStore()
            store.delete()
            self.renewCredentials()
            return

        sheets = sheets['sheets']

        selectedSheet = None
        
        if sheetId is not None:
            for sheet in sheets:
                sId = sheet['properties']['sheetId']
                title = sheet['properties']['title']
                if sId == sheetId:
                    selectedSheet = title
                    break
        if selectedSheet is None:
            selectedSheet = sheets[0]['properties']['title']

        data = []
        framesData = None
        textData = None
        if self.rangeFrames:
            result = list(service.spreadsheets().values()).get(
                spreadsheetId=spreadsheetId, range=selectedSheet + '!' + self.rangeFrames).execute()
            values = result.get('values', [])
            if len(values) > len(values[0]):
                framesData = [x[0] for x in values]
            else:
                framesData = values[0]

        if self.rangeText:
            result = list(service.spreadsheets().values()).get(
                spreadsheetId=spreadsheetId, range=selectedSheet + '!' + self.rangeText).execute()
            values = result.get('values', [])
            if len(values) > len(values[0]):
                textData = [x[0] for x in values]
            else:
                textData = values[0]
            

        if not textData:
            print('Invalid data. Aborting.')
            return

        for i, v in enumerate(textData):
            v = ''.join( [ "%02X " % ord( x ) for x in v ] ).strip()
            frame = 0
            if framesData and i < len(framesData):
                frame = framesData[i]
            data.append({'hex':v, 'frame':frame})

        jstring = json.dumps(data)
        cmds.setAttr(self.node+".animatedType", jstring, type="string")
        cmds.refreshEditorTemplates()
        print('Done Importing SpreadSheet')

    def processSheet(self):
        store = getCredentialsStore()
        credentials = store.get()
        if not credentials or credentials.invalid:
            self.renewCredentials()
        else:
            self.getSheetData(credentials)

def getCredentialsStore():
    from os import path as os_path
    from os import makedirs as os_makedirs
    home_dir = os_path.expanduser('~')
    credential_dir = os_path.join(home_dir, '.credentials')
    if not os_path.exists(credential_dir): 
        os_makedirs(credential_dir)
    credential_path = os_path.join(credential_dir, CREDENTIALS_FILENAME)
    store = Storage(credential_path)
    return store

def storeCredentials(credential):
    store = getCredentialsStore()
    store.put(credential)
    credential.set_store(store)

def loadSheet(name, url, rangeFrames, rangeText):
    reader = SpreadSheetReader(name, url, rangeFrames, rangeText)
    t1 = threading.Thread(target = reader.processSheet)
    t1.start()
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
