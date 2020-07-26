import discord
from discord.ext import commands
import sqlite3
import sys
import asyncio
import math
import random
from random import randrange



class lvl(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
    @commands.Cog.listener()
    async def on_message(self, message):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO levels(guild_id, user_id, exp, lvl) VALUES(?,?,?,?)")
            val = (message.guild.id, message.author.id, 2, 0)
            cursor.execute(sql, val)
            db.commit()
        else: 
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
            result1 = cursor.fetchone()
            exp = int(result1[1])
            sql =("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
            val = (exp + randrange(8), str(message.guild.id), str(message.author.id))
            cursor.execute(sql, val)
            db.commit()
            
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
            result2 = cursor.fetchone()
            
            xp_start = int(result2[1])
            lvl_start = int(result2[2])
            xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
            if xp_end < xp_start:
                await message.channel.send(f'{message.author.mention} has leveled up to level {lvl_start + 1}')
                sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? and user_id = ?")
                val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (0, str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
                
    @commands.command()
    async def rank(self, ctx, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('That user is not yet ranked')
            else:
                embed = discord.Embed(colour=0xEAFF15, title=f"User Info - {user.name}")
                embed.set_footer(text=f"Requested by {ctx.author}")
                embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name="Level:", value= str(result[2]))
                embed.add_field(name="EXP:", value= str(result[1]))
                await ctx.send(embed=embed)
            cursor.close()
            db.close()
        elif user is None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('That user is not yet ranked')
            else:
                embed = discord.Embed(colour=0xEAFF15, title=f"User Info - {ctx.message.author.name}")
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                embed.set_footer(text=f"Requested by {ctx.author}")
                embed.add_field(name="Level:", value= str(result[2]))
                embed.add_field(name="EXP:", value= str(result[1]))
                await ctx.send(embed=embed)
            cursor.close()
            db.close()
            
def setup(bot):
    bot.add_cog(lvl(bot))
    print('level system Cog Loaded')
        