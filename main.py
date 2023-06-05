import os, discord, random, json
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
    # Backup to end the interaction early if there is an input on dice of an invalid amount
    if dice_sides <= 0:
        embed = discord.Embed(title='ERROR', description=f'{interaction.user}! You can\'t run the "roll" command with a roll of: {dice_sides}!\nIt must be a positive integer', color=0xff00c8)
        await interaction.response.send_message(embed=embed, ephemeral=False)
        return # Does nothing other then end the function
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

# THE FOLLOWING IS CODE FROM "TheProperGlitch". The URL is here: https://github.com/TheProperGlitch/Dnd-Tracker

#Setup:
try:
    os.chdir("Users")
except FileNotFoundError:
    #This doesn't matter :3
    os.mkdir("Users")
    os.chdir("Users")
files = os.listdir('.')
#This is here to remove the file added to github by the repo
try:
    files.remove("null..txt")
except ValueError:
    #The file it can't find isn't needed, so its fine :3
    pass

#Showing all creatures:
@client.tree.command()
async def c_show(interaction: discord.Interaction):
    user = interaction.user.id
    if f"{user}.json" in files:
        with open(f"{user}.json", "r") as file:
            user_objects = json.load(file)
        if user_objects["creature_amount"] == 0:
            msg = "Sorry, but it seems that you have no creatures to look at."
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            creature_amount = user_objects["creature_amount"]
            creature_list = user_objects["creature_list"]
            final_list = ''
            for i in range(creature_amount):
                final_list = final_list + f"{i+1}: Name:{creature_list[str(i+1)][0]}, Health:{creature_list[str(i+1)][1]}, Dex Modifier:{creature_list[str(i+1)][2]} \n Notes:{creature_list[str(i+1)][3]}; "
            interaction.response.send_message(final_list)

#Editting a creature:
@client.tree.command()
async def c_edit(interaction: discord.Interaction, creature_number: int, name: str = None, health: int = None, dexterity: int = None, notes: str = None):
    """
    Allows the user to edit a creature's attributes.
    """
    # Function code goes here
    user = interaction.user.id
    if f"{user}.json" in files:
        with open(f"{user}.json", "r") as file:
            user_objects = json.load(file)
        if user_objects["creature_amount"] == 0:
            msg = "Sorry, but it seems that you have no creatures to look at."
            interaction.response.send_message(msg, ephemeral=True)
        else:
            print("What creature would you like to edit?")
            creature_list = user_objects["creature_list"]
            editing = creature_number
            if name != None:
                creature_list[str(editing)][0] = name
            if health != None:
                creature_list[str(editing)][1] = health
            if dexterity != None:
                creature_list[str(editing)][2] = dexterity
            if notes != None:
                creature_list[str(editing)][3] = notes
            setName = f"Name: {creature_list[str(editing)][0]}"
            setHealth = f"Health: {creature_list[str(editing)][1]}"
            setDext = f"Dexterity: {creature_list[str(editing)][2]}"
            setNotes = f"Notes: {creature_list[str(editing)][3]}"
            user_objects["creature_list"] = creature_list
            with open(f"{user}.json", "w") as file:
                json.dump(user_objects, file)
            msg = f'Done! Creature {creature_number}\'s data is below:\n{setName}\n{setHealth}\n{setDext}\n{setNotes}'
            interaction.response.send_message(msg, ephemeral=True)

    else:
        msg = "Sorry, but it seems that you have no creatures to look at."
        interaction.response.send_message(msg, ephemeral=True)

#Making a new creature:
@client.tree.command()
async def c_make(interaction: discord.Interaction, name: str, health: int, dexterity: int, notes: str = ""):
    """
    Prompts the user to create a new creature and saves it.
    """
    # Function code goes here
    creature = []
    creature_list = {}
    creature.append(name)
    creature.append(int(health))
    creature.append(int(dexterity))
    creature.append(notes)
    user = interaction.user.id
    if f"{user}.json" in files:
        with open(user+".json", "r") as file:
            user_objects = json.load(file)
        creature_amount = user_objects["creature_amount"]
        creature_amount += 1
        creature_list = user_objects["creature_list"]
        creature_list[creature_amount] = creature
        user_objects["creature_list"] = creature_list
        user_objects["creature_amount"] = creature_amount
        with open(f"{user}.json", "w") as file:
            json.dump(user_objects, file)
    else:
        creature_list = {1: creature}
        user_objects = {"creature_amount" : 1, "creature_list" : creature_list, "encounter_amount" : 0, "encounter_list" : {}}
        with open(f"{user}.json", "w") as file:
            json.dump(user_objects, file)
    msg = 'Done!'
    interaction.response.send_message(msg, ephemeral=True)

#Copying a creature that has already been made
@client.tree.command()
async def c_copy(interaction: discord.Interaction, creature_id: int):
    user = interaction.user.id
    if f"{user}.json" in files:
        with open(f"{user}.json", "r") as file:
            user_objects = json.load(file)
        if user_objects["creature_amount"] == 0:
            msg = "Sorry, but it seems that you have no creatures to copy."
            interaction.response.send_message(msg, ephemeral=True)
        else:
            creature_amount = user_objects["creature_amount"]
            creature_list = user_objects["creature_list"]

            copying = creature_id
            creature = creature_list[str(copying)]
            creature_amount+=1
            creature_list[creature_amount] = creature
            user_objects["creature_amount"] = creature_amount
            user_objects["creature_list"] = creature_list
            with open(f"{user}.json", "w") as file:
                json.dump(user_objects, file)
            msg = "Done!"
            interaction.response.send_message(msg, ephemeral=True)

    else:
        msg = "Sorry, but it seems that you have no creatures to copy."
        interaction.response.send_message(msg, ephemeral=True)

#Showing all encounters
@client.tree.command()
async def e_show(interaction: discord.Interaction):
    user = interaction.user.id
    if f"{user}.json" in files:
        with open(f"{user}.json", "r") as file:
            user_objects = json.load(file)
        encounter_list = user_objects["encounter_list"]
        encounter_amount = user_objects["encounter_amount"]
        if encounter_amount == 0:
            msg = "Sorry, but we could not find any encounters in your file. \nTry making an encounter."
            interaction.response.send_message(msg, ephemeral=True)
        else:
            encountersList = ""
            for object in encountersList:
                encountersList = encountersList + f"{str(object)}: {encounter_list[object]}; "
            msg = f'{encountersList}'
            interaction.response.send_message(msg, ephemeral=True)

#Copying an encounter that has already been made
@client.tree.command()
async def e_copy(interaction: discord.Interaction):
    """NO CODE"""
    msg = 'Oops... We don\'t have code for this yet! Visit this command soon!'
    interaction.response.send_message(msg, ephemeral=True)
#Editing an encounter that has already been made
@client.tree.command()
async def e_edit(interaction: discord.Interaction):
    """NO CODE"""
    msg = 'Oops... We don\'t have code for this yet! Visit this command soon!'
    interaction.response.send_message(msg, ephemeral=True)

#TEMP DISCLAIMER
@client.tree.command()
async def notice(interaction: discord.Interaction):
    embed = discord.Embed(title='NOTEBOARD', description='S-So... its a bit difficult to make something to run encounters... It might take a long time... Go to TheProperGlitch\'s DnD thing for now (attached below). It works very well. Give me a bit to get the code working on other stuff :3 -Pawos Howl', color=0x2528D2, url="https://github.com/TheProperGlitch/Dnd-Tracker")
    interaction.response.send_message(embed=embed, ephemeral=True)

# #Making an encounter
# def e_make():
#     """
#     Allows the user to create an encounter. (Q for quick make, D for detailed.) Note: Quick made encounters will not be saved.
#     """
#     # Function code goes here
#     print("Would you like to quick-make an encounter or be more detailed? (Q for quick make, D for detailed.) \nNote: Quick made encounters will not be saved.")
#     encounter_type = input("")
#     if encounter_type.lower() == "q":
#         print("How many creatures are there?")
#         amount_of_creatures=int(input(""))
#         turn = 0
#         initiative_tracking = {}
#         while turn < amount_of_creatures:
#             print("What is the creatures name?")
#             name = input('')
#             print("What is the creatures initiative? (Numbers only!)")
#             initiative = int(input(''))
#             while initiative in initiative_tracking:
#                 print("I'm sorry, but two creatures cannot have the same initiative.\nWhat should the new initiative be?")
#                 initiative = int(input(''))
#             print("What is the creatures health? (Numbers only!)")
#             health = input('')
#             print("What other notes do you have?")
#             notes = input('')
#             creature = [name, initiative, health, notes]
#             if health == "":
#                 health = 1
#             initiative_tracking[initiative] = [creature]
#             turn += 1
#         playing = True
#         while playing:
#             for key in sorted (initiative_tracking.keys(), reverse=True):
#                 if playing == False:
#                     break
#                 active = True
#                 while active:
#                     print(f"It is {initiative_tracking[key][0][0]}'s turn! \nWhat would you like to do? \nCommands:(H: Heal Self, D: Damage, N: Next, E: End)")
#                     action = input("")
#                     if action.lower() == "h":
#                         print(f"{initiative_tracking[key][0][0]} is at {initiative_tracking[key][0][2]} health.")
#                         print("For how much would you like heal for? (Integers only!)")
#                         health_healed = int(input(""))
#                         initiative_tracking[key][0][2] = str(health_healed + int(initiative_tracking[key][0][2]))
#                         print(f"{initiative_tracking[key][0][0]} is now at {initiative_tracking[key][0][2]} health.")
#                     elif action.lower() == "d":
#                         print(f"{initiative_tracking[key][0][0]} is at {initiative_tracking[key][0][2]} health.")
#                         print("For how much damage would you like to do? (Integers only!)")
#                         damage_dealt = int(input(""))
#                         initiative_tracking[key][0][2] = str(int(initiative_tracking[key][0][2]) - damage_dealt)
#                         print(f"{initiative_tracking[key][0][0]} is now at {initiative_tracking[key][0][2]} health.")
#                     elif action.lower() == "n": 
#                         active = False
#                     elif action.lower() == "e":
#                         playing = False
#                         active = False
#     else:
#         if f"{user}.json" in files:
#             with open(f"{user}.json", "r") as file:
#                 user_objects = json.load(file)
#             creature_list = user_objects["creature_list"]
#             creature_amount = user_objects["creature_amount"]
#             encounter_list = user_objects["encounter_list"]
#             encounter_amount = user_objects["encounter_amount"]
#             non_added_list = creature_list.copy()
#             encounter = []
#             while True:
#                 print(f"Creatures added: {encounter}")
#                 print("Which creature would you like to add to the encounter? Integer only!")
#                 print("0: End")
#                 for creature_key in non_added_list:
#                     creature = non_added_list[creature_key]
#                     print(f"{creature_key}: Name: {creature[0]}, Health: {creature[1]}, Initiative: {creature[2]}, Notes: {creature[3]}")
#                 chosen = int(input())
#                 if chosen == 0:
#                     print("Done")
#                     break
#                 encounter.append(non_added_list[str(chosen)]) 
#                 non_added_list.pop(str(chosen))
#                 if len(non_added_list) == 0:
#                     print("All creatures added!")
#                     break
#             encounter_amount += 1
#             encounter_list[encounter_amount] = encounter
#             user_objects["encounter_amount"] = encounter_amount
#             user_objects["encounter_list"] = encounter_list
#             with open(f"{user}.json", "w") as file:
#                 json.dump(user_objects, file)
#         else:
#             print("Sorry, but it seems you have no creatures, please make some and then try again.")

# #Using a made encounter
# def e_use():
#     if f"{user}.json" in files:
#         with open(f"{user}.json", "r") as file:
#             user_objects = json.load(file)
#         encounter_list = user_objects["encounter_list"]
#         encounter_amount = user_objects["encounter_amount"]
#         if encounter_amount == 0:
#             print("Sorry, but we could not find any encounters in your file. \nTry making an encounter.")
#         else:
#             print("Which encounter would you like to use:")
#             for object in encounter_list:
#                 print(f"{str(object)}: {encounter_list[object]}")
#             encounter_choice = input("")
#             encounter = encounter_list[encounter_choice]
#             initiative_tracking = {}
#             for creature in encounter:
#                 name = creature[0]
#                 initiative = random.randint(1,20) + creature[1]
#                 while initiative in initiative_tracking:
#                     initiative = random.randint(1,20) + creature[1]
#                 health = creature[2]
#                 notes = creature[3]
#                 initiative_tracking[initiative] = [creature]

#             playing = True
#             while playing:
#                 for key in sorted(initiative_tracking.keys(), reverse=True):
#                     if playing == False:
#                         break
#                     active = True
#                     while active:
#                         print(f"It is {initiative_tracking[key][0][0]}'s turn! \nWhat would you like to do? \nCommands:(H: Heal Self, D: Damage, N: Next, E: End)")
#                         action = input("")
#                         if action.lower() == "h":
#                             print(f"{initiative_tracking[key][0][0]} is at {initiative_tracking[key][0][2]} health.")
#                             print("For how much would you like heal for? (Integers only!)")
#                             health_healed = int(input(""))
#                             initiative_tracking[key][0][2] = str(health_healed + int(initiative_tracking[key][0][2]))
#                             print(f"{initiative_tracking[key][0][0]} is now at {initiative_tracking[key][0][2]} health.")
#                         elif action.lower() == "d":
#                             print(f"{initiative_tracking[key][0][0]} is at {initiative_tracking[key][0][2]} health.")
#                             print("For how much damage would you like to do? (Integers only!)")
#                             damage_dealt = int(input(""))
#                             initiative_tracking[key][0][2] = str(int(initiative_tracking[key][0][2]) - damage_dealt)
#                             print(f"{initiative_tracking[key][0][0]} is now at {initiative_tracking[key][0][2]} health.")
#                         elif action.lower() == "n":
#                             active = False
#                         elif action.lower() == "e":
#                             playing = False
#                             active = False
#     else:
#         print("Sorry, but we could not find a file with your name. \nTry making a creature.")

# LEAVE AT BOTTOM
client.run(TOKEN)