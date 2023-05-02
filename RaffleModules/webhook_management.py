import requests

def size_entry_webhook(raffle_name, email, size, image, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Size? Launches Raffle Entered",
        "color": None,
        "fields": [
            {
            "name": "Name",
            "value": raffle_name
            },
            {
            "name": "Email",
            "value": f"||{email}||"
            },
            {
            "name": "Size",
            "value": size
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": image
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=discord_webhook)

def size_accgen_webhook(email, password, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Size? Launches Account Generated",
        "color": None,
        "fields": [
            {
            "name": "Email",
            "value": email
            },
            {
            "name": "Password",
            "value": f"||{password}||"
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=discord_webhook)

def size_winchecker_webhook(title, option_size, image, orderstatus, addressline1, addressline2, postcode, email, password, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Size? Launches Win Logged",
        "color": None,
        "fields": [
            {
            "name": "Name",
            "value": title
            },
            {
            "name": "Email",
            "value": email,
            "inline": True
            },
            {
            "name": "Password",
            "value": f"||{password}||",
            "inline": True
            },
            {
            "name": "Size",
            "value": option_size
            },
            {
            "name": "Address Line 1",
            "value": f"||{addressline1}||",
            "inline": True
            },
            {
            "name": "Address Line 2",
            "value": f"||{addressline2}||",
            "inline": True
            },
            {
            "name": "Postcode",
            "value": f"||{postcode}||",
            "inline": True
            },
            {
            "name": "Order Status",
            "value": orderstatus
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": image
        }
        }
    ],
    "attachments": []
    }

    requests.post(webhook, json=discord_webhook)

def footpatrol_entry_webhook(raffle_name, email, size, image, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Footpatrol Launches Raffle Entered",
        "color": None,
        "fields": [
            {
            "name": "Name",
            "value": raffle_name
            },
            {
            "name": "Email",
            "value": f"||{email}||"
            },
            {
            "name": "Size",
            "value": size
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": image
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=discord_webhook)

def footpatrol_accgen_webhook(email, password, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Footpatrol Launches Account Generated",
        "color": None,
        "fields": [
            {
            "name": "Email",
            "value": email
            },
            {
            "name": "Password",
            "value": f"||{password}||"
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=discord_webhook)

def footpatrol_winchecker_webhook(title, option_size, image, orderstatus, addressline1, addressline2, postcode, email, password, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Footpatrol Launches Win Logged",
        "color": None,
        "fields": [
            {
            "name": "Name",
            "value": title
            },
            {
            "name": "Email",
            "value": email,
            "inline": True
            },
            {
            "name": "Password",
            "value": f"||{password}||",
            "inline": True
            },
            {
            "name": "Size",
            "value": option_size
            },
            {
            "name": "Address Line 1",
            "value": f"||{addressline1}||",
            "inline": True
            },
            {
            "name": "Address Line 2",
            "value": f"||{addressline2}||",
            "inline": True
            },
            {
            "name": "Postcode",
            "value": f"||{postcode}||",
            "inline": True
            },
            {
            "name": "Order Status",
            "value": orderstatus
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": image
        }
        }
    ],
    "attachments": []
    }

    requests.post(webhook, json=discord_webhook)


def hipstore_entry_webhook(raffle_name, email, size, image, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Hipstore Launches Raffle Entered",
        "color": None,
        "fields": [
            {
            "name": "Name",
            "value": raffle_name
            },
            {
            "name": "Email",
            "value": f"||{email}||"
            },
            {
            "name": "Size",
            "value": size
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": image
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=discord_webhook)

def hipstore_accgen_webhook(email, password, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Hipstore Launches Account Generated",
        "color": None,
        "fields": [
            {
            "name": "Email",
            "value": email
            },
            {
            "name": "Password",
            "value": f"||{password}||"
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=discord_webhook)

def hipstore_winchecker_webhook(title, option_size, image, orderstatus, addressline1, addressline2, postcode, email, password, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Hipstore Launches Win Logged",
        "color": None,
        "fields": [
            {
            "name": "Name",
            "value": title
            },
            {
            "name": "Email",
            "value": email,
            "inline": True
            },
            {
            "name": "Password",
            "value": f"||{password}||",
            "inline": True
            },
            {
            "name": "Size",
            "value": option_size
            },
            {
            "name": "Address Line 1",
            "value": f"||{addressline1}||",
            "inline": True
            },
            {
            "name": "Address Line 2",
            "value": f"||{addressline2}||",
            "inline": True
            },
            {
            "name": "Postcode",
            "value": f"||{postcode}||",
            "inline": True
            },
            {
            "name": "Order Status",
            "value": orderstatus
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": image
        }
        }
    ],
    "attachments": []
    }

    requests.post(webhook, json=discord_webhook)

def afew_entry_webhook(raffle_name, email, size, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Afew Raffle Entered",
        "color": None,
        "fields": [
            {
            "name": "Name",
            "value": raffle_name
            },
            {
            "name": "Email",
            "value": f"||{email}||"
            },
            {
            "name": "Size",
            "value": size
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=discord_webhook)

def flatspot_entry_webhook(raffle_name, email, size, webhook):

    discord_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Flatspot Raffle Entered",
        "color": None,
        "fields": [
            {
            "name": "Name",
            "value": raffle_name
            },
            {
            "name": "Email",
            "value": f"||{email}||"
            },
            {
            "name": "Size",
            "value": size
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=discord_webhook)

def astro_logs(mode, site):
    data = {
    "content": None,
    "embeds": [
        {
        "title": mode,
        "color": None,
        "fields": [
            {
            "name": "Site",
            "value": site
            }
        ],
        "footer": {
            "text": "Powered by Nocto",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        }
        }
    ],
    "attachments": []
    }
    requests.post("https://discord.com/api/webhooks/1049060318153805884/8U3E7ecsiWv6hZKQBNCGZyBG5UQyi3FAwNs6nnPARxOAuEgTrgQ2ibTHFOFfKpBaYRGL", json=data)