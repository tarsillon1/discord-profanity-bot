# Spaghetti code but its python so its fine

import os

import discord

from profanity import predict_profanity

from model import explain, respond, is_talking_to_bot

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

USERS = set(os.getenv("USERS").split(","))

MODERATE = os.getenv("MODERATE") == "true"

SHOULD_DELETE_PROFANITY = os.getenv("SHOULD_DELETE_PROFANITY") == "true"

SHOULD_DELETE_ATTACHMENTS = os.getenv("SHOULD_DELETE_ATTACHMENTS") == "true"

client = discord.Client(intents=discord.Intents.all())


async def moderate(message: discord.Message):
    if not MODERATE:
        return
    
    author =  message.author.name
    if author not in USERS:
        return
    
    content = message.content
    should_filter = predict_profanity(content)

    mention = '<@'+ str(message.author.id) +'>'
    
    if should_filter:
        if SHOULD_DELETE_PROFANITY:
            await message.delete()

        explanation = explain(content)
        await message.channel.send(mention +" " + explanation)
        return True

    has_attachment = len(message.attachments) > 0
    if has_attachment and SHOULD_DELETE_ATTACHMENTS:
        await message.delete()
        await message.channel.send(mention + " no attachments. Learn to code idiot.")
        return True
    

@client.event
async def on_message(message: discord.Message):
    if message.author.id == client.user.id:
        return

    moderated = await moderate(message)
    if moderated:
        return
    
    content = message.content
    author =  message.author.name
    is_mentioned = client.user.mentioned_in(message) | is_talking_to_bot(content)
    if is_mentioned:
        response = respond(author, content)
        await message.channel.send(response)


client.run(TOKEN)
