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

role_list = [
    'General Member',
    'Active Member',
    'Loyal Member',
    'Official Member',
    'Krazy Member',
    'Insane Member',
    'Prodigy Member',
    'Immortal Member',
    'Legendary Member',
    'Champion Member'
]


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

    elif count % 50 == 0.0:
        level = count / 50 # Simple math to determine level
        if level % 10 == 0: 
            try:
                role = discord.utils.get(message.guild.roles, name=role_list[int((level/10))-1])
                await message.author.add_roles(role)
                await message.channel.send(f'Congratulations {message.author.mention}! You have been awarded the {role.name} role for earning level **{level}**!')
            except:
                print("We couldn't find the role or something")

        else:
                # Get the announcement channel
                announcement_channel = bot.get_channel(announcement_channel_id)
            
                if announcement_channel:
                    # Send announcement message
                    await announcement_channel.send(f'{message.author.mention} has reached level **{level}**. GG!')
                else:
                    print("We couldn't find the channel or something")

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

@bot.command()
async def leaderboard(ctx):
    with open('message_count.json', 'r') as f:
        message_count = json.load(f)
        
    # Sort the message count dictionary by values (message counts) in descending order
    sorted_message_count = dict(sorted(message_count.items(), key=lambda item: item[1], reverse=True))

    # Create an embed
    embed = discord.Embed(title="Message Leaderboard", color=0xde852a)
    
    # Add top 10 users to the embed
    count = 0
    for user_id, message_count in sorted_message_count.items():
        user = bot.get_user(int(user_id))
        if user is not None:
            count += 1
            # Convert message count to levels
            level = message_count // 50
            embed.add_field(name=f"#{count} • {user.name} • LVL: {level}", value='', inline=False)
        if count == 10:
            break
    
    # Send the embed
    await ctx.send(embed=embed)

#damn brit token
bot.run("")
