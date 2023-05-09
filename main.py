import discord
from discord.ext import commands
from keep_alive import keep_alive
from ppsize import ppsize
from stan_user import stan_user
from random_fact import random_fact
from setup import Student
import _canvas
from replit import db
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


@bot.command(name='pp', aliases=['ppsize', 'penis'])
async def pp(ctx, user: discord.User):
  await ppsize(ctx, user)


@pp.error
async def pp_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ppsize(ctx, ctx.message.author)


@bot.command()
async def stan(ctx, user: discord.User):
  await stan_user(ctx, user)


@bot.command()
async def fact(ctx):
  await random_fact(ctx)

async def hasToken(ctx):
  try:
    user = Student(db["canvas_tokens"][str(ctx.message.author)])
    return user
  except KeyError:
    await ctx.send(
      "Token not found. Please type *!!token <canvas_token>*\n\nThis is found in Canvas>Account>Settings>New Token"
    )
    return None
    
@bot.command()
async def token(ctx, token):
  try:
    user = Student(token)
    await ctx.send("Token added! :D\nDelete your token message asap!")
    db["canvas_tokens"][str(ctx.message.author)] = token
  except:
    await ctx.send("Invalid token.")
    return

@bot.command(name="hws")
async def hws(ctx, course, date, dated=None):
  user = await hasToken(ctx)

  if user == None:
    return
    
  result = _canvas.printAssignments(user, course, date, dated)

  if result == 0:
    result = "Failed. Course not found."
  elif result == None:
    result = "No assignments found. Yay!"

  await ctx.send(result)

@hws.error
async def hws_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(
      "Please write the command like so: *!!hws <code> <range>*\n(ex. !!hws dsalg 1000 = all dsalg assignments for the next 1000 days)\n(Also you can add the -U flag after to include undated assignments)"
    )


@bot.command(name="hwsall")
async def hwsall(ctx, date, dated=None):
  user = await hasToken(ctx)

  if user == None:
    return

  exists = False
  
  for course in user.courses:
    result = _canvas.printAssignments(user, course.name[:12], date, dated)
    if result != 0 and result != None:
      exists = True
      await ctx.send(result)

  if exists == False:
    await ctx.send("No assignments found. Gladge!")

@hwsall.error
async def hwsall_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(
      "Please write the command like so: *!!hwsall <range>*\n(ex. !!hws 1000 = all assignments for the next 1000 days)\n(Also you can add the -U flag after to include undated assignments)"
    )

@bot.command()
async def hwdet(ctx, course, name):
  user = await hasToken(ctx)

  if user == None:
    return

  result = _canvas.getAssignmentDetailed(user, course, name)
  await ctx.send(result)

@hwdet.error
async def hwdet_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(
      "Please write the command like so: *!!hwdet <course> <keyword>*\n(ex. !!hwdet dsalg midterm = dsalg assignment with name closest to 'midterm')"
    )

    

  







@bot.command()
async def com(ctx):
  instructions = [
    "!!fact",
    "!!pp <@user>",
    "!!stan <@user",
    "!!token <token>",
    "!!hws <course> <range> -U (optional)",
    "!!hwsall <range> -U (optional)",
    "!!hwdet <course> <keyword>"
  ]
  await ctx.send("\n".join(instructions))
  

keep_alive()
bot.run(TOKEN)
