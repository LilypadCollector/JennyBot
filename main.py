# Project imports
from lovenotes import get_note, write_note, delete_note, clear, reset_cycle
from credentials import discord_token, firebase_certificate, clear_password, reset_cycle_password  # Secret stuff. Git ignored

# Discord imports
import discord

# Firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Discord setup
client = discord.Client()

# Firebase setup
cred = credentials.Certificate(firebase_certificate)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Global variables
help_text = "Ok (: these commands are for jennys friends" \
            "\n> ;write <text> - Writes a love note to Jenny." \
            "\n> ;delete <lovenote id> - Deletes love note."


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content
    channel = message.channel

    if message.author == client.user:
        return

    if msg == ";help":
        await channel.send(help_text)

    if msg == ";lovenote":
        note, author = get_note()
        if note is None:
            await channel.send("Lovenote machine broke. Tell Danny to fix >:(")
        if author is None:  # For if cycle is at 0 again
            await channel.send("> " + note)
        else:
            await channel.send("> " + note + "\n- " + author)

    # Secret code for create
    if msg.startswith(';write '):
        note = str(msg).replace(";write ", "", 1)
        doc_id = write_note(note, message.author.display_name)
        await channel.send("Wrote a love note: \n\n> " + note + "\n\nby " + message.author.display_name + " (" + str(message.author) + ")\nDoc ID: " + doc_id)

    # Secret code for delete
    if msg.startswith(';delete '):
        doc_id = str(msg).replace(";delete ", "")
        deleted = delete_note(doc_id)

        if deleted is None:
            await channel.send("No lovenote found to delete!")
        else:
            await channel.send("Deleted:\n\n> " + deleted['text'] + "\n\nby " + deleted['author'])

    if msg == clear_password:
        await channel.send("Clearing all lovenotes...")
        count = clear()
        if count == 0:
            await channel.send("Failed. No lovenotes to clear.")
        else:
            await channel.send("Done. Cleared " + str(count))

    if msg == reset_cycle_password:
        count = reset_cycle()
        if count == 0:
            await channel.send("Failed. No lovenotes exist in our collection.")
        else:
            await channel.send("Successfully reset cycles for " + str(count) + " lovenotes.")

client.run(discord_token)
