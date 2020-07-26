import discord
from discord.ext import commands
import asyncio
import sys
import sqlite3


TOKEN = 'NzMzMDYwODExOTMyNjk2NjA2.Xw-N-w.y-oyn8zOXoHVTGYagK6cKRzebh8'

description = '''Gekota'''

class Bot(commands.Bot):

    async def start(self, *args, **kwargs):
        import os, pickle
        if os.path.exists(cooldown_info_path):  # on the initial run where "cd.pkl" file hadn't been created yet
            with open(cooldown_info_path, 'rb') as f:
                d = pickle.load(f)
                for name, func in self.commands.items():
                    if name in d:  # if the Command name has a CooldownMapping stored in file, override _bucket
                        self.commands[name]._buckets = d[name]
        return await super().start(*args, **kwargs)

    async def logout(self):
        import pickle
        with open(cooldown_info_path, 'wb') as f:
            # dumps a dict of command name to CooldownMapping mapping
            pickle.dump({name: func._buckets for name, func in self.commands.items()}, f)
        return await super().logout()

bot = commands.Bot(command_prefix='^', description=description)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main(
        guild_id TEXT,
        msg TEXT,
        channel_id TEXT
        )
        ''')
    return

cogs = ['cogs.moderation','cogs.welcome', 'cogs.funCommands', 'cogs.friendcode', 'cogs.quotes', 'cogs.currency']


if __name__ == '__main__':
    for extension in cogs:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('failed to load {extension}', file=sys.stderr)
            traceback.print_exc()
bot.run(TOKEN)