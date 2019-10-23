import discord

from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix='.')
status = cycle(['Bear Simulator 2019'])
bad_words = cycle(['', 'fuck', 'kys', 'bitch', 'nigga', 'nigger', 'fucker', 'fucka', 'sex', 'mofo', 'ass', 'cock', 'dick'])

# on ready
@client.event
async def on_ready():
	change_status.start()
	print ("working on ready")
	print (discord.Role.members)

# message to let people know to be inclusive
@client.event
async def on_message(ctx):
	if "guys" in ctx.content:
		await ctx.author.send("'Guys' isn't the most inclusive term, maybe try 'folks' instead?")
	if next(bad_words) in ctx.content:
		await ctx.channel.send("No swearing allowed! Admins have been notified.")

# generic command handling
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("Command does not exist.")

# generic ping
@client.command()
async def ping(ctx):
	await ctx.send("Bear hug!")

# clear commands
@client.command()
@commands.has_role('execs')
async def clear(ctx, amount:int):
	await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRole):
		await ctx.send("This is an admin-only command!")
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please specify the amount of messages to clear.")

# kick commands
@client.command()
@commands.has_role('execs')
async def kick(ctx, member : discord.Member, *, reason=" for misbehaving"):
	member.kick(reason=reason)

@kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingRole):
		await ctx.send("This is an admin-only command!")

# ban commands
@client.command()
@commands.has_role('execs')
async def ban(ctx, member : discord.Member, *, reason=" for misbehaving"):
	member.ban(reason=reason)

@ban.error
async def ban_error(ctx, error):
	if isinstance(error, commands.MissingRole):
		await ctx.send("This is an admin-only command!")

# tasks loop for status change
@tasks.loop(seconds=10)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))

client.run('NjE5MDM0MjAyODU1MzA5MzEy.XXCXCA.Vf-jMM3PjcVhPtyzBYu-xDbPLkA')