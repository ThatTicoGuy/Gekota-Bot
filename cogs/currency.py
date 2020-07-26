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

class currency(commands.Cog, name='currency'):
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    
    #When user types they gain 0-5 exp
    @commands.Cog.listener()
    async def on_message(self, message):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM eco WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main.eco(guild_id, user_id, exp) VALUES(?,?,?)")
            val = (message.guild.id, message.author.id, 2)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else: 
            cursor.execute(f"SELECT user_id, exp FROM main.eco WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
            result1 = cursor.fetchone()
            exp = int(result1[1])
            sql =("UPDATE main.eco SET exp = ? WHERE guild_id = ? and user_id = ?")
            val = (exp + randrange(6), str(message.guild.id), str(message.author.id))
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        
        
            
    #The rest of this spaghetti code is just in the group color
    @commands.group(invoke_without_command=True)
    async def color(self, ctx):
        await ctx.send('Current colors that you can buy: Red, Pink, Yellow, Green, Blue')
        
    #Buy Color commands, not hard coded anymore but poorly coded    
    @color.command()
    async def buy(self, ctx, roles):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT exp FROM main.eco WHERE user_id = '{ctx.message.author.id}' and guild_id = '{ctx.message.author.guild.id}'")
        result = cursor.fetchone()
        exp = int(result[0])
        cursor.execute(f"SELECT role1, role2, role3, role4, role5, role6, role7, role8 FROM SetRoles WHERE guild_id = '{ctx.message.author.guild.id}'")
        result = cursor.fetchone()
        role1, role2, role3, role4, role5, role6, role7, role8 = str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]), str(result[7])
        member = ctx.message.author
        message = ctx.message.author
        names1 = [role1, role2, role3, role4, role5, role6, role7, role8]
        if exp >= 3000:
            user = discord.Member
            hasrole = discord.utils.find(lambda r: r.name == roles, ctx.message.author.roles)
            x = None
            if hasrole:
                await ctx.send('You already own that role')
            elif roles == names1[0] or roles == names1[1] or roles == names1[2] or roles == names1[3] or roles == names1[4] or roles == names1[5] or roles == names1[6] or roles == names1[7]: 
                if roles == names1[0]:
                    x = '1'
                elif roles == names1[1]:
                    x = '2'
                elif roles == names1[2]:
                    x = '3'
                elif roles == names1[3]:
                    x = '4'
                elif roles == names1[4]:
                    x = '5'
                elif roles == names1[5]:
                    x = '6'
                elif roles == names1[6]:
                    x = '7'
                elif roles == names1[7]:
                    x = '8'
                else:
                    ctx.send('what the hell did you do')
                await ctx.send(f"Role bought: `{roles}` do ^color setrole '{roles}' to equip the role")
                sql = (f'UPDATE main.eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = (exp - 3000, str(ctx.message.author.guild.id), str(ctx.message.author.id))
                cursor.execute(sql, val)
                cursor.execute(f'SELECT guild_id FROM customroles WHERE guild_id = {ctx.guild.id} and user_id = {ctx.message.author.id}')
                result2 = cursor.fetchone()
                if result2 is None:
                    cursor.execute("INSERT INTO customroles("+ 'role' + x + ", guild_id, user_id) VALUES (?,?,?)", (roles, ctx.guild.id, ctx.message.author.id))
                else:
                    cursor.execute(f"UPDATE customroles SET "+ 'role' + x +" = ? WHERE guild_id = ? and user_id = ?", (roles, str(ctx.message.author.guild.id), str(ctx.message.author.id)))
                db.commit()
            else:
                await ctx.send('Please select a color')
                
        else:
            await ctx.send('Cannot make the purchase')
        db.commit()
        cursor.close()
        db.close()
       

    #Set role to a specific color role thanks Nick for helping out
    
    @color.command()
    async def setrole(self, ctx, rolename):
        for x in range(7):
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT role1, role2, role3, role4, role5, role6, role7, role8 FROM customroles WHERE user_id = '{ctx.message.author.id}' and guild_id = '{ctx.message.author.guild.id}'")
            user_id = ctx.author.id
            guild_id = ctx.guild.id
            mroles = dict([[r.name, r] for r in ctx.author.roles])
            original_len = list(mroles.keys())
            mroles = dict([[r.name, r] for r in ctx.author.roles])
            cursor.execute(f"SELECT * FROM customroles WHERE  user_id = '{ctx.message.author.id}' and guild_id = '{ctx.message.author.guild.id}'")
            sqlret = cursor.fetchone()
            if rolename.lower() in [mroles[r].name.lower() for r in mroles]:
                    await ctx.send('You already have this role equiped')
                    break
            if not sqlret:
                await ctx.send("Error Fetching Roles")
                break
            if not any(sqlret):
                await ctx.send("You do not have any roles")
                return
            if rolename not in sqlret:
                await ctx.send("You do not own this role")
                return
            try:
                groles = dict([[r.name.lower(), r] for r in ctx.guild.roles])
                if rolename in groles:
                    mroles[groles[rolename].id] = groles[rolename]
            except Exception as e:
                continue
            if original_len != list(mroles.keys()):
                newroles = [mroles[r] for r in mroles]
                await ctx.author.edit(roles=newroles)
                await ctx.send("Assigned new roles or removed old roles.")
                return
            await ctx.send("User has not changed roles.")
            break
        db.commit()
        cursor.close()
        db.close()
   
        
    #See amount of money of user
    @color.command()
    async def eco(self, ctx, user:discord.User=None):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT exp FROM main.eco WHERE user_id = '{ctx.message.author.id}' and guild_id = '{ctx.message.author.guild.id}'")
        result = cursor.fetchone()
        await ctx.send('User has no balance') if result is None else await ctx.send(f"{ctx.message.author.name}'s current money:  `{result[0]}`")
        db.commit()
        cursor.close()
        db.close()
       
        
    #Gamble Machine :)
    @color.command()
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
                
    #Set roles in different guilds MAX 8    
    @color.command()
    async def roleadd(self, ctx, text, *, roles):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT guild_id FROM SetRoles WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if text == '1' or text == '2' or text == '3' or text == '4' or text == '5' or text == '6' or text == '7' or text == '8':
                if result is None:
                    keyword = {text}
                    cursor.execute("INSERT INTO SetRoles("+ 'role' + str(text) + ", guild_id) VALUES (?,?)", (roles, ctx.guild.id))
                    await ctx.send(f"Role '{text}' set to: `{roles}`")
                elif result is not None:
                    cursor.execute("UPDATE SetRoles SET "+ 'role' + str(text) +" = ? WHERE guild_id = ?", (roles, ctx.guild.id))
                    await ctx.send(f"Role '{text}' set to: `{roles}`") 
            db.commit()
            cursor.close()
            db.close() 
            
    @color.command()
    async def set(self, ctx, roles):
         db = sqlite3.connect('main.sqlite')
         cursor = db.cursor()
    
def setup(bot):
    bot.add_cog(currency(bot))
    print('Currency Loaded!')