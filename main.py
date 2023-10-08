import json
import os
import random
import time
import discord
from discord.ext import commands, tasks

# Construct file paths using the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))
settings_file = os.path.join(script_directory, 'settings.json')
accounts_file = os.path.join(script_directory, 'accounts.txt')
cooldown_file = os.path.join(script_directory, 'cooldown.txt')


# Load the JSON data from the file

with open('settings.json', 'r') as json_file:
    data = json.load(json_file)

# Extract the values from the loaded data
TOKEN = data["TOKEN"]
ROLE = data["ROLE"]
SENT_MESSAGES_FILE = data["SENT_MESSAGES_FILE"]
PREFIX = data["PREFIX"]
OWNER = data["OWNER_ID"]
COMMANDNAME = data["COMMAND"]
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.remove_command("help")

# Load messages from file into a list
def load_messages():
    with open(accounts_file, "r") as f:
        messages = [line.strip() for line in f.readlines()]
    return messages

# Save messages back to file
def save_messages(messages):
    with open(accounts_file, "w") as f:
        f.write("\n".join(messages))

# Check if user has already used the command within the last 24 hours
def check_cooldown(user_id):
    with open("cooldown.txt", "r") as f:
        cooldowns = [line.strip().split(",") for line in f.readlines()]
    for cooldown in cooldowns:
        if cooldown[0] == str(user_id):
            if int(cooldown[1]) + 86400 > int(time.time()):
                return False
            else:
                cooldown[1] = str(int(time.time()))
                with open("cooldown.txt", "w") as f:
                    f.write("\n".join([",".join(cooldown) for cooldown in cooldowns]))
                return True
    cooldowns.append([str(user_id), str(int(time.time()))])
    with open("cooldown.txt", "w") as f:
        f.write("\n".join([",".join(cooldown) for cooldown in cooldowns]))
    return True

# Check if there are enough messages in the file
def check_stock():
    with open(accounts_file, "r") as f:
        messages = [line.strip() for line in f.readlines()]
    if len(messages) < 5:
        return False
    return True
@bot.command(help="This command you just ran")
async def help(ctx):
    embed = discord.Embed(
        title="Bot Help",
        description="Here are some available commands:",
        color=discord.Color.blue()
    )

    # Add commands and their descriptions to the embed
    for command in bot.commands:
        if not command.hidden:
            embed.add_field(
                name=command.name,
                value=command.help or "No description provided",
                inline=False
            )

    await ctx.send(embed=embed)
# Send a DM to the user with 5 random messages from the file
send_messages_queue = []

# Send a DM to the user with 5 random messages from the file
@bot.command(name=COMMANDNAME, help="Sends 5 Mails to your DM.")
@commands.has_role(ROLE)
async def dynamic_command(ctx):
    if not check_cooldown(ctx.author.id):
        await ctx.reply("You have already used this command within the last 24 hours.")
        return
    if not check_stock():
        await ctx.reply("UH OH, Seems to be no more stock :")
        return
    messages = load_messages()
    random.shuffle(messages)
    user = ctx.author
    for message in messages[:5]:
        await user.send(message)
        messages.remove(message)
    save_messages(messages)
    await ctx.reply("sent in DMs!")

# Save sent messages back to file
def save_sent_messages(messages):
    with open(SENT_MESSAGES_FILE, "w") as f:
        f.write("\n".join(messages))
# Check stock every hour and send notification if it's low
@tasks.loop(hours=2)
async def check_stock_loop():
    if not check_stock():
        owner = await bot.fetch_user(OWNER)
        await owner.send("Stock is low!")
        await owner.send(file=discord.File(accounts_file))

@bot.event
async def on_ready():
    print("Bot is ready.")
    await bot.change_presence(activity=discord.Game(name="Managing Inventory - AdnanV2#3596"))

    check_stock_loop.start()

bot.run(TOKEN)
