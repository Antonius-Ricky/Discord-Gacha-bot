import discord
import json
from fruit import Fruit
import time
import os
import random
bot_prefix = '.'
user_data_file = 'user_data.json'

ROLL_COOLDOWN = 120
roll_cooldowns = {}
sell_cooldowns = {}
give_cooldowns = {}
givefruit_cooldowns = {}


current_directory = os.path.dirname(__file__)
image_folder_name = "images"
image_folder_path = os.path.join(current_directory, image_folder_name)
fruit = Fruit(image_folder_path)

duel_challenges = {}


last_sale_info = {"fruit_name_original_case": "", "quantity": 0, "total_value": 0}
last_give_info = {"amount": 0, "target_user": ""}
last_sellall_info = {"total_value": 0} 


def load_user_data():
    try:
        with open(user_data_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

def save_user_data(data):
    try:
        with open(user_data_file, 'w') as file:
            json.dump(data, file, indent=4)
        return True  
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False  

def calculate_total_value(inventory, beri):
    total_value = beri
    fruit = Fruit(image_folder_path) 
    for item in inventory:
        fruit_name = item["name"]
        quantity = item.get("quantity", 1)
        total_value += quantity * fruit.get_fruit_value(fruit_name)
    return total_value
    

def get_response(message: str, fruit, username):
    global last_sale_info
    global last_give_info
    global total_command_count
    global last_sellall_info
    
    data = load_user_data()

    if not message.startswith(bot_prefix):
        return None, None, None 
    p_message = message[len(bot_prefix):].strip().lower()


    if p_message == 'register':
        if username not in data:
            data[username] = {"inventory": []}
            save_user_data(data)
            return f'You are now registered, {username}!', None, None
        else:
            return f'You are already registered, {username}.', None, None

    if username not in data:
        return f'You need to register first. Type {bot_prefix}register to register.', None, None
    
    if p_message == 'hello':
        
        embed = discord.Embed(
            title=f'Hello, {username}!',
            description='Selamat datang ! Saya adalah bot yang diciptakan oleh Amory yang dapat membantu Anda dengan berbagai fitur.',
            color=discord.Color.green()
        )

        embed.add_field(name='Commands', value='Gunakan `.info` untuk melihat command yang tersedia.', inline=False)
        embed.add_field(name='Support', value='Dukung Amory dengan mengirim donasi mulai dari Rp.1000 [Donate disini](https://trakteer.id/amoryg/tip?open=true).', inline=False)

        return None, embed, None

    if p_message.startswith('rank'):
        parts = p_message.split()

        if len(parts) == 1: 
            target_user = username
        elif len(parts) == 2: 
            target_user = parts[1].lower()
        else:
            return "Invalid command. Please use `.rank` to see your own rank or `.rank <username>` to see another user's rank.", None, None

        user_values = {user: calculate_total_value(data[user]["inventory"], data[user].get("beri", 0)) for user in data}
        sorted_users = sorted(user_values.items(), key=lambda x: x[1], reverse=True)

     
        target_user_rank = next((i + 1 for i, (user, _) in enumerate(sorted_users) if user == target_user), None)

     
        embed = discord.Embed(
            title=f'{target_user}\'s Rank',
            color=discord.Color.gold()
        )

        if target_user_rank is not None:
            embed.add_field(name=f"Current Rank: #{target_user_rank}", value=f"Total Value: ${user_values[target_user]}", inline=True)
        else:
            embed.add_field(name="Rank: Not Ranked Yet", value=f"{target_user} is not ranked yet.", inline=True)

        return None, embed, None

    if p_message == 'user':
        total_users = len(data)

        embed = discord.Embed(
            title='Total Users',
            description=f'There are currently {total_users} registered users.',
            color=discord.Color.blue()
        )

        return None, embed, None

    if p_message.startswith('sell'):
        parts = p_message.split()

        if len(parts) == 2 and parts[1].lower() == 'all':
            total_beri = 0
            sold_items = []

            # Check cooldown for selling all
            if username in sell_cooldowns and time.time() - sell_cooldowns[username] < 1:
                remaining_time_seconds = int(1 - (time.time() - sell_cooldowns[username]))
                minutes, seconds = divmod(remaining_time_seconds, 1)
                cooldown_message = f'Successfully sold all fruits in your inventory for ${last_sellall_info["total_value"]}! Use `.beri` to check your current beri'
                return cooldown_message, None, None

            inventory = data.get(username, {}).get("inventory", [])
            beri = data.get(username, {}).get("beri", 0)

            for item in inventory:
                item_name = item["name"]
                item_quantity = item.get("quantity", 1)

                fruit_name_original_case = item_name
                fruit_value = fruit.get_fruit_value(fruit_name_original_case)
                total_value = fruit_value * item_quantity
                total_beri += total_value

                sold_items.append({
                    "fruit_name_original_case": fruit_name_original_case,
                    "quantity": item_quantity,
                    "total_value": total_value
                })

            data[username]["beri"] = beri + total_beri
            inventory.clear()
            save_user_data(data)

            sell_cooldowns[username] = time.time() + 0.1

            # Update last_sellall_info
            last_sellall_info["total_value"] = total_beri

            sell_result_message = f'Successfully sold all fruits in your inventory for ${total_beri}! Use `.beri` to check your current beri'
            return sell_result_message, None, None
        elif len(parts) == 2:
            fruit_to_sell = parts[1].lower()
            quantity_to_sell = 1
        elif len(parts) == 3:
            fruit_to_sell = parts[1].lower()
            try:
                quantity_to_sell = int(parts[2])
            except ValueError:
                quantity_to_sell = 1
        elif len(parts) == 1:
            return "Invalid format. Please use this format: `.sell fruit_name [quantity]`.", None, None
        else:
            return "Too many arguments. Please use this format: `.sell fruit_name [quantity]` or `.sell all`.", None, None

        if quantity_to_sell < 0:
            return "Invalid amount. Please provide a non-negative number.", None, None
        if username in sell_cooldowns and time.time() - sell_cooldowns[username] < 1:
            remaining_time_seconds = int(1 - (time.time() - sell_cooldowns[username]))
            minutes, seconds = divmod(remaining_time_seconds, 1)
            cooldown_message = f'Successfully sold {last_sale_info["quantity"]} {last_sale_info["fruit_name_original_case"]}(s) for ${last_sale_info["total_value"]}! Use `.beri` to check your current beri'
            return cooldown_message, None, None

        inventory = data.get(username, {}).get("inventory", [])
        beri = data.get(username, {}).get("beri", 0)
        original_case_items = {item["name"].lower(): item for item in inventory}
        fruit_instance_to_sell = original_case_items.get(fruit_to_sell, None)

        sell_success = False

        for item in inventory:
            item_name = item["name"]
            item_quantity = item.get("quantity", 1)

            if item_name.lower() == fruit_to_sell:
                
                if item_quantity >= quantity_to_sell:
                    fruit_name_original_case = item["name"]
                    fruit_value = fruit.get_fruit_value(fruit_name_original_case)
                    total_value = fruit_value * quantity_to_sell
                    data[username]["beri"] = beri + total_value

                    item["quantity"] -= quantity_to_sell
                    if item["quantity"] == 0:
                        inventory.remove(item)

                    save_user_data(data)

                    last_sale_info["fruit_name_original_case"] = fruit_name_original_case
                    last_sale_info["quantity"] = quantity_to_sell
                    last_sale_info["total_value"] = total_value

                    sell_success = True
                    break
        if sell_success:
            sell_cooldowns[username] = time.time() + 0.1
            sell_result_message = f'Successfully sold {quantity_to_sell} {fruit_name_original_case}(s) for ${total_value}! Use `.beri` to check your current beri'
            return sell_result_message, None, None
        else:
            return f"You don't have {fruit_to_sell} or enough {fruit_to_sell} to sell in your inventory.", None, None

    if p_message.startswith('berigive'):
        parts = p_message.split()
        if len(parts) != 3:
            return "Invalid command format. Use `.berigive {username} {amount}`.", None, None

        _, target_user, amount_str = parts

        try:
            amount = int(amount_str)
        except ValueError:
            return "Invalid amount. Please provide a valid number.", None, None

        if amount < 0:
            return "Invalid amount. Please provide a non-negative number.", None, None

        if username not in data:
            return f'You need to register first. Type {bot_prefix}register to register.', None, None

        sender_beri = data[username].get("beri", 0)

        if sender_beri < amount:
            return "You don't have enough beri to give or the beri is already sent.", None, None

        if target_user not in data:
            return f"User {target_user} not found.", None, None

        if username in give_cooldowns and time.time() - give_cooldowns[username] < 1:
            remaining_time_seconds = int(1 - (time.time() - give_cooldowns[username]))
            minutes, seconds = divmod(remaining_time_seconds, 1)
            cooldown_message = f'Successfully gave {amount} beri to {target_user}! Your current beri: ${data[username]["beri"]}. {target_user}\'s current beri: ${data[target_user]["beri"]}.'
            return cooldown_message, None, None

        give_success = False

        data[username]["beri"] = sender_beri - amount
        data[target_user]["beri"] += amount

        save_user_data(data)

        give_success = True 
        if give_success:
            give_cooldowns[username] = time.time() + 0.1

            return f'Successfully gave {amount} beri to {target_user}! Your current beri: ${data[username]["beri"]}. {target_user}\'s current beri: ${data[target_user]["beri"]}.', None, None
        else:
            return f"You don't have {fruit_to_sell} in your inventory.", None, None

    if p_message.startswith('fruitgive'):
        parts = p_message.split()

        if len(parts) == 4:
            target_user = parts[1].lower()
            fruit_to_give = parts[2].lower()
            try:
                amount_to_give = int(parts[3])
            except ValueError:
                return "Invalid amount. Please provide a valid number.", None, None
        elif len(parts) == 3:
            target_user = parts[1].lower()
            fruit_to_give = parts[2].lower()
            amount_to_give = 1
        elif len(parts) == 2:
            target_user = parts[1].lower()
            fruit_to_give = None  # Set to None when no fruit is specified
            amount_to_give = 1
        else:
            return "Invalid format. Please use this format: `.fruitgive {username} {fruit} {quantity}`.", None, None

        if amount_to_give < 0:
            return "Invalid amount. Please provide a non-negative number.", None, None

        if username not in data:
            return f'You need to register first. Type {bot_prefix}register to register.', None, None

        if target_user not in data:
            return f"User {target_user} not found.", None, None

        if target_user == username and fruit_to_give is not None:
            return "You can't give fruits to yourself.", None, None

        if username in givefruit_cooldowns and time.time() - givefruit_cooldowns[username] < 1:
            remaining_time_seconds = int(1 - (time.time() - givefruit_cooldowns[username]))
            minutes, seconds = divmod(remaining_time_seconds, 1)
            cooldown_message = f'Successfully gave {amount_to_give} {fruit_to_give}(s) to {target_user}! Check your inventory to see your current fruit quantity.'
            return cooldown_message, None, None

        givefruit_success = False

        giver_inventory = data.get(username, {}).get("inventory", [])
        receiver_inventory = data.get(target_user, {}).get("inventory", [])
        original_case_items_giver = {item["name"].lower(): item for item in giver_inventory}
        fruit_instance_to_give = original_case_items_giver.get(fruit_to_give, None)

        for item in giver_inventory:
            item_name = item["name"]
            item_quantity = item.get("quantity", 1)

            if item_name.lower() == fruit_to_give:
                
                if item_quantity >= amount_to_give:
                    fruit_name_original_case = item["name"]
                    # Check if the fruit already exists in the receiver's inventory
                    receiver_fruit_instance = next((item for item in receiver_inventory if item["name"].lower() == fruit_to_give), None)

                    if receiver_fruit_instance:
                        receiver_fruit_instance["quantity"] += amount_to_give
                    else:
                        receiver_inventory.append({"name": item_name, "quantity": amount_to_give})

                    item["quantity"] -= amount_to_give
                    if item["quantity"] == 0:
                        giver_inventory.remove(item)

                    save_user_data(data)

                    last_give_info["target_user"] = target_user
                    last_give_info["amount"] = amount_to_give

                    givefruit_success = True
                    break

        if givefruit_success:
            givefruit_cooldowns[username] = time.time() + 1  # Set cooldown to 1 second
            givefruit_result_message = f'Successfully gave {amount_to_give} {fruit_name_original_case}(s) to {target_user}! Check your inventory to see your current fruit quantity.'
            return givefruit_result_message, None, None
        else:
            return f"You don't have {fruit_to_give} or enough {fruit_to_give} to give in your inventory.", None, None

    if p_message.startswith('value'):
        # Split the command into words
        command_words = p_message.split(' ')

        # Check if there is a second word (i.e., a specified fruit name)
        if len(command_words) > 1:
            # Extract the specified fruit from the command
            requested_fruit = command_words[1].capitalize()

            fruit_names = fruit.get_fruit_names()

            # Check if the requested fruit is valid
            if requested_fruit in fruit_names:
                fruit_value = fruit.get_fruit_value(requested_fruit)
                fruit_rarity = fruit.fruits_rarity[requested_fruit]
                fruit_percentage = fruit.chance_percentage[fruit_rarity.lower()]

                # Create an embed object
                embed = discord.Embed(title=f'{requested_fruit} Value and Rarity', color=0x00ff00)  # You can customize the color

                # Add the image of the requested fruit to the embed
                requested_fruit_image_path = fruit.get_fruit_image({"name": requested_fruit})
                embed.set_image(url=f'attachment://{requested_fruit_image_path}.png')

                # Add fields to the embed
                embed.add_field(name='Value', value=f'${fruit_value}', inline=True)
                embed.add_field(name='Rarity', value=fruit_rarity, inline=True)
                embed.add_field(name='Percentage', value=f'{fruit_percentage}%', inline=True)

                return None, embed, requested_fruit_image_path
            else:
                return 'Invalid fruit name. Please provide a valid fruit name.', None, None
        else:
            return 'Please specify a fruit name with format `.value <specific fruit name>` ', None, None


    if p_message.startswith('top'):
        parts = p_message.split()
        top_count = 1  # Default to top 1 if no count is provided
        if len(parts) > 1:
            try:
                top_count = int(parts[1])
            except ValueError:
                return "Invalid count. Please provide a valid number for the top command.", None, None

        if top_count <= 0:
            return "Invalid count. Please provide a positive number for the top command.", None, None

        # Calculate the range of users based on the specified top count
        start_index = (top_count - 1) * 10
        end_index = top_count * 10

        user_values = {username: calculate_total_value(data[username]["inventory"], data[username].get("beri", 0)) for username in data}
        sorted_users = sorted(user_values.items(), key=lambda x: x[1], reverse=True)
        selected_users = sorted_users[start_index:end_index]

        # Create an embedded message for the selected top rankings
        embed = discord.Embed(
            title=f'Top {start_index + 1}-{end_index} Rankings',
            color=discord.Color.gold()
        )

        # Add information about the selected top users to the embedded message
        for i, (user, total_value) in enumerate(selected_users, start=start_index + 1):
            embed.add_field(name=f"{i}. {user}", value=f"Total Value: ${total_value}", inline=True)

        return None, embed, None
                
    if p_message == 'donasi':
        donation_link = 'https://trakteer.id/amoryg/tip?open=true'

        # Create an embedded message for the donation link
        embed = discord.Embed(
            title='Support Amory',
            description='Terima kasih sudah menggunakan botnya! Support Amory mulai dari Rp.1000 melalui Trakteer.',
            color=discord.Color.gold()
        )
        embed.add_field(name='Donate Now', value=f'[Klik disini]({donation_link})')

        return None, embed, None


    if p_message.startswith('chance'):
        parts = p_message.split()

        if len(parts) == 2:
            requested_rarity = parts[1].lower()
        else:
            return "Invalid command format. Use `.chance <common/uncommon/rare/legendary/mythical>`.", None, None

        # Validate the requested rarity
        valid_rarities = ['common', 'uncommon', 'rare', 'legendary', 'mythical']
        if requested_rarity not in valid_rarities:
            return "Invalid rarity. Use `.chance <common/uncommon/rare/legendary/mythical>`.", None, None

        # Create an embedded message for the chance command
        embed = discord.Embed(
            title=f'{requested_rarity.capitalize()} Fruit Rarity and Chance',
            color=discord.Color.green()
        )

        # Add information about the rarity and chance to the embedded message
        for fruit_name, rarity in fruit.fruits_rarity.items():
            if rarity.lower() == requested_rarity:
                embed.add_field(name=f'{fruit_name} - {rarity}', value=f'Chance: {fruit.chance_percentage[rarity.lower()]}%', inline=True)

        return None, embed, None


    if p_message.startswith('inventory'):
        parts = p_message.split()
        if len(parts) == 1:  # .inventory command without specifying a user
            target_user = username
        elif len(parts) == 2:  # .inventory command with a specified user
            target_user = parts[1].lower()
        else:
            return "Invalid command. Please use `.inventory` to see your own inventory or `.inventory <username>` to see another user's inventory.", None, None

        if target_user in data:
            inventory = data[target_user]["inventory"]
            beri = data[target_user].get("beri", 0)
            total_value = calculate_total_value(inventory, beri)

            if not inventory:
                return f"{target_user}'s Inventory is empty or check your current beri with .beri.", None, None

            # Create an embedded message for the inventory
            embed = discord.Embed(
                title=f"{target_user}'s Inventory (Total Value: ${total_value}):\n",
                color=discord.Color.blue()
            )

            for item in inventory:
                item_name = item["name"]
                item_quantity = item.get("quantity", 1)
                embed.add_field(name=f"{item_name} x{item_quantity}", value="", inline=False)

            embed.add_field(name="Current beri : ", value=f"${beri}", inline=False)

            return None, embed, None
        else:
            return f"User tidak dapat ditemukan atau Jangan gunakan tag , gunakan username contoh : .inventory amoryg,Klik profile untuk melihat username", None, None

    if p_message.startswith('beri'):
        parts = p_message.split()

        if len(parts) == 1:  # .belly command without specifying a user
            target_user = username
        elif len(parts) == 2:  # .belly command with a specified user
            target_user = parts[1].lower()
        else:
            return "Invalid command. Please use `.beri` to see your own beri or `.beri <username>` to see another user's beri.", None, None

        if target_user in data:
            target_beri = data[target_user].get("beri", 0)

            # Create an embedded message for the beri
            embed = discord.Embed(
                title=f"{target_user}'s beri",
                description=f"{target_user}'s current beri is: ${target_beri}",
                color=discord.Color.blue()
            )

            return None, embed, None
        else:
            return f"User not found. Please use a valid username.", None, None

    if p_message == 'botinvite':
        invite_link = 'https://discord.com/api/oauth2/authorize?client_id=1170990354812641361&permissions=1084681092160&scope=bot'
        
        invite_embed = discord.Embed(
            title='Invite the Bot',
            description=f'You can invite the bot to your server using the following link:',
            color=discord.Color.blue()
        )
        invite_embed.add_field(name='Invite Link', value=f'[Click here to invite the bot]({invite_link})')

        return None, invite_embed, None
  
    if p_message == 'info':
        # Create an embedded message for the bot commands
        embed = discord.Embed(
            title='Bot Commands',
            description='Here are some available commands (this bot is created by Amory):',
            color=discord.Color.blue()
        )

        embed.add_field(name=f'{bot_prefix}hello', value='Greet the bot', inline=False)
        embed.add_field(name=f'{bot_prefix}register', value='Register username', inline=False)
        embed.add_field(name=f'{bot_prefix}inventory', value='Show user inventory', inline=False)
        embed.add_field(name=f'{bot_prefix}beri', value='Show current beri in inventory', inline=False)
        embed.add_field(name=f'{bot_prefix}roll', value='Roll a random fruit', inline=False)
        embed.add_field(name=f'{bot_prefix}sell', value='Sell fruit to beri', inline=False)
        embed.add_field(name=f'{bot_prefix}donasi', value='Kirim donasi kepada amory mulai dari 1000', inline=False)
        embed.add_field(name=f'{bot_prefix}berigive', value='Give your beri to someone!', inline=False)
        embed.add_field(name=f'{bot_prefix}fruitgive', value='Give your fruit to someone!', inline=False)
        embed.add_field(name=f'{bot_prefix}value', value='Show the value of chosen fruit', inline=False)
        embed.add_field(name=f'{bot_prefix}top', value='Showing User ranking with most beri', inline=False)
        embed.add_field(name=f'{bot_prefix}rank', value='Show your current rank', inline=False)
        embed.add_field(name=f'{bot_prefix}user', value='Show current registered user', inline=False)
        embed.add_field(name=f'{bot_prefix}botinvite', value='Link to invite the bot to your server!', inline=False)

        return None, embed, None
    

    if p_message == 'roll':
        if username in roll_cooldowns and time.time() - roll_cooldowns[username] < ROLL_COOLDOWN:
            remaining_time_seconds = int(ROLL_COOLDOWN - (time.time() - roll_cooldowns[username]))

            minutes, seconds = divmod(remaining_time_seconds, 60)
            return f'{username}, you are on cooldown. Please wait {minutes} minute(s) and {seconds} second(s) before rolling again.', None, None

        random_fruit = fruit.get_random_fruit()

        if random_fruit:
            fruit_name = random_fruit["name"]
            fruit_image_path = fruit.get_fruit_image(random_fruit)

            if fruit_image_path:
                inventory = data.setdefault(username, {"inventory": []})["inventory"]

                fruit_in_inventory = next((item for item in inventory if item["name"] == fruit_name), None)

                if fruit_in_inventory:
                    fruit_in_inventory["quantity"] = fruit_in_inventory.get("quantity", 1) + 1
                    save_user_data(data)

                    roll_cooldowns[username] = time.time()

                    embed = discord.Embed(
                        title=f'{username} rolled another {fruit_name}!',
                        description=f'You now have {fruit_in_inventory["quantity"]} {fruit_name}(s) in your inventory.',
                        color=discord.Color.green()
                    )
                    embed.set_image(url=f'attachment://{fruit_name}.png')

                    return (
                        f'{username} rolled another {fruit_name}! It has been added to your inventory. '
                        f'You now have {fruit_in_inventory["quantity"]} {fruit_name}(s) in your inventory.',
                        embed,
                        fruit_image_path
                    )
                else:
                    inventory.append({"name": fruit_name, "quantity": 1})
                    save_user_data(data)

                    roll_cooldowns[username] = time.time()

                    embed = discord.Embed(
                        title=f'You rolled a {fruit_name}!',
                        description=f'Image of {fruit_name}',
                        color=discord.Color.green()
                    )
                    embed.set_image(url=f'attachment://{fruit_name}.png')

                    return (
                        f'{username} rolled a {fruit_name}! It has been added to your inventory. '
                        f'You now have 1 {fruit_name} in your inventory.',
                        embed,
                        fruit_image_path
                    )

        return 'Image not found for the selected fruit.', None, None

    donation_link = 'https://trakteer.id/amoryg/tip?open=true'

   
    embed = discord.Embed(
        title='Command Tidak dapat ditemukan',
        description='Command yang anda tulis tidak dapat digunakan sekarang, tulis `.info` untuk command yang tersedia',
        color=discord.Color.gold()
    )
    embed.add_field(name='Jangan lupa support Amory dengan donasi di link ini', value=f'[Klik disini]({donation_link})')

    return None, embed, None

    