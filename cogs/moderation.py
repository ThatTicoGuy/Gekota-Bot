import discord
from discord.ext import commands
import asyncio
import sys
import sqlite3
import datetime
from datetime import timezone, tzinfo, timedelta

class moderationCog(commands.Cog, name='moderation'):
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
    @commands.command()
    async def clear(self,ctx,*, number: int=None):
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                if number is None:
                    await ctx.send('Please put a number')
                else:
                    deleted = await ctx.message.channel.purge(limit=number)
            except:
                await ctx.send('Cannot purge a message')
                    
        else:
            await ctx.send('You do not have perms')
                
    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM main.moderation WHERE guild_id = {user.guild.id}')
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f'SELECT msg FROM main.moderation WHERE guild_id = {user.guild.id}')
            result1 = cursor.fetchone()
            mention = user.mention
            guild = user.guild
            currenttime = datetime.datetime.now()
            if user.guild_permissions.manage_messages:
                await ctx.send('Cannot kick this user')
            elif ctx.message.author.guild_permissions.kick_members:
                if reason is None:
                    await ctx.guild.kick(user=user, reason='none')
                    embed = discord.Embed(colour=0xF26E00, description=str(result1[0]).format(mention=mention, user=user, guild=guild, reason=reason))
                    embed.set_thumbnail(url=f"{user.avatar_url}")
                    embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar_url}")
                    embed.set_footer(text=f"{currenttime}")
            
                    channel = self.bot.get_channel(id=int(result[0]))
                    await channel.send(embed=embed)
                else:
                    await ctx.guild.kick(user=user, reason=reason)
                    embed = discord.Embed(colour=0xF26E00, description=str(result1[0]).format(mention=mention, user=user, guild=guild, reason=reason))
                    embed.set_thumbnail(url=f"{user.avatar_url}")
                    embed.set_author(name=f"Staff: {ctx.author}")
                    embed.set_footer(text=f"{currenttime}")
                    
                    
                    channel = self.bot.get_channel(id=int(result[0]))
                    
                    await channel.send(embed=embed)
                    
            else:
                await ctx.send('You cannot do this action')
            
            
    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM main.moderation WHERE guild_id = {user.guild.id}')
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f'SELECT msg1 FROM main.moderation WHERE guild_id = {user.guild.id}')
            result1 = cursor.fetchone()
            mention = user.mention
            guild = user.guild
            currenttime = datetime.datetime.now()
            if user.guild_permissions.manage_messages:
                await ctx.send('Cannot ban this user')
            elif ctx.message.author.guild_permissions.ban_members:
                if reason is None:
                    await ctx.guild.ban(user=user, reason='none')
                    embed = discord.Embed(colour=0x651111, description=str(result1[0]).format(mention=mention, user=user, guild=guild, reason=reason))
                    embed.set_thumbnail(url=f"{user.avatar_url}")
                    embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar_url}")
                    embed.set_footer(text=f"{currenttime}")
            
                    channel = self.bot.get_channel(id=int(result[0]))
                    await channel.send(embed=embed)
                else:
                    await ctx.guild.ban(user=user, reason=reason)
                    embed = discord.Embed(colour=0x651111, description=str(result1[0]).format(mention=mention, user=user, guild=guild, reason=reason))
                    embed.set_thumbnail(url=f"{user.avatar_url}")
                    embed.set_author(name=f"Staff: {ctx.author}")
                    embed.set_footer(text=f"{currenttime}")
                    
                    
                    channel = self.bot.get_channel(id=int(result[0]))
                    await channel.send(embed=embed)
                        
            else:
                await ctx.send('You cannot do this action')
            
    @commands.group(invoke_without_command=True)
    async def modconfig(self, ctx):
        await ctx.send('Commands: mod channel <#channel> mod text <message>')
        
    @modconfig.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id FROM main.moderation WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                sql = ('INSERT INTO main.moderation(guild_id, channel_id) VALUES(?,?)')
                val = (ctx.guild.id, channel.id)
                await ctx.send(f'channel has been set to {channel.mention}')
            elif result is not None:
                sql = ('UPDATE main.moderation SET channel_id = ? WHERE guild_id = ?')
                val = (channel.id, ctx.guild.id)
                await ctx.send(f'channel has been set to {channel.mention}')
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close
            
    @modconfig.command()
    async def kickm(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id FROM main.moderation WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                sql = ('INSERT INTO main.moderation(guild_id, msg) VALUES(?,?)')
                val = (ctx.guild.id, text)
                await ctx.send(f'Kick and ban message has been set to: `{text}`')
            elif result is not None:
                sql = ('UPDATE main.moderation SET msg = ? WHERE guild_id = ?')
                val = (text, ctx.guild.id)
                await ctx.send(f'Kick and ban message has been updated to `{text}`')
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close
            
    @modconfig.command()
    async def banm(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id FROM main.moderation WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                sql = ('INSERT INTO main.moderation(guild_id, msg1) VALUES(?,?)')
                val = (ctx.guild.id, text)
                await ctx.send(f'Kick and ban message has been set to: `{text}`')
            elif result is not None:
                sql = ('UPDATE main.moderation SET msg1 = ? WHERE guild_id = ?')
                val = (text, ctx.guild.id)
                await ctx.send(f'Kick and ban message has been updated to `{text}`')
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close
        

def setup(bot):
    bot.add_cog(moderationCog(bot))
    print('Moderation Loaded!')