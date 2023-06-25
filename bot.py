<<<<<<< HEAD
import discord
from discord.ext import tasks
import responses
from dotenv import load_dotenv
import os
import json

load_dotenv()


async def send_message(message, user_message, is_private):
    try:
        username = str(message.author)
        user_id = message.author.id
        response = responses.handle_response(user_message, username, user_id)
        await message.author.send(
            response
        ) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


async def send_product_info(user, products):
    message_content = f"Ahoy {user.name},\n\n"
    message_content += (
        "We've spotted some treasures that meets yer price alert criteria:\n\n"
    )
    for product_info in products:
        product_name = product_info["product"]
        product_price = product_info["price"]
        product_url = product_info["url"]
        # Wrap the URL with angle brackets to disable the link preview
        message_content += (
            f"**Treasure Name:** {product_name}\n"
            f"**Doubloons Needed:** {product_price}\n"
            f"**Map (URL):** <{product_url}>\n\n"
        )
    message_content += "If ye be interested, cast yer eyes on the maps above. Thank ye for sailin' with us!"
    await user.send(content=message_content)


def run_discord_bot():
    TOKEN = os.getenv("TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.typing = False
    intents.presences = False

    client = discord.Client(intents=intents)

    @tasks.loop(hours=24)  # This will run the task every 24 hours
    async def check_product_prices():
        print("Checking product prices...")
        thresholds = responses.read_thresholds()
        product_data = responses.read_product_data()
        for username, user_info in thresholds.items():
            user_id = user_info["id"]
            threshold = user_info.get("threshold", float("inf"))
            user_urls = user_info.get("urls", [])
            user = await client.fetch_user(user_id)  # Get the User object for this user
            matching_products = []
            for product in product_data:
                # Check if the product URL matches one of the user's URLs
                if product["url"] not in user_urls:
                    continue

                price = responses.parse_price(product["price"])
                if price is None:
                    product["price"] = "Could not determine price"
                    matching_products.append(product)
                elif price <= threshold:
                    matching_products.append(product)
            if matching_products:
                await send_product_info(user, matching_products)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")
        check_product_prices.start()

    @client.event
    async def on_message(message):
        print(f"Message type: {message.type}")
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")
        print(f"Message type: {type(message.content)}")
        print(f"Raw message object: {message}")

        if user_message and user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
=======
import discord
from discord.ext import tasks
import responses
from dotenv import load_dotenv
import os
import json

load_dotenv()


async def send_message(message, user_message, is_private):
    try:
        username = str(message.author)
        user_id = message.author.id
        response = responses.handle_response(user_message, username, user_id)
        await message.author.send(
            response
        ) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


async def send_product_info(user, products):
    message_content = f"Ahoy {user.name},\n\n"
    message_content += (
        "We've spotted some treasures that meets yer price alert criteria:\n\n"
    )
    for product_info in products:
        product_name = product_info["product"]
        product_price = product_info["price"]
        product_url = product_info["url"]
        # Wrap the URL with angle brackets to disable the link preview
        message_content += (
            f"**Treasure Name:** {product_name}\n"
            f"**Doubloons Needed:** {product_price}\n"
            f"**Map (URL):** <{product_url}>\n\n"
        )
    message_content += "If ye be interested, cast yer eyes on the maps above. Thank ye for sailin' with us!"
    await user.send(content=message_content)


def run_discord_bot():
    TOKEN = os.getenv("TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.typing = False
    intents.presences = False

    client = discord.Client(intents=intents)

    @tasks.loop(hours=24)  # This will run the task every 24 hours
    async def check_product_prices():
        print("Checking product prices...")
        thresholds = responses.read_thresholds()
        product_data = responses.read_product_data()
        for username, user_info in thresholds.items():
            user_id = user_info["id"]
            threshold = user_info.get("threshold", float("inf"))
            user_urls = user_info.get("urls", [])
            user = await client.fetch_user(user_id)  # Get the User object for this user
            matching_products = []
            for product in product_data:
                # Check if the product URL matches one of the user's URLs
                if product["url"] not in user_urls:
                    continue

                price = responses.parse_price(product["price"])
                if price is None:
                    product["price"] = "Could not determine price"
                    matching_products.append(product)
                elif price <= threshold:
                    matching_products.append(product)
            if matching_products:
                await send_product_info(user, matching_products)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")
        check_product_prices.start()

    @client.event
    async def on_message(message):
        print(f"Message type: {message.type}")
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")
        print(f"Message type: {type(message.content)}")
        print(f"Raw message object: {message}")

        if user_message and user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
>>>>>>> abac259843d2efb38b26b44b3495af7629246b1b
