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

    elif p_message.startswith("!help"):
        return (
            "**Avast ye! Here be the commands ye can use:**\n\n"
            "`!config threshold [amount]` - Set yer doubloon limit. If a treasure costs less than this, we'll alert ye.\n"
            "`!config url [url]` - Add a map to yer list. We'll keep an eye on the treasures at this location.\n"
            "`!config clear` - Remove all yer maps and doubloon limit.\n"
            "`!showconfig` - See all yer maps and doubloon limit.\n"
            "`!help` - Display this list of commands.\n"
        )

    if p_message == "!forceshowdata":
        product_data = read_product_data()
        # Format JSON with indent and wrap it in a code block
        formatted_json = json.dumps(product_data, indent=4)
        return f"```json\n{formatted_json}\n```"

    if p_message.startswith("!config threshold "):
        try:
            threshold = float(p_message.split(" ", 3)[2])
            thresholds = read_thresholds()
            if username in thresholds:
                thresholds[username]["threshold"] = threshold
            else:
                thresholds[username] = {
                    "id": user_id,
                    "threshold": threshold,
                    "urls": [],
                }
            write_thresholds(thresholds)
            return f"Threshold for {username} has been set to {threshold}"
        except:
            return "Could not set threshold. Please use the format `!config threshold <number>`"

    if p_message.startswith("!config url "):
        url = message.split(" ", 2)[2]
        if not url.startswith(("http://", "https://")):
            return "Arr, ye need to start yer URL with 'http://' or 'https://', matey."

        if not any(
            website in url
            for website in ["g2a.com", "instant-gaming.com", "store.steampowered.com"]
        ):
            return "Yarr, we only be supportin' URLs from 'g2a.com', 'instant-gaming.com', or 'store.steampowered.com', matey."

        thresholds = read_thresholds()
        if username in thresholds:
            user_config = thresholds[username]
            if "urls" in user_config:
                if url in user_config["urls"]:
                    return "Arr, this URL be already in yer list, matey."
                else:
                    user_config["urls"].append(url)
            else:
                user_config["urls"] = [url]
        else:
            thresholds[username] = {
                "id": user_id,
                "threshold": None,
                "urls": [url],
            }
        write_thresholds(thresholds)
        return f"Arr! We've added this here map <{url}> for ye, {username}!"

    if p_message == "!showconfig":
        thresholds = read_thresholds()
        if username in thresholds:
            user_config = thresholds[username]
            threshold = user_config.get("threshold", "No bounty set")
            urls = (
                "\n".join([f"<{url}>" for url in user_config.get("urls", [])])
                or "No maps set"
            )
            return f"Here's yer pirate's code, **{username}**:\n**Bounty:** {threshold}\n**Maps:**\n{urls}"
        else:
            return "Arr! We've got no code for ye, matey."

    if p_message.startswith("!config clear"):
        thresholds = read_thresholds()
        if username in thresholds:
            thresholds[username] = {
                "id": user_id,
            }
            write_thresholds(thresholds)
            return f"Arr! We've cleared all yer maps and doubloon limit, {username}!"
        else:
            return (
                f"Arr! We couldn't find any maps or doubloon limit for ye, {username}!"
            )


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
    # Remove $ and € symbols and replace comma with period
    price_str = price_str.replace("$", "").replace("€", "").replace(",", ".").strip()

    # Try to extract the first float value in the string
    try:
        price = float(price_str)
        return price
    except ValueError:
        return None
