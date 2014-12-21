import os, sys, time, re
import subprocess
import pprint
import shutil

def main():


  while True:
    dldir = 'downloaded/'
    prdir = 'printed/'
    for f in os.listdir(dldir):
      if not re.match(r'.*\.jpg$', f):
        continue
      if os.path.isfile(prdir + f):
        continue

      print "printing", f
      retcode = subprocess.call(["echo", "lp", "-d", "ELIZA_DOOLEY", "-o", "media=Postcard.Fullbleed", dldir+f])
      if retcode == 0:
        os.symlink(dldir+f, prdir+f)
        print "printed and copied", f
      else:
        print "failed to print", f
        break


    time.sleep(10)

if __name__ == "__main__":
  main()
