from http.server import BaseHTTPRequestHandler
import time
import requests
import json
import os
import socketserver
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")
model = os.getenv("MODEL") or "gemma2-9b-it"

clients = []
PORT = int(os.getenv("SERVER_PORT"))

def make_req(prompt):
    res = []
    # print(prompt)
    for x in prompt[0]:
        start = time.time()
        data = {
            "messages": [{
                "role": "user",
                "content": x
            }],
            "model": model
        }
        req = requests.post('https://api.groq.com/openai/v1/chat/completions',
                            headers={
                                "Content-Type": "application/json",
                                "Authorization": "Bearer %s" % (key)
                                },
                            data=json.dumps(data)
                            )

        res.append({
            "Prompt": x,
            "Source": model,
            "Content": json.loads(req.content)['choices'][0]['message']['content'],
            "TimeRecd": start,
            "TimeSent": time.time()
        })
    return res

def sendToClients(data):
    i = 0
    for x in clients:
        # print("http://%s:%s" % (x[0], 7000+i))
        requests.post("http://%s:%s" % (x[0], 7000+i), data=data)
        i += 1


class LLMServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.client_address not in clients:
            clients.append(self.client_address)
            # print(clients)

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data.decode('utf-8'))
        # print(post_data)
        req = make_req(post_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

        response = json.dumps({
            "ClientId": post_data[1],
            "data": req
        })

        self.wfile.write(response.encode('utf-8'))
        sendToClients(response)

Handler = LLMServer
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server running at port", PORT)
    httpd.serve_forever()
