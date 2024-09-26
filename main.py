import os

import discord


from transformers import pipeline


pipe = pipeline("text-classification", model="parsawar/profanity_model_3.1")


def predict(content: str):
    return pipe.predict(content)[
        0]['label'] == '1'


TOKEN = os.getenv('DISCORD_TOKEN')

USERS = set(os.getenv("USERS").split(","))

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_message(message: discord.Message):
    if message.author.name not in USERS:
        return

    should_filter = pipe.predict(message.content)[
        0]['label'] == '1'

    result = "OK"

    if should_filter:
        result = "DELETE"
        await message.delete()

    print(result + ": " + message.author.name + ": " + message.content)

client.run(TOKEN)
