import requests


async def random_fact(ctx):
  r = requests.get(
    "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
  r_json = r.json()
  await ctx.send(r_json["text"])


def generate_quote():
  api_url = 'https://api.themotivate365.com/stoic-quote'
  response = requests.get(api_url)
  json = response.json()
  if response.status_code == requests.codes.ok:
    return json["quote"] + f" ({json['author']})"
  else:
    return "Failed! Please try again D:"
