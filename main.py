from curses.ascii import isalpha
import mysql.connector
import csv

from numpy import empty

# Creating the connector.
cnx = mysql.connector.connect(
    user="root",
    password="toor",
    host="localhost")
# Cursor to be able to execute MySQL.
crs = cnx.cursor()


# Displaying the databases in MySQL.
DB_NAME = "dungeon"
crs.execute(f"SHOW DATABASES LIKE \'{DB_NAME}\';")
current_db = crs.fetchall()

# Checking if the database named after me is already existing.
# If not, it can't be said anymore.
if current_db == []:
    crs.execute(f"CREATE DATABASE {DB_NAME};")
    crs.execute(f"USE {DB_NAME};")

    # Forbidden entries in the database.
    forbidden = ['NA', 'N/A', 'None', 'indefinite']

    # Creating a table for the players.
    pc_query = """
  	CREATE TABLE player(
        id INT AUTO_INCREMENT PRIMARY KEY,
    	pcName VARCHAR(255),
    	race VARCHAR(255),
    	class VARCHAR(255),
    	level INT,
    	balance INT
 	 );
  	"""
    crs.execute(pc_query)

    # Inputing the data from the csv files into the newly created database.
    with open("files/pc.csv", "r", newline="") as pc_file:
        pc = csv.reader(pc_file)
        # Jump over first line.
        next(pc)
        for row in pc:
            for i in range(len(row)):
                if row[i] in forbidden:
                    row[i] = None
            crs.execute(
                "INSERT INTO player (pcName,race,class,level,balance) VALUES (%s, %s, %s, %s, %s);", row)
            cnx.commit()
    pc_file.close

    # Creating a table for the races.
    races_query = """
  	CREATE TABLE races(
    	raceName VARCHAR(255) PRIMARY KEY,
    	rarity VARCHAR(255),
    	sourcebook VARCHAR(255)
 	 );
  	"""
    crs.execute(races_query)

    # Inputing the data from the csv files into the newly created database.
    with open("files/races.csv", "r", newline="") as races_file:
        races = csv.reader(races_file)
        # Jump over first line.
        next(races)
        for row in races:
            # Replace the strings in the integer fields by Null values.
            for i in range(len(row)):
                if row[i] in forbidden:
                    row[i] = None
            # Insert the data row by row in the table.
            crs.execute(
                "INSERT INTO races (raceName,rarity,sourcebook) VALUES (%s, %s, %s);", row)
            cnx.commit()
    races_file.close

    # Creating a table for the classes.
    classes_query = """
  	CREATE TABLE classes(
    	className VARCHAR(255) PRIMARY KEY,
    	classType VARCHAR(255),
    	bludgeoning BOOLEAN,
        slashing BOOLEAN,
        piercing BOOLEAN,
        special BOOLEAN,
    	hitdice VARCHAR(255),
        light BOOLEAN,
        medium BOOLEAN,
        heavy BOOLEAN,
        shield BOOLEAN
 	 );
  	"""
    crs.execute(classes_query)

    # Inputing the data from the csv files into the newly created database.
    with open("files/classes.csv", "r", newline="") as classes_file:
        classes = csv.reader(classes_file)
        # Jump over first line.
        next(classes)
        for row in classes:
            for i in range(len(row)):
                if row[i] in forbidden:
                    row[i] = None
            crs.execute(
                "INSERT INTO classes (className,classType,bludgeoning,slashing,piercing,special,hitdice,light,medium,heavy,shield) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", row)
            cnx.commit()
    classes_file.close

    # Creating a table for the weapons.
    weapons_query = """
  	CREATE TABLE weapons(
    	weaponName VARCHAR(255) PRIMARY KEY,
    	value INT,
    	distance VARCHAR(255),
    	damage VARCHAR(255),
    	type VARCHAR(255),
        difficulty VARCHAR(255)
 	 );
  	"""
    crs.execute(weapons_query)

    # Inputing the data from the csv files into the newly created database.
    with open("files/weapons.csv", "r", newline="") as weapons_file:
        weapons = csv.reader(weapons_file)
        # Jump over first line.
        next(weapons)
        for row in weapons:
            for i in range(len(row)):
                if row[i] in forbidden:
                    row[i] = None
            crs.execute(
                "INSERT INTO weapons (weaponName,value,distance,damage,type,difficulty) VALUES (%s, %s, %s, %s, %s, %s);", row)
            cnx.commit()
    weapons_file.close

    # Creating a table for the weapons.
    armours_query = """
    CREATE TABLE armours(
        armourName VARCHAR(255) PRIMARY KEY,
        weight VARCHAR(255),
        value INT,
        ac VARCHAR(255)
    );
    """
    crs.execute(armours_query)

    # Inputing the data from the csv files into the newly created database.
    with open("files/armours.csv", "r", newline="") as armours_file:
        armours = csv.reader(armours_file)
        # Jump over first line.
        next(armours)
        for row in armours:
            for i in range(len(row)):
                if row[i] in forbidden:
                    row[i] = None
            crs.execute(
                "INSERT INTO armours (armourName,weight,value,ac) VALUES (%s, %s, %s, %s);", row)
            cnx.commit()
    weapons_file.close

# Use the desired database.
crs.execute(f"USE {DB_NAME};")

# The function to display the menu.
def menu():
    print('''
1. List all the items in the setup.
2. List the weapons and armors the player characters can buy.
3. Count the number of races per sourcebook.
4. List the name of all player characters corresponding to a given criteria.
5. List all weapons ordered by range.
Q. Quit
-----------------------------------------------------------------
        ''')

    # Take the input from the user.
    choice = input("Please choose an option from the above: ")

    if choice == '1':
        print("All the existing weapons and armours in this setup:")
        crs.execute("SELECT weaponName FROM weapons UNION SELECT armourName FROM armours;")
        shop = crs.fetchall()
        # Display only the desired cleaned value from the tuple.
        for item in shop:
            print(item[0])
        # Coming back to the menu
        user = input("Press any key to come back to the menu ")
        menu()
    elif choice == '2':
        pc = input("Please enter the name of a player character: ")
        crs.execute(f"SELECT balance from player WHERE pcName=\'{pc}\'")
        balance = int(crs.fetchone()[0])
        print(balance)
        crs.execute(f"SELECT weaponName FROM weapons WHERE value<=\"{balance}\" UNION SELECT armourName FROM armours WHERE value<=\"{balance}\";")
        output = crs.fetchall()
        if output == []:
            print('Sorry, this player is too poor to shop here.')
        else:
            print(f'The chosen player {pc} can buy, for {balance} golds:')
            for item in output:
                print(item[0])
        user = input("Press any key to come back to the menu ")
        menu()
    elif choice == '3':
        print("Number of races per sourcebook:")
        crs.execute("SELECT COUNT( raceName ), sourcebook FROM races GROUP BY sourcebook;")
        shop = crs.fetchall()
        # Display only the desired cleaned value from the tuple.
        for item in shop:
            print(item[1], ':', item[0])
        # Coming back to the menu
        user = input("Press any key to come back to the menu ")
        menu()
    elif choice == '4':
        print('''Would you like to search:
1. A type of class.
2. A race.
3. A type of weapon.
4. A type of armour.
Q. Quit
-----------------------------------------------------------------
        ''')
        subchoice = input("Please choose an option from the above: ")
        if subchoice == '1':
            pc = input("Please enter a type of class (martial, zealot or spellcaster): ").lower()
            if pc not in ["martial","zealot", "spellcaster"]:
                print("This is not a known type of class")
                menu()
            else:
                crs.execute(f"SELECT pcName FROM player JOIN classes ON player.class = classes.className WHERE classes.classType=\"{pc}\";")
                shop = crs.fetchall()
                # Display only the desired cleaned value from the tuple.
                if shop == []:
                    print(f"No {pc} player has been registered to this day.")
                else:
                    print(f"All the {pc} player characters:")
                    for item in shop:
                        print(item[0])
                # Coming back to the menu
                user = input("Press any key to come back to the menu ")
                menu()
        elif subchoice == '2':
            pc = input("Please enter a chosen race: ").lower()
            crs.execute(f"SELECT pcName FROM player WHERE race=\"{pc}\";")
            shop = crs.fetchall()
            # Display only the desired cleaned value from the tuple.
            if shop == []:
                print(f"No {pc} player has been registered to this day.")
            else:
                print(f"All the {pc} player characters:")
                for item in shop:
                    print(item[0])
            # Coming back to the menu
            user = input("Press any key to come back to the menu ")
            menu()
        elif subchoice == '3':
            shop = []
            weapon = input("Which weapon are you interested in? ").lower()
            crs.execute(f"SELECT weaponName FROM weapons;")
            result = crs.fetchall()
            for i in result:
                shop.append(i[0])
            if weapon not in shop:
                print("This is not a known type of weapon")
                menu()
            else:
                crs.execute(f"SELECT type FROM weapons WHERE weaponName=\"{weapon}\";")
                wtype = crs.fetchone()[0]
                crs.execute(f"SELECT pcName FROM player JOIN classes ON player.class = classes.className WHERE classes.{wtype}=\"1\";")
                wlist = crs.fetchall()
                # Display only the desired cleaned value from the tuple.
                if wlist == []:
                    print(f"No player can use that.")
                else:
                    print(f"All the player characters who can bear a {weapon}:")
                    for item in wlist:
                        print(item[0])
                # Coming back to the menu
                user = input("Press any key to come back to the menu ")
                menu()
        elif subchoice == '4':
            shop = []
            armour = input("Which armour did you loot? ").lower()
            crs.execute(f"SELECT armourName FROM armours;")
            result = crs.fetchall()
            for i in result:
                shop.append(i[0])
            if armour not in shop:
                print("I don\'t think it is an armour...")
                menu()
            else:
                crs.execute(f"SELECT weight FROM armours WHERE armourName=\"{armour}\";")
                weight = crs.fetchone()[0]
                crs.execute(f"SELECT pcName FROM player JOIN classes ON player.class = classes.className WHERE classes.{weight}=\"1\";")
                wlist = crs.fetchall()
                # Display only the desired cleaned value from the tuple.
                if wlist == []:
                    print(f"No player can wear that.")
                else:
                    print(f"All the player characters who can use {armour}:")
                    for item in wlist:
                        print(item[0])
                # Coming back to the menu
                user = input("Press any key to come back to the menu ")
                menu()
        elif choice == 'Q' or choice == 'q':
            menu()
    if choice == '5':
        print("All the existing weapons ordered by range:")
        crs.execute("SELECT weaponName,distance FROM weapons ORDER BY distance ASC, weaponName ASC;")
        shop = crs.fetchall()
        # Display only the desired cleaned value from the tuple.
        for item in shop:
            print(item[0]+', '+item[1])
        # Coming back to the menu
        user = input("Press any key to come back to the menu ")
        menu()
    elif choice == 'Q' or choice == 'q':
        print("Farewell")
        exit()
    else:
        print("This is not a valid input.")
        exit()


menu()
