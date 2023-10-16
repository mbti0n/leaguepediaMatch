from mwrogue.esports_client import EsportsClient
import datetime as dt
from datetime import datetime
import re
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

date = datetime.utcnow().date()

site = EsportsClient("lol")
getScore = site.cargo_client.query(
    tables="ScoreboardGames=SG, Tournaments=T",
    join_on="SG.OverviewPage=T.OverviewPage",
    fields="SG.OverviewPage, SG.DateTime_UTC, SG.Tournament, SG.Team1Gold, SG.Team2Gold, SG.Team1Score, SG.Team1Dragons, SG.Team2Dragons, SG.Team1Barons, SG.Team2Barons, SG.Team1Towers, SG.Team2Towers, SG.Team1Kills, SG.Team2Kills, SG.Team2Score, SG.Gamelength, SG.Team1Bans, SG.Team2Bans, SG.Winner, SG.VOD, SG.Team1Players, SG.Team2Players, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.Patch, SG.GameId, SG.Team1Picks, SG.Team2Picks",
    where=f"SG.DateTime_UTC >= '{str(date-dt.timedelta(1))} 00:00:00' AND SG.DateTime_UTC <= '{str(date+dt.timedelta(1))} 00:00:00' AND SG.Tournament LIKE 'Worlds%'"
)

getPlayer = site.cargo_client.query(
    tables="ScoreboardGames=SG, ScoreboardPlayers=SP, Tournaments=T",
    join_on="SG.GameId=SP.GameId, SP.OverviewPage=T.OverviewPage",
    fields="SG.Tournament, SP.GameId, SP.Champion, SP.Link, SP.Role, SP.CS, SP.Kills, SP.Deaths, SP.Assists, SP.DamageToChampions, SP.SummonerSpells, SP.KeystoneRune, SP.SecondaryTree",
    where=f"SG.DateTime_UTC >= '{str(date-dt.timedelta(1))} 00:00:00' AND SG.DateTime_UTC <= '{str(date+dt.timedelta(1))} 00:00:00' AND SG.Tournament LIKE 'Worlds%'"
)

processed_player1 = []
processed_player2 = []
player = []
champion = []
role = []
gameId = []
cs = []
kills = []
deaths = []
assists = []
damage = []
spells = []
keystoneRune = []
secondaryTree = []

for i in range (0, len(getPlayer)):
    # Player name
    if "(" in getPlayer[i]['Link']:
        getPlayer[i]['Link'] = re.sub(r'\s*\([^)]*\)', '', getPlayer[i]['Link'])
    player.append(getPlayer[i]['Link'])

    champion.append(getPlayer[i]['Champion'])
    role.append(getPlayer[i]['Role'])
    gameId.append(getPlayer[i]['GameId'])
    cs.append(getPlayer[i]['CS'])
    kills.append(getPlayer[i]['Kills'])
    deaths.append(getPlayer[i]['Deaths'])
    assists.append(getPlayer[i]['Assists'])
    
    # Damage dealt
    dmg = str(getPlayer[i]['DamageToChampions'])
    getDamage = re.sub("\D", "", dmg)
    dmg = str(format(int(getDamage),',d'))
    damage.append(dmg)

    # Spells
    getSpells = re.sub(",", " ", getPlayer[i]['SummonerSpells'])    
    if "Barrier" in getSpells:
        getSpells = re.sub("Barrier", "<:barrier:1148340195649929327>", getSpells)
    if "Cleanse" in getSpells:
        getSpells = re.sub("Cleanse", "<:cleanse:1148340197235380284>", getSpells)
    if "Ignite" in getSpells:
        getSpells = re.sub("Ignite", "<:ignite:1148340202595684424>", getSpells)
    if "Exhaust" in getSpells:
        getSpells = re.sub("Exhaust", "<:exhaust:1148340198397198456>", getSpells)
    if "Flash" in getSpells:
        getSpells = re.sub("Flash", "<:flash:1148340199282196540>", getSpells)
    if "Ghost" in getSpells:
        getSpells = re.sub("Ghost", "<:ghost_haste:1148340200053936188>", getSpells)
    if "Heal" in getSpells:
        getSpells = re.sub("Heal", "<:heal:1148340201098330243>", getSpells)
    if "Smite" in getSpells:
        getSpells = re.sub("Smite", "<:smite:1148340203828817930>", getSpells)
    if "Teleport" in getSpells:
        getSpells = re.sub("Teleport", "<:teleport:1148340238545068165>", getSpells)
    spells.append(getSpells)
    
    # Keystone rune
    getKeystoneRune = getPlayer[i]['KeystoneRune']
    if "Press the Attack" in getKeystoneRune:
        getKeystoneRune = re.sub("Press the Attack", "<:PressTheAttack:1148359370187472986>", getKeystoneRune)
    if "Lethal Tempo" in getKeystoneRune:
        getKeystoneRune = re.sub("Lethal Tempo", "<:LethalTempo:1148359365095604224>", getKeystoneRune)
    if "Fleet Footwork" in getKeystoneRune:
        getKeystoneRune = re.sub("Fleet Footwork", "<:FleetFootwork:1148359280676839584>", getKeystoneRune)
    if "Conqueror" in getKeystoneRune:
        getKeystoneRune = re.sub("Conqueror", "<:Conqueror:1148359273907241083>", getKeystoneRune)
    if "Electrocute" in getKeystoneRune:
        getKeystoneRune = re.sub("Electrocute", "<:Electrocute:1148359277078130690>", getKeystoneRune)
    if "Predator" in getKeystoneRune:
        getKeystoneRune = re.sub("Predator", "<:Predator:1148359289761697872>", getKeystoneRune)
    if "Dark Harvest" in getKeystoneRune:
        getKeystoneRune = re.sub("Dark Harvest", "<:DarkHarvest:1148359275727573042>", getKeystoneRune)
    if "Hail of Blades" in getKeystoneRune:
        getKeystoneRune = re.sub("Hail of Blades", "<:HailOfBlades:1148359286712438805>", getKeystoneRune)
    if "Summon Aery" in getKeystoneRune:
        getKeystoneRune = re.sub("Summon Aery", "<:SummonAery:1148359372364316785>", getKeystoneRune)
    if "Arcane Comet" in getKeystoneRune:
        getKeystoneRune = re.sub("Arcane Comet", "<:ArcaneComet:1148359271583584267>", getKeystoneRune)
    if "Phase Rush" in getKeystoneRune:
        getKeystoneRune = re.sub("Phase Rush", "<:PhaseRush:1148359366135791796>", getKeystoneRune)
    if "Glacial Augment" in getKeystoneRune:
        getKeystoneRune = re.sub("Glacial Augment", "<:GlacialAugment:1148359282581045329>", getKeystoneRune)
    if "Unsealed Spellbook" in getKeystoneRune:
        getKeystoneRune = re.sub("Unsealed Spellbook", "<:UnsealedSpellbook:1148359373601652896>", getKeystoneRune)
    if "First Strike" in getKeystoneRune:
        getKeystoneRune = re.sub("First Strike", "<:FirstStrike:1148359279347257354>", getKeystoneRune)
    if "Grasp of the Undying" in getKeystoneRune:
        getKeystoneRune = re.sub("Grasp of the Undying", "<:GraspOfTheUndying:1148359283969363988>", getKeystoneRune)
    if "Aftershock" in getKeystoneRune:
        getKeystoneRune = re.sub("Aftershock", "<:VeteranAftershock:1148359293205225543>", getKeystoneRune)
    if "Guardian" in getKeystoneRune:
        getKeystoneRune = re.sub("Guardian", "<:Guardian:1148359285177323571>", getKeystoneRune)
    keystoneRune.append(getKeystoneRune)
    
    # Secondary tree
    getSecondaryTree = getPlayer[i]['SecondaryTree']
    if "Precision" in getSecondaryTree:
        getSecondaryTree = re.sub("Precision", "<:precision:1148354767660265554>", getSecondaryTree)
    if "Domination" in getSecondaryTree:
        getSecondaryTree = re.sub("Domination", "<:domination:1148354765756059649>", getSecondaryTree)
    if "Sorcery" in getSecondaryTree:
        getSecondaryTree = re.sub("Sorcery", "<:sorcery:1148354768725626920>", getSecondaryTree)
    if "Inspiration" in getSecondaryTree:
        getSecondaryTree = re.sub("Inspiration", "<:inspiration:1148354770332041389>", getSecondaryTree)
    if "Resolve" in getSecondaryTree:
        getSecondaryTree = re.sub("Resolve", "<:resolve:1148354771984588942>", getSecondaryTree)
    secondaryTree.append(getSecondaryTree)
    
    # Player info dictionary
    playerInfo = [
    {'GameId': gameId, 'Player': player, 'Champion': champion, 'Role': role, 'CS': cs, 'Kills': kills, 'Deaths': deaths, 'Assists': assists, 'Damage': damage, 'Spells': spells, 'KeystoneRune': keystoneRune, 'SecondaryTree': secondaryTree}
    for gameId, player, champion, role, cs, kills, deaths, assists, damage, spells, keystoneRune, secondaryTree in zip(gameId, player, champion, role, cs, kills, deaths, assists, damage, spells, keystoneRune, secondaryTree)
    ]
    


matchData = getScore[len(getScore)-1]
    
# Player names
player1 = matchData['Team1Players'].split(",")
for i in range (0, len(player1)):
    if "(" in player1[i]:
        player1[i] = re.sub(r'\s*\([^)]*\)', '', player1[i])
player2 = matchData['Team2Players'].split(",")
for i in range (0, len(player2)):
    if "(" in player2[i]:
        player2[i] = re.sub(r'\s*\([^)]*\)', '', player2[i])

# Picked champions
pick1 = matchData['Team1Picks'].split(",")
pick2 = matchData['Team2Picks'].split(",")

gameId = matchData['GameId']

# Team 1 Player data
listTeam1 = [{'Player': player1, 'Champion': pick1} for player1, pick1 in zip(player1, pick1)]
for i in range (0, len(playerInfo)):
    if playerInfo[i]['Player'] == listTeam1[0]['Player']:
        player1Data1 = f"**{listTeam1[0]['Player']} ({playerInfo[i]['Role']}):** {listTeam1[0]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"
    if playerInfo[i]['Player'] == listTeam1[1]['Player']:
        player1Data2 = f"**{listTeam1[1]['Player']} ({playerInfo[i]['Role']}):** {listTeam1[1]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"
    if playerInfo[i]['Player'] == listTeam1[2]['Player']:
        player1Data3 = f"**{listTeam1[2]['Player']} ({playerInfo[i]['Role']}):** {listTeam1[2]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"
    if playerInfo[i]['Player'] == listTeam1[3]['Player']:
        player1Data4 = f"**{listTeam1[3]['Player']} ({playerInfo[i]['Role']}):** {listTeam1[3]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"
    if playerInfo[i]['Player'] == listTeam1[4]['Player']:
        player1Data5 = f"**{listTeam1[4]['Player']} ({playerInfo[i]['Role']}):** {listTeam1[4]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"

team1Data = f"{player1Data1}\n{player1Data2}\n{player1Data3}\n{player1Data4}\n{player1Data5}\n"

# Team 2 Player data
listTeam2 = [{'Player': player2, 'Champion': pick2} for player2, pick2 in zip(player2, pick2)]
for i in range (0, len(playerInfo)):
    if playerInfo[i]['Player'] == listTeam2[0]['Player']:
        player2Data1 = f"**{listTeam2[0]['Player']} ({playerInfo[i]['Role']}):** {listTeam2[0]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"
    if playerInfo[i]['Player'] == listTeam2[1]['Player']:
        player2Data2 = f"**{listTeam2[1]['Player']} ({playerInfo[i]['Role']}):** {listTeam2[1]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"
    if playerInfo[i]['Player'] == listTeam2[2]['Player']:
        player2Data3 = f"**{listTeam2[2]['Player']} ({playerInfo[i]['Role']}):** {listTeam2[2]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"
    if playerInfo[i]['Player'] == listTeam2[3]['Player']:
        player2Data4 = f"**{listTeam2[3]['Player']} ({playerInfo[i]['Role']}):** {listTeam2[3]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"
    if playerInfo[i]['Player'] == listTeam2[4]['Player']:
        player2Data5 = f"**{listTeam2[4]['Player']} ({playerInfo[i]['Role']}):** {listTeam2[4]['Champion']} {playerInfo[i]['Spells']} {playerInfo[i]['KeystoneRune']}{playerInfo[i]['SecondaryTree']}\n{playerInfo[i]['Kills']}/{playerInfo[i]['Deaths']}/{playerInfo[i]['Assists']}, {playerInfo[i]['CS']} CS, {playerInfo[i]['Damage']} DMG"

team2Data = f"{player2Data1}\n{player2Data2}\n{player2Data3}\n{player2Data4}\n{player2Data5}\n"

# Duration
duration = matchData['Gamelength']

# Kills
kill1 = matchData['Team1Kills']
kill2 = matchData['Team2Kills']

# Golds
gold1 = str(matchData['Team1Gold'])
getGold1Raw = re.sub("\D", "", gold1)
gold1 = str(format(int(getGold1Raw),',d'))

gold2 = str(matchData['Team2Gold'])
getGold2Raw = re.sub("\D", "", gold2)
gold2 = str(format(int(getGold2Raw),',d'))

# Dragons
dragon1 = matchData['Team1Dragons']
dragon2 = matchData['Team2Dragons']

# Barons
baron1 = matchData['Team1Barons']
baron2 = matchData['Team2Barons']

# Towers destroyed
tower1 = matchData['Team1Towers']
tower2 = matchData['Team2Towers']

# Banned champions
ban1List = matchData['Team1Bans'].split(",")
ban2List = matchData['Team2Bans'].split(",")
ban1 = ', '.join(map(str, ban1List))
ban2 = ', '.join(map(str, ban2List))

# League name
leagueName = matchData['Tournament']
overview = matchData['OverviewPage']
stage = re.sub(rf"{overview}_(.*?)_.*", r'\1', gameId)

# Team names
team1 = matchData['Team1']
team2 = matchData['Team2']

# Score
score1 = matchData['Team1Score']
score2 = matchData['Team2Score']
score = f"{team1} ({score1}) {kill1}\n{team2} ({score2}) {kill2}"

# Patch
patch = matchData['Patch']

# Date and time
getDateTime = matchData['DateTime UTC']
dtime = datetime.strptime(getDateTime, '%Y-%m-%d %H:%M:%S')
dateTime = dtime.strftime('%B %d, %Y at %I:%M %p')

# Discord webhook
webhook = DiscordWebhook(url="") # Webhook URL
embed = DiscordEmbed(title=f"{score}", color="03b2f8")
embed.set_author(name=f"{leagueName}\n{stage}")
embed.set_footer(text=f"{dateTime} (UTC)")
embed.add_embed_field(name=f"Duration", value=f"{duration}")
embed.add_embed_field(name="Ban", value=f"**{team1}:** {ban1}\n**{team2}:** {ban2}", inline=False)
embed.add_embed_field(name=f"{team1}", value=f"{team1Data}")
embed.add_embed_field(name=f"{team2}", value=f"{team2Data}", inline=False)
embed.add_embed_field(name=f"Dragons/Baron", value=f"**{team1}:** {dragon1}/{baron1}\n**{team2}:** {dragon2}/{baron2}")
embed.add_embed_field(name=f"Towers", value=f"**{team1}:** {tower1}\n**{team2}:** {tower2}")
embed.add_embed_field(name=f"Gold", value=f"**{team1}:** {gold1}\n**{team2}:** {gold2}")
embed.add_embed_field(name="Patch", value=patch)
webhook.add_embed(embed)
response = webhook.execute()
time.sleep(1)