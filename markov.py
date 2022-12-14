"""A Markov chain generator that can tweet random messages."""
import os
import discord
import sys
from random import choice


def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ''
    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()
    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    keys = list(chains.keys())
    key = choice(keys)

    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text).

        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    return ' '.join(words)


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

#Get response made from chain
markov_response = make_text(chains)

#Discord Bot
intents = discord.Intents.default()
intents.message_content = True

markov_bot_client = discord.Client(intents=intents)

@markov_bot_client.event
async def on_ready():
    print(f'{markov_bot_client.user} has logged in!')

@markov_bot_client.event
async def on_message(message):
    if message.author == markov_bot_client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    elif message.content.startswith('Do you have an example of a Markov Chain?'):
        #Get response made from chain
        markov_response = make_text(chains)
        await message.channel.send(markov_response)
    
    #referred to stackoverflow post for guidance. 
    #https://stackoverflow.com/questions/62239816/how-do-i-make-the-bot-respond-when-someone-mentions-it-discord-py
    elif markov_bot_client.user.mentioned_in(message):
        markov_response = make_text(chains)
        await message.channel.send(markov_response)
        
markov_bot_client.run(os.environ['DISCORD_TOKEN'])