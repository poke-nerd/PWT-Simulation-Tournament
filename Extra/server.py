import asyncio
from pokemon_showdown import ShowdownServer

async def main():
    server = ShowdownServer()
    await server.listen('192.168.1.17', 8000)

if __name__ == "__main__":
    asyncio.run(main())
