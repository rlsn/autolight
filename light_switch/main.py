from machine import Pin,PWM
import time
from web import *
import uasyncio as asyncio
from ir_rx.nec import NEC_8
from ir_tx.nec import NEC

onboard = Pin(2, Pin.OUT)
# recv_pin = Pin(22, Pin.IN)
recv_pin = Pin(4, Pin.IN, Pin.PULL_UP)
send_pin = Pin(22, Pin.OUT, value=0)
nec = NEC(send_pin)
REMOTE = "192.168.0.104"
blink_intv = 5

address = 0x0000
data = 0x11

def transmit():
    nec.transmit(address, data)  # address, data




# def recv_callback(data, addr, ctrl):
#     if data < 0:  # NEC protocol sends repeat codes.
#         print('Repeat code.')
#     else:
#         print('Data {:02x} Addr {:04x}'.format(data, addr))
        
#         # if data==0x11:
#         #     print("received ir signal")
#         #     http_get(f"http://{REMOTE}/toggle")

#         if data==0x43:
#             recv_signal()
# ir = NEC_8(recv_pin, recv_callback)       

async def blink():
    while 1:
        onboard.on()
        await asyncio.sleep(0.1)
        onboard.off()
        await asyncio.sleep(blink_intv)

async def signal():
    for i in range(5):
        onboard.on()
        await asyncio.sleep(0.1)
        onboard.off()
        await asyncio.sleep(0.1)



def execute(command):
    print(command)
    if command=="toggle":
        transmit()
        

## ASYNC

async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    command = str(request_line).split(' ')[1].strip('/')
    execute(command)
    response = "ok".encode()
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'.encode())
    writer.write(response)

    await writer.drain()
    writer.close()
    await writer.wait_closed()
    print("Client disconnected")


async def main():
    await signal()
    connect_WIFI()
    await signal()
    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    asyncio.create_task(blink())
    print("Server started")
    await signal()

    last_value = 1
    while 1:
        current_value = recv_pin.value()
        if current_value==0 and last_value == 1:
            print("received toggle signal")
            if http_get(f"http://{REMOTE}/toggle"):
                transmit()
                await signal()
        last_value = recv_pin.value()
        await asyncio.sleep(0.1)


asyncio.run(main())