@color.command()
    async def buy(self, ctx, roles):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT exp FROM main.eco WHERE user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()
        exp = int(result[0])
        member = ctx.message.author
        message = ctx.message.author
        #roles = discord.utils.get(member.guild.roles, name='red', 'blue', 'yellow', 'pink', 'green')
        red = discord.utils.get(member.guild.roles, name='red')
        blue = discord.utils.get(member.guild.roles, name='blue')
        yellow = discord.utils.get(member.guild.roles, name='yellow')
        pink = discord.utils.get(member.guild.roles, name='pink')
        green = discord.utils.get(member.guild.roles, name='green')
        if exp >= 3000: 
            if roles == 'red':
                await member.add_roles(red)
                await ctx.send(f'Role bought: Red')
                sql = (f'UPDATE main.eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = (exp - 3000, str(ctx.message.author.guild.id), str(ctx.message.author.id))
                cursor.execute(sql, val)
                db.commit()
            elif roles == 'blue':
                await member.add_roles(blue)
                await ctx.send(f'Role bought: Blue')
                sql = (f'UPDATE main.eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = (exp - 3000, str(ctx.message.author.guild.id), str(ctx.message.author.id))
                cursor.execute(sql, val)
                db.commit()
            elif roles == 'yellow':
                await member.add_roles(yellow)
                await ctx.send(f'Role bought: Yellow')
                sql = (f'UPDATE main.eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = (exp - 3000, str(ctx.message.author.guild.id), str(ctx.message.author.id))
                cursor.execute(sql, val)
            elif roles == 'pink':
                await member.add_roles(pink)
                await ctx.send(f'Role bought: Pink')
                sql = (f'UPDATE main.eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = (exp - 3000, str(ctx.message.author.guild.id), str(ctx.message.author.id))
                cursor.execute(sql, val)
            elif roles == 'green':
                await member.add_roles(green)
                await ctx.send(f'Role bought: Green')
                sql = (f'UPDATE main.eco SET exp = ? WHERE guild_id = ? and user_id = ?')
                val = (exp - 3000, str(ctx.message.author.guild.id), str(ctx.message.author.id))
                cursor.execute(sql, val)   
            else:
                await ctx.send('Please select a color')
                
        else:
            await ctx.send('Cannot make the purchase')
        db.commit()
        cursor.close()
        db.close()