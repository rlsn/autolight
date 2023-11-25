#https://github.com/lemariva/micropython-camera-driver

from machine import Pin,PWM
import time
from web import *
import uasyncio as asyncio
import camera

onboard = PWM(Pin(4))
onboard.duty(0)
light_duty = 1
blink_intv = 5
frame_rate = 1


async def signal():
    for i in range(5):
        onboard.duty(light_duty)
        await asyncio.sleep(0.1)
        onboard.duty(0)
        await asyncio.sleep(0.1)
async def blink():
    while 1:
        onboard.duty(light_duty)
        await asyncio.sleep(0.1)
        onboard.duty(0)
        await asyncio.sleep(blink_intv)

async def init_camera():
    try:
        camera.init(0, format=camera.JPEG, framesize=camera.FRAME_HQVGA,
                    fb_location=camera.PSRAM)
    except:
        camera.deinit()
        await asyncio.sleep(1)
        # If we fail to init
        camera.init(0, format=camera.JPEG, framesize=camera.FRAME_HQVGA,fb_location=camera.PSRAM)
    camera.quality(6)

async def transmit_frame(remote, max_tries = 10, seperator=b"-fb-"):
    # capture frame
    try:
        n_try = 0
        buf = False
        while (n_try < max_tries and buf == False): #{
            # wait for sensor to start and focus before capturing image
            buf = camera.capture()
            if (buf == False): await asyncio.sleep(0.2)
            n_try += 1
        
        if type(buf) is bytes and len(buf) > 0:
            pkg = buf+seperator
            remote.sendall(pkg)
            print('sent:', len(pkg))
        else:
            print("capture failed")
    except:
        print("frame transmit failed")

async def streaming_video(remote, frame_rate = 5):
    while True:        
        await transmit_frame(remote)
        await asyncio.sleep(1/frame_rate)

async def main():
    await signal()
    connect_WIFI()
    remote = connect_remote()
    # prepare camera
    await signal()

    await init_camera()
    print("Camera ready")
    
    asyncio.create_task(streaming_video(remote, frame_rate))
    await signal()

    await blink()

asyncio.run(main())
