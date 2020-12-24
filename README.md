# JennyBot
A Discord bot for my girlfriend's 21st birthday. Written in Python, and uses [discord.py](https://discordpy.readthedocs.io/en/latest/index.html) (API wrapper for Discord) and [Google Firestore](https://cloud.google.com/firestore) (NoSQL Firebase database).

## Installation

This bot is intended for private use, so there will not be a Discord bot link or executable file available for download. To make a copy of the JennyBot for personal use, overwrite `discord_token` and `firebase_certificate` in `main.py` with a unique Discord bot token and Firestore configuration key, respectively. Initialize the variables `clear_password` and `reset_cycle_password` with secret commands of your choice.

## Lovenotes

Users write love notes for some recipient. Everytime the recipient executes a command, they will see one unopened note each time.

If the bot runs out of unread notes, it will recycle past notes until a new note is written.

#### Usage

The following commands are to be typed in any channel that the JennyBot can access.

`;write <text>` - Writes a lovenote to be stored in the database.

`;delete <doc ID>` - Deletes lovenote of the given identifier.

> NOTE: The document ID is printed immediately after a `;write` command.

`;lovenote` - Prints a lovenote along with its author.
