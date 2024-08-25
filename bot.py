import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Required if your bot processes messages

bot = commands.Bot(command_prefix='/', intents=intents)

channel_id = 1234567891234567891  # Replace this with your channel ID for the lists
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    bot.all_members = []  # Initialize an attribute for all members
    bot.reacted_members = set()  # Initialize an attribute for reacted members

@bot.slash_command(name='nuke_testing', description='BOOM.')
async def nuke_testing(ctx):
    list_channel = bot.get_channel(channel_id)
    if not list_channel:
        await ctx.respond("The specified channel for lists was not found.")
        return

    # Send the reaction message in the channel where the command was used
    message_reactions = await ctx.channel.send("React here.")
    await message_reactions.add_reaction('👍')

    members = ctx.guild.members
    bot.all_members = [member.display_name for member in members if not member.bot]
    member_list = '\n'.join(bot.all_members)

    # Embed for all members sent to the specified channel
    embed_members = discord.Embed(title="NUKE TIME 😈 | All Members", color=discord.Color.red())
    embed_members.add_field(name="All Members", value=member_list or "No members found.", inline=False)
    await list_channel.send(embed=embed_members)

    # Embed for reactions sent to the specified channel
    embed_reactions = discord.Embed(title="NUKE TIME 😈 | Members Who Reacted", color=discord.Color.red())
    embed_reactions.add_field(name="Members Who Reacted", value="No reactions yet.", inline=False)
    embed_reactions_msg = await list_channel.send(embed=embed_reactions)

    async def check_reactions():
        def check(reaction, user):
            return user != bot.user and str(reaction.emoji) == '👍' and user.display_name not in bot.reacted_members and reaction.message.id == message_reactions.id

        while True:
            reaction, user = await bot.wait_for('reaction_add', check=check)
            bot.reacted_members.add(user.display_name)
            current_reactions = '\n'.join(bot.reacted_members)
            new_embed = discord.Embed(title="NUKE TIME 😈 | Members Who Reacted", color=discord.Color.red())
            new_embed.add_field(name="Members Who Reacted", value=current_reactions or "No reactions yet.", inline=False)
            await embed_reactions_msg.edit(embed=new_embed)

    bot.loop.create_task(check_reactions())

@bot.slash_command(name='finalize', description='Finalize the member listing.')
async def finalize(ctx):
    list_channel = bot.get_channel(channel_id)
    if not list_channel:
        await ctx.send("The specified channel for lists was not found.")
        return

    non_reacted_members = '\n'.join(member for member in bot.all_members if member not in bot.reacted_members)
    embed_final = discord.Embed(title="NUKE TIME 😈 | Non-reacted Members", description=non_reacted_members or "All members reacted.", color=discord.Color.green())
    await list_channel.send(embed=embed_final)

bot.run('')  # Ensure to replace this with your token
