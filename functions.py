import discord
import random
from replit import db

# When a string is inputted returns a Discord embed
def embed(string):
  embed = discord.Embed(description=string, color=discord.Colour.red())
  return embed
  
# Shuffles the teams and then puts them into the DB 
def seeding():
  allTeams = db["TeamNames"]
  random.shuffle(allTeams)
  tempTeams=[]
  for i in range(0, len(allTeams), 2):
    tempTeams.append([allTeams[i],allTeams[i+1]])
  db["TeamNames"] = tempTeams

# Returns the TeamNames as a string depending on if it is the first or proceeding 
def bracketString(firstRound=True, finalRound = False):
  allTeams = db["TeamNames"]
  output="**__Single Elimination Bracket__**"
  if (firstRound):
    print()
    for match in allTeams:
      output = output + "\n"*2 + match[0] + "\n" + match[1]
  elif(finalRound):
    for match in allTeams:
      print(match,"printed")
      print(type(match))
      if match!=[]:
        output = output + "\n"*2 + "The Winner of the Tournament is: \n :partying_face:" + match[0] + ":partying_face:"
  else:
    tempTeams=[]
    index = 1
    while index<=(len(allTeams)-1):
      print(index)
      tempTeams.append([allTeams[index-1][0], allTeams[index][0]])
      index+=2
    for match in tempTeams:
      output = output + "\n"*2 + match[0] + "\n" + match[1]
    db["TeamNames"] = tempTeams
  return output

#checks if the match already has a result when given the match number
def checkValid(match):
  allTeams = db["TeamNames"]
  if (len(allTeams[match]) == 1):
    return False
  return True

# del db["TeamNames"]
# del db["numTeams"]
# print(db["TeamNames"])
# print(db["TeamNames"])
# print((db["TeamNames"])[0])