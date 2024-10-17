import os

import discord

from profanity import predict_profanity

from explain import explain

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

USERS = set(os.getenv("USERS").split(","))

SHOULD_DELETE = os.getenv("SHOULD_DELETE") == "true"

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_message(message: discord.Message):
    author =  message.author.name
    if author not in USERS:
        return

    content = message.content
    should_filter = predict_profanity(content)

    result = "OK"
    mention = '<@'+ str(message.author.id) +'>'

    if should_filter:
        result = "DELETE"
        if SHOULD_DELETE:
            await message.delete()

        explanation = explain(content)
        await message.channel.send(mention +" " + explanation)

    has_attachment = len(message.attachments) > 0
    if has_attachment and SHOULD_DELETE:
        result = "DELETE"

        await message.delete()
        await message.channel.send(mention + " no attachments. Learn to code idiot.")

    print(result + ": " + message.author.name + ": " + content)


client.run(TOKEN)
