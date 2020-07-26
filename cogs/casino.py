import discord
from discord.ext import commands
import asyncio
import sys
import sqlite3
import time
import datetime
import math
import random
from random import randrange
from discord.utils import get

class casino(commands.Cog, name='currency'):
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
      
    @commands.group(invoke_without_command=True)
    async def casino(self, ctx):
        await ctx.send('Current colors that you can buy: Red, Pink, Yellow, Green, Blue')  
    @casino.command()
    async def roll(self, ctx, *, text):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT exp FROM eco WHERE user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()
        exp = int(result[0])
        oldexp = int(result[0])
        amount = int(text)
        if amount >= exp or amount >= 500:
            await ctx.send('Please input a correct amount, must be less than 500')
        else:
            WORDS = (':yellow_square:', ':apple:', ':frog:', ':banana:', ':pear:')
            chance1, chance2, chance3 = random.choice(WORDS), random.choice(WORDS), random.choice(WORDS)
            embed = discord.Embed(colour=0xDFBDB5, description=':frog: **Gekota Slot** :frog:')
            embed.add_field(name="Slot 1:", value=chance1)
            embed.add_field(name="Slot 2:", value=chance2)
            embed.add_field(name="Slot 3:", value=chance3)
            await ctx.send('Rolling...')
            await ctx.send(embed=embed)
            if chance1 == WORDS[2] and chance2 == WORDS[2] and chance3 == WORDS[2]:
                await ctx.send('Jackpot! `x 5`')
                sql = (f'UPDATE eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = ((exp - amount) + (amount * 5), str(ctx.message.author.guild.id), str(ctx.message.author.id))
            elif chance1 == chance2 and chance1 == chance3:
                await ctx.send('You have won `x 3`')
                sql = (f'UPDATE eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = ((exp - amount) + (amount * 3), str(ctx.message.author.guild.id), str(ctx.message.author.id))
            elif chance1 == chance2 or chance1 == chance3 or chance3 == chance2:
                await ctx.send('you have won `x 2`')
                sql = (f'UPDATE eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = ((exp - amount) + (amount * 2), str(ctx.message.author.guild.id), str(ctx.message.author.id))
            else:
                sql = (f'UPDATE eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = (exp - amount, str(ctx.message.author.guild.id), str(ctx.message.author.id))
                await ctx.send(f"Amount lost: `'{amount}'`")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        
def setup(bot):
    bot.add_cog(casino(bot))
    print('Currency Loaded!')