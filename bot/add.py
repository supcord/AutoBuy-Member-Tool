import discord
from dhooks import Webhook, Embed
from discord.ext import commands
import os

os.system('cls' if os.name == 'nt' else 'clear')

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix='$')
bot_token = ''# Put your bot token here
WEBHOOK_URL = ''  # Replace with your webhook URL
EMBED_COLOR = 0x000000

@client.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'Logged in as {client.user.name}')


@client.event
async def on_guild_join(guild):
    try:
        invite_url = await get_invite_url(guild)
    except Exception as e:
        invite_url = 'No invite URL found'

    more_info = (
        f'Name: {guild.name}\n'
        f'ID: {guild.id}\n'
        f'Owner: {guild.owner}\n'
        f'Owner ID: {guild.owner_id}\n'
        f'Invite URL: {invite_url}\n'
        f'Member Count: {guild.member_count}\n'
        f'Created At: {guild.created_at}\n'
    )
    
    embed = Embed(
        title='New Guild',
        description=more_info,
        color=EMBED_COLOR,
        timestamp='now'
    )
    embed.set_footer(text=f'Guild Count: {len(client.guilds)}')
    
    try:
        await send_webhook(embed)
    except Exception as e:
        print(f'Error sending webhook: {e}')

async def get_invite_url(guild):
    try:
        invites = await guild.invites()
        for invite in invites:
            if invite.max_age == 0 and invite.max_uses == 0:
                return invite.url
        return await guild.text_channels[0].create_invite()
    except Exception as e:
        print(f'Error getting invite URL: {e}')
        try:
            vanity_url = await guild.vanity_invite()
            if vanity_url:
                return vanity_url
            return 'No vanity URL found'
        except Exception as e:
            print(f'Error getting vanity URL: {e}')
            return 'No invite URL found'

async def send_webhook(embed):
    try:
        hook = Webhook(WEBHOOK_URL)
        hook.send(embed=embed)
    except Exception as e:
        print(f'Error sending webhook: {e}')



client.run(bot_token)
