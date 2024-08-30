#!/usr/bin/env python3
import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

prompt_arr = open(r'./input.txt', 'r').readlines()
key = os.getenv("GROQ_API_KEY")
model = os.getenv("MODEL") or "gemma2-9b-it"

def make_req(prompt):
    start = time.time()
    data = {
        "messages": [{
            "role": "user",
            "content": prompt
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

    return [prompt, json.loads(req.content), start, time.time()]


# res = [json.loads(make_req([x])) for x in create_dict(prompt_arr, True)]
# choices = [x['choices']['message']['content'] for x in res]
# print(res[1])
#
reqs = [make_req(x) for x in prompt_arr]
res = [{
    "Prompt": x[0],
    "Message": x[1]['choices'][0]['message']['content'] or x[1],
    "TimeSent": x[2],
    "TimeRecvd": x[3],
    "Source": model
} for x in reqs]

# print(res)

with open('output.json', 'w') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)
