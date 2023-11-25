import network
import socket
import uasyncio as asyncio


SSID='Xiaomi_55B5'
PASSWORD='83653890'
REMOTE = '192.168.0.104'
PORT = 5789

def connect_WIFI():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('success, network config:', wlan.ifconfig())


def connect_remote():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"connecting to {REMOTE}:{PORT}")
    s.connect((REMOTE, PORT))
    print(f"successfully connected to {REMOTE}")
    return s

