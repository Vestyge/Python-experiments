import discord
import asyncio
import json
import sys

description = '''Starblast Event Server Bot'''
client = discord.Client()

def init():
    global config
    global conf_file
    # more genearl solution for handeling args may be good, but this will do for now.
    #defaulting to dev means people are less likely to accidentally cause a mess by running things in production.
    conf_file = 'dev'
    if "--conf" in sys.argv:
        #This is bad pratice. Deal with it :P
        conf_file = sys.argv[sys.argv.index("--conf") + 1]
    #Opens the file
    with open(conf_file + '.json') as conf_data:
        try:
            config = json.load(conf_data)
            print("Configuration from " + conf_file + '.json as been read!')
        except:
            print("Unable to find or read configuration file, quitting.")
            exit()
            
init()           
#allows us to close off team swapping
teamJoinOpen = True
    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="Starblast.io"))

def getTeams(server):
    blue = discord.utils.get(server.roles, id=config['teams']['blue'])
    red = discord.utils.get(server.roles, id=config['teams']['red'])
    green = discord.utils.get(server.roles, id=config['teams']['green'])
    purple = discord.utils.get(server.roles, id=config['teams']['purple'])
    yellow = discord.utils.get(server.roles, id=config['teams']['yellow'])
    teams = {
    'blue' : blue,
    'red' : red,
    'green': green,
    'purple': purple,
    'yellow': yellow
    }
    return teams

@client.event
async def on_message(message):
    #filter message
    if (not(message.author.id in config['admins']) and ("discord.gg" in message.content)):
        await client.delete_message(message)
        
        
    #define team roles, as well as a list of teams to permit looping
    global teamJoinOpen
    if message.server == None:
        return
    teams = getTeams(message.server)
    #admin only commands
    if message.author.id in config['admins']:
        if message.content.startswith('!clear'):
            tmp = await client.send_message(message.channel, 'Clearing messages...')
            async for msg in client.logs_from(message.channel):
                await client.delete_message(msg)
        elif message.content.startswith('!time'):
            time = int(message.content[6:9]) * 60
            default = client.get_channel(config['channels']['announcements'])
            await asyncio.sleep(time)
            await client.send_message(default, message.content[9:])
        elif message.content.startswith('!tell'):
            default = client.get_channel(config['channels']['announcements'])
            await client.send_message(default, message.content[6:])
        elif message.content.startswith('!echo'):
            default = client.get_channel(config['channels']['general'])
            await client.send_message(default, message.content[6:])
        elif message.content.startswith('!lock'):
            teamJoinOpen = False
            await client.send_message(message.channel, "Roll assignemtns have been locked")
        elif message.content.startswith('!unlock'):
            teamJoinOpen = True
            await client.send_message(message.channel, "Roll assignemtns have been locked")
        elif message.content.startswith('!batch'):
            role = message.content[7:]
            for member in client.get_all_members():
                try:
                    await client.add_roles(member,teams[role])
                except BaseException as e:
                    print(e)
                    pass
        elif message.content.startswith('!assign all'):
            assignCount = 0;
            for member in list(message.server.members):
                try:
                    needsRole = True
                    for role in member.roles:
                        if role.name.lower() in teams:
                            needsRole = False
                    if needsRole:        
                        await assignToLowestTeam(member)
                        assignCount += 1;
                except BaseException as e:
                    print(e)
                    pass
            await client.send_message(message.channel,"All users have been assigned. {0} members were assigned".format(assignCount));
        elif message.content.startswith('!DM '):
            dmCount = 0;
            userCount = 0;
            for member in list(message.server.members):
                userCount += 1;
                try:
                    await client.send_message(member, message.content[4:])
                    dmCount += 1
                    if dmCount % 100 == 0:
                        await client.send_message(message.channel,"So far {0} of {1} members were messaged".format(dmCount,userCount));
                except:
                    pass
            await client.send_message(message.channel,"All users have been messaged. {0} of {1} members were messaged".format(dmCount,userCount));
                    
    #team join commands
    for team, data in teams.items():
        if message.content.lower().startswith('!' + team) and (teamJoinOpen or message.author.id in config['admins']):
            try:
                await client.add_roles(message.author, data)
            except:
                pass
            for key, value in teams.items():
                if key != team:
                    try:
                        await client.remove_roles(message.author, value)
                    except:
                        pass
            #throws error, but works. No idea why.
            await client.delete_message(message)

async def assignToLowestTeam(member):
    teams = getTeams(member.server)
    counts = {}
    for team, role in teams.items():
        counts[team] = 0
    for n_member in client.get_all_members():
        for team, role in teams.items():
            if role in n_member.roles:
                counts[team] += 1
    lowest_team = min(counts, key=counts.get)
    try:
        await client.add_roles(member,teams[lowest_team])
        await client.send_message(member,("Welcome to the  Starblast.io Team Mode Event Server! you have been automatically assigned to the **{0} team**. \n" + 
        "While the {0} team is awesome, if it does not suit your fancy, you can change your team by typing `![team]` into the general chat. \n\n" +
        "**Warning:** You will only be able to join the voice chat for the team you are a member of. If you join the wrong team during the event, you will be unable to communicate with other players on your team").format(lowest_team)) 
    except:
        pass   

@client.event
async def on_member_join(member):
    server = member.server
    log = client.get_channel(config['channels']['log'])
    em = discord.Embed(title='Greetings, ' + member.name + '!', description='Welcome to the Starblast.io Team Mode Event Server! Be prepared for the Battle of Alpha Centauri, pilot!', colour=0x0065fd)
    em.set_author(name=member.name, icon_url=client.user.default_avatar_url)
    await client.send_message(log, embed=em)
    await assignToLowestTeam(member)

@client.event
async def on_member_remove(member):
    server = member.server
    log = client.get_channel(config['channels']['log'])
    em = discord.Embed(title='Goodbye, ' + member.name + '!', description=member.name + ' has left the server.',
                       colour=0x0065fd)
    em.set_author(name=member.name, icon_url=client.user.default_avatar_url)
    await client.send_message(log, embed=em)

##@client.event
##async def on_voice_state_update(before, after):
##    red = discord.utils.get(before.server.roles, id='306088323221422081')
##    blue = discord.utils.get(before.server.roles, id='306088088076288003')
##    green = discord.utils.get(before.server.roles, id='306088361339125771')
##    purple = discord.utils.get(before.server.roles, id='306088382222565377')
##    yellow = discord.utils.get(before.server.roles, id='331489325550141441')
##    #log = client.get_channel("306087546872528896")
##    #pilot = discord.utils.get(before.server.roles, id='320783951612608523')
##
##    if not before.voice == after.voice:
##        try:
##            if after.voice_channel.id == "306089087624806401":
##                await client.add_roles(after, red)
##                await client.remove_roles(after, blue, green, purple, yellow)
##                #await client.send_message(log, "{0.mention} has joined Team Red!".format(after))
##            if after.voice_channel.id == "306089139931971586":
##                await client.add_roles(after, blue)
##                await client.remove_roles(after, red, green, purple, yellow)
##                #await client.send_message(log, "{0.mention} has joined Team Blue!".format(after))
##            if after.voice_channel.id == "306089111356178432":
##                await client.add_roles(after, green)
##                await client.remove_roles(after, blue, red, purple, yellow)
##                #await client.send_message(log, "{0.mention} has joined Team Green!".format(after))
##            if after.voice_channel.id == "306089017991233536":
##                await client.add_roles(after, purple)
##                await client.remove_roles(after, blue, red, green, yellow)
##                #await client.send_message(log, "{0.mention} has joined Team Purple!".format(after))
##            if after.voice_channel.id == "331489699975790603":
##                await client.add_roles(after, yellow)
##                await client.remove_roles(after, blue, red, green, purple)
##                #await client.send_message(log, "{0.mention} has joined Team Yellow!".format(after))s
##        except AttributeError:
##            pass


client.run(config['token'])

