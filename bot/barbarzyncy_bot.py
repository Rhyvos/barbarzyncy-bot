import time
import asyncio
import socket

from utils.bot_logger import bot_logger

logger = bot_logger("barbarzyncy_bot")

async def handle_connection(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    logger.info(f"Received {message!r} from {addr!r}")

    response = "pong"
    writer.write(response.encode())
    await writer.drain()

    logger.info("Closing the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_connection, 'localhost', 12345)  # Dostosuj port i adres, jeśli potrzebujesz

    addr = server.sockets[0].getsockname()
    logger.info(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())