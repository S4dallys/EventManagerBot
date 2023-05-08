import random

templates = [
  "I'm telling you {mention} is as cracked as he is jacked, i saw him at 7/11 the other day buying adult diapers and a 6 pack of redbull. I asked him what the diapers are for and he said \"they are to contain my full power so i dont absolutely shit on these kids\" then he bhopped out the door",
  "If {mention} has a million fans I am one of them. If {name} has ten fans I am one of them. If {name} has no fans, that means I am no more on the earth. If the World is against {name}, I am against the World. I love {name} till my last breath.",
  "Who is {mention}? For the blind, He is the vision. For the hungry, He is the chef. For the thirsty, He is the water. If {name} thinks, I agree. If {name} speaks, I’m listening. If {name} has one fan, it is me. If {name} has no fans, I don’t exist.",
  "I really love {mention}. Like, a lot. Like, a whole lot. You have no idea. I love them so much that it is inexplicable, and I'm ninety-nine percent sure that I have an unhealthy obsession. I will never get tired of listening that sweet, angelic voice of theirs. It is my life goal to meet up with them in real life and just say hello to them. I wish for nothing but their happiness. If it were for them, I would give my life without any second thoughts. Without them, my life would serve no purpose. I really love {name}.",
  "{mention} isn't so great? Are you kidding me? When was the last time you saw a player with such aim ability and movement? {name} puts the game in another level, and we will be blessed if we ever see a player with his skill and passion for the game again. {random} breaks records. {random2} breaks records. {name} breaks the rules. You can keep your statistics. I prefer the magic.",
  "Carried? Never. {mention} never gets carried. I would personally like to thank {name}, for carrying me. Without you this team would've been nothing. On this day I will give thanks to {name} in the tournament. Thank you.",
  "I've seen {mention} play, he doesn't even use a monitor. He visualizes the map in a detailed rendering, completely in his mind. He has a biological wallhack; his godlike perception highlights all enemies within light-years. His eyes are closed as his mouse gracefully swerves across the table, making immaculate twitches as he flicks from head to head. The bullets that escape his gun barrel are surgical; each making a deadly strike in between his opponent's eyes. His spray control is otherworldly, his crosshair erratically jolting across the screen as his wrist muscles perfectly predict the next bullet's location. Time literally stops as he peeks, sunlight curving as his trigger finger impacts his left mouse button, sending enemies to a digital shadow realm before they even know what happened. He is un-killable. He is undefeatable. This \"man\" is the epitome of eternal.",
  "In the first age, in the first battle, when the shadows first lengthened, one stood. Burned by the embers of Armageddon, his soul blistered by the fires of Hell and tainted beyond ascension, he chose the path of perpetual torment. In his ravenous hatred he found no peace, and with boiling blood he scoured the Umbral Plains seeking vengeance against the dark lords who had wronged him. He wore the crown of the Night Sentinels, and those that tasted the bite of his sword named him... the {mention}.",
  "Since {mention} is the paragon of human virtue without equal past or present, she is most resplendent in love, tributes and accolades. Waking or sleeping, I must not forget {name}’s great boon and in order to return her favour by day and by night, I should only think of fulfilling my loyalty.",
  "Now, I want to clarify, ain't nothing wrong with being gay. Love is love, and all that. It's just that, as far as I know, I am pretty damn straight. Up until this point, I have been pretty firm in my heterosexuality. But fuck it, who am I to run from the truth? {mention} is sooo cute. Every time I see his smile, my heart melts a little bit. Anyone who denies his cuteness is either blind, or an inhuman monster. Dare I say it... {name} is my husbando, and nobody will ever take that away from me."
]


async def stan_user(ctx, arg):
  rand = random.randint(0, len(templates) - 1)

  members_list = [m for m in ctx.guild.members if not m.bot and (m != arg)]

  def get_random():
    if len(members_list) == 0:
      return ctx.message.author
    rand1 = random.choice(members_list)
    members_list.remove(rand1)
    return rand1

  await ctx.send(templates[rand].format(mention=arg.mention,
                                     name=arg.name,
                                     random=get_random().name,
                                     random2=get_random().name))
