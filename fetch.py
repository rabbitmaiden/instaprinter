#!/usr/bin/python
import sys
import time
import requests
import pprint
import os, re, subprocess, shutil
import os.path
import time
from PIL import Image
from StringIO import StringIO
from termcolor import colored

def say (msg):
  print colored('[' + time.strftime('%H:%M:%S') + '] ' + msg, "green")
  return

def fetchtag ( tag, args = {}):
  path = 'tags/' + tag + '/media/recent'
  return callapi(path, args)

def callapi ( path, args={} ):
  base_url = 'https://api.instagram.com/v1/'
  client_id = '457803cfe7bd47caa45a0bc8193cd7f6'

  url = base_url + path + '?client_id=' + client_id + '&'

  for k in args:
    url += k + '=' + args[k]

  #say ("fetching "+url) 

  r = requests.get(url)
  if r.status_code != 200:
    print "Error fetching", url
    sys.exit(1)
  return r.json()

def downloadphoto ( url ):
  r = requests.get(url)
  if r.status_code != 200:
    print "Error fetching image", url
    sys.exit(1)
  i = Image.open(StringIO(r.content))
  return i

def main():
  min_tag_id = False

  tag = open('tag.txt').read().strip();

  say("Tag is "+tag)

  if not tag:
    print "Could not determine tag"
    sys.exit(1)

  banner_file = 'banners/'+tag+'.jpg'
  banner = Image.open(banner_file)

  # OSX 
  #border = (25, 30)
  #dpi = (168, 168)

  # rPi
  border = (10, 0)
  dpi = (168, 168)

  # loop forever
  while True:

    args = {}

    if min_tag_id != False:
      args['min_tag_id'] = min_tag_id

    json = fetchtag(tag, args)
    
    if 'data' in json and len(json['data']) > 0:
      say ("Found " + str(len(json['data'])) + " photos")
      for photo in json['data']:
        photo_id = photo['id']
        photo_author = photo['user']['username']
        photo_name = 'downloaded/'+photo_id+'_'+photo_author+'.jpg'

        # check if we have this one already
        if os.path.isfile(photo_name):
          #say("skipping " + photo_id + " - already downloaded")
          continue
        elif photo['type'] != 'image':
          #say("skipping " + photo_id + " - not an image")
          continue

        # download the photo
        say("Downloading photo from "+photo['user']['username'] + " (" + photo_id + ")" )

        image = downloadphoto(photo['images']['standard_resolution']['url'])

        # resize if smaller than 640
        if image.size[0] != 640:
          #say("resizing " + photo_id + " to 640")
          image = image.resize((640, 640))

        
        final = Image.open('blank.jpg');


        final.paste(image, (border[0],border[1]))
        final.paste(banner, (border[0],border[1] + 640))

        final.save(photo_name, 'jpeg', dpi=dpi)

        del final
        del image


#    else:
#      say("nothing after "+ min_tag_id+ " found")

    if 'next_min_id' in json['pagination']:
      min_tag_id = json['pagination']['next_min_id']

    printing()
    time.sleep(15)

def printing():
    dldir = 'downloaded/'
    prdir = 'printed/'
    for f in os.listdir(dldir):
      if not re.match(r'.*\.jpg$', f):
        continue
      if os.path.isfile(prdir + f):
        continue
      say("Printing "+f)
      retcode = actuallyprint(dldir+f)

      if retcode == 0:
        subprocess.call(['touch', prdir+f])
      else:
        print "failed to print", f
        break

def actuallyprint(filename):
  #retcode = subprocess.call(["echo", "lp", "-d", "ELIZA_DOOLEY", "-o", "media=Postcard.Fullbleed", filename])
  # rpi
  retcode = subprocess.call(["lp", filename])
  return retcode


def reprint():
    dldir = 'downloaded/'
    files = []
    for f in os.listdir(dldir):
      if not re.match(r'.*\.jpg$', f):
        continue
      files.append(f)

    files.sort(key=lambda x: os.path.getmtime(dldir+x), reverse=True)
  
    start = 0
    numshown = 5
    while True:
      print colored("Reprint photo: ", "green")
      remaining = len(files) - start
      ceil = numshown if remaining > numshown else remaining
      for i in range(start, start+ceil):
        print colored(str(i)+". "+files[i], "yellow")
      num = raw_input("Enter file number to reprint, m for more: ")
      

      if (num == 'm'):
        start = start + numshown
        start = 0 if start > len(files) else start

      else:
        num = int(num)
        if files[num]:
          say("Reprinting "+files[num])
          actuallyprint(dldir+files[num])
          break


    interrupt()

def run():
  try:
    main()
  except KeyboardInterrupt:
    interrupt()
  

def interrupt():
  print colored("\nCommands available:\n p - reprint photo\n r - resume\n x - exit", "cyan")
  command = raw_input(colored("? ", "yellow"))
  if (command == 'p'):
    try:
      reprint()
    except KeyboardInterrupt:
      interrupt()
    return 0
  elif (command == 'r'):
    run()
    return 0
  elif (command == 'x'):
    sys.exit(0)
  else:
    interrupt()
    return 0

if __name__ == "__main__":
  run()
