import network
import socket

web_id='123456789'
web_pw='123456789'

def connect_WIFI():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(web_id, web_pw)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def http_get(url):
    try:
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))

        while True:
            data = s.recv(100)
            if data:
                print(str(data, 'utf8'), end='')
            else:
                break
        
        s.close()
        return 1
    except Exception as e:
        print("http error:", e)
        return 0

if __name__=="__main__":
    connect_WIFI()