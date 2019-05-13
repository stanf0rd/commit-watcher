#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import string, json
from deploy import deploy
from event_processor import processEvent

from config import DEPLOY_CONFIG


def start():
    for key in DEPLOY_CONFIG.items():
        errorMessage = deploy(key)
        print((
            "{} deployment successful".format(key.capitalize()),
            errorMessage
        )[bool(errorMessage)])


# class Handler(BaseHTTPRequestHandler):
#     def _set_response(self):
#         self.send_response(200)
#         self.end_headers()

#     def do_POST(self):
#         contentLength = int(self.headers['Content-Length'])
#         event = str(self.headers['X-GitHub-Event'])
#         data = self.rfile.read(contentLength)
#         if (not data):
#             return
#         jsonData = json.loads(data.decode('utf-8'))

#         message = processEvent(event, jsonData)

#         self._set_response()

#         waveBot.send_message(
#             chat_id=-1001206951073,
#             text=message,
#             parse_mode='Markdown',
#             disable_web_page_preview=True,
#         )


# def run():
#     serverAddress = ('', 7200)
#     server = HTTPServer(serverAddress, Handler)
#     print('Starting server...\n')
#     try:
#         server.serve_forever()
#     except KeyboardInterrupt:
#         pass
#     server.server_close()
#     print('Stopping server...\n')


# run()

start()
