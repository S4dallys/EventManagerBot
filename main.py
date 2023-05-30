import discord
import random
from Paginator import Simple
from discord.ext import commands
from keep_alive import keep_alive
from ppsize import ppsize
from stan_user import stan_user
from generate import random_fact, generate_quote
from anime import getAnimeOrManga, getMedia
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
async def inspire(ctx):
  quote = generate_quote()
  await ctx.send(quote)


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
    result = ["Failed. Course not found."]
  elif result == None:
    result = ["No assignments found. Yay!"]

  for e in result:
    await ctx.send(e)


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
      for e in result:
        await ctx.send(e)

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

  for e in result:
    await ctx.send(e)


@hwdet.error
async def hwdet_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(
      "Please write the command like so: *!!hwdet <course> <keyword>*\n(ex. !!hwdet dsalg midterm = dsalg assignment with name closest to 'midterm')"
    )


@bot.command()
async def pick(ctx, *args):
  rand = random.randint(0, len(args) - 1)
  await ctx.send(args[rand])


@bot.command()
async def Help(ctx):
  instructions = [
    "!!fact", "!!pp <@user>", "!!stan <@user", "!!inspire", "!!pick <item> <item> ...",
    "!!token <token>", "!!hws <course> <range> -U (optional)",
    "!!hwsall <range> -U (optional)", "!!hwdet <course> <keyword>", "!!kitsu <type> (optional params: !!kitsu for details)", "!!kitsurand <type>"
  ]
  await ctx.send("\n".join(instructions))


@bot.command()
async def kitsu(ctx, type, *args):
  flags = {i.split("=")[0]: i.split("=")[1] for i in args}

  try:
    output = getAnimeOrManga(type, flags)
  except:
    await ctx.send("Error! Something might be wrong with search parameters or no media found.")
    return

  embeds = []

  for media in output:
    embed = discord.Embed(color=discord.Color.random())
    
    for pair in media["details"].items():
      embed.add_field(name=pair[0], value=pair[1], inline=True)

    embed.add_field(name="Description", value=media["description"][:1020])
  
    embed.set_thumbnail(url=media["image-url"])

    embeds.append(embed)

  simple = Simple(InitialPage=0)
  await simple.start(ctx=ctx, pages=embeds)

@kitsu.error
async def kitsu_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(
      "Command usage: !!kitsu <media> OPTIONAL param=value\n\nPossible params: keyword, cat, year, status, subtype, page\nExamples:\n!!kitsu anime cat=horror year=2020 status=finished\n!!kitsu anime cat=slice%of%life keyword=tokyo subtype=movie page=2\n!!kitsu manga cat=thriller,psychological status=current\n\n*note: default page is 1, set to values above 1 to move forward.\nUse % instead of spaces when writing keyword values.\nAlso, year and subtype does not work with manga.*"
    )

@bot.command()
async def kitsurand(ctx, type, *args):
  offset = random.randint(1, 8000)
  media = getMedia(type, offset)

  embed = discord.Embed()

  for pair in media["details"].items():
    embed.add_field(name=pair[0], value=pair[1], inline=True)
  embed.add_field(name="Description", value=media["description"][:1020])
  embed.set_thumbnail(url=media["image-url"])

  await ctx.send(embed=embed)

  

@bot.command()
async def kitsucats(ctx):
  await ctx.send(
    "Violence, Plot Continuity, Stereotypes, Tone Changes, Action, Adventure, Angst, Anime Influenced, Anthropomorphism, Blackmail, Comedy, Detective, Drama, Ecchi, Yuri, Fantasy, Ghost, Harem, Henshin, Horror, Magical Girl, Mystery, Parasite, Psychological, Romance, Science Fiction, Super Power, Supernatural, Thriller, Vampire, Virtual Reality, Zombie, Countryside, Desert, Earth, Fantasy World, Future, Isekai, Island, Parallel Universe, Past, Present, Space, Summer, Josei, Kids, Seinen, Shoujo, Shounen, Anti War, Coming Of Age, Conspiracy, Cooking, Crime, Disaster, Family, Friendship, Gender Bender, Law And Order, Military, Netorare, Parental Abandonment, Politics, Proxy Battles, Religion, Revenge, Rotten World, School Life, Slavery, Slice of Life, Sports, The Arts"
  )
  
  
    


keep_alive()
bot.run(TOKEN)
