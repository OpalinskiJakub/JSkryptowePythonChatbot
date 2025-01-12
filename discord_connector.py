import discord
from discord import Intents
import requests
import json

DISCORD_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

class RestaurantBot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} and ready to respond!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        payload = {"sender": str(message.author.id), "message": message.content}
        headers = {"Content-Type": "application/json"}
        response = requests.post(RASA_SERVER_URL, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            rasa_responses = response.json()
            for rasa_response in rasa_responses:
                if rasa_response.get("text"):
                    await message.channel.send(rasa_response.get("text"))
        else:
            await message.channel.send("Sorry, I couldn't process your request.")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = RestaurantBot(intents=intents)
client.run(DISCORD_TOKEN)

