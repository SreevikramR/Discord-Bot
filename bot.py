import discord
from discord.ext import commands, tasks
import random
from itertools import cycle

client = commands.Bot(command_prefix=".")

client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=".help"))
    print("Bot is ready.")
    servers = list(client.guilds)
    print(f'Part of {str(len(servers))} Servers')


@client.command()
async def ping(ctx):
    embed = discord.Embed(
        title=f"Pong! {round(client.latency * 1000)}ms",
        colour=discord.Colour.blue()
    )
    embed.set_footer(text="Bot made by TheRealViki#3300")
    await ctx.send(embed=embed)


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

    embed = discord.Embed(
        title=f"__Question:__ {question}\n__Answer:__ {random.choice(responses)}",
        colour=discord.Colour.blue()
    )
    embed.set_footer(text="Bot made by TheRealViki#3300")

    await ctx.send(embed=embed)


@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(
        title=f"{amount} messages have successfully been terminated :sunglasses:",
        colour=discord.Colour.blue()
    )
    embed.set_author(name=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)
    embed.set_footer(text="Bot made by TheRealViki#3300")

    await ctx.send(embed=embed)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete in the form of   **.clear <number>**')


@client.group(invoke_without_command=True)
async def help(ctx, *, message=None):
    if message == "mod":
        embed = discord.Embed(
            title='**Moderation Commands**',
            decription='These commands require admin permissions',
            colour=discord.Colour.blue()
        )

        embed.add_field(name="These commands require admin permissions to run", value="**  **", inline=False)
        embed.add_field(name='__.warn <member> <reason__>', value='Warns a member for any specifiable reason through DM', inline=False)
        embed.add_field(name='__.kick <member>__', value='Kicks a member from the server', inline=False)
        embed.add_field(name='__.ban <member>__', value='Bans a member from the server', inline=False)
        embed.add_field(name='__.unban <member#1243>__', value='Unbans a member in the server', inline=False)
        embed.set_footer(text="Bot made by TheRealViki#3300")
        msg = await ctx.send(embed=embed)
        return


    embed = discord.Embed(
        title = '**Help is Here!**',
        colour = discord.Colour.blue()
    )
    embed.add_field(name='__.help mod__', value='View all moderation commands (Admin Permissions required)',inline=False)
    embed.add_field(name='__.ask <question>__', value='Ask any question that will give you a yes or no answer', inline=False)
    embed.add_field(name='__.clear <number>__', value='Clears <number> of messages in the text channel', inline=False)
    embed.add_field(name='__.ping__', value='Gives you the Ping of the bot', inline=False)
    embed.add_field(name='__.tell <member> <message>__', value='DM anyone by mentioning them with the message through the bot', inline=False)
    embed.add_field(name="__.embed <text>__", value="Embeds the text.")
    embed.add_field(name='Octave Support Server', value ='[Support Server](https://discord.com/api/oauth2/authorize?client_id=816985180459892746&permissions=8&scope=bot)', inline=False)
    embed.set_footer(text="Bot made by TheRealViki#3300")
    msg = await ctx.send(embed=embed)


@client.command()
async def embed(ctx, *, message):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title=f"{message}", colour=discord.Colour.blue())

    await ctx.send(embed=embed)


@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify what you want to embed in the form of **.embed <text>**')


@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.send(f'You have been kicked from the server `{ctx.guild.name}` by `{ctx.author.display_name}`')
    await member.kick(reason=reason)
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{member.mention} has been kicked from the server by {ctx.author.display_name}")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have admin permissions to run this command')


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.send(f'You have been banned from the server `{ctx.guild.name}` by `{ctx.author.display_name}`')
    await member.ban(reason=reason)
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{member.mention} has been banned from the server.")
    await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have admin permissions to run this command')


@ban.error
async def ben_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Member was not found')


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.channel.send(f"{user.mention} has been unbanned")
            await user.send(f'You have been Unbanned from the Server `{ctx.guild.name}`')
            await ctx.guild.unban(user)
            return


@client.command()
async def tell(ctx, member: discord.Member, *, message):
    await ctx.channel.purge(limit=1)
    await member.send(message)
    await member.send(f"Sent by {ctx.author.display_name} via Octave Bot")
    await ctx.send(f'{ctx.author.mention} Your message has been sent successfully')


@tell.error
async def tell_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify who you want to dm to by mentioning them and the message in the form of **.embed <member> <message>**')


@client.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, reason):
    await ctx.channel.purge(limit=1)
    await member.send(f"You have been warned by `{ctx.author.display_name}` in the server `{ctx.guild.name}` for the reason - `{reason}`")
    await ctx.send(f'{ctx.author.mention} Your warning has been sent successfully')


@warn.error
async def tell_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify who you want to warn by mentioning them and the reason of warning **.warn <member> <reason>**')


client.run("ODE2OTg1MTgwNDU5ODkyNzQ2.YEC6vQ.LTlfnV8tlxgZeUd_Tar465HBymo")
