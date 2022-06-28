import discord
from discord.ext import commands
# Embed utility functions from Cricket

def simple_embed(title='Command Embed', icon='', body='', imageUrl='', imageFile: discord.File = None, ctx: discord.ApplicationContext = None):
    """Generates a simple embed with a title, icon, body, and image

    Args:
        title (str, optional): Title of the embed. Defaults to 'Command Embed'.
        icon (str, optional): Emoji to place before the title. Defaults to no icon.
        body (str, optional): The body of the embed. Intended to be used as a status or output for commands. Defaults to no body.
        imageUrl (str, optional): Image URL to place in the embed. Defaults to ''.
        imageUrl (discord.File, optional): Image file to place in the embed. Defaults to 'None'.
        ctx (discord.ApplicationContext, optional): Ctx of the command, used to populate a rich footer. Defaults to 'None'.

    Returns:
        _type_: _description_
    """    
    EMOJI_KEY = {
        'Success':'✅',
        'Warning':'⚠️',
        'Failure':'❌',
        'YouTube':'<:youtubeicon:884155771556859984>',
        'Twitch':'<:twitchicon:887868334979317801>',
        'Discord':'<:discordicon:887868333716807680>',
        'Smash':'<:smashicon:895839672956239882>',
        'Minecraft':'<:GrassBlock:924075881562009640>'
              }
    if icon in EMOJI_KEY:
        emoji = EMOJI_KEY[icon]
    else: 
        emoji = icon
        
    STATUS_KEY = {
        'idk':'❌ Something broke somewhere, try again later',
        'Permissions':'❌ I don\'t have permission to do that :(',
        'Length':'❌ Please don\'t paste the entire Bee Movie script, it\'s much too long',
        'NotFound':'❌ I couldn\'t find what you\'re looking for, sorry'
              }
    embed = discord.Embed(color=0xc84268)
    if emoji:
        embed.title = f'{emoji} {title}'
    else:
        embed.title = title
    if body:
        if body in STATUS_KEY:
            description = STATUS_KEY[body]
        else: 
            description = body
        embed.description = description
    if imageUrl:
        embed.set_image(url=imageUrl)
    elif imageFile:
        embed.set_image(url=f"attachment://{imageFile.filename}")
    if ctx:
      embed.set_footer(text=f"/{ctx.command} | Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
    return embed

class LinkButton(discord.ui.View):
    def __init__(self, ctx: commands.Context, buttons: dict, timeout: int = None):
        """A View that displays buttons that link to a URLs.
        
        Usage (setting message is unneccessary if you don't want to disable the link):
            view = LinkButton(ctx, timeout=None, buttons={"Discord": "https://discord.com", "GitHub": "https://github.com"})
            message = await ctx.respond("This is a button!", view=view)
            view.message = message
            
        Args:
            ctx (commands.Context)
            buttons (dict): A dictionary of {label: url} to display as buttons.
            timeout (int): The amount of time to wait before disabling the buttons. Defaults to None.
        """
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.message: discord.Message = None
        for label in buttons:
            self.add_item(discord.ui.Button(label=label, style=discord.ButtonStyle.link, url=buttons[label]))

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit_original_message(view=self)
