import discord
from discord.ext import commands
import utils
from utils import CONFIG, ALLOWED_CHANNEL_ID
import os
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(str(CONFIG.get('welcome_message')).format(username=f"{member.mention}"))
    else:
        print("Welcome channel not found.")


@bot.event
async def on_command_error(ctx, error):
    channel = discord.utils.get(
        ctx.guild.text_channels, name="on-command-error"
    )
    if channel:
        await channel.send(f"Error: {error}")
    else:
        print("Error channel not found.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.strip()

    if message.channel.id in ALLOWED_CHANNEL_ID or not msg:
        utils.append_message("user", f"{message.author.display_name}: {msg}")

        if msg.startswith('?'):
            msg_with_name = f"{message.author.display_name}: {msg[1:]}"
            ai_response = utils.completion(msg_with_name)
            await message.reply(ai_response)

    await bot.process_commands(message)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 100):
    print("Clearing messages...")
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'✅ Deleted {len(deleted)} messages.', delete_after=10)
    if ctx.channel.id in ALLOWED_CHANNEL_ID:
        utils.clear_message()


bot.run(os.getenv("DISCORD_TOKEN"))
