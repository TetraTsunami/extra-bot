import os
import re

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SUPPORT_GUILD = int(os.getenv('SUPPORT_GUILD'))
if os.getenv('DEBUG_GUILD'): DEBUG = int(os.getenv('DEBUG_GUILD'))

bot = commands.Bot(command_prefix="c!", debug_guilds=[DEBUG])
bot = discord.Bot() # Create a bot object


class KeypadView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
        keypad = [
            [1,2,3],
            [4,5,6],
            [7,8,9],
            ["*",0,"#"]
        ]
        
        for y in range(4):
            for x in range(3):
                self.add_item(KeypadButton(x, y, keypad[y][x]))
                
class KeypadButton(discord.ui.Button):
    def __init__(self, x: int, y: int, label: str = "\u200b", ):
        super().__init__(style=discord.ButtonStyle.secondary, label=label, row=y)
        self.label = label
        self.x = x
        self.y = y
    async def callback(self, interaction: discord.Interaction):
        original_message = interaction.message
        original_message_content = re.sub("```", "", original_message.content)
        await interaction.response.edit_message(content=f"```{original_message_content}{self.label}```")

@bot.slash_command() # Create a slash command
async def keypad(ctx):
    view = KeypadView(bot)
    await ctx.respond("``` ```", view=view)
    
bot.run(TOKEN) # Run the bot

