import socket
import sys
import time
import os
import asyncio

REMOTE = "192.168.0.103"
PORT = 80

async def serve_client(reader, writer):
    print("Client connected:", reader._transport.get_extra_info('peername')[0])
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    request = str(request_line)
    # execute(request)
    response = "ok\n"

    print("writing response")
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'.encode())
    writer.write(response.encode())
    print("done writing")

    await writer.drain()
    writer.close()
    await writer.wait_closed()
    print("Client disconnected")

async def main():
    asyncio.create_task(asyncio.start_server(serve_client, '0.0.0.0', PORT))
    print(f"Server started, press ctl+c to terminate")
    while 1:
        await asyncio.sleep(5)

if __name__=="__main__":
    asyncio.run(main())
