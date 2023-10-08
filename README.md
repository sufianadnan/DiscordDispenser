# DiscordDispener

## Description
This is a Discord bot written in Python that performs various functions, including sending random messages to users' DMs.
The bot gets 5 random messages/emails from a textfile and sends it to users' DMs. A cooldown of 24hrs is also set so they can't abuse it.

## Prerequisites
- Python 3.7
- Discord.py library

## Features
- Sends 5 random messages to a user's DM.
- Cooldown system to prevent abuse.
- Checks for available stock of messages.
- Notifies the owner when stock is low.

## Usage
To use this bot, you need to set up a `settings.json` file with the required configurations. Refer to the script for more details.

## Installation
1. Clone this repository: `git clone <repository_url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure the `settings.json` file.
4. Run the bot: `python bot.py`

## Configuration
You need to configure the `settings.json` file with your Discord bot token, role, and other settings.
You will also set the prefix and command name in this file.

## Commands
- `!help`: Displays a list of available commands.
- `!<COMMANDNAME>`: Sends 5 random messages to your DM if you have the required role.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to [Discord.py](https://discordpy.readthedocs.io/en/stable/) for the Discord API wrapper.

