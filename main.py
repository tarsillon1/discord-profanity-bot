import os

import discord

from transformers import pipeline

pipe = pipeline("text-classification", model="parsawar/profanity_model_3.1")

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_message(message):
    print(message.author + ": " + message.content)
    should_filter = pipe.predict(message.content)[
        0]['label'] == '1'
    if should_filter:
        message.delete()

client.run(TOKEN)
