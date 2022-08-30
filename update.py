import requests
import os
from qiniu import Auth, put_file, etag,BucketManager,CdnManager
import qiniu.config

access_key = os.environ["ACCESS_KEY"]
secret_key = os.environ["SECRET_KEY"]
sub_url = os.environ["SUB_URL"]
surge_url = os.environ["SURGE_URL"]
cdn_url = os.environ["CDN_URL"]
convert_url = os.environ["CONVERT_URL"]

if os.path.exists("tmp"):
    os.remove("tmp")
else:
    os.mknod("tmp")

req_url = f"{convert_url}?target=clash&url={sub_url}&list=true"
ret = requests.get(req_url)

req_text = ret.text

if "password" in req_text:
    open("clash.yml", "w").write(req_text)
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    bucket_name = 'blog_cdn'
    key = 'clash.yml'
    token = q.upload_token(bucket_name, key, 3600)
    localfile = './clash.yml'
    ret, info = bucket.delete(bucket_name, key)
    ret, info = put_file(token, key, localfile, version='v2') 

    
req_url = f"{convert_url}?target=quanx&url={sub_url}&list=true"
ret = requests.get(req_url)

req_text = ret.text

if "password" in req_text:
    open("quanx.yml", "w").write(req_text)
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    bucket_name = 'blog_cdn'
    key = 'quanx.yml'
    token = q.upload_token(bucket_name, key, 3600)
    localfile = './quanx.yml'
    ret, info = bucket.delete(bucket_name, key)
    ret, info = put_file(token, key, localfile, version='v2') 

    
req_url = surge_url
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
    bucket = BucketManager(q)
    bucket_name = 'blog_cdn'
    key = 'surge.yml'
    token = q.upload_token(bucket_name, key, 3600)
    localfile = './surge.yml'
    ret, info = bucket.delete(bucket_name, key)
    ret, info = put_file(token, key, localfile, version='v2') 
    
q = Auth(access_key, secret_key)
cdn_manager = CdnManager(q)
urls = [
    f'{cdn_url}/surge.yml',
    f'{cdn_url}/quanx.yml',
    f'{cdn_url}/clash.yml'

]
refresh_url_result = cdn_manager.refresh_urls(urls)
print(refresh_url_result)
