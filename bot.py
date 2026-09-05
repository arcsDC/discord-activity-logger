import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = get_log_channel()
    if channel:
        await channel.send(f"✅ **{member}** joined the server.")

@bot.event
async def on_member_remove(member):
    channel = get_log_channel()
    if channel:
        await channel.send(f"❌ **{member}** left the server.")

@bot.event
async def on_member_update(before, after):
    if before.name != after.name:
        channel = get_log_channel()
        if channel:
            await channel.send(f"📝 **{before}** changed their name to **{after}**.")

def get_log_channel():
    channel_id = os.getenv("LOG_CHANNEL_ID")
    if not channel_id:
        return None
    return bot.get_channel(int(channel_id))

@bot.command(name="setlogchannel")
@commands.has_permissions(administrator=True)
async def set_log_channel(ctx):
    os.environ["LOG_CHANNEL_ID"] = str(ctx.channel.id)
    await ctx.send(f"Log channel set to {ctx.channel.mention}.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN environment variable is required.")
    bot.run(token)
