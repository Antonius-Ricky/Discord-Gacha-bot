import discord
import os
from Token import TOKEN
from responses import get_response
from fruit import Fruit

current_directory = os.path.dirname(__file__)
image_folder_name = "images"
image_folder_path = os.path.join(current_directory, image_folder_name)
fruit = Fruit(image_folder_path)



async def send_message(message, user_message, is_private):
    try:
        response = get_response(user_message, fruit, str(message.author))
        if response[1]:  # Check if embed is present
            text, embed, image_path = response
            if text:  # Check if text is present
                if image_path:
                    await message.channel.send(text, embed=embed, file=discord.File(image_path))
                else:
                    await message.channel.send(text, embed=embed)
            else:
                await message.channel.send(embed=embed, file=discord.File(image_path)) if image_path else await message.channel.send(embed=embed)
        else:
            await message.author.send(response[0]) if is_private else await message.channel.send(response[0])
    except Exception as e:
        print(e)

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running :D ')
        
    @client.event
    async def on_message(message):
        if message.author.bot:  # Ignore messages from bots
            return

        if not isinstance(message, discord.Message):  # Check if message is a valid discord.Message object
            print(f"Received invalid message: {message}")
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message.startswith('?'):
            user_message = user_message[1:]
            response = get_response(user_message, fruit, username) 
            if response[0] and response[1]:
                text, embed, image_path = response
                await message.channel.send(text, embed=embed, file=discord.File(image_path))
            else:
                await send_message(message, user_message, is_private=True)
        else:
            response = get_response(user_message, fruit, username) 
            if response[0] and response[1]:
                text, embed, image_path = response

                # Check if the attribute exists before setting the thumbnail
                if hasattr(message.author, 'avatar_url'):
                    embed.set_thumbnail(url=message.author.avatar_url)

                await message.channel.send(text, embed=embed, file=discord.File(image_path))
            else:
                await send_message(message, user_message, is_private=False)

    client.run(TOKEN)

run_discord_bot()
