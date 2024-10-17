import os

import discord

from profanity import predict_profanity

from model import explain, respond

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
    
    is_mentioned = client.user.mentioned_in(message)
    if is_mentioned:
        response = respond(author, content)
        await message.channel.send(response)

    print(result + ": " + author + ": " + content)


client.run(TOKEN)
