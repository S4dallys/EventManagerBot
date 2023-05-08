import requests


async def random_fact(ctx):
  r = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
  r_json = r.json()
  await ctx.send(r_json["text"])