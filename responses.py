import random
import json
import os


def handle_response(message, username=None, user_id=None) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"

    if p_message == "we lit":
        return "on god homie, for real."

    if p_message == "shut up":
        return "say less."

    if p_message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        return "`This is a help message.`"
    if p_message == "!forceshowdata":
        product_data = read_product_data()
        # Format JSON with indent and wrap it in a code block
        formatted_json = json.dumps(product_data, indent=4)
        return f"```json\n{formatted_json}\n```"

    if p_message.startswith("!config threshold "):
        try:
            threshold = float(p_message.split(" ", 3)[2])
            thresholds = read_thresholds()
            thresholds[username] = {
                "id": user_id,
                "threshold": threshold,
            }
            write_thresholds(thresholds)
            return f"Threshold for {username} has been set to {threshold}"
        except:
            return "Could not set threshold. Please use the format `!config threshold <number>`"


def read_product_data():
    with open("product-data.json", "r") as file:
        data = json.load(file)
    return data


def read_thresholds():
    if os.path.exists("thresholds.json"):
        with open("thresholds.json", "r") as file:
            return json.load(file)
    else:
        return {}


def write_thresholds(thresholds):
    with open("thresholds.json", "w") as file:
        json.dump(thresholds, file)


def parse_price(price_str):
    price_str = price_str.replace("$", "").strip()
    return float(price_str)
