await ctx.message.delete()
                sniped_messages[ctx.channel] = []  # Clear the list after sending all messages
            else:
                embed = Embed(
                    title='Error',
                    description='No deleted messages to snipe.'
                )
                await ctx.send(embed=embed)
                await ctx.message.delete()
        else:
            embed = Embed(
                title='Error',
                description='Invalid mode. Use !snipe recent or !snipe all.'
            )
            await ctx.send(embed=embed)
            await ctx.message.delete()
    else:
        embed = Embed(
            title='Error',
            description='No deleted messages to snipe.'
        )
        await ctx.send(embed=embed)
        await ctx.message.delete()


@client.command()
async def ltcprice(ctx):
    await ctx.message.delete()
    print(f"{d1} {Fore.GREEN}[+]{Fore.GREEN}{Fore.RESET} Command \"ltcprice\" used.{Fore.RESET}")
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        embed_price = discord.Embed(title = "Ltc Price", description = f"The current price of Litecoin is ${price:.2f}")
        await ctx.send(embed=embed_price)
    else:
        embed_error = discord.Embed(title = "Error", description = f"Failed to fetch currnet litecoin price!")
        await ctx.send(embed=embed_error)


@client.command()
async def binance(ctx):
    embed = discord.Embed(title = "Binance", description = f"Mail: SOON\nId: SOON")
    await ctx.message.delete()
    await ctx.send(embed=embed)


@client.command()
async def revoke(ctx, key_: str = None):
    if key_ is None:
        await ctx.send(embed=discord.Embed(title="Invalid Key", description="Please provide a key to revoke", color=0x000000))
        return
    if ctx.author.id not in allowed_ids:
        await ctx.send(embed = discord.Embed(title = "Invalid Permissions", description = "You do not have permission to use this command", color = 00000))
        return
    if 'https://discord.com/' in key_:
        key_ = key_.split('&state=')[1]
    else:
        key_ = key_.strip()
    
    result, details = Key.check(key_)
    url = f"{redirect}/check/{key_}"

    if result is False:
        status = "Used Key"
    elif result is True:
        status = "Valid Key"
    else:
        await ctx.message.delete()
        await ctx.send(embed=discord.Embed(title="Invalid Key", description=f"Key: {key_}\nError: {details}", color=0x000000))
        return
    
    if status == "Used Key":
        await ctx.message.delete()
        await ctx.send(embed=discord.Embed(title="Invalid Key", description=f"Key: {key_}\nError: Key has already been used", color=0x000000))
        return
    else:
        with open('keys.json') as f:
            keys_data = json.load(f)
        
        if key_ not in keys_data:
            await ctx.message.delete()
            await ctx.send(embed=discord.Embed(title="Invalid Key", description=f"Key: {key_}\nError: Key does not exist", color=0x000000))
            return
        else:
            keys_data.pop(key_)
            with open('keys.json', 'w') as f:
                json.dump(keys_data, f, indent=4)
            await ctx.message.delete()    
            await ctx.send(embed=discord.Embed(title="Success", description=f"Key: {key_}\nStatus: Key has been revoked", color=0x000000))
            return
        


def run_bot():
    client.run(main_token)

if name == 'main':
    from threading import Thread
    thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 1337})
    thread.start()
    run_bot()
