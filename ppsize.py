import random


async def ppsize(ctx, arg):
  rand = random.random()

  if rand < 0.6:
    low = 0
    high = 7
  elif rand < 0.95:
    low = 8
    high = 28
  else:
    low = 40
    high = 80

  inch = random.randint(low, high)

  if inch == 0:
    emote = '<:Jebaited:711151475996491806>'
  if inch == 69:
    emote = '<:gigachad:1015244601776406581>'
  elif inch < 4:
    emote = '<:ICANT:1015270574563532860>'
  elif inch < 13:
    emote = '<:Clap:1077602420630241290>'
  elif inch < 30:
    emote = '<:BOOBA:1015245334802350121>'
  else:
    emote = '<:monkaW:913239703954808885>'

  await ctx.send(f"{arg.mention} has a {inch} inch pp {emote}")