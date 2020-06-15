import random
import threading
import time
import gc
import math
# Init player controller variables
global statselect
statselect = {'Str': 0, 'Dex': 0, 'Con': 0, 'Int': 0, 'Wis': 0, 'Cha': 0}

# Init Player Class
class player(object):
    def __init__(self, name, occupation, desc, maxhp, hp, inv, stats, skills, carryweight, armor, armoreq, weapon):
        self.name = name
        self.occupation = occupation
        self.desc = desc
        self.maxhp = maxhp
        self.hp = hp
        self.inv = inv
        self.stats = stats
        self.skills = skills
        self.carryweight = carryweight
        self.armor = armor
        self.armoreq = armoreq
        self.weapon = weapon
        
    def defaultattributes(self):
        self.name = 'John Doe'
        self.occupation = NoOccupation
        self.desc = {'sex': 'male', 'height': 84, 'eyecolor': 'brown', 'haircolor': 'brown', 'build': 'swole', 'pasttime': 'long walks on the beach'}
        self.maxhp = 5
        self.hp = self.maxhp
        self.inv = []
        self.stats = {'Str': 10, 'Dex': 10, 'Con': 10, 'Int': 10, 'Wis': 10, 'Cha': 10}
        self.skills = []
        self.carryweight = 50
        self.armoreq = {'Headgear': NoArmor, 'Chest': NoArmor, 'Arms': NoArmor, 'Legs': NoArmor, 'Feet': NoArmor, 'Bonus': NoArmor}
        self.armor = [0, 0]
        self.weapon = Greatclub
    def armorcalc(self):
        # Match Current Armor Value to Reflect Equipped Armor and Occupation Bonuses
        physarmor = 0
        for physical in self.armoreq:
            physarmor = physarmor + self.armoreq[physical].phys_prot
        self.armor[0] = physarmor
        self.armor[0] = int(self.armor[0] + self.occupation.resistance[0] + (math.floor(self.stats['Dex']/5)))
        
        magarmor = 0
        for magical in self.armoreq:
            magarmor = magarmor + self.armoreq[magical].magic_prot
        self.armor[1] = magarmor
        self.armor[1] = int(self.armor[1] + self.occupation.resistance[1] + (math.floor(self.stats['Dex']/5)))

        # hardupdate makes sure that the current player attributes are reflected by stats and currently equipped items and armor
    def hardupdate(self):
        self.maxhp = 5 + 2 * self.stats['Con']
        self.hp = self.maxhp
        self.carryweight = 5 * self.stats['Str']
        self.armorcalc()
        
        # Match Statbonuses to Reflect Current Occupation
        statadd = {'Str': 10, 'Dex': 10, 'Con': 10, 'Int': 10, 'Wis': 10, 'Cha': 10}
        for key in statadd:
            statadd[key] = statadd[key] + statselect[key]
            try:
                statadd[key] = statadd[key] + self.occupation.statbonus[key]
            except KeyError:
                pass
        self.stats = statadd.copy()
            
        # Match Inventory to Reflect Starting Equipment
        for item in self.occupation.startingitems:
            if item in self.inv:
                pass
            else:
                self.inv.append(item)
        for skill in self.occupation.skills:
            if skill in self.skills:
                pass
            else:
                self.skills.append(skill)
    # Handles equipping of Armor and Weapons        
    def equiparmor(self,invarmor,location):
        if invarmor in self.inv:
            if invarmor is type(armor) and (invarmor.atype == 'All' or location):
                print "You equipped your %s on your %s." %(invarmor.name, location)
                self.armoreq[location] = invarmor
                self.armorcalc()   
            else:
                print "You cannot equip that as an armor!"
        else:
            print "You don't have that in your inventory!"
            
    def equipweapon(self,invweapon):
        if invweapon in self.inv:
            if invweapon is type(weapon):
                print "You equipped your %s as a weapon. This weapon does %s damage." %(invweapon.name,invweapon.dmg)
                self.weapon = invweapon
            else:
                print "You cannot equip that as a weapon!"
        else:
            print "You don't have that in your inventory!"
    def describe(self):
        print "Your name is %s. You are a %s who is %s inches tall. You have %s eyes, %s hair, and are %s. Your favorite pasttime is %s." %(self.name, self.desc['sex'], self.desc['height'], self.desc['eyecolor'], self.desc['haircolor'], self.desc['build'], self.desc['pasttime'])

# Init Weapon, Spells, Armor, Skill, and Occupation Classes
class weapon(object):
    def __init__(self, name, dmg, desc, weight, cost):
        self.name = name
        self.dmg = dmg
        self.desc = desc
        self.weight = weight
        self.cost = cost
        
class spell(object):
    def __init__(self, name, dmg, effect, desc, cost):
        self.name = name
        self.dmg = dmg
        self.effect = effect
        self.desc = desc
        self.cost = cost
        
class armor(object):
    def __init__(self, name, phys_prot, magic_prot, atype, desc, weight, cost):
        self.name = name
        self.phys_prot = phys_prot
        self.magic_prot = magic_prot
        self.desc = desc
        self.atype = atype
        self.weight = weight
        self.cost = cost
        
class skill(object):
    def __init__(self, name, desc, timesperday):
        self.name = name
        self.desc = desc
        self.timesperday = timesperday
        
class occupation(object):
    def __init__(self, name, dmgbonus, resistance, startingitems, skills, statbonus, desc):
        self.name = name
        self.dmgbonus = dmgbonus
        self.resistance = resistance
        self.startingitems = startingitems
        self.statbonus = statbonus
        self.desc = desc
        self.skills = skills
        
# Create Weapons
Stick = weapon("A Large Stick", 1, "This is the stick you found on the side of a road.", 1, 0)
Longsword = weapon("Longsword", 5, "A longsword. a trusty weapon viewed highly by any upstanding adventurer.", 3, 20)
Dagger = weapon("Dagger", 2, "A short, concealable dagger. Dangerous in any hands, but especially by those with cunning.", 0, 5)
Greatclub = weapon("Greatclub", 4, "A massive wooden club. It looks heavy, but you are sure that in the right hands it could be devastating.", 5, 7)
Warhammer = weapon("Warhammer", 5, "A very large, two handed hammer. Favored by religous fighters, this weapon is incredibly powerful",4, 20)
Longbow = weapon("Longbow", 5, "A large, powerful bow, complete with arrows. The weapon of a true huntsman.",3, 20)
Quarterstaff = weapon("Quarterstaff", 3, "A long, hardwood stave, capable of dealing large amounts of blugeoning damage when in the right hands.", 2, 5)

# Create Spells
Fireball = spell("Fireball", 10, 'Attack', "A scroll of Fireball. Looks rather dangerous.", 20)

# Create Armors
NoArmor = armor("No Armor", 0, 0,'All', "You don't currently have armor equipped in this place.", 0, 0)
IronHelm = armor("Iron Helm", 3, 2, 'Headgear', "A sturdy iron helmet. Not much else to say.", 2, 10)
IronChestplate = armor("Iron Chestplate", 5, 2, 'Chest', "A sturdy iron chestplate. Won't stop an arrow, but is sure to protect you decently well.", 5, 20)
IronGreaves = armor("Iron Greaves", 2, 1, 'Legs', "Sturdy iron shinplates. Not sure what you are gonna do about your kneecaps (or thighs), but these will have to do.", 3, 10)
IronGauntlets = armor("Iron Gauntlets", 2, 1, 'Arms', "Sturdy iron gauntlets. A bit heavy and cumbersome, but certainly good for strangling goblins.", 3, 10)
SturdyBoots = armor("Sturdy Boots", 2, 0, 'Feet', "Nice, rugged boots. Great for stomping around taverns and stepping on small rocks.", 2, 10)

# Create Skills
MultiAttack = skill('Multi-Attack','Combat Skill. Allows for two attacks in a row next turn.', 3)
Spellcasting = skill('Spellcasting','Allows for the casting of spells with a spellbook, inside or outside combat.', -1)
Sneak = skill('Sneak','Provides a major bonus for sneak checks.', 5)
Networking = skill('Networking','Allows for cheaper shop rates and connections to the criminal underground.', -1)
Rage = skill('Rage','Combat Skill. Enter a frenzy for the next 2 rounds that allows for increased attack but decreased defense', 3)
UnarmedStrike = skill('Unarmed Strike','Combat Skill. Strike without a weapon, dealing damage equal to (STR+INT)/5', 3)
Dodge = skill('Dodge','Combat Skill. Negate all enemy damage when they next attack.', 3)
FormShift = skill('Form Shift','Combat Skill. For the next 3 rounds, enter beast form, boosting STR, DEX, and CON stats by 3 and physical damage by 4.', 2)
Smite = skill('Smite','Combat Skill. Use devine powers to deal 5 damage to opponent, and an additional 5 if they are undead.', 3)
Disengage = skill('Disengage','Combat Skill. Sink into the shadows and retreat to a safer distance, providing some time before the enemy can catch up', 2)


# Create Occupations
NoOccupation = occupation("No Occupation", [0,0],[0,0],[],[],{}, "You have no current occupation.")
Fighter = occupation("Fighter", [2,0],[1,0],[Longsword, IronHelm],[MultiAttack],{'Str':1,'Dex':1,'Con':1}, "You are a fighter. Highly trained in most fighting styles, you are very versitile on the battlefield.")
Mage = occupation("Mage", [0,2],[0,2],['Spellbook'],[Spellcasting],{'Wis':2,'Cha':1}, "You are a mage. Having poured years of your life into studying the arcane, you finally feel ready to use your mighty powers.")
Thief = occupation("Thief", [1,0],[1,2],[Dagger,'Lockpick'],[Sneak,Networking],{'Dex':2,'Cha':1}, "You are a thief. An expert at sneaking about, you are familiar with the criminal underground.")
Barbarian = occupation("Barbarian", [3,0],[3,2],[Greatclub],[Rage],{'Str':3}, "You are a barbarian. A great brute with anger issues, many fear your ability to kick ass and tall stature.")
Monk = occupation("Monk", [2,0],[3,2],[Quarterstaff],[UnarmedStrike,Dodge],{'Str':1,'Dex':2}, "You are a monk. Harnessing the power of the inner mind, you use jedi-like abilities to defeat your foes.")
Druid = occupation("Druid", [0,1],[0,1],[Stick, 'Spellbook'],[FormShift,Spellcasting],{'Int':2,'Cha':1}, "You are a druid. Intelligent and in tune with nature, you use your form shift to deal devastating damage to enemies.")
Paladin = occupation("Paladin", [1,1],[1,2],[Warhammer],[Smite,Spellcasting],{'Str':2,'Wis':1}, "You are a paladin. A strong religious fighter, you are able to use physical prowess as well as spellcasting to devastating effect.")
Ranger = occupation("Ranger", [2,0],[1,1],[Longbow, Dagger],[Sneak,Disengage],{'Dex':2,'Con':1}, "You are a ranger. Experienced in hunting and tracking, you are a deadly force that takes advantage of distance to deal with your targets.")

# Create a list of all of the current occupations, because for some reason we cant access all occupations any other way.
occupation_list = []
for obj in gc.get_objects():
    if isinstance(obj, occupation):
        occupation_list.append(obj)
        
# Make player object, then fill it with the default bullshit        
Player = player(0,0,0,0,0,0,0,0,0,0,0,0)
Player.defaultattributes()
Player.hardupdate()

# Character Creation and Menus

def CharacterCreation():
    print "Welcome to Character Creation!"
    time.sleep(0.25)
    Player.name = raw_input("Please enter a name for your character.  > ")
    print "Hello, %s." %Player.name
    print "Please tell us a little bit about %s." %Player.name
    Player.desc['sex'] = raw_input("What is your preffered sexual gender? (M/F/?)  > ")
    Player.desc['height'] = raw_input("What is your player's height? (in inches)  > ")
    Player.desc['eyecolor'] = raw_input("What is your player's eyecolor?  > ")
    Player.desc['haircolor'] = raw_input("What is your player's haircolor?  > ")
    Player.desc['build'] = raw_input("What is your player's physical build? (thin, built, chunky, etc)  > ")
    Player.desc['pasttime'] = raw_input("What is your player's favorite pasttime?  > ")
    print
    print "Thank you for the information. Now it is time for you to select an occupation for your character."
    print "Your occupation will determine much of your playstyle, starting equipment and skills, and will provide a small bonus to some of your attributes."
    time.sleep(2)
    
    # Create a list of occupation names based off of the occupation objects.
    occupation_names = []
    for obj in occupation_list:
        occupation_names.append(obj.name)
    i = 0
    # Query loop to handle occupation selection
    while i == 0:
        print "Please select an occupation for your character. Your choices are:"
        for obj in occupation_list:
            print " -- %s -- " %obj.name
        player_occupation = raw_input("> ")
        player_occupation = player_occupation.capitalize()
        if player_occupation in occupation_names:
            for obj in occupation_list:
                if player_occupation == obj.name:
                    player_occupation = obj
            print "You have chosen %s as an occupation. The description is as follows:" %player_occupation.name
            print player_occupation.desc
            print
            j = 0
            while j == 0:
                yn = raw_input("Are you sure you want to select this occupation for your character? This selection is permanent. (Y/N) > ")
                if yn.lower() in ('y','yes'):
                    print "You have decided to become a %s." %player_occupation.name.lower()
                    time.sleep(2)
                    print
                    Player.occupation = player_occupation
                    Player.hardupdate()
                    StatSelection()
                    j = 1
                    i = 1
                elif yn.lower() in ('n','no'):
                    print "You have decided that the %s occupation is not for you. Please go back and select another from the list." %player_occupation.name.lower()
                    j = 1    
                    time.sleep(2)
                else:
                    print "I couldn't understand. Please go back and try again."
        else:
            print "I couldn't understand. Please go back and try again."

# Display current stats in a nice way. I was too lazy to type this twice. Its not really elegant.
def StatDisplay(readfrom):
    print "Your current attributes are as follows:"
    print "'Str' : %s -- The strength attribute is used for physical checks like athletics and lifting, as well as to determine how much you can carry at one time." %readfrom['Str']
    print "'Dex' : %s -- The dexterity attribute is used for physical checks like climbing and swimming, as well as to determine your dodge percentage." %readfrom['Dex']
    print "'Con' : %s -- The constitution attribute is used for poison checks, as well as to determine your max HP." %readfrom['Con']
    print "'Int' : %s -- The intelligence attribute is used for observational checks, such as perception and investigation." %readfrom['Int']
    print "'Wis' : %s -- The wisdom attribute is used for spellcasting checks, as well as to determine crit percentage." %readfrom['Wis']
    print "'Cha' : %s -- The charisma attribute is used for persuasion checks, as well as to determine bartering rates." %readfrom['Cha']

def StatSelection():    
    i = 0
    # Make temporary attribute dictionary because dictionaries are gay
    tempstats = Player.stats.copy()
    points = 26
    while i == 0:
        StatDisplay(tempstats)
        print "You currently have %s points left." %points
        if points == 0:
            print "You have used up all your points! Are you happy with your current stats?"
            yn = raw_input('(Y/N)  > ')
            if yn.lower() in ('y','yes'):
                # Commit stats to the player object from tempstats
                Player.stats = tempstats.copy()
                for key in tempstats:
                    statselect[key] = tempstats[key] - 10
                    try:
                        statselect[key] = statselect[key] - Player.occupation.statbonus[key]
                    except KeyError:
                        pass
                Player.hardupdate()
                i = 1
            if yn.lower() in ('n','no'):
                print "Would you like to reset your stats back to their default values?"
                yn = raw_input('(Y/N)  > ')
                if yn.lower() in ('y','yes'):
                    print "Resetting attributes..."
                    print
                    # Reset stats and points
                    tempstats = Player.stats.copy()
                    points = 26
                if yn.lower() in ('n','no'):
                    print "You may need to lower an attribute to get more points back."
                    # Yes I know I am giving the player an extra point here and they could theoretically abuse this to get 20's in every stat but I dont really give a shit.
                    points += 1
        else:
            selection = raw_input("Which attribute would you like to change? [Str, Dex, Con, Int. Wis, Cha]  > ")
            selection = selection.capitalize()
            for stat in tempstats:
                if selection.capitalize() == stat:
                    # Make sure the player isnt trying any fucky shit while editing their stats.
                    print "You have chosen to modify your %s attribute." %selection.capitalize()
                    statmod = raw_input("By how many points would you like to modify this stat? (Max 20)  > ")
                    try:
                        statmod = int(statmod)
                        if statmod <= points and (0 < (tempstats[selection] + statmod) <= 20):
                            tempstats[selection] = tempstats[selection] + statmod
                            points = points - statmod
                            print "Your new %s attribute is %s." %(selection,tempstats[selection])
                        elif statmod > points:
                            print "You don't have enough points left!"
                        elif (tempstats[selection] + statmod) > 20:
                            print "You can't increase a stat to more than 20!"
                        elif (tempstats[selection] + statmod) <= 0:
                            print "After lowering your %s attribute that much, you begin to feel woozy and quickly lose consiousness. Maybe that was a bad idea...." %selection
                            print "GAME OVER... BETTER LUCK NEXT TIME"
                            time.sleep(4)
                            raise SystemExit
                        else:
                            print "Sorry, it looks like you typed something in wrong."
                    except ValueError:
                        print "Nice try, idiot. Go back and put an integer in."
                    
                            
def PlayerMenu():
    i = 0
    while i == 0:
        print "Type 'i' to view inventory, 's' to view player stats and attributes, 'x' to view skills, 'e' to equip weapons and armor, 'q' to quit game, and 'd' to view your description"
        time.sleep(0.25)
        choice = raw_input("What would you like to do?  > ")
        choice = choice.lower()
        # Display Inventory
        if choice in ('i','inv','inventory'):
            print "--%s's Inventory--" %Player.name
            totalweight = 0
            for item in Player.inv:
                try: 
                    print "- %s -- %s lbs" %(item.name,item.weight)
                    totalweight += item.weight
                except AttributeError:
                    print "- %s -- 0 lbs" %item
            print
            print "Total Weight -- %s lbs" %totalweight
            print '----------------------'
            try:
                print "Equipped Weapon -- %s" %Player.weapon.name
                print "Weapon Damage - %s" %Player.weapon.dmg
                print "Cost - %s    Weight - %s lbs" %(Player.weapon.cost,Player.weapon.weight)
            except AttributeError:
                print "You have no equipped weapon. Type 'e' to equip a weapon in your inventory!"
            print '----------------------'
            print "-Equipped Armor-"
            armorweight = 0
            for armor in Player.armoreq:
                print "%s -- %s -- %s lbs" %(armor, Player.armoreq[armor].name, Player.armoreq[armor].weight)
                armorweight += Player.armoreq[armor].weight
            print '----------------------'
       # Display Stats 
        if choice in ('s','stats','attribute','attributes'):
            print "--%s's Stats and Attributes--" %Player.name
            StatDisplay(Player.stats)
            print '----------------------'
            print "Max HP - %s -- Current HP - %s" %(Player.maxhp,Player.hp)
            print "Occupation - %s -- Carry Weight - %s" %(Player.occupation.name, Player.carryweight)
            print "Physical Armor - %s -- Magical Armor - %s" %(Player.armor[0],Player.armor[1])
            print '----------------------'
        # Display Skills and Descriptions
        if choice in ('x','skills','skill'):
            print "--%s's Skills--" %Player.name
            for p_skill in Player.skill:
                if Player.p_skill.timesperday == -1:
                     print "%s - Infinite Times/Day - %s" %(Player.p_skill.name, Player.p_skill.desc)
                else:
                    print "%s - %s Times/Day - %s" %(Player.p_skill.name, Player.p_skill.timesperday, Player.p_skill.desc)
            print '----------------------'
        # Display Player Description
        if choice in ('d','desc','description'):
            print Player.describe()
            print
        # Quit from Menu
        if choice in ('q','quit'):
            print "Are you sure you want to quit the game? There is currently no way to save, so next time you will have to make a new character."
            yn = raw_input("(Y/N)?  > ")
            yn = yn.lower()
            if yn in ('y','yes'):
                raise SystemExit
            else:
                pass
        # Equip Menu
        if choice in ('e','equip'):
            print "Don't look here, it isnt finished. I don't know how im going to fucking do this bit."