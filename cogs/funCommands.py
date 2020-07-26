import discord
from discord.ext import commands
import sqlite3
import sys
import asyncio



class fun(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
    @commands.command()
    async def feed(self, ctx):
        await ctx.send(str('{} has fed the ~~pig~~ frog').format(ctx.message.author.mention))
        
    @commands.command()
    async def f(self, ctx):
        await ctx.send("Some one has said an f in the chat")
        
    @commands.command()
    async def who(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="Account Created:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Join Date Server:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        
        await ctx.send(embed=embed)
        
    @commands.command()
    async def ian(self, ctx):
        await ctx.send("Ian")
        
def setup(bot):
    bot.add_cog(fun(bot))
    print('Fun Cog Loaded')