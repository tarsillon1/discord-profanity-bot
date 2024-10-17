import os

import discord

from profanity import predict_profanity

from explain import explain


TOKEN = os.getenv('DISCORD_TOKEN')

USERS = set(os.getenv("USERS").split(","))

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_message(message: discord.Message):
    if message.author.name not in USERS:
        return

    content = message.content
    should_filter = predict_profanity(content)

    result = "OK"

    if should_filter:
        result = "DELETE"
        await message.delete()

        explanation = explain(content)
        message.channel.send(explanation)

    print(result + ": " + message.author.name + ": " + content)


client.run(TOKEN)
