import os
import discord
from discord.ext import commands
from time import sleep
from functions import embed, seeding, bracketString, checkValid
from replit import db


client = commands.Bot(command_prefix = '>')

@client.event
async def on_ready():
    print("Bot is Ready.")

# This Command is to Purge Messages
@commands.has_permissions(administrator = True)
@client.command(aliases = ["purge","delete","clear"])
async def sell(ctx, amount = 5):
  await ctx.channel.purge(limit = amount+1)
  embed=discord.Embed(description=f"**Successfully sold {amount} message(s) in {ctx.channel}!**", color=discord.Colour.green())
  await ctx.send(embed = embed, delete_after=3)

# This command edits a message of the bot in the current channel when given message id
@client.command()
async def editHere(ctx, idMes):
  message = await ctx.channel.fetch_message(idMes)
  # await ctx.send(embed="Enter the new message:")
  await ctx.send(embed= embed("Enter the New Message:")) 
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel  
  msg = (await client.wait_for("message", check=check)).content
  print(msg)
  await message.edit(content= msg)
  sleep(3)  #delays purge by 3 seconds
  await ctx.channel.purge(limit = 3)

#This command edits the bots message in any specified channel and message with ID
@client.command()
async def edit(ctx, idChan, idMes):
  channel = client.get_channel(int(idChan))
  message = await channel.fetch_message(idMes)
  await ctx.send(embed= embed("Enter the New Message:"))   
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel  
  msg = (await client.wait_for("message", check=check)).content
  print(msg)
  await message.edit(content= msg)
  sleep(3)  #delays purge by 3 seconds
  await ctx.channel.purge(limit = 3)

#sends a bot message to a channel of users choice, or current channel when not specified
@client.command()
async def send(ctx, idChan=None):
  await ctx.send(embed= embed("Enter a Message:"))  
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel
  msg = (await client.wait_for("message", check=check)).content
  print(msg)
  if (idChan!=None):
    channel = client.get_channel(int(idChan))
    await channel.send(msg)
    sleep(3)  #delays purge by 3 seconds
    await ctx.channel.purge(limit = 3)
  else:
    sleep(3)  #delays purge by 3 seconds
    await ctx.channel.purge(limit = 3)
    await ctx.channel.send(msg)

#Creates a tournament, by getting team(s) information and posting the bracket
@client.command()
async def startTournament(ctx):
  await ctx.send(embed= embed("How many teams will be participating? (Ensure the number is an exponent of 2)"))   
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel  
  numTeams = (await client.wait_for("message", check=check)).content
  db["numTeams"] = int(numTeams)

  await ctx.send(embed= embed("Enter the names of all participating teams seperated by commas and a '-' in place of spaces"))
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel  
  allTeamNames = (await client.wait_for("message", check=check)).content
  allTeamNames = allTeamNames.split(",")
  db["TeamNames"] = allTeamNames
  seeding()  #Randomizes the seeding of all teams

  await ctx.send(embed= embed("Enter the Channel ID of where the Bracket should be Posted"))
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel  
  bracketID = (await client.wait_for("message", check=check)).content
  bracketChannel = client.get_channel(int(bracketID))
  bracket = await bracketChannel.send(bracketString())
  db["BracketMessage"] = [bracket.id, bracket.channel.id]
  sleep(3)
  await ctx.channel.purge(limit = 7)

#This commands wipes all Tournament data from the DB
@client.command()
async def deleteTournament(ctx):
  del db["TeamNames"]
  del db["numTeams"]
  del db["BracketMessage"]
  await ctx.send(embed= embed("Tournament Data has been Deleted"))
  sleep(3)
  await ctx.channel.purge(limit = 2)

#This command updates a tournament win
@client.command()
async def matchUpdate(ctx, match):
  match = int(match) - 1
  if(checkValid(match)) == False:
    await ctx.send(embed= embed(f"Match {match} score has already been recorded. Bracket can be updated when all matchs have been recorded"))
    return
  teamNames = (db["TeamNames"])[match]
  await ctx.send(embed= embed(f"Who won? 0 for {teamNames[0]} and 1 for {teamNames[1]}"))
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel  
  matchWinner = int((await client.wait_for("message", check=check)).content)
  (db["TeamNames"])[match].remove(teamNames[matchWinner])
  await ctx.send(embed= embed(f"Match {match+1} winner has been updated."))
  sleep(3)
  await ctx.channel.purge(limit = 4)

#This command returns the score of a specified match
@client.command()
async def matchStatus(ctx,match):
  match = int(match) - 1
  currentMatch = (db["TeamNames"])[match]
  if checkValid(match):
    await ctx.send(embed= embed(f"Match {match+1} between {currentMatch[0]} and {currentMatch[1]} winner has not yet been decided."))
  else:
    await ctx.send(embed= embed(f"Match {match+1} winner was {currentMatch[0]}."))
  sleep(4)
  await ctx.channel.purge(limit = 2)
    
#This command updates the Bracket Message with new games
@client.command()
async def updateBracket(ctx, final=None):
  bracketChannel = client.get_channel(int((db["BracketMessage"])[1]))
  bracketMessage = await bracketChannel.fetch_message(int((db["BracketMessage"])[0]))
  if (final != None):
    await bracketMessage.edit(content = bracketString(False, True))
  else:
    await bracketMessage.edit(content = bracketString(False))

client.run(os.environ['DISCORD_BOT_KEY'])
