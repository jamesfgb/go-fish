# Card game - Go Fish
# James Francis, Apr 2020
#
# 29/04/2020 BAF Added in Beth's bit
# 05/06/2020 JGF Full dummy game loop with everyone passing
# 14/06/2020 JGF Can type in the human move --- in test

# SETUP

import random
import time

TEST = False
names = ['Gertrude', 'Doris', 'Boris', 'Bert', 'Larry'] # ['Boris', 'Doris', 'Horace', 'Norris', 'Phyllis']
suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
shortranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


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

# ==== SOME FUNCTIONS FOR PLAYING THE GAME ====


# Tidy up a string, replacing all non alphanumeric with spaces, getting rid of multiple, leading and trailing spaces
# !!! program this later

# The human player has input their move, 
# the computer checks it makes sense, works out what it means, and confirms it with the human
def workOutHumanMove(movetext):
    askplayer = -1
    askcard = -1
    action = -1 # which works like this: -1=couldn't figure it out, 0=nothing input or changed mind, 1=quit, 2=ask player for a card
    movetext = movetext.strip()
    # !!! need to tidy the text up properly but program that later
    if movetext=='':
        action = 0
    elif movetext.upper()=='Q': 
        # player wants to quit
        action = 1
    elif len(movetext)<11:
        # not long enough to contain a valid move
        print('That makes no sense you dinkus!')
    elif movetext[:4].upper()=='ASK ':
        # wants to ask for a card, so work out which player
        movetext = movetext[4:]
        if TEST:
            print('---DECODING : <ASK>+"', movetext, '"', sep='')
        if movetext[1]==' ':
            # match the initial to a player
            for i in range(len(playernames)):
                if movetext[0].upper()==playernames[i][0].upper() and i != humanpos:
                    # found the player the human wants to ask
                    askplayer = i
            if TEST:
                print('---DECODING : Player #', askplayer, sep='')
            if askplayer != -1:
                # the next word should be 'for'
                movetext = movetext[2:]
                if movetext[:4].upper()=='FOR ':
                    # finally work out which card the human is asking for
                    movetext = movetext[4:]
                    if TEST:
                        print('---DECODING : <ASK>+<Player #', askplayer, '>+"', movetext, '"', sep='')
                    for i in range(len(shortranks)):
                        if movetext.upper()==shortranks[i]:
                            # found the card the human wants to ask for
                            askcard = i
                            action = 2
                    if askcard==-1:
                        # couldn't match the card
                        print('What on earth is ', movetext, '?', sep='')
                else:
                    # didn't find a 'for' after the player initial
                    print('I don\'t know what "', movetext, '" is supposed to mean.', sep='')
            else:
                # the initial after 'ask' didn't match a player
                print('There is no player', movetext[0], 'in the game.')
        else:
            # after 'ask' there wasn't a single character then a space
            print('You need to give a player\'s initial.')
    else:
        # can't work out what this move means
        print('That\'s not a proper move you dinkus!')

    # we've now finished analysing the human's move input, so repeat back for confirmation 
    if action==1:
        print()
        print('So you want to leave the game because you\'ve got the mardies. Is that right?')
    elif action==2:
        print('So you\'re going to say "', playernames[askplayer], ', do you have any ', ranks[askcard],'s?" Is that right?', sep='')

    # get confirmation if we need it
    if action>0:
        confirm = input('Press ENTER to continue, or type N then ENTER to change your mind. ')
        if confirm.strip() != '':
            action = 0

    return {'action':action, 'ask':askplayer, 'card':askcard}

# Carry out the human player's move
def doHumanMove(askplayer, askcard):
    cardcount = 0
    for c in range(length(hand[askplayer])):
        if hand[askplayer][c][0]==askcard:
            pass
            

# === MAIN GAME LOOP ===
gameover = False
while not gameover:
    for p in range(players):
        if p==humanpos:
            # Human player's turn. Input a move, check it, and repeat until they input a valid move 
            # !!! display their hand and the state of the game
            print('Your turn now. This is your hand:')
            showcards(hand[p], 0)
            print('\nPlease enter your move: ', end='')
            while True:
                movetext = input()
                if movetext.strip() != '':
                    decoded = workOutHumanMove(movetext)
                    if decoded['action']>0: 
                        # successful input so go on to carry it out
                        break
                print('Try again, or type Q then ENTER to quit: ', end='')

            # !!! carry out their move
            # !!! check it's legal : human must have one of the cards, and player must have some cards
            print()
            if decoded['action']==1: 
                gameover = True
            elif decoded['action']==2:
                print('Actually doing the move isn\'t programmed yet.')
            print()

        else:
            # computer turn   !!! need to program the computer play
            print()
            print(playernames[p], "to play next. Not programmed yet,", playernames[p], "will pass.")
            response = input("Press ENTER to continue.")
            print()

        if gameover:
            break

# game finished so say goodbye
print("Game finished, hope you enjoyed it! Play again soon.")
