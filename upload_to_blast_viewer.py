import urllib, urllib2, urlparse, requests, uuid

file_to_upload = "d:\\blastdb\\out\\foo.99"
## file_to_upload = "/home/azureuser/BLAST/blastdb/inputncbi"
file_to_upload = "/home/azureuser/BLAST/blastout/blastout.99"
file_to_upload = '/home/azureuser/BLAST/blastout/blastout.99'

print('loading from %s' % file_to_upload)
data_to_upload = open(file_to_upload, 'r').read()
print(data_to_upload)

upload_url = "http://bov.bioinfo.cas.unt.edu/cgi-bin/parseBlast.cgi"

r = requests.post(upload_url, files = { 'uploadfile': ('blastout.99', data_to_upload) })
print(r.text)
print(r.headers)
print(r.status_code)

print('hash = %s' %  urlparse.parse_qs(r.url)["http://bov.bioinfo.cas.unt.edu/cgi-bin/viewhits.cgi?hash"][0])
print('id = %s' %  uuid.uuid4().hex)
