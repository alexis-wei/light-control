from network import WLAN, STA_IF
from network import mDNS
import network
import time

wlan = WLAN(STA_IF)
wlan.active(True)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)



# wlan.connect('​Alexis', '13131313', 5000)
# for x in range(0, 10):
#     if not wlan.isconnected():
#         print("Waiting for wlan connection")
#         time.sleep(1)
#     else:
#         break



print("WiFi connected at", wlan.ifconfig()[0])
# Advertise as 'hostname', alternative to IP address
try:
    hostname = '​Alexis'
    mdns = mDNS(wlan)
    mdns.start(hostname, "MicroPython REPL")
    mdns.addService('_repl', '_tcp', 23, hostname)
    print("Advertised locally as {}.local".format(hostname))
except OSError:
    print("Failed starting mDNS server - already started?")

# start telnet server for remote login
from network import telnet

print("start telnet server")
telnet.start(user='​Alexis', password='​13131313')

# fetch NTP time
from machine import RTC

print("inquire RTC time")
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

timeout = 10
for _ in range(timeout):
    if rtc.synced():
        break
    print("Waiting for rtc time")
    time.sleep(1)


if rtc.synced():
    print(time.strftime("%c", time.localtime()))
else:
    print("could not get NTP time")
