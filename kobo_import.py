import tempfile, shutil, sys, subprocess, json 
import populate_xmeta as px

def kobo_import(kobo_username, auth_token):
   kobo_url = "https://kc.kobotoolbox.org/%s" % (kobo_username)
   kobo_import_forms(kobo_url, auth_token)
   kobo_import_data(auth_token)

def kobo_import_forms(kobo_url, auth_token):
   forms = json.loads(subprocess.check_output(["curl", "-X", "GET", "https://kc.kobotoolbox.org/api/v1/forms", "-H", "Authorization: Token %s" % (auth_token)]))
   for form in forms:
      formid = form['formid']

      xlsform = subprocess.check_output(["curl", "-X", "GET", "https://kc.kobotoolbox.org/api/v1/forms/%s/form.xls" % (formid), "-H", "Authorization: Token %s" % (auth_token)])
      xform = json.loads(subprocess.check_output(["curl", "-X", "GET", "https://kc.kobotoolbox.org/api/v1/forms/%s/form.json" % (formid), "-H", "Authorization: Token %s" % (auth_token)]))
      fid = xform['id_string']
      vid = xform['version']
      path = formid
      xform = json.dumps(xform, sort_keys=True,indent=4, separators=(',', ': '))
      px.populate_xmeta_kobo(fid,vid,kobo_url,path,xlsform,xform)

def kobo_import_data(auth_token):
   forms = json.loads(subprocess.check_output(["curl", "-X", "GET", "https://kc.kobotoolbox.org/api/v1/forms", "-H", "Authorization: Token %s" % (auth_token)]))
   for form in forms:
      formid = form['formid']

      submissions = json.loads(subprocess.check_output(["curl", "-X", "GET", "https://kc.kobotoolbox.org/api/v1/data/%s" % (formid), "-H", "Authorization: Token %s" % (auth_token)]))
      for xdata in submissions:
         sid = str(xdata['_id'])
         fid = xdata['_xform_id_string']
         vid = xdata['__version__']
         device_id = "kobo"
         device_ip = "kobo"
         device_type = "kobo"
         xdata = json.dumps(xdata, sort_keys=True,indent=4, separators=(',', ': '))
         px.populate_xdata_kobo(sid,fid,vid,device_id,device_ip,device_type,xdata)

if __name__ == '__main__':
   if len(sys.argv) == 3:
      kobo_import(sys.argv[1],sys.argv[2])
   else:
      print("Usage: %s kobo username, kobo authorization token" % sys.argv[0])

