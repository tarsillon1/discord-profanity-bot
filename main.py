import os

import discord

import logging

from transformers import pipeline

logger = logging.getLogger()
logger.setLevel(logging.INFO)

pipe = pipeline("text-classification", model="parsawar/profanity_model_3.1")

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_message(message: discord.Message):
    logger.info(message.author.name + ": " + message.content)

    should_filter = pipe.predict(message.content)[
        0]['label'] == '1'
    if should_filter:
        await message.delete()

client.run(TOKEN)
