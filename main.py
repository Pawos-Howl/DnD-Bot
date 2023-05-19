import os, discord, random
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = False
intents.guild_messages = False
client = commands.Bot(command_prefix=":3",intents=intents)
ADMIN_IDS = [979210001556070491, 809870005914566676]

NatReactMessage = True
NatReactEmote = True

guildsopen = []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    try:
        for v in client.guilds:
            guildsopen.append(v.name)
        synced = await client.tree.sync()
        print(f'synced {len(synced)} command(s)')
    except Exception as exception:
        print(exception)

@client.tree.command()
async def roll(interaction: discord.Interaction, dice_sides: int, number_of_dice: int = 1, add: int = None, multiply: int = None):
    # a natural 1, ouch man...(doggy); bad luck?(doggy); lets hope for a better roll next time.(doggy); yay, a nat 1 /j(doggy); Gotta wish you were a halfling(james); 
    nat1_reactList = ["A natural 1, ouch man...","Bad luck?","Lets hope for a better roll next time.","yay, a nat 1 /j","Gotta wish you werer a halfling."]
    nat1_reactAuth = ["Samaris","Samaris","Samaris","Samaris","James"]
    nat20_reactList = ["..."]
    nat20_reactAuth = ["..."]

    amount_of_dice = number_of_dice
    dice_add = add
    dice_multiply = multiply
    dice_sum = 0
    dice_rolls = []

    # "Rolls" the dice
    for i in range(amount_of_dice):
        randomNumber = random.randint(1, dice_sides)
        dice_rolls.append(randomNumber)
        dice_sum += randomNumber

    if add != None: dice_sum += add
    if multiply != None: dice_sum = int(dice_sum)*int(multiply)

    # Gives a "nice" looking output
    if len(dice_rolls) == 1 and dice_multiply == None and dice_add == None: return f'The random number is {dice_sum}'
    appendRoll = ''
    if dice_add != None: appendRoll += f'Added:{dice_add}; '
    if dice_multiply != None: appendRoll += f'Multiplied:{dice_multiply}; '
    if len(dice_rolls) == 1: appendRoll += f'Roll:{dice_rolls[0]}'
    if len(dice_rolls) >= 2: 
        rollsAppend = ''
        for i in range(0, len(dice_rolls)-1):
            rollsAppend += f'{dice_rolls[i]}, '
        rollsAppend += f'{dice_rolls[i+1]}'
        appendRoll += f'Rolls:{rollsAppend}'
    msg =  f'The result is {dice_sum}\n{appendRoll}'
    # Post work for if the result was either nat20/20 or nat1
    # Use this! https://www.w3schools.com/python/python_strings_format.asp
    if NatReactMessage and len(dice_rolls) == 1:
        rollReact = ''
        if dice_rolls[0] == 1:
            #This is a nat1
            natReaction = nat1_reactList[random.randint(0, len(nat1_reactList-1))]
            natReactionAuthor = nat1_reactAuth[nat1_reactList.index(natReaction)]
            rollReact = f'\n{natReaction} - {natReactionAuthor}'
        if dice_rolls[0] == 20 and dice_sides == 20:
            #This is a nat20/20
            natReaction = nat20_reactList[random.randint(0, len(nat20_reactList-1))]
            natReactionAuthor = nat20_reactAuth[nat20_reactList.index(natReaction)]
            rollReact = f'\n{natReaction} - {natReactionAuthor}'
        msg = msg + rollReact
    interactionMessage = await interaction.response.send_message(msg)
    if NatReactEmote and len(dice_rolls) == 1:
        if dice_rolls[0] == 1:
            #This is a nat 1
            await interactionMessage.add_reaction('1108177315663466586')
        if dice_rolls[0] == 20 and dice_sides == 20:
            #This is a nat20/20
            await interactionMessage.add_reaction('1108177315663466586')



@client.tree.command()
async def stopbot(interaction: discord.Interaction):
    """[ADMIN ONLY] This will forcefully stop the bot."""
    if interaction.user.id == 979210001556070491 or interaction.user.id == 809870005914566676:
        embed = discord.Embed(title='Confirmed', description=f'The bot is stopping itself...', color=0x3cb043)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        exit("Terminating")
    else:
        embed = discord.Embed(title='ERROR', description=f'{interaction.user}! You are not allowed to run the `stopbot` command! That command is for admin use only.\n>:c You are not allowed to do that!', color=0xff00c8)
        await interaction.response.send_message(embed=embed, ephemeral=True)

client.run(TOKEN)