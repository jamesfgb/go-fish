# Card game - Go Fish
# James Francis, Apr 2020
#
# 29/04/2020 BAF Added in Beth's bit

# SETUP

import random
import time

TEST = 0
names = ['Gertrude', 'Doris', 'Boris', 'Bert', 'Larry'] # ['Boris', 'Doris', 'Horace', 'Norris', 'Phyllis']
suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

# FUNCTIONS

# Print a list of cards.  If num>0 then it will print up to that number of cards rather than the whole list
def showcards(cards, num):
    if num==0:
        num = len(cards)
    else:
        num = min(num, len(cards))
    for c in range(num):
        print(cards[c])


# construct the pack of cards
pack = []
for suit in suits:
    for rank in ranks:
        card = (rank, suit)
        pack.append(card)


# shuffle the pack - randomly move cards
for i in range(100):
    cardpos = random.randint(0, 51)
    newpos = random.randint(0, 50)
    card = pack.pop(cardpos)
    pack.insert(0, card)

# check by printing the first 10
if TEST:
    print("--- JUST CHECKING!")
    print(len(pack), "cards in the pack.  Here are the first ten:")
    showcards(pack, 10)
    print()

# cool bit that Beth did here
# introduce the players.  Ask the player's name and how
# many people they would like to play against
# Tell them the other players' names
# Make a list with players in the game ##including the human
print("Hi there, welcome to Go Fish!!")
name = input("What is your name? ")
print("\nHi",name,)
players = int(input("You can play against up to 4 people. \n"
               "How many people would you like to play against? "))
playernames = names[0:players]
print("You are playing agianst",playernames[0],end=" ")
for i in range(1,players):
   print("and",playernames[i],end=" ")
print("\n")


# add the human into the list of players, then deal all the hands
playernames.append(name)
players += 1
humanpos = players - 1
if players<=4:
    dealsize = 7
elif players==5:
    dealsize = 6
else:
    dealsize = 5

print("Dealing the cards")
time.sleep(1)

hand = [[] for p in range(players)]
for r in range(dealsize):
    for p in range(players):
        hand[p].append(pack.pop(0))

#check we've done a sensible deal
if TEST:
    print("--- JUST CHECKING!")
    for p in range(players):
        print("Hand", p+1)
        showcards(hand[p], 0)
        print()
    print("Pack has", len(pack), "cards left")

# show the human their hand, say what order we play in, and ask if they're ready to start
print(name, ", this is your hand.  Good luck with it!")
showcards(hand[humanpos], 0)
print()
print("We'll play in this order: ", end='')
for p in range(players):
    print(playernames[p], end='')
    if p<players-1:
        print(', ', end='')
#print()
response = input("\nPress ENTER to start playing")
print()

# Start playing
gameover = False
while not gameover:
    for p in range(players):
        if p==humanpos:
            # player's turn  !!! need to program it
            # simply input allowing quit only for now
            print("Your turn now. Please enter your move. All you can actually do yet is type Q then ENTER to quit.")
            response = input()
            print()
            if response.upper()=="Q":
                gameover = True
        else:
            # computer turn   !!! need to program the computer play
            print(playernames[p], "to play next. Not programmed yet,", playernames[p], "will pass.")
            response = input("Press ENTER to continue.")
            print()
        if gameover:
            break

# game finished so say goodbye
print("Game finished, hope you enjoyed it! Play again soon.")