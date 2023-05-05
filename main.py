import discord
from discord.ext import commands
from keep_alive import keep_alive
from ppsize import ppsize
import os

TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!!', intents=intents)


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}')


@bot.command()
async def hello(ctx):
  await ctx.send("Hello!")


@bot.command(name='pp', aliases=['ppsize', 'penis', 'pp'])
async def pp(ctx, user: discord.User):
  await ppsize(ctx, user)


@pp.error
async def pp_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ppsize(ctx, ctx.message.author)


keep_alive()
bot.run(TOKEN)
