import os

import discord
from dotenv import load_dotenv
import threading
import globalhelper

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

globalhelper.client = discord.Client()

@globalhelper.client.event
async def on_ready():
    print(client.user,"has connected")


@globalhelper.client.event
async def on_message(msg):
    print(msg.content)



# client.run(TOKEN)


# tbot = bot()
# tbot.setDaemon(True)
# tbot.start()

# client.login(TOKEN)
# run = threading.Thread(target=client.run)
# run.start()
