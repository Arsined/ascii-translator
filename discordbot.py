import asyncio

import discord
from discord.ext import commands

config = {
    'token': 'MTA0MTI2MjUxNzUzNzc1NTE4Ng.GleMMT.0tNMYSJq7xdgyTz52K0Z1PKrPMYgHwMA9rwQbs',
    'prefix': '1',
}

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.default())

@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        with open("C:/Users/Denis/PycharmProjects/Apple/ascii-translator/out.txt", "r") as f:
            message = await ctx.channel.send("```" + f.read(1848) + "```")
            for _ in range(100):
                await asyncio.sleep(0.7)
                await message.edit(content="```" + f.read(1848) + "```")

bot.run(config['token'])