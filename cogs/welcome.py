import discord
from discord.ext import commands
import sqlite3
import sys
import asyncio



class welcome(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM main WHERE guild_id = {member.guild.id}')
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f'SELECT msg FROM main WHERE guild_id = {member.guild.id}')
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild
            embed = discord.Embed(colour=0x95efcc, description=str(result1[0]).format(members=members, mention=mention, user=user, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"", icon_url=f"{member.avatar_url}")
            
            channel = self.bot.get_channel(id=int(result[0]))
            
            await channel.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        await ctx.send('Commands: welcome channel <#channel> welcome text <message>')
    
        
    @welcome.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                sql = ('INSERT INTO main(guild_id, channel_id) VALUES(?,?)')
                val = (ctx.guild.id, channel.id)
                await ctx.send(f'channel has been set to `{channel.mention}`')
            elif result is not None:
                sql = ('UPDATE main SET channel_id = ? WHERE guild_id = ?')
                val = (channel.id, ctx.guild.id)
                await ctx.send(f'channel has been set to `{channel.mention}`')
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close
            
    @welcome.command()
    async def text(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                sql = ('INSERT INTO main(guild_id, msg) VALUES(?,?)')
                val = (ctx.guild.id, text)
                await ctx.send(f'message has been set to `{text}`')
            elif result is not None:
                sql = ('UPDATE main SET msg = ? WHERE guild_id = ?')
                val = (text, ctx.guild.id)
                await ctx.send(f'message has been Updated to `{text}`')
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close
            
def setup(bot):
    bot.add_cog(welcome(bot))
    print('Welcome Cog Loaded')