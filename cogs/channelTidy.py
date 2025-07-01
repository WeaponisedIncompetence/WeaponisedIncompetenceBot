import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
import discord.utils
from datetime import datetime, timedelta


class channelControl(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self,message):
        channel = message.channel
        author = message.author
        if channel.name == "trial-request":
            if "WeaponisedIncompetence" in author.name:
                timePosted = message.created_at
                timedOut = timePosted + timedelta(days=2)
                if timedOut < datetime.now():
                    await message.delete()

    
    
def setup(bot):
    bot.add_cog(channelControl(bot))
