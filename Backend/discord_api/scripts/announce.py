import sys
import discord
import logging
import asyncio

# logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
discordClient = discord.Client(intents=intents)

async def announce(anime_title, user_id):
    await discordClient.wait_until_ready()
    messagePayload = "```" + anime_title + " successfully synced from transmission" + "```"
    try:
        messageRecipient = await discordClient.fetch_user(user_id)  # User ID should be an integer
        await messageRecipient.create_dm()
        DMRoom = messageRecipient.dm_channel
        await DMRoom.send(messagePayload)
        await discordClient.close()
        await discordClient.clear()
    except discord.NotFound:
        print(f"User with ID {user_id} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

@discordClient.event
async def on_ready():
    print('Logged in as')
    print(discordClient.user.name)
    print(discordClient.user.id)
    
    # Call announce with proper arguments
    await announce(sys.argv[2], int(sys.argv[3]))
    print('-------')
    await discordClient.close()
    await discordClient.clear()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python announce.py [token] [anime title] [discord user id]")
        sys.exit(1)
    token = sys.argv[1]
    if token:
        try:
            discordClient.run(token)
        finally:
            # Make sure that all aiohttp resources are closed
            if discordClient.http._HTTPClient__session and not discordClient.http._HTTPClient__session.closed:
                asyncio.run(discordClient.http._HTTPClient__session.close())
    else:
        print("No token provided")
        sys.exit(1)
