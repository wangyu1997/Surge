import requests
import os
from qiniu import Auth, put_file, etag
import qiniu.config

access_key = os.environ["ACCESS_KEY"]
secret_key = os.environ["SECRET_KEY"]
clash_url = os.environ["CLASH_URL"]
sub_url = os.environ["SUB_URL"]

if os.path.exists("tmp"):
    os.remove("tmp")
else:
    os.mknod("tmp")

req_url = f"http://h4.noway.top:25500/sub?target=clash&url={sub_url}&list=true"
ret = requests.get(req_url)

req_text = ret.text

if "password" in req_text:
    open("clash.yml", "w").write(req_text)
    q = Auth(access_key, secret_key)
    bucket_name = 'blog_cdn'
    key = 'clash.yml'
    token = q.upload_token(bucket_name, key, 3600)
    localfile = './clash.yml'
    ret, info = bucket.delete(bucket_name, key)
    ret, info = put_file(token, key, localfile, version='v2') 

    
req_url = f"http://h4.noway.top:25500/sub?target=quanx&url={sub_url}&list=true"
ret = requests.get(req_url)

req_text = ret.text

if "password" in req_text:
    open("quanx.yml", "w").write(req_text)
    q = Auth(access_key, secret_key)
    bucket_name = 'blog_cdn'
    key = 'quanx.yml'
    token = q.upload_token(bucket_name, key, 3600)
    localfile = './quanx.yml'
    ret, info = bucket.delete(bucket_name, key)
    ret, info = put_file(token, key, localfile, version='v2') 

    
req_url = clash_url
ret = requests.get(req_url)

req_text = ret.text

node_info = req_text[req_text.find('[Proxy]'):req_text.find('[Proxy Group]')].strip()
node_list = []
for node in node_info.split('\n')[1:]:
    if node.startswith('['):
        node_list.append(node)
req_text = '\n'.join(node_list)

if "password" in req_text:
    open("surge.yml", "w").write(req_text)
    q = Auth(access_key, secret_key)
    bucket_name = 'blog_cdn'
    key = 'surge.yml'
    token = q.upload_token(bucket_name, key, 3600)
    localfile = './surge.yml'
    ret, info = bucket.delete(bucket_name, key)
    ret, info = put_file(token, key, localfile, version='v2') 
    

