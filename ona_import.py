import tempfile, shutil, sys, subprocess, json 
import populate_xmeta as px

def ona_import(auth_token): 
   token_test = subprocess.check_output(["curl", "-X", "GET", "https://api.ona.io/api/v1/forms", "-H", "Authorization: Token %s" % (auth_token)])
   if token_test == '{"detail":"Invalid token."}':
      print("Invalid authorization token")
      return
   else:
      ona_import_forms(auth_token)
      ona_import_data(auth_token)

def ona_import_forms(auth_token):
   forms = json.loads(subprocess.check_output(["curl", "-X", "GET", "https://api.ona.io/api/v1/forms", "-H", "Authorization: Token %s" % (auth_token)]))
   for form in forms:
      formid = form['formid']

      xlsform = subprocess.check_output(["curl", "-X", "GET", "https://api.ona.io/api/v1/forms/%s/form.xls" % (formid), "-H", "Authorization: Token %s" % (auth_token)])
      xform = json.loads(subprocess.check_output(["curl", "-X", "GET", "https://api.ona.io/api/v1/forms/%s/form.json" % (formid), "-H", "Authorization: Token %s" % (auth_token)]))
      fid = xform['id_string']
      vid = xform['version']
      ona_url = form['created_by']
      path = formid
      xform = json.dumps(xform, sort_keys=True,indent=4, separators=(',', ': '))
      px.populate_xmeta_ona(fid,vid,ona_url,path,xlsform,xform)

def ona_import_data(auth_token):
   forms = json.loads(subprocess.check_output(["curl", "-X", "GET", "https://api.ona.io/api/v1/forms", "-H", "Authorization: Token %s" % (auth_token)]))
   for form in forms:
      formid = form['formid']

      submissions = json.loads(subprocess.check_output(["curl", "-X", "GET", "https://api.ona.io/api/v1/data/%s" % (formid), "-H", "Authorization: Token %s" % (auth_token)]))
      for xdata in submissions:
         sid = str(xdata['_id'])
         fid = xdata['_xform_id_string']
         vid = xdata['_version']
         device_id = "ona"
         device_ip = "ona"
         device_type = "ona"
         xdata = json.dumps(xdata, sort_keys=True,indent=4, separators=(',', ': '))
         px.populate_xdata_ona(sid,fid,vid,device_id,device_ip,device_type,xdata)

if __name__ == '__main__':
   if len(sys.argv) == 2:
      ona_import(sys.argv[1])
   else:
      print("Usage: %s ONA API key" % sys.argv[0])


