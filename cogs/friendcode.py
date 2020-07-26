import discord
from discord.ext import commands
import asyncio
import sys
import sqlite3
import datetime
from datetime import timezone, tzinfo, timedelta

class friendcode(commands.Cog, name='friendcode'):
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
        
    @commands.command()
    async def addcode(self, ctx, *, text):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM main.friendcode WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO friendcode(guild_id, user_id, friendcode) VALUES(?,?,?)")
            val = (ctx.guild.id, ctx.author.id, text)
            await ctx.send(f'Your friend code has been set to: {text}')
        elif result is not None:
            sql = ('UPDATE main.friendcode SET friendcode = ? WHERE user_id = ?')
            val = (text, ctx.author.id)
            await ctx.send(f'Your friend code has been updated to: {text}')
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
           
        
           

            
    @commands.command()
    async def code(self, ctx, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT friendcode FROM friendcode WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('User has not added friend code')
            else:
                embed = discord.Embed(colour=0xEAFF15, title=f"Nintendo Switch Friend Code: {user.name}")
                embed.set_footer(text=f"Requested by {ctx.author}")
                embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name="Friend Code:", value= str(result[0]))
                await ctx.send(embed=embed)
            cursor.close()
            db.close()
        elif user is None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT friendcode FROM friendcode WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('User has not added switch code')
            else:
                embed = discord.Embed(colour=0xEAFF15, title=f"Nintendo Switch Friend Code:  {ctx.message.author.name}")
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                embed.set_footer(text=f"Requested by {ctx.author}")
                embed.add_field(name="FriendCode:", value= str(result[0]))
                await ctx.send(embed=embed)
            cursor.close()
            db.close()
            
        
def setup(bot):
    bot.add_cog(friendcode(bot))
    print('Friendcode Loaded!')