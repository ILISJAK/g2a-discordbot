import random
import json


def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"
    
    if p_message == "we lit":
        return "on god homie, for real."

    if p_message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        return "`This is a help message.`"
    if p_message == "!productdata":
        product_data = read_product_data()
        # Format JSON with indent and wrap it in a code block
        formatted_json = json.dumps(product_data, indent=4)
        return f"```json\n{formatted_json}\n```"

    return "I didn't understand that command."


def read_product_data():
    with open("product-data.json", "r") as file:
        data = json.load(file)
    return data
