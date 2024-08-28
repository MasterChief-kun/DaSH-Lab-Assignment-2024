from http.server import BaseHTTPRequestHandler
import requests
import json
import os
import socketserver
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")
model = os.getenv("MODEL") or "gemma2-9b-it"
client_id = int(os.getenv("CLIENT_ID"))
SERVER_PORT = os.getenv("SERVER_PORT")
PORT = int(os.getenv("PORT")) + client_id
INPUT = os.getenv("INPUT")

prompt_arr = open(INPUT, 'r').readlines()[0 + (client_id*4):4 + (client_id*4)]
# print(prompt_arr)

def create_json(data):
    if (os.path.isfile('output-%s.json' % client_id)):
        with open('output-%s.json' % client_id, 'r+') as f:
            beg = json.load(f)
            beg['data'].append(data)
            f.seek(0)
            json.dump(beg, f, ensure_ascii=False, indent=4)
    else:
        with open('output-%s.json' % client_id, 'w') as f:
            json.dump(data, f, indent=4)


def make_req(prompt_arr):
    # prompt = [{ 'prompt': x, 'ClientId': client_id } for x in prompt_arr]
    res = requests.post("http://127.0.0.1:%s" % SERVER_PORT, data=json.dumps([prompt_arr, client_id]))
    create_json(json.loads(res.content))


   
class LLMClient(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        get_data = self.rfile.read(content_length)
        get_data = json.loads(get_data.decode('utf-8'))

        if client_id != get_data['ClientId']:
            get_data["Source"] = "user"

        create_json(get_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

        response = json.dumps({
            "ClientId": client_id,
            "status": "Success"
        })
        # sendToClients(response)

        self.wfile.write(response.encode('utf-8'))

Handler = LLMClient
make_req(prompt_arr)
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Client running at port", PORT)
    httpd.serve_forever()
