import os

import discord
from dotenv import load_dotenv

from discord.ext import commands

from pymongo import MongoClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

mongo_client = MongoClient(f"mongodb+srv://dev:{MONGO_PASSWORD}@cluster0.ulzen.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = mongo_client.get_database("discord-cas")

bot = commands.Bot(command_prefix=';')

VERIFIED_ROLE_NAME = "cas-verified"


async def is_verified(user_id):
    users = list(db.users.find({"user_id": str(user_id)}))
    print(users)
    return True if len(users) else False


async def assign_role(ctx, user):
    roles = ctx.guild.roles
    role_names = [role.name for role in roles]

    if VERIFIED_ROLE_NAME not in role_names:
        await ctx.guild.create_role(name=VERIFIED_ROLE_NAME)

    required_role = [role for role in roles if role.name == VERIFIED_ROLE_NAME]

    await user.add_roles(required_role[0])


@bot.command(name="verify")
async def verify_user(ctx):
    user_id = ctx.message.author.id
    verification = await is_verified(user_id)

    if verification:
        await assign_role(ctx, ctx.message.author)
        await ctx.send(f"Yayy verified")
    else:
        await ctx.send(f"Ew not verified.")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)