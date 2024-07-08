import discord
from mcrcon import MCRcon as r
import os
import subprocess
import json
from discord.ext import commands
import asyncio
directory = "/dir/to/bot"
token = "yourbottoken"
mcdir = f"{directory}/mcservers.json"
owner = 0 # your discord id
ip = "0.0.0.0" # your ip
null = False
bot = discord.Bot(debug_guilds=[0]) # replace 0 with your guild ID, or delete debug_guilds
def get_info(server):
    path = os.getcwd()
    os.chdir(f"{directory}{server}")
    separator = "="
    keys = {}
    try:
        with open(f'{directory}{server}/server.properties', 'r') as f:
            for line in f:
                if separator in line:
                    name, value = line.split(separator, 1)
                    keys[name.strip()] = value.strip()
        os.chdir(path)
        return keys
    except:
        return null
def get_owners():
    with open(f"{directory}/owners.json","r") as f:
        owners = json.load(f)
    return owners
def get_servers():
    with open(mcdir,"r") as f:
        jsonservers = json.load(f)
    return jsonservers
@bot.command(description="Gives ip for a server.")
async def get_ip(context,server):
    info = get_info(server)
    iport = f"{ip}:{info['server-port']}"
    await context.respond(iport)
@bot.command(description="Adds a server")
async def add_server(context, server: str, port: int, password: str):
    owners = get_owners()
    if int(context.author.id) in owners:
        mcservers = get_servers()
        if not str(server) in mcservers:
            mcservers[server] = {}
            mcservers[server]["port"] = int(port)
            mcservers[server]["pass"] = str(password)
            with open("mcservers.json","w") as f:
                json.dump(mcservers, f, indent=4)
            await context.respond(f"Added server named {server} with port: {port}, and password: {password}", ephemeral=True)
        else:
            await context.respond(f"Server {server} already exists", ephemeral=True)
    else:
        await context.respond("You do not have permission to run this command", ephemeral=True)

@bot.command(name="shutdown", description="Shuts down the bot")
async def shutdown(context):
    if context.author.id == int(owner):
        await context.respond("Shutting down..")
        await bot.change_presence(status=discord.Status.offline)
        # await stop_all()
        quit()
    if not context.author.id == int(owner):
        await context.respond("You cannot run this command.")

@bot.command(name="sync_commands")
async def sync_commands(ctx: discord.ApplicationContext):
    if ctx.author.id == int(owner):
        await ctx.defer(ephemeral=True)
        await bot.sync_commands(force=True, guild_ids=[ctx.guild.id])
        await ctx.respond("Synced commands")
    else:
        await context.respond("You cannot run this command.")

@bot.command(description="Adds an owner")
async def add_owner(context, member: discord.Member):
    owners = get_owners()
    if int(context.author.id) in owners:
        if not int(member.id) in owners:
            owners.insert(0,int(member.id))
            with open(f"{directory}/owners.json","w") as f:
                json.dump(owners, f)
            await context.respond(f"Added user named {member.display_name}, with id: {member.id}")
        else:
            await context.respond(f"Owner {member.display_name} already exists")
    else:
        await context.respond("You do not have permission to run this command")

@bot.command(description="Removes an owner")
async def remove_owner(context, member: discord.Member):
    owners = get_owners()
    if int(context.author.id) == owner:
        owners = get_owners()
        if int(member.id) in owners:
            owners.remove(member.id)
            with open("owners.json","w") as f:
                json.dump(owners, f)
            await context.respond(f"Removed user named {member.display_name}, with id: {member.id}")
        else:
            await context.respond(f"Owner {member.display_name} does not exist")
    else:
        await context.respond("You do not have permission to run this command")

@bot.command(description="Gets bot's ping")
async def ping(context):
    await context.respond(f"My ping is {round(bot.latency*1000)}ms")
@bot.command(description="Lists all servers")
async def servers(context):
    async with context.typing():
        mcservers = get_servers()
        embed = discord.Embed(title="Servers")
        for server in os.listdir(directory):
            info = get_info(server)
            if info == null:
                embed.add_field(name=server, value="Offline")
            else:

                if server in mcservers:
                    try:
                        with r(host="0.0.0.0", port=int(mcservers[server]["port"]),password=mcservers[server]["pass"]) as f:
                            resp = f.command('list')
                        embed.add_field(name=server, value="Online")
                    except:
                        embed.add_field(name=server, value="Offline")
        await context.respond(embed=embed)
@bot.command(description="Lists all players in a server")
async def list(context, server):
    mcservers = get_servers()
    await context.defer()
    if str(server) in mcservers:
        try:
            print("0.0.0.0")
            print(mcservers[server]["port"])
            print(mcservers[server]["pass"])
            with r(host="0.0.0.0", port=int(mcservers[server]["port"]),password=mcservers[server]["pass"]) as f:
                resp = f.command('list')
            await context.respond(resp)
        except Exception as e:
            await context.respond(f"Server is offline.\n{e}")
    else:
        await context.respond(f"No such server {server}")
@bot.command(description="Gives access to the console")
async def console(context, server, *, command):
    await context.defer()
    owners = get_owners()
    if int(context.author.id) in owners:
        mcservers = get_servers()
        if str(server) in mcservers:
            try:
                with r(host="0.0.0.0", port=int(mcservers[server]["port"]),password=mcservers[server]["pass"]) as f:
                    resp = f.command(command)
                await context.respond(resp)
            except:
                await context.respond("Server is offline.")
        else:
            await context.respond(f"No such server {server}")
    else:
        await context.respond("You do not have permission to run this command")
@bot.command(description="Whitelist a user")
async def whitelist(context, server, setting, user):
    await context.defer()
    owners = get_owners()
    if int(context.author.id) in owners:
        try:
            mcservers = get_servers()
            with r(host="0.0.0.0", port=int(mcservers[server]["port"]),password=mcservers[server]["pass"]) as f:
                resp = f.command(f'whitelist {setting} {user}')
            await context.respond(resp)
        except:
            await context.respond("Server is offline.")
    else:
        await context.respond("You do not have permission to run this command")
@bot.command(description="Starts a server")
async def start(context, server):
    await context.defer()
    owners = get_owners()
    if int(context.author.id) in owners:
        for folder in os.listdir(directory):
            if server == folder:
                    try:
                        mcservers = get_servers()
                        with r(host="0.0.0.0", port=int(mcservers[server]["port"]),password=mcservers[server]["pass"]) as f:
                            resp = f.command('list')
                        await context.respond(f"Failed to start server, {server} is already running.")
                    except:
                        try:
                            path = os.getcwd()
                            os.chdir(f"{directory}{folder}")
                            subprocess.Popen(["sh","start.sh"],shell=False)
                            os.chdir(path)
                            await context.respond("Server started :white_check_mark:")
                        except:
                            await context.respond(f"Failed to start server, {server} :negative_squared_cross_mark:")

                        
    else:
        await context.respond("You do not have permission to run this command")
@bot.command(description="stop")
async def stop(context, server):
    await context.defer()
    owners = get_owners()
    if int(context.author.id) in owners:
        mcservers = get_servers()
        if str(server) in mcservers:
            try:
                with r(host="0.0.0.0", port=int(mcservers[server]["port"]),password=mcservers[server]["pass"]) as f:
                    resp = f.command('stop')
                #serversonline -= 1
                await context.respond("Stopped server :octagonal_sign:")
            except:
                await context.respond("Server is already offline.")
        else:
            await context.respond(f"No such server {server}")
    else:
        await context.respond("You do not have permission to run this command")



@bot.event
async def on_ready():
    print(f"{bot.user} Ready")
bot.run(token)
