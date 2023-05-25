import os, discord, random
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = False
intents.guild_messages = False
client = commands.Bot(command_prefix=":3",intents=intents)
ADMIN_IDS = [979210001556070491, 809870005914566676, 675559827425984582]

NatReactMessage = True
NatReactEmote = True

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        client.tree.copy_global_to(guild=guild)
        await client.tree.sync(guild=guild)
    
@client.tree.command()
async def roll(interaction: discord.Interaction, dice_sides: int, reason: str = None, number_of_dice: int = 1, add: int = None, multiply: int = None):
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
    appendRoll = ''

    # "Rolls" the dice
    for i in range(amount_of_dice):
        randomNumber = random.randint(1, dice_sides)
        dice_rolls.append(randomNumber)
        dice_sum += randomNumber
    
    #REMOVE THIS ITS RIGGING!
    dice_sum = 1
    dice_rolls = [1]
    print("THIS RESULT IS RIGGED")
    appendRoll += "THIS WAS A RIGGED RESULT; "

    if add != None: dice_sum += add
    if multiply != None: dice_sum = int(dice_sum)*int(multiply)

    # Gives a "nice" looking output
    if reason != None: appendRoll += f'Rolled for: {reason}\n'
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
    if NatReactMessage and len(dice_rolls) == 1:
        rollReact = ''
        if dice_rolls[0] == 1:
            #This is a nat1
            randPlace = random.randint(1, (len(nat1_reactList)-1))
            natReaction = nat1_reactList[randPlace]
            natReactionAuthor = nat1_reactAuth[randPlace]
            rollReact = f'\n{natReaction} - {natReactionAuthor}'
        if dice_rolls[0] == 20 and dice_sides == 20:
            #This is a nat20/20
            randPlace = random.randint(1, (len(nat20_reactList)-1))
            natReaction = nat20_reactList[randPlace]
            natReactionAuthor = nat20_reactAuth[randPlace]
            rollReact = f'\n{natReaction} - {natReactionAuthor}'
        msg = msg + rollReact
    await interaction.response.send_message(msg)
    message = await interaction.original_response()
    if NatReactEmote and len(dice_rolls) == 1:
        if dice_rolls[0] == 1:
            #This is a nat 1
            await message.add_reaction("<:nat1:1108177281249189938>")
        if dice_rolls[0] == 20 and dice_sides == 20:
            #This is a nat20/20
            await message.add_reaction("<:nat20:1108177315663466586>")

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