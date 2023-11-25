import socket
import sys
import time
import os
from threading import Thread
  
import asyncio

PORT = 5789
seperator=b"-fb-"

async def main():
    reader, writer = await asyncio.open_connection('', PORT)
    for i in range(20):
        await asyncio.sleep(0.5)
        writer.write("hello123456\n".encode()+seperator)
        await writer.drain()
        print("sent")


    writer.close()
    await writer.wait_closed()
    print("done")


if __name__=="__main__":
    asyncio.run(main())
