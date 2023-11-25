import socket
import sys
import time
import os
from threading import Thread
  
import asyncio

PORT = 5789
seperator=b"-fb-"

async def handle_client(reader, writer):
    print("connection estalished:", reader._transport.get_extra_info('peername')[0])
    timeout=0
    while(1):
        try:
            task = asyncio.wait_for(reader.readuntil(seperator), timeout=10)
            byte_data = await task
            if len(byte_data)>0:
                timeout=0
                print("received len", len(byte_data))

                data = byte_data.rstrip(seperator)
                with open('out.jpg', 'wb') as out_file:
                    out_file.write(data)
                    print("img written")

            else:
                raise asyncio.exceptions.IncompleteReadError()
        except asyncio.exceptions.IncompleteReadError:
            timeout+=1
            await asyncio.sleep(1)
            print("waiting ...")
        except asyncio.exceptions.TimeoutError:
            print("timeout, connection closed")
            break

        if timeout>10:
            print("timeout, close connection")
            break
    writer.close()
    await writer.wait_closed()

async def main():
    asyncio.create_task(asyncio.start_server(handle_client, '0.0.0.0', PORT))
    print(f"Server started on {PORT}, press ctl+c to terminate")
    while 1:
        await asyncio.sleep(5)

if __name__=="__main__":
    asyncio.run(main())
