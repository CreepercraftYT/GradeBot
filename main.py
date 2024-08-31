from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message

import webserver
from responses import get_response
import nextcord
from nextcord.ext import commands
import sqlite3

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True #NOQA
client: Client = Client(intents=intents)

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix = "!", intents=intents)
cogs = [

    "grades",
]
@bot.event
async def on_ready():
    print("bot is running")
if __name__ == "__main__":
    for cog in cogs:
        bot.load_extension(cog)
webserver.keep_alive()
bot.run(os.environ.get("DISCORD_TOKEN"))

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print(':v')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await  message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running, along with the bot')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)



def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()