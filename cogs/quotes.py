import discord
from discord.ext import commands
import asyncio
import sys
import sqlite3
import datetime
from datetime import timezone, tzinfo, timedelta

class quotes(commands.Cog, name='quotes'):
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
        
    @commands.command()
    async def addquote(self, ctx, *, text):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM quotes WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO quotes(guild_id, user_id, quote) VALUES(?,?,?)")
            val = (ctx.guild.id, ctx.author.id, text)
            await ctx.send(f'Your quote has been set to: {text}')
        elif result is not None:
            sql = ('UPDATE main.quotes SET quote = ? WHERE user_id = ?')
            val = (text, ctx.author.id)
            await ctx.send(f'Quote has been updated to : {text}')
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
           
    @commands.command()
    async def quote(self, ctx, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT quote FROM quotes WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('User has no quote')
            else:
                await ctx.send(f"{user.name}'s quote: {result[0]}")
            cursor.close()
            db.close()
        elif user is None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT quote FROM quotes WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('That user has no quote')
            else:
                await ctx.send(f"{ctx.message.author.name}'s quote:  {result[0]}")
            cursor.close()
            db.close()
            
        
def setup(bot):
    bot.add_cog(quotes(bot))
    print('Quotes loaded!')