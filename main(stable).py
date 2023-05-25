import os, discord, random
from discord.ext.commands import Bot
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(Bot):

    def __init__(self):
        self.MY_GUILD = discord.Object(id=int(os.getenv('DISCORD_GUILD')))
        super().__init__(intents=discord.Intents.default(),command_prefix="!roll ")

    async def on_ready(self):
        print("Bot is online!")

    async def setup_hook(self):
        self.tree.copy_global_to(guild=self.MY_GUILD)
        await self.tree.sync(guild=self.MY_GUILD)

client = MyClient()


@client.tree.command()
async def roll(interaction: discord.Interaction, dice_sides: int, number_of_dice: int = 1, dice_add: int = None, dice_multiply: int = None):
    dice_sum = 0
    dice_rolls = []

    # "Rolls" the dice
    for i in range(number_of_dice):
        randomNumber = random.randint(1, dice_sides)
        dice_rolls.append(randomNumber)
        dice_sum += randomNumber

    if dice_add != None: dice_sum += dice_add
    if dice_multiply != None: dice_sum = int(dice_sum)*int(dice_multiply)

    appendRoll = ''
    if dice_add != None: appendRoll += f'Added:{dice_add}; '
    if dice_multiply != None: appendRoll += f'Multiplied:{dice_multiply}; '
    print("add/multiplied")
    if len(dice_rolls) == 1: appendRoll += f'Roll:{dice_rolls[0]}'
    if len(dice_rolls) >= 2: 
        rollsAppend = ''
        for i in range(0, len(dice_rolls)-1):
            rollsAppend += f'{dice_rolls[i]}, '
        rollsAppend += f'{dice_rolls[i+1]}'
        appendRoll += f'Rolls:{rollsAppend}'
    
    msg = f'The result is {dice_sum}\n{appendRoll}'
    await interaction.response.send_message(msg)

# @client.tree.command()
# async def legacyroll(interaction: discord.Interaction, number: int, add: int = None):
#     """Standard rolling! Roll any sided die and add whatever to it!"""
#     randValue = random.randint(1, number)
#     if add == None: msg = f'The random number is {randValue}'
#     if add != None: msg = f'The random number is {randValue+add}.\nAdded:{add}; Original Roll:{randValue}'
#     await interaction.response.send_message(msg)

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