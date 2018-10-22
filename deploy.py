import sys
reload(sys)
sys.setdefaultencoding('utf8')
import tempfile, shutil, os
import populate_xmeta as px

def deploy(url,commit,paths):
   p = tempfile.mkdtemp(prefix='/tmp/xlsform')
   os.chdir(p)
   os.system("git clone %s repo" % (url,))
   os.chdir("repo")
   os.system("git checkout %s" % (commit,))
   for x in paths:
      print "Deploying '%s' '%s' '%s' . . ." % (url, commit, x),
      fid, vid = px.populate_xmeta(url,commit,x)
      print "'%s' '%s'" % (fid, vid)
   shutil.rmtree(p)

if __name__ == '__main__':
   if len(sys.argv) > 3:
      deploy(sys.argv[1],sys.argv[2],sys.argv[3:])
   else:
      print("Usage: %s git_url commit(full commit hash) path" % sys.argv[0])
