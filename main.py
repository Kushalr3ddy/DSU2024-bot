
from tkn import token
import discord
from discord.ext import commands
from random import randint,choice
from tester import check
import keep_alive
import wikipedia
import datetime as dt
mods = []
cmd =";"
t = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
intents=discord.Intents.all()
client = commands.Bot(command_prefix= cmd,intents=intents)
#####events
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game(";help"))
    print(f"logged in as {client.user}")

@client.event
async def on_member_join(member):
    with open("joined.log","a") as f:
        f.write(f"{t}:{member} has joined")
    await member.send(f"Welcome! to DSU2024\nmake sure you select the role as per your section by reacting to the message in #section-roles")

@client.event
async def on_member_remove(member):
    with open("left.log","a") as f:
        f.write(f"{t}:{member} has left")
    #await member.send("Welcome! to DSU2024")

@client.event
async def on_message(ctx):
    if str(ctx.author) == str(client.user):
        return
    if str(ctx.author) in mods:
        return
    if ctx.content.startswith("http"):
            return
    #print(f"{now.strftime("%d/%m/%Y %H:%M:%S")}|{ctx.author}:{ctx.author.id}:{ctx.content}")
    file1 = open("myfile.txt", "a")  # append mode 
    file1.write(f"{t}|{ctx.channel.id}:{ctx.author}:{ctx.content}\n") 
    try:
        result = check(str(ctx.content))
    
        if result == True:
            with open("bad_language.txt","a") as f:
                f.write(f"{t}|{ctx.author}:{ctx.author.id}:{ctx.channel.id}:{ctx.content}")
            #me = await client.get_user_info(ctx.author)
            #await ctx.send_message(ctx.author, "#The message")
    except:
        pass
    await client.process_commands(ctx)

###

#####commands
@client.command()
async def hello(ctx):
    """returns hello"""
    await ctx.send(f"hello there {ctx.author}")

@client.command()
async def joined(ctx,member:discord.Member):
    """Shows when a user joined the server"""
    await ctx.send(f"{member.name} joined on {member.joined_at}")

@client.command()
async def repeat(ctx,message,no=1):
    """Repeats a message
    usage:\n;repeat <your-message>"""
    if no <101:
        await ctx.send(f"{message}\n"*no)
    else:
        await ctx.send("max no of times a message can be repeated is 20")

@client.command()
async def roll(ctx):
    """random number between 1 to 6"""
    await ctx.send(f"{ctx.author} rolled a {randint(1,7)}")

@client.command()
async def flip(ctx):
    """flips a coin\nreturns heads or tails"""
    coin = ["heads","tails"]
    await ctx.send(f"{ctx.author} flipped {choice(coin)}")

@client.command()
async def source(ctx):
    """source code for the bot"""
    await ctx.send("https://github.com/kushalr3ddy/DSU2024-bot")


###


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=1):
    """clears specified no of messages (default is 1)\n
    usage: ;clear <no-of-messages>"""
    await ctx.channel.purge(limit=amount+1)

@client.command()
@commands.has_permissions(manage_messages=True)
async def set_prefix(ctx,prefix):
    """changes the command prefix of the bot"""
    client.command_prefix=prefix
    await ctx.send(f"prefix set to ```{prefix}```")

@client.command()
async def wiki(ctx,query,lines=2):
    """does wikipedia search"""
    try:
        if len(query) == 0:
            await ctx.send("usage ;wiki [search]")
        else:
            await ctx.send(wikipedia.summary(query,lines))
    except:
        return
        #await ctx.send("search not found or some error has occured")
######error_handling
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("arguments missing")
    elif isinstance(error,commands.MissingPermissions):
        await ctx.send("you're not allowed to do that")
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send("command not found\ntype ;help for more info")




keep_alive.keep_alive()
client.run(token)