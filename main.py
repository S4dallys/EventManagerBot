import discord
from discord.ext import commands
import os
from replit import db
from datetime import date, time, datetime
import json

print(db["events"])

TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!!', intents=intents)


class Event:

  def __init__(self):
    self.name = ''
    self.description = ''
    self.date = 0
    self.time = 0
    self.invitees = []
    self.host = 0

  def display_date(self):
    return self.date.strftime('%A %d-%b-%Y')

  def display_time(self):
    return self.time.strftime('%I:%M%p')

  def display_users(self):
    return [user.name for user in self.invitees]

  def days_until(self, date):
    pass

  def createEvent(self, event_json):
    e = json.loads(event_json)

    self.name = e["name"]
    self.description = e["description"]
    self.date = datetime.strptime(e["date"], "%y-%m-%d").date()
    self.time = datetime.strptime(e["time"], "%H-%M-%S").time()
    self.host = bot.get_user(e["host"])
    self.invitees = [bot.get_user(x) for x in e["invitees"]]

    return self


BLUE = '#2596be'
GREEN = '#03fc6b'
RED = '#cf2115'
PURPLE = '#c71aaa'
YELLOW = '#e8d823'

YES_EMOJI = '👍'
NO_EMOJI = '👎'
OK_EMOJI = '👌'
CHECK_EMOJI = '✅'
X_EMOJI = '❌'
GEAR_EMOJI = '⚙️'
NOTES_EMOJI = '📝'
FWD_EMOJI = '➡️'
BCK_EMOJI = '⬅️'
CANCEL_EMOJI = '🛑'

EMOJI_LIST = [CANCEL_EMOJI, FWD_EMOJI]

valid = 0
event = Event()


async def emb_statement(ctx, colour, title, img, statements):
  embed = discord.Embed(title=title, colour=discord.Colour.from_str(colour))
  embed.set_thumbnail(url=img)

  for value in statements:
    embed.add_field(name='', value=value, inline=False)

  message = await ctx.send(embed=embed)
  return message


async def react_steps(message):
  for emoji in EMOJI_LIST:
    await message.add_reaction(emoji)


async def wait_for_react(ctx, message):

  def check(reaction, user):
    return user == author and str(reaction.emoji) in EMOJI_LIST

  try:
    reaction, user = await bot.wait_for('reaction_add',
                                        timeout=25.0,
                                        check=check)
  except:
    await message.clear_reactions()
    statement = ['Event creation timeout.', '*error code - mf slow asf*']
    await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)
    return False
  else:
    return EMOJI_LIST.index(reaction.emoji) + 1


async def wait_for_msg(ctx):

  def check(m):
    return m.author == author

  try:
    message = await bot.wait_for('message', timeout=25.0, check=check)
  except:
    statement = ['Event creation timeout.', '*error code - mf slow asf*']
    await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)
    return False
  else:

    return message


async def cancel_creation(ctx):
  statement = ['Event creation cancelled.']
  await emb_statement(ctx, PURPLE, f'See you next time! {YES_EMOJI}', '',
                      statement)


async def get_input(ctx, message):
  await react_steps(message)
  valid = await wait_for_react(ctx, message)

  if valid == False:
    return False
  elif valid == 1:
    await cancel_creation(ctx)
    return False
  else:
    return valid


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}')


async def set_desc(ctx):
  global valid
  statement = [
    f'Please write event description, {author.mention} {NOTES_EMOJI}'
  ]
  delete = await emb_statement(ctx, GREEN, '', '', statement)

  message = await wait_for_msg(ctx)
  await delete.delete()

  if message == False:
    valid = False
    return

  event.description = message.content

  statement = [
    f'Event **{event.name}** description set. **(1/5)**',
    f'{event.description}',
    f'*Please react below to continue or cancel. {OK_EMOJI}*'
  ]
  message = await emb_statement(ctx, GREEN, f'Success! {CHECK_EMOJI}', '',
                                statement)

  valid = await get_input(ctx, message)
  await message.delete()


async def set_date(ctx):
  global valid
  statement = [
    f'Please write date, {author.mention} {NOTES_EMOJI}',
    'Format: **YYYY/MM/DD**'
  ]
  delete = await emb_statement(ctx, GREEN, '', '', statement)
  message = await wait_for_msg(ctx)
  await delete.delete()

  if message == False:
    valid = False
    return

  try:
    d = [int(x) for x in message.content.split('/')]
    event.date = date(d[0], d[1], d[2])
  except Exception as e:
    valid = False
    statement = ['Invalid date.', '*error code - idk*']
    print(e)
    await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)
    return

  statement = [
    f'Event **{event.name}** date set. **(2/5)**',
    f'{event.display_date()}',
    f'*Please react below to continue or cancel. {OK_EMOJI}*'
  ]
  message = await emb_statement(ctx, GREEN, f'Success! {CHECK_EMOJI}', '',
                                statement)

  valid = await get_input(ctx, message)
  await message.delete()


async def set_time(ctx):
  global valid
  statement = [
    f'Please write time, {author.mention} {NOTES_EMOJI}',
    'Format: **HH:MM (24hr format)**'
  ]
  delete = await emb_statement(ctx, GREEN, '', '', statement)

  message = await wait_for_msg(ctx)
  await delete.delete()

  if message == False:
    valid = False
    return

  try:
    t = [int(x) for x in message.content.split(':')]
    event.time = time(t[0], t[1], 0, 0, None)
  except Exception as e:
    valid = False
    print(e)
    statement = ['Invalid time.', '*error code - your fault*']
    await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)
    return

  statement = [
    f'Event **{event.name}** date set. **(3/5)**', 
    f'{event.display_time()}', 
    f'*Please react below to continue or cancel. {OK_EMOJI}*'
  ]
  message = await emb_statement(ctx, GREEN, f'Success! {CHECK_EMOJI}', '',
                                statement)

  valid = await get_input(ctx, message)
  await message.delete()

def add_to_db(event_list):
  db["events"] = []
  for event in event_list:
    event.date = event.date.strftime('%y-%m-%d')
    event.time = event.time.strftime('%H-%M-%S')
    event.host = event.host.id
    event.invitees = [x.id for x in event.invitees]
    event_json = json.dumps(event.__dict__)
    db["events"].append(event_json)

def convertEvents():
  event_list = []
  for event in db["events"]:
    x = Event()
    event_list.append(x.createEvent(event))
  return event_list

async def set_invitees(ctx):
  global valid
  statement = [
    f'Who do you want to invite?, {author.mention} {NOTES_EMOJI}',
    'Format: **@user @user @user**', 'Type **ALL** to invite everyone!'
  ]
  delete = await emb_statement(ctx, GREEN, '', '', statement)
  
  message = await wait_for_msg(ctx)
  await delete.delete()

  if message == False:
    valid = False
    return

  del event.invitees[:]

  if message.content == 'ALL':
    for user in bot.get_all_members():
      if user != bot.user and not user.bot:
        event.invitees.append(user)
  else:
    event.invitees.append(message.author)
    for user in message.content.split(' '):
      try:
        if bot.get_user(int(user[2:-1])) not in event.invitees:
          event.invitees.append(bot.get_user(int(user[2:-1])))
      except:
        pass

  statement = [
    f'Users have been invited to **{event.name}**. **(4/5)**', 
    f'{", ".join(event.display_users())}',
    f'*Please react below to continue or cancel. {OK_EMOJI}*'
  ]
  message = await emb_statement(ctx, GREEN, f'Success! {CHECK_EMOJI}', '',
                                statement)

  valid = await get_input(ctx, message)
  await message.delete()


async def finish_event(ctx):
  try:
    statement = [
      '*SUMMARY OF EVENT:*', f'**{event.name}**',
      f'Hosted by: {event.host}', f'*{event.description}*',
     f'**{event.display_date()}** at **{event.display_time()}**',
      '**Invited:**', f'{", ".join(event.display_users())}'
    ]
  except Exception as e:
    print(e)

  message = await emb_statement(ctx, RED, 'One last thing... :eyes:',
                                event.host.display_avatar.url, statement)

  await message.add_reaction(X_EMOJI)
  await message.add_reaction(CHECK_EMOJI)

  def check(reaction, user):
    return user == author and str(reaction.emoji) in [CHECK_EMOJI, X_EMOJI]

  try:
    reaction, user = await bot.wait_for('reaction_add',
                                        timeout=25.0,
                                        check=check)
  except:
    await message.clear_reactions()
    statement = ['Event creation timeout.', '*error code - mf slow asf*']
    await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)
    return False
  else:
    if str(reaction.emoji) == '✅':
      event_list = convertEvents()
      event_list.append(event)
      add_to_db(event_list)

      statement = [
        f'Event **{event.name}** added to database!',
        f'{GEAR_EMOJI} Type *!!help* to check out other commands'
      ]
      await emb_statement(ctx, RED, f'SUCCESS! {NOTES_EMOJI}',
                          bot.user.display_avatar.url, statement)
    else:
      await cancel_creation(ctx)
      return


@bot.command()
async def create(ctx, arg):
  global valid
  global author
  author = ctx.message.author

  event.name = arg
  event.host = author

  statement = [
    f'Event **{event.name}** has been created.\n',
    f'*Please react below to continue or cancel. {OK_EMOJI}*'
  ]
  message = await emb_statement(ctx, GREEN, f'Success! {CHECK_EMOJI}', '',
                                statement)

  valid = await get_input(ctx, message)

  await message.delete()

  if valid == 2:
    await set_desc(ctx)
  else:
    return

  if valid == 2:
    await set_date(ctx)
  else:
    return

  if valid == 2:
    await set_time(ctx)
  else:
    return

  if valid == 2:
    await set_invitees(ctx)
  else:
    return

  if valid == 2:
    await finish_event(ctx)
  else:
    return


@create.error
async def create_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    statement = [
      f'Please enter valid name!\n\n{GEAR_EMOJI} Use *!!help* for more info.',
      'Tip: Use " " to add spaces to event name!'
    ]

    await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)

@bot.command()
async def events(ctx):
  event_list = convertEvents()
  ind = 0
  while (True and len(event_list) > 0):
    event = event_list[ind]

    statement = [
      f'**{event.name}**',
      f'Hosted by: {event.host}', f'*{event.description}*',
      f'**{event.display_date()}** at **{event.display_time()}**',
      '**Invited:**', f'{", ".join(event.display_users())}'
    ]

    message = await emb_statement(ctx, str(event.host.color), '',
                                  event.host.display_avatar.url, statement)

    await message.add_reaction(BCK_EMOJI)
    await message.add_reaction(FWD_EMOJI)

    def check(reaction, user):
      return user == ctx.author and str(
        reaction.emoji) in [BCK_EMOJI, FWD_EMOJI]

    try:
      reaction, user = await bot.wait_for('reaction_add',
                                          timeout=15.0,
                                          check=check)
    except Exception as e:
      print(e)
      await message.clear_reactions()
      return
    else:
      if str(reaction.emoji) == FWD_EMOJI and ind < len(event_list) - 1:
        ind = ind + 1
      elif str(reaction.emoji) == BCK_EMOJI and ind >= 1:
        ind = ind - 1
      else:
        pass

      await message.delete()

  else:
    statement = [
      'Sorry! There are no events currently in the database.',
      f'{GEAR_EMOJI} Type *!!create (event name)* to start making some!'
    ]
    await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)


@bot.command()
async def delete(ctx, arg):
  event_list = convertEvents()
  for event in event_list:
    if event.name == arg:
      statement = [
        f'Event **{event.name}** has been removed'
      ]
      await emb_statement(ctx, str(event.host.color), f'Success! {CHECK_EMOJI}', '', statement)
      event_list.remove(event)
      add_to_db(event_list)
      return

  statement = [
    'Could not find specified event.', f'Try using " " for event names with multiple words {YES_EMOJI}'
  ]
  
  await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)

@bot.command()
async def nextevent(ctx):
  event_list = convertEvents()
  try:
    min_date = event_list[0]
  except:
    statement = [
      'Sorry! There are no events currently in the database.',
      f'{GEAR_EMOJI} Type *!!create (event name)* to start making some!'
    ]
    await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)
    return
    
  
  for event in event_list:

    if event.date < date.today():
      continue
    elif event.date == date.today() and event.time < datetime.now().time():
      continue
    
    if event.date < min_date.date:
      min_date = event
    elif event.date == min_date.date:
      if event.time < min_date.time:
        min_date = event

  statement = [
      f'**{min_date.name}**',
      f'Hosted by: {min_date.host}', f'*{min_date.description}*',
      f'**{min_date.display_date()}** at **{min_date.display_time()}**',
      '**Invited:**', f'{", ".join(min_date.display_users())}',
      f'**{(min_date.date - date.today()).days} days left!! :eyes:**'
  ]

  await emb_statement(ctx, str(event.host.color), f'Next Event! {OK_EMOJI}', event.host.display_avatar.url, statement)

@bot.command()
async def leave(ctx, arg):
  author = ctx.message.author

  event_list = convertEvents()
  for event in event_list:
    if event.name == arg:
      if event.host == author:
        statement = [
          'Sorry! Host cannot leave own event. That be hella weidchamp ong.',
          f'{GEAR_EMOJI} Type *!!delete (event name)* to delete event.'
        ]
        await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)
        return
        
      try:
        event.invitees.remove(author)
      except:
        statement = [
          'Sorry! You are not currently invited to this event.',
          f'{GEAR_EMOJI} Type *!!join (event name)* to join one!'
        ]
        await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)
        return

      statement = [
          f'You have been removed from event {event.name}!'
      ]
      await emb_statement(ctx, GREEN, f'Success! {CHECK_EMOJI}', '', statement)
      add_to_db(event_list)
      return

  statement = [
    'Could not find specified event.', f'Try using " " for event names with multiple words {YES_EMOJI}'
  ]
  await emb_statement(ctx, BLUE, f'Error! {X_EMOJI}', '', statement)
  return
      
      
    

bot.run(TOKEN)
