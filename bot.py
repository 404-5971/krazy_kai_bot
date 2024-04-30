import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Load the JSON file or create a new one if it doesn't exist
def load_data():
    try:
        with open('message_count.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create it with an empty dictionary
        save_data({})
        return {}

# Save data to the JSON file
def save_data(data):
    with open('message_count.json', 'w') as file:
        json.dump(data, file, indent=4)

announcement_channel_id = 1195406286297243679

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency is {latency}ms')

@bot.event
async def on_member_join(member):
    channel=bot.get_channel(1195413648244486215)
    await channel.send(f'{member.mention} joined the server!')

# Event: When a message is sent
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Load data
    data = load_data()
    
    # Increment message count for the user
    user_id = str(message.author.id)
    count = data.get(user_id, 0) + 1
    data[user_id] = count
    
    # Check if the user has sent 250 messages
    if count == 250:
        # Get the role to assign
        role = discord.utils.get(message.guild.roles, name="Affilate Member")
        if role:
            # Assign the role to the user
            await message.author.add_roles(role)
            await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **5**!')

    elif count == 500:
        role = discord.utils.get(message.guild.roles, name="General Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **10**!')

    elif count == 1000:
        role = discord.utils.get(message.guild.roles, name="Active Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **20**!')

    elif count == 1500:
        role = discord.utils.get(message.guild.roles, name="Loyal Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **30**!')
        
    elif count == 2000:
        role = discord.utils.get(message.guild.roles, name="Official Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **40**!')

    elif count == 2500:
        role = discord.utils.get(message.guild.roles, name="Krazy Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **50**!')

    elif count == 3000:
        role = discord.utils.get(message.guild.roles, name="Insane Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **60**!')

    elif count == 3500:
        role = discord.utils.get(message.guild.roles, name="Prodigy Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **70**!')

    elif count == 4000:
        role = discord.utils.get(message.guild.roles, name="Immortal Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **80**!')

    elif count == 4500:
        role = discord.utils.get(message.guild.roles, name="Legendary Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **90**!')

    elif count == 5000:
        role = discord.utils.get(message.guild.roles, name="Legendary Member")
        await message.author.add_roles(role)
        await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **100**!')

    # Check if the user has sent a multiple of 50 messages
    if count % 50 == 0:
        # Calculate the level
        level = count // 50
        
        # Get the announcement channel
        announcement_channel = bot.get_channel(announcement_channel_id)
        
        if announcement_channel:
            # Send announcement message
            await announcement_channel.send(f'{message.author.mention} has reached level **{level}**. GG!')
    
    # Save data
    save_data(data)
    
    await bot.process_commands(message)

# Command: Check message count
@bot.command()
async def message_count(ctx):
    data = load_data()
    user_id = str(ctx.author.id)
    count = data.get(user_id, 0)
    await ctx.send(f'You have sent {count} messages.')

bot.run("MTIzNDYzMjcxNDUxNTI1MTIyMA.GT4zEY.PA9Jge04fnEUt2_1K_T_O-w0gwnOGXbFML4q1Q")