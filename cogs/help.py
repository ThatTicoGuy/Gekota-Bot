class help(commands.Cog, name='help'):
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(colour=0xDFBDB5, description='**Help Commands**')
        embed.add_field()
        
def setup(bot):
    bot.add_cog(help(bot))
    print('help Loaded!')
