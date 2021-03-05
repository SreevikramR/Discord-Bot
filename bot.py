import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_member_join(member):
    print(f"""{member} has joined a server.""")

@client.event
async def on_member_remove(member):
    print(f"""{member} has left a server.""")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
async def ask(ctx, *, question):
    responses = ["It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Yes - definitely.",
"You may rely on it.",
"As I see it, yes.",
"Most likely.",
"Outlook good.",
"Yes.",
"Signs point to yes.",
"Reply hazy, try again.",
"Ask again later.",
"Better not tell you now.",
"Cannot predict now.",
"Concentrate and ask again.",
"Don't count on it.",
"My reply is no.",
"My sources say no.",
"Outlook not so good.",
"Very doubtful."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command()
async def clear(ctx, amount=1000000000000000000000):
    await ctx.channel.purge(limit=amount)
    await ctx.send("All old messages have been terminated! :sunglasses: ")

client.run("ODE2OTg1MTgwNDU5ODkyNzQ2.YEC6vQ.08GWcbqbrDta9ZuzKLyAkE5DC9g")