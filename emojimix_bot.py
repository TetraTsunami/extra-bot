import json
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .embed import simple_embed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SUPPORT_GUILD = int(os.getenv('SUPPORT_GUILD'))
if os.getenv('DEBUG_GUILD'): DEBUG = int(os.getenv('DEBUG_GUILD'))

bot = commands.Bot(command_prefix="c!", debug_guilds=[DEBUG])
bot = discord.Bot() # Create a bot object
  
  
EMOJIROOT = "https://www.gstatic.com/android/keyboard/emojikitchen";
#                                  https://www.gstatic.com/android/keyboard/emojikitchen/20210831/1f41f/1f41f_1f616.png
# Valid url: "u1f41f_u1f616.png": "https://www.gstatic.com/android/keyboard/emojikitchen/20210831/u1f41f/u1f41f_u1f616.png",
# rooturl/date/left/left_right.png

class Emoji():
    def __init__(self, emoji: str) -> None:
        self.emoji = emoji
        self.hex = '{:x}'.format(ord(emoji))
        
def find_combo_date(emoji1: Emoji, emoji2: Emoji):
#     {
#   "2615": [
#     { "leftEmoji": "1f600", "rightEmoji": "2615", "date": "20201001" },
    # open text/emojiData.json to find date
    
    with open("./text/emojiData.json") as f:
        data = json.load(f)
        
        for combo in data[emoji2.hex]:
            if combo["leftEmoji"] == emoji1.hex:
                return combo["date"]    
    raise LookupError("Could not find combo date") 
    
def get_emoji_combo_url(emoji1: Emoji, emoji2: Emoji):
    try:
        date = find_combo_date(emoji1, emoji2)
        return EMOJIROOT + "/" + date + "/u" + emoji1.hex + "/u" + emoji1.hex + "_u" + emoji2.hex + ".png"
    except LookupError:
        date = find_combo_date(emoji2, emoji1) # try the other way around
        return EMOJIROOT + "/" + date + "/u" + emoji2.hex + "/u" + emoji2.hex + "_u" + emoji1.hex + ".png"
    raise LookupError("Invalid emoji combo")
        
class Dropdown(discord.ui.Select):
    def __init__(self, bot, x: int, y: int, options: list, placeholder: str):
        self.bot = bot
        self.pseudoValue = None
        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            options=options,
        )
    async def set_value(self, option: discord.SelectOption):
        """Sets the value of the dropdown to the given option, without activating a callback.
        
        Example:
            # Set the value of the dropdown to a random option
            await item.set_value(random.choice(item.options))
        """
        # we're changin the placeholder to reflect a value!
        self.placeholder = option.label
        self.pseudoValue = option.label

    async def callback(self, interaction: discord.Interaction):
        self.placeholder = self.values[0]
        self.pseudoValue = self.values[0]
        await self.view.select(interaction)
        
class DropdownRandomButton(discord.ui.Button):
    def __init__(self, y: int, label: str = "\u200b", ):
        super().__init__(style=discord.ButtonStyle.primary, row=y)
        # self.view = view
        self.label = "🔀"
        self.y = y
    async def callback(self, interaction: discord.Interaction):
        await self.view.shuffle_items(interaction)
        
        
class DropdownView(discord.ui.View):
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx
        super().__init__()
        
        placeholder = "Choose an emoji"
        options = [
            discord.SelectOption(label="😀"),
            discord.SelectOption(label="😁"),
            discord.SelectOption(label="😂"),
            discord.SelectOption(label="🤣"),
            discord.SelectOption(label="😃"),
            discord.SelectOption(label="😄"),
        ]
                
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.bot, y=0, x=0, options=options, placeholder=placeholder))
        self.add_item(DropdownRandomButton(y=1))
        self.add_item(Dropdown(self.bot, y=2, x=0, options=options, placeholder=placeholder))
    
    async def shuffle_items(self, interaction: discord.Interaction):
        for item in self.children:
            if isinstance(item, discord.ui.Select):
                await item.set_value(random.choice(item.options))
        dropdownValues = [item.pseudoValue for item in self.children if isinstance(item, discord.ui.Select)]
        try:
            get_emoji_combo_url(Emoji(dropdownValues[0]),Emoji(dropdownValues[1]))
            await self.select(interaction)

        except LookupError:
            await self.shuffle_items(interaction)
                    
    async def select(self, interaction: discord.Interaction):
        dropdownValues = [item.pseudoValue for item in self.children if isinstance(item, discord.ui.Select)]
        if dropdownValues[0] and dropdownValues[1]:
            await interaction.response.edit_message(embed=simple_embed(title="Emoji Kitchen", icon="🥺", imageUrl=get_emoji_combo_url(Emoji(dropdownValues[0]),Emoji(dropdownValues[1])), ctx=self.ctx), view=self)
        pass

@bot.slash_command()
async def emojimix(ctx):
    view = DropdownView(bot, ctx)
    await ctx.respond(embed=simple_embed(title="Emoji Kitchen", icon="🥺", body="Select two emoji to mix", ctx=ctx), view=view)
    
bot.run(TOKEN) # Run the bot

