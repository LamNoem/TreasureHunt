# Lamontagne_Noemie_TreasureHuntClasses.py
# Description: treasure hunt game
# Date Created: 5/09/2024
# Last Modified: 5/13/2024

import random
import time

#Class containing methods relating to the treasure in the game
class Treasure:
    #generating random coordinates for treasure
    def GenTreasure(self):
        '''
        :return: a list of treasure coordinates. A list containing lists with 2 items (coordinates). [[y,x],[y,x]]
        '''
        treasure_list = []
        #10 trasure coordinates
        for i in range(10):
            treasure_list.append([random.randint(0,9), random.randint(0,9)])

        #no duplicate treasure positions
        while len(treasure_list) != len({str(x) for x in treasure_list}):
            treasure_list = []
            for i in range(10):
                treasure_list.append([random.randint(0, 9), random.randint(0, 9)])
        return treasure_list

    #generates a random value for loot
    def GenLoot(self):
        '''
        :return: int
        '''
        vals = [100, 250, 500, 1000]
        val = random.choice(vals)
        return val

# A class containing methods for the ambush in the game
class Ambush:
    #generate the random coordinate for the ambush
     def GenAmbush(self):
         '''
         :return: list with 2 items [int, int] (coordinate)
         '''
         ambush_coord = [random.randint(0,9), random.randint(0,9)]
         return ambush_coord

# A class containing methods for the escape in the game
class Escape:
    # generate the random coordinate for the escape
    def GenEscape(self):
        '''
        :return: list with 2 items [int, int] (coordinate)
        '''
        escape_coord = [random.randint(0,9), random.randint(0,9)]
        return escape_coord

# A class containing methods for the pirates in the game
class Pirates:

    #generates coordinates for pirates
    def GenPirates(self):
        '''
        :return: a list of pirate coordinates. A list containing lists with 2 items (coordinates). [[y,x],[y,x]]
        '''
        pirate_list = []
        #4 pirates
        for i in range(4):
            pirate_list.append([random.randint(0,9), random.randint(0,9)])

            # no duplicate pirate positions
            while len(pirate_list) != len({str(x) for x in pirate_list}):
                pirate_list = []
                for i in range(4):
                    pirate_list.append([random.randint(0, 9), random.randint(0, 9)])

        return pirate_list

    #Moving (changing the coordinate of the) pirates randomly amongst the possible positions.
    def MovePirates(self, pirate_coords, used):
        '''
        :param pirate_coords: List containing coordinates [[y,x],[y,x]] (lists with two int items) (The current coordinates of the pirates).
        :param used: coordinates (list with two int items, [y,x]) that are no longer available for various reasons. (already the coordinate of an ambush, escape, treasure or previous pirate encounter).
        :return: new pirate coordinates. List containing coordinates [[y,x],[y,x]].
        '''

        #finding possible positions a pirate in a certain coordinate could "move" into
        def PossiblePirateCoords(coord,used):
            '''
            :param coord: pirate coordinate (list, [y,x])
            :param used: coordinates (list with two int items, [y,x]) that are no longer available for various reasons. (already the coordinate of an ambush, escape, treasure or previous pirate encounter).
            :return: List of possible coordinates [[y,x],[y,x]] where x and y are integers.
            '''
            #possible coordinates in ideal situation
            possible_pos = [[coord[0], coord[1]], [coord[0] - 1, coord[1]], [coord[0] + 1, coord[1]], [coord[0], coord[1] - 1], [coord[0], coord[1] + 1], [coord[0]+1, coord[1]-1], [coord[0]+1, coord[1]+1], [coord[0]-1, coord[1]-1], [coord[0]-1, coord[1]+1]]
            #TypeError: 'int' object is not subscriptable
            #list of coordinates that are not possible
            ToBeRemoved = []
            #detecting invalid coordinates
            #coordinates cannot be already used and cannot be outside the game board.
            for v in possible_pos:
                if v in used:
                    ToBeRemoved.append(v)
                    continue

                if v[0] < 0:
                    ToBeRemoved.append(v)
                    continue

                elif v[1] < 0:
                    ToBeRemoved.append(v)
                    continue

                elif v[0] > 9:
                    ToBeRemoved.append(v)
                    continue

                elif v[1] > 9:
                    ToBeRemoved.append(v)
                    continue

                else:
                    continue

            #using the invalid list remove the invalid coordinates from the possible coordinates list
            for c in ToBeRemoved:
                possible_pos.remove(c)

            return possible_pos

        #For each current pirate coord, assign a new (possible) coord
        count = 0
        for i in pirate_coords:
            possible_moves = PossiblePirateCoords(i, used)
            pirate_coords[count] = random.choice(possible_moves)
            count = count + 1

        return pirate_coords


# A class containing methods for the scallywag in the game
class scallywag:

    #generate random coordinate for the scallywag
    def GenScally(self):
        '''
        :return: coordinate (list with 2 int items)
        '''
        pos = [random.randint(0, 9), random.randint(0, 9)]
        return pos

#A class containing the gameboard and gameplay method. Combines the other objects/classes/pieces into one full game structure.
class GamePlay(Treasure,Ambush,Escape,Pirates,scallywag):

    #gameboard
    def __init__(self):
        self.Gboard = [
                ["_","_","_","_","_","_","_","_","_","_"],
                ["_","_","_","_","_","_","_","_","_","_"],
                ["_","_","_","_","_","_","_","_","_","_"],
                ["_","_","_","_","_","_","_","_","_","_"],
                ["_","_","_","_","_","_","_","_","_","_"],
                ["_","_","_","_","_","_","_","_","_","_"],
                ["_","_","_","_","_","_","_","_","_","_"],
                ["_","_","_","_","_","_","_","_","_","_"],
                ["_","_","_","_","_","_","_","_","_","_"],
                ["_","_","_","_","_","_","_","_","_","_"]
                  ]

    #gameplay method
    def play(self):
        '''
        :return: none
        '''
        #displaying highscore, stored in a separate file.
        with open("Highscore", "r") as highscore:
            score = int(highscore.read())
            print("Current Highscore: "+ str(score))
        #condition for continued gameplay
        x = True
        #generating initial scallywag position. in position and coordinate form.
        pos = self.CoordToPosition(super().GenScally())
        coord = self.PositionToCoord(pos)
        #initial loot
        loot = 0
        #generating treasure, ambush, escape, and pirates.
        #Ensuring that they do not overlap initially.
        used = []
        used.append(pos)
        treasure_coords = super().GenTreasure()
        while used in treasure_coords:
            treasure_coords = super().GenTreasure()
        for i in treasure_coords:
            used.append(i)
        ambush_coord = super().GenAmbush()
        while ambush_coord in used:
            ambush_coord = super().GenAmbush()
        used.append(ambush_coord)
        escape_coord = super().GenEscape()
        while escape_coord in used:
            escape_coord = super().GenEscape()
        used.append(escape_coord)

        pirate_coords = super().GenPirates()
        comb1 = []
        for i in pirate_coords:
            comb1.append(i)
        for v in used:
            comb1.append(v)

        #show treasure
        for i in treasure_coords:
            self.Gboard[i[0]][i[1]] = "T"

        #if u add the used coordinates to the pirates coordinates and then find duplicates, that is because there was overlap to be corrected
        while len(comb1) != len({str(v) for v in comb1}):
            pirate_coords = super().GenPirates()
            for i in pirate_coords:
                comb1.append(i)
            for v in used:
                comb1.append(v)


        # show pirates
        for i in pirate_coords:
            self.Gboard[i[0]][i[1]] = "P"
        #Begin Gameplay when play function is called on a gameplay object
        #each loop represents a round
        while x:

            #determine possible next positions for the scallywag
            possible_positions = self.PossiblePositions(pos)
            #display legent and initial loot
            print("a. Play game\nb. How to play\nc. Legend\nd. Exit")
            print("Loot: " + str(loot))

            #Store the character that was previously displayed on the gameboard in the current scallywag location
            was = self.Gboard[self.PositionToCoord(pos)[0]][self.PositionToCoord(pos)[1]]
            #replace that character by an S, then display the gameboard which will show the scallywag's current position
            self.Gboard[self.PositionToCoord(pos)[0]][self.PositionToCoord(pos)[1]] = "S"
            print("Positions [00 - 09]:"+str(self.Gboard[0]) + "\n" + "Positions [10 - 19]:"+ str(self.Gboard[1]) + "\n" + "Positions [20 - 29]:"+str(self.Gboard[2]) + "\n" + "Positions [30 - 39]:"+str(
                self.Gboard[3]) + "\n" + "Positions [40 - 49]:"+str(self.Gboard[4]) + "\n" + "Positions [50 - 59]:"+str(self.Gboard[5]) + "\n" + "Positions [60 - 69]:"+str(
                self.Gboard[6]) + "\n" + "Positions [70 - 79]:"+str(self.Gboard[7]) + "\n" + "Positions [80 - 89]:"+str(self.Gboard[8]) + "\n" + "Positions [90 - 99]:"+str(self.Gboard[9]))
            #Then replace the character that was previously on the gameboard so that it will remain displayed once the scallywag moves on.
            self.Gboard[self.PositionToCoord(pos)[0]][self.PositionToCoord(pos)[1]] = was
            #Ask the player what they want to do
            play = input(f"Your current position is {pos}\nWhat do you want to do for this round?: ")
            #exit game if instructed
            if play == 'd':
                print("\nGoodbye")
                x = False
            #display legend if instructed
            if play == 'c':
                print("T - full treasure\nt - empty treasure\nP - pirate, YIKES!\nX - escape the island\nS - the scallywag … YOU!\n")
            #display instructions if instructed
            if play == 'b':
                print("You may move one unit horizontally or vertically to explore the game board and collect as many points as possible.\nFind the escape in order to leave the island with your loot.\nBeware the ambush!")
                print("Avoid the pirates, keep in mind you can run into the pirates and the pirates can run into you. So don't move into a pirates position and avoid a pirates possible movements.")
            #play the next round if instructed
            if play == 'a':
                #ask for next position
                #error proofing
                try:
                    move = int(input(f"which position would like to move to? Your options are {possible_positions}: "))
                except:
                    move = -1
                #new scallywag position in position and coordinate form
                pos = move
                coord = self.PositionToCoord(pos)
                #error proofing
                while pos not in possible_positions:
                    print("Not a valid position, enter a new valid position")
                    move = int(input(f"which position would like to move to? Your options are {possible_positions}: "))
                    pos = move
                    coord = self.PositionToCoord(pos)

                #scallywag runs into treasure
                if coord in treasure_coords:
                    #update loot randomly
                    loot = loot + super().GenLoot()
                    #add empty treasure to board
                    self.Gboard[self.PositionToCoord(pos)[0]][self.PositionToCoord(pos)[1]] = "t"
                    #remove the looted treasure from treasure_coordinates
                    #cannot run into the same treasure twice
                    treasure_coords.remove(coord)
                    print("\n")
                    print("YAYAYAYAYAYAYAYAYA TREASURE")
                    print("Your loot is now: "+str(loot))
                    time.sleep(3)
                    print("\n")

                #scallywag runs into ambush
                if coord == ambush_coord:
                    #why does the ambush need to move to a new location
                    loot = 0
                    print("\n")
                    print("OH NOOOOOOOOOOOOOOO\nAMBUSH")
                    print("   X           X  ")
                    print("         D        ")
                    print("xxxxxxxxxxxxxxxxxx")
                    print("LOOT: "+str(loot))
                    print("GAME OVER! YOU LOSE")
                    #exit game
                    x = False
                    continue

                #scallywag runs into the escape
                if coord == escape_coord:
                    #update game board
                    self.Gboard[self.PositionToCoord(pos)[0]][self.PositionToCoord(pos)[1]] = "X"
                    print("\n")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("YOU HAVE A CHANCE TO ESCAPE WITH YOUR LOOT!")
                    print("LOOT: "+str(loot))
                    print("You may leave now or continue exploring and escape later at this position!")
                    #option to escape with loot
                    exit = input("Do you want to escape (y/n)? ")
                    #if safe exit, display loot and update highscore if needed then exit game. otherwise continue to next round. Scallywag can still return to the escape later.
                    if exit == 'y':
                        print('YOU ESCAPED WITH YOUR LOOT!')
                        print("LOOT: "+str(loot))
                        with open("Highscore", "r") as highscore:
                            score = int(highscore.read())
                            if loot > score:
                                print("NEW HIGHSCORE!: "+ str(loot))
                                with open("Highscore", "w") as highscore:
                                    highscore.write(str(loot))
                        x = False
                        continue
                    else:
                        time.sleep(3)
                        continue

                #if scallywag runs into pirates
                if coord in pirate_coords:
                    print("\n")
                    print("Aaaarrrrgggghhhh!")
                    print("Pirate Yikes!")
                    print("\n")
                    #update gameboard
                    self.Gboard[self.PositionToCoord(pos)[0]][self.PositionToCoord(pos)[1]] = "p"
                    #no longer an available coordinate for moving pirates
                    used.append(coord)
                    #super().PirateEncounter(coord)
                    #remove the encountered pirate. There will be one less pirate moving around.
                    pirate_coords.remove(coord)
                    #half loot
                    loot = loot//2
                    print("YOU LOST HALF YOUR LOOT :(")
                    print("Loot is now: "+str(loot))
                    time.sleep(3)

                #Before the next round, move the pirates
                for i in pirate_coords:
                    self.Gboard[i[0]][i[1]] = "_"
                pirate_coords = super().MovePirates(pirate_coords, used)
                for i in pirate_coords:
                    self.Gboard[i[0]][i[1]] = "P"

                #if a pirate has moved onto the scallywag
                if coord in pirate_coords:
                    print("\n")
                    print("Aaaarrrrgggghhhh!")
                    print("Pirate Yikes!")
                    print("\n")
                    #update gameboard
                    self.Gboard[self.PositionToCoord(pos)[0]][self.PositionToCoord(pos)[1]] = "p"
                    #no longer an available coordinate for moving pirates
                    used.append(coord)
                    #super().PirateEncounter(coord)
                    #remove the encountered pirate. There will be one less pirate moving around.
                    pirate_coords.remove(coord)
                    #half loot
                    loot = loot//2
                    print("YOU LOST HALF YOUR LOOT :(")
                    print("Loot is now: "+str(loot))
                    time.sleep(3)

    #could have been used to verify if a location was available for moving pirates or other
    #if i had used a game structure that used two versions of the gameboard
    #but with my game structure using "used" coordinates instead of two gameboards, I have no need for this method.
    #I have kept this method in case I find a use for it and because it is described in the rubric.

    #method that determines if there is a character of meaning on the gameboard
    def isVacant(self, location):
        '''
        :param location: int position to be considered
        :return: boolean
        '''
        coord = self.PositionToCoord(location)
        if self.Gboard[coord[0]][coord[1]] == "_":
            return True
        else:
            return False

    #method for the possible possitions of the scallywag
    def PossiblePositions(self, p):
        '''
        :param p: int, current scallywag position
        :return: list of possible positions (int) [int,int]
        '''
        #scallywag cannot venture outside the dimensions of the board.
        coord = self.PositionToCoord(p)
        possible_positions = [[coord[0]-1,coord[1]],[coord[0]+1,coord[1]], [coord[0],coord[1]-1], [coord[0],coord[1]+1]]
        count = 0
        for i in possible_positions:
            if i[0] < 0:
                possible_positions.remove(i)
            elif i[1] < 0:
                possible_positions.remove(i)
            elif i[0] > 9:
                possible_positions.remove(i)
            elif i[1] > 9:
                possible_positions.remove(i)
            else:
                continue

        for i in possible_positions:
            possible_positions[count] = self.CoordToPosition(i)
            count = count + 1
        return possible_positions

    #the integer position format is used by the player and the list coordinate format is used by the code when navigating the gameboard.

    #method to convert an integer position to a list coordinate
    def PositionToCoord(self,location):
        '''
        :param location: integer, position on the game board
        :return: list [y,x], coordinate on the game board
        '''
        if location >= 90:
            y = 9
            x = location - 90
        elif location >= 80:
            y = 8
            x = location - 80
        elif location >= 70:
            y = 7
            x = location - 70
        elif location >= 60:
            y = 6
            x = location - 60
        elif location >= 50:
            y = 5
            x = location - 50
        elif location >= 40:
            y = 4
            x = location - 40
        elif location >= 30:
            y = 3
            x = location - 30
        elif location >= 20:
            y = 2
            x = location - 20
        elif location >= 10:
            y = 1
            x = location - 10
        else:
            y = 0
            x = location - 0
        coord = [y,x]
        return coord

    #method to convert a list coordinate to an integer position
    def CoordToPosition(self, coord):
        '''
        :param coord: list [y,x], coordinate on the game board
        :return: integer, position on the game board
        '''
        position = coord[0]*10 + coord[1]
        return position

    #returns a string representation of the gameplay class/the game board
    def __str__(self):
        print(str(self.Gboard[0])+"\n"+
              str(self.Gboard[1])+"\n"+
              str(self.Gboard[2])+"\n"+
              str(self.Gboard[3])+"\n"+
              str(self.Gboard[4])+"\n"+
              str(self.Gboard[5])+"\n"+
              str(self.Gboard[6])+"\n"+
              str(self.Gboard[7])+"\n"+
              str(self.Gboard[8])+"\n"+
              str(self.Gboard[9]))


