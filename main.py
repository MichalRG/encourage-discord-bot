import discord
import os
from discord import message
import requests
import json
import random
from replit import db

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depress"]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person!"
]


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db['encouragements']
    if encouragements:
      encouragements.append(encouraging_message)
      db['encouragements'] = encouragements
    else:
      db['encouragements'] = [encouraging_message]
  else:
    db['encouragements'] = [encouraging_message]


def delete_encouragment(index):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']

    if encouragements and len(encouragements) > index:
      del encouragements[index]
      db['encouragements'] = encouragements
      print(f"Deleted Sucessfuly {db['encouragements']}")
  else:
    encouragements = []


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg_content = message.content

  if msg_content.startswith('!hello'):
    await message.channel.send('Hello!')

  elif msg_content.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  elif db['responding'] and any(word in msg_content for word in sad_words):
    options = starter_encouragements

    if 'encouragements' in db.keys():
      options = options + list(db['encouragements'])

    random_answer = random.choice(options)

    await message.channel.send(random_answer)

  elif msg_content.startswith('!new'):
    encouraging_message = msg_content.split('!new ', 1)[1]

    update_encouragements(encouraging_message)

    await message.channel.send('New encouraging message added.')

  elif msg_content.startswith('!del'):
    encouragements = []

    if 'encouragements' in db.keys():
      index = int(msg_content.split('!del', 1)[1])

      delete_encouragment(index)

      encouragements = db['encouragements']

    await message.channel.send(list(encouragements))

  elif msg_content.startswith('!list'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']

    await message.channel.send(list(encouragements))

  elif msg_content.startswith("!responding") and len(msg_content) > 11:
    value = msg_content.split("!responding ", 1)[1]
    
    if value.lower() == "true":
      db['responding'] = True

      await message.channel.send("Responding is on.")
    else:
      db['responding'] = False

      await message.channel.send("Responding is off.")

  elif "lonely" in msg_content:
    await message.channel.send("I'm here for you")


if "responding" not in db.keys():
  db['responding'] = True

my_secret = os.environ['TOKEN']
client.run(my_secret)
