import scipy as sc
import os
import time

class Engine(object):

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def init(self):
        self.creator = "LwiD"

    def readlist(self, list_given, list_dtype):
        #A simple function to interpret list input, assuming the input is on the form [1,2,3,4] or [1, 2, 3, 4]
        started = False
        list_got = []
        for letter in list_given:
            if letter == "[":
                started = True
                new = True
            if started and new and letter != "," and letter != "[":
                list_element = letter
                new = False
            elif started and not new and letter != "," and letter != "]":
                list_element += letter
            elif started and letter == ",":
                list_got.append( list_dtype(list_element) )
                new = True
            if letter == "]":
                list_got.append( list_dtype(list_element) )
                break
        return list_got

    def run_menu(self):
        #This is where the fun happens
        #And where the application is launched
        clear = self.clear
        while True:
            clear()
            print("Welcome to the dynamic text engine\n")
            print("Please specify what you want to do by typing the relevant command to your desired action:\n")

            print("(1) Read a character \n")
            print("(2) Create a character \n")
            print("(c) Credits \n")
            print("(e) Exit \n")
            choice = input()
            if choice == "1":
                #This block is the loading of a preexisting character.
                
                loading = True
                while loading:
                    file = input("Please input file name (minus the .dat extension): ")
                    try:
                        chars[file] = self.read_character(file + ".dat")
                        loading = False
                    except NameError:
                        chars = {}
                        chars[file] = self.read_character(file + ".dat")
                        loading = False
                    
                    except FileNotFoundError:
                        print("There's no such character in the library, do you want to: \n")
                        print("(1) Try again \n")
                        print("(2) Make the character \n")
                        print("(3) Cancel \n")
                        choice_error1 = input()
                        if choice_error1 == "2":
                            self.character_creation(complex=True)
                        if choice_error1 == "3":
                            break

                print_char_choice = input("Do you want to see your character y/n ?")

                if print_char_choice.upper() == "Y":
                    clear()
                    print(chars[file])
                    print("\n")
                    input("Press enter to continue") 
            if choice == "2":
                self.character_creation(complex=True)
        
            if choice == "c":
                clear()
                print("This program was created by: Lars, Bingedrinker of Coffee\n")
                input("Press enter to go back")

            if choice == "e":
                break
        
    def read_character(self, sheet):
        #This is to read charsheets
        #The function takes one argument
        #Which is a string with the name of the charsheet file
        #And returns a dict with the character information
        with open(sheet, 'r+') as char_file:
            char_commented = char_file.readlines()
            char = {}
            for line in char_commented:
                if line[0:3] != '***' and line[0] != '\n':
                    #Reading everything that isn't a comment in the raw character file data
                    line = line.split()

                    for k in range(1, len(line)-1):
                        if line[-1] == 'dtype=int':
                            line[k] = int(line[k])
                        elif line[-1] == 'dtype=float':
                            line[k] = float(line[k])
                        else:
                            line[k] = str(line[k])

                    char[line[0]] = line[1:-1]

        return char

class DnD5e(Engine):
    #Functions that only work for DnD 5e
    def character_creation(self, complex=False):
        #A standard function for generating a character for
        # the read_character function
        # Unless otherwise specified, the function will
        # generate a simple character. Complex characters
        # might be player haracters or essential NPC
        if complex:
            self.clear()

            print("Hello and welcome to the character generation screen for DnD 5e. \n")
            char_name = input("Please enter your character's name: \n")
            print("\nEvery character fight in his/her own way,")
            print("but this way is defined by the character's class")
            char_class = input("What is your class, hero? \n")
            print("\nNow that your class is written down, it is important to know what level you are.")
            char_level = int(input("What is your level?\n"))
            char_background = input("\nNow that we know your level, what is your background?\n")
            char_race = input("What is your character's race?\n")
            roll_stats = input("\nNow we need to find your stats, do you want to (1) Roll for stats or (2) Write them in ?")
            if roll_stats == '1':
                stats_rolled = sc.zeros(6)
                for i, stat in enumerate(stats_rolled):
                    stats_rolled[i] = self.roll_stat()
            
            print("When assigning the stats, write them in in the following fashion:\n [<str>,<dex>,<con>,<int>,<wis>,<cha>] \n")
            if roll_stats:
                print("Since you rolled for stats, you get to assign the following numbers as your stats:\n")
                print(stats_rolled)
            
            char_stats = self.readlist(input(), list_dtype=int)
            char_stats = sc.array(char_stats)
            stat_mods = self.get_mods(char_race)


            filename = char_name + ".dat"
            with open(filename, "w+") as newsheet:
                #newsheet.write("*** Character created at %c" %(time.clock()))
                newsheet.write("\nchar_name %s dtype=str" %(char_name))
                newsheet.write("\nchar_class %s dtype=str" %(char_class))
                newsheet.write("\nchar_race %s dtype=str" % (char_race))
                newsheet.write("\nchar_background %s dtype=str"% (char_background))
                newsheet.write("\nchar_level %d dtype=int" %(char_level))
                newsheet.write("\nstr %d dtype=int" % (char_stats[0] + stat_mods[0]))
                newsheet.write("\ndex %d dtype=int" % (char_stats[1] + stat_mods[1]))
                newsheet.write("\ncon %d dtype=int" % (char_stats[2] + stat_mods[2]))
                newsheet.write("\nint %d dtype=int" % (char_stats[3] + stat_mods[3]))
                newsheet.write("\nwis %d dtype=int" % (char_stats[4] + stat_mods[4]))
                newsheet.write("\ncha %d dtype=int" % (char_stats[5] + stat_mods[5]))
        return False

    def get_mods(self, race):
        #This will be a pretty long function
        #For aquiring a skill mod for any race.
        #Index 0 is str, 1 is dex, 2 is con, int is 3
        #wis is 4 and cha is 5
        skill_mod = sc.zeros(6)
        if race.lower() == "hill dwarf":
            skill_mod[2] = 2
            skill_mod[4] = 1

        elif race.lower() == "mountain dwarf":
            skill_mod[2] = 2
            skill_mod[0] = 2

        elif race.lower() == "high elf":
            skill_mod[1] = 2
            skill_mod[3] = 1

        elif race.lower() == "wood elf":
            skill_mod[1] = 2
            skill_mod[4] = 1

        elif race.lower() == "dark elf" or race.lower() == "lightfoot halfling":
            skill_mod[1] = 2
            skill_mod[5] = 1

        elif race.lower() == "stout halfling":
            skill_mod[1] = 2
            skill_mod[2] = 1

        elif race.lower() == "human":
            skill_mod = sc.ones(6, dtype=int)

        elif race.lower() == "dragonborn":
            skill_mod[0] = 2
            skill_mod[5] = 1

        elif race.lower() == "forest gnome":
            skill_mod[3] = 2
            skill_mod[1] = 1

        else:
            print("The race you've given: %s is currently not supported!" % (race))
            print("This might be because it doesn't exist, or you might have written it wrong.\n")
            print("Please write in your racial bonuses like this [<str>, <dex>, <con>, <int>, <wis>, <cha>]\n")
            skill_mod_inputted = self.readlist(input())
            for i, skill in enumerate(skill_mod_inputted):
                skill_mod[i] = int(skill)

        return skill_mod
    def roll_stat(self):
        #A small function for rolling for a stat
        rolls = sc.random.random_integers(1,6, 4)
        lowest_roll = sc.amin(rolls)
        result = sc.sum(rolls) - lowest_roll
        return result