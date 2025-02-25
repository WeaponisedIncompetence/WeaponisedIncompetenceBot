import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import discord.utils
import pymongo
import pymongo.mongo_client

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
myclient = pymongo.MongoClient(os.environ["MONGODB_URI"])

bot = commands.Bot(intents=intents)
guild = bot.get_guild(1276103481287249990)
mydb = myclient["Weaponised_Incompetence"]
bottoken = os.environ["DISCORD_TOKEN"]


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


##Running a sim explanation


@bot.slash_command(
    name="howtosim",
    description="Help me run and import a sim into WoWAudit",
    guild_ids=[1276103481287249990],
)
async def howtosim(ctx):
    await ctx.respond(
        "Hi there, "
        + ctx.author.display_name
        + "! I understand that somebody is unsure how to sim properly. Please find below an explanation on how to get this working. If anyone else needs assistance, please type /helpsim."
    )
    embed1 = discord.Embed(
        title="How to sim & import to WowAudit",
        url="https://wowaudit.com/eu/draenor/weaponised-incompetence/main/wishlists/personal",
        description="This is a short tutorial on how to get your sim data into the WoWAudit system.",
    )
    embed1.add_field(
        name="Step 1",
        value="Navigate to [our WoWAudit sims submission page](https://wowaudit.com/eu/draenor/weaponised-incompetence/main/wishlists/personal). Taking note of the text below the submission box.",
        inline=True,
    )
    embed1.set_image(url="https://i.imgur.com/riAll6X.png")
    embed2 = discord.Embed()
    embed2.add_field(
        name="Step 2",
        value="If you are a DPS or Tank player, navigate to [RaidBots](https://www.raidbots.com/simbot). If you are a Healer, you will be headed to [QuestionablyEpic](https://questionablyepic.com/live/). For the purposes of this tutorial, we will use the RaidBots interface.",
        inline=True,
    )
    embed3 = discord.Embed()
    embed3.add_field(
        name="Step 3",
        value="Making sure you have the [Simulationcraft](https://www.curseforge.com/wow/addons/simulationcraft) addon installed, log into WoW and type /simc in the chatbox, making sure you copy the output.",
        inline=True,
    )
    embed4 = discord.Embed()
    embed4.add_field(
        name="Step 4",
        value="Now that you have your simc text string, navigate to submitting a sum using the Droptimiser feature within Raidbots or the Upgrade Finder feature in QuestionablyEpic, pasting your simc text into the box at the top of the screen, or top right for QE.",
        inline=True,
    )
    embed5 = discord.Embed()
    embed5.add_field(
        name="Step 5",
        value="Once you have done this, scroll down until you find the Simulation Options section, which looks like the image below. Make sure you copy the settings we looked at in step 1, or your sim will not be accepted. Once this has been done, and the correct Source and raid difficulty have been set, run the sim.",
    )
    embed5.set_image(url="https://i.imgur.com/kNpgklH.png")
    embed6 = discord.Embed()
    embed6.add_field(
        name="Step 6",
        value='Once this has been run, find the "Share Report URL" button and go back to the [WoWAudit](https://wowaudit.com/eu/draenor/weaponised-incompetence/main/wishlists/personal) tab we opened in step 1. Simply dump your link in the text box and click go. Any errors will be displayed in red immediately below the textbox - they are fairly self explanatory. Provided you have followed the steps correctly, when you click go, you should get a green message. Import successful. Repeat this process for multiple difficulties as necessary. ',
    )
    embed6.set_image(url="https://i.imgur.com/rgfrZVI.png")
    await ctx.respond(
        embeds=(embed1, embed2, embed3, embed4, embed5, embed6), ephemeral=True
    )


##Chat Purge


@bot.slash_command(
    name="clearchat",
    description="Purges chat. Must have the Administrator role to action",
    guild_ids=[1276103481287249990],
)
async def clearchat(ctx, number: int):
    if ctx.author.guild_permissions.administrator:
        limit = int(51)
        if number > limit:
            await ctx.respond(
                "I can only delete up to 50 messages at a time. This is to ensure I don't nuke entire channels. If you wish to do this and have permissions, simply right click -> duplicate channel and delete the original one",
                ephemeral=True,
            )
        elif number < limit:
            await ctx.channel.purge(limit=number)
            await ctx.respond(
                "Purged " + str(number) + " chat messages.", ephemeral=True
            )
    else:
        await ctx.respond("You do not have clearance to do this.", ephemeral=True)


##ProfessionCheck


@bot.slash_command(
    name="professioncheck",
    description="Returns a list of members with the given profession role",
    guild_ids=[1276103481287249990],
)
async def professioncheck(
    ctx: discord.ApplicationContext,
    profession: discord.Option(
        str,
        choices=[
            "Alchemy",
            "Blacksmithing",
            "Enchanting",
            "Engineering",
            "Inscription",
            "Jewelcrafting",
            "Leatherworking",
            "Tailoring",
        ],
    ),  # type: ignore
):
    if discord.utils.get(ctx.guild.roles, name=profession):
        serverrole = discord.utils.get(ctx.guild.roles, name=profession)
        members_list = "\n".join(str(member.mention) for member in serverrole.members)
        await ctx.respond(
            f"The users with the {profession} role are: \n{members_list}",
            ephemeral=True,
        )
    else:
        await ctx.respond(
            f"No members currently in the {profession} role", ephemeral=True
        )


## Sim reminder


@bot.slash_command(name="prompthowtosim", guild_ids=[1276103481287249990])
async def prompthowtosim(ctx):
    await ctx.channel.send(
        "Need to know how to sim? Type /helpsim for detailed instructions."
    )


@bot.slash_command(name="commands", guild_ids=[1276103481287249990])
async def help(ctx):
    sname = ctx.guild.name
    embed = discord.Embed(title=sname, url="", description="Help")
    embed.add_field(
        name="Click below for a list of bot commands.",
        value="[Click Here](https://github.com/WeaponisedIncompetence/WeaponisedIncompetenceBot/blob/main/README.md)",
    )

    await ctx.respond(embed=embed, ephemeral=True)


## Approving trial automation


@bot.slash_command(name="trialapproved", guild_ids=[1276103481287249990])
async def trialApproved(ctx, name: discord.Member):
    officerRole = discord.utils.get(ctx.guild.roles, name="Officer")
    leadershipRole = discord.utils.get(ctx.guild.roles, name="Leadership")
    if (officerRole in ctx.author.roles) or (leadershipRole in ctx.author.roles):
        if discord.utils.get(name.roles, name="Trial Request"):
            roleToAdd = discord.utils.get(ctx.guild.roles, name="Trial")
            roleToRemove = discord.utils.get(ctx.guild.roles, name="Trial Request")
            await name.add_roles(roleToAdd)
            await name.remove_roles(roleToRemove)
            channel = discord.utils.get(ctx.guild.channels, name="trial-request")
            guildChat = discord.utils.get(ctx.guild.channels, name="guild-chat")
            raidTalk = discord.utils.get(ctx.guild.channels, name="raid-talk")
            raidAnnouncements = discord.utils.get(
                ctx.guild.channels, name="raid-announcements"
            )
            await channel.send(
                f"Welcome to the guild as a trial, {name.mention}. Please post in the {guildChat} or {raidTalk} channels with your character name, server and faction to get an invite once you're online. Information about our raid can be found in the {raidAnnouncements} channel, or elsewhere in this section."
            )

    await ctx.send(f"asd")


##Trial request message


@bot.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
        newRole = next(role for role in after.roles if role not in before.roles)
        if newRole.name == "Trial Request":
            channel = discord.utils.get(before.guild.channels, name="trial-request")
            currentMember = discord.utils.get(after.guild.members, id=after.id)
            await channel.send(
                f"Hi there {currentMember.mention}, I see you have requested the "
                "Trial Request"
                " role. Please submit a trial request by clicking at the top of this channel and an officer will be with you in due course. This notification will be automatically deleted after 48 hours. Alternatively, if this was a mistake, please return to the {id:customize} channel. ",
                delete_after=172800,
            ),
    if len(after.roles) < len(before.roles):
        lostRole = next(role for role in before.roles if role not in after.roles)
        if lostRole.name == "Trial Request":
            channel = discord.utils.get(before.guild.channels, name="trial-request")
            currentMember = discord.utils.get(after.guild.members, id=after.id)
            async for message in channel.history(limit=None):
                if (
                    f"Hi there {currentMember.mention}, I see you have requested the "
                    "Trial Request"
                    ""
                ) in message.content:
                    await message.delete()


bot.run(bottoken)
