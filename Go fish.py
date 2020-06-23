# Card game - Go Fish
# James Francis, Apr 2020
#
# 29/04/2020 BAF Added in Beth's bit
# 05/06/2020 JGF Full dummy game loop with everyone passing
# 14/06/2020 JGF Can type in the human move --- in test

# === SETUP : Python libraries and program settings ===

import random
import time

TEST = False
names = ['Gertrude', 'Doris', 'Boris', 'Bert', 'Larry']  # ['Boris', 'Doris', 'Horace', 'Norris', 'Phyllis']
suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
shortranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANKS_IN_PACK = 10

# === FUNCTIONS needed throughout the program ===

# Print a list of cards.  If num>0 then it will print up to that number of cards rather than the whole list
# !!! need to print cards and hands in a nicer way
def showcards(cards, num):
    if num==0:
        num = len(cards)
    else:
        num = min(num, len(cards))
    for c in range(num):
        print(list(cards[c].values()))


# Check for a set of 4 cards in a player's hand
# Remove the matching cards if one is found
def checkForSet(cards):
    cardcount = {x:0 for x in ranks}
    setfound = ''
    for c in cards:
        cardcount[c['rank']] += 1
        if cardcount[c['rank']]==4:
            setfound = c['rank']
            break
    if setfound!='':
        for c in cards.copy():
            if c['rank']==setfound:
                cards.remove(c)
    return setfound

# === GET THE GAME STARTED ===

# construct the pack of cards
pack = []
for suit in suits:
    for rank in ranks[13 - RANKS_IN_PACK:]:
        card = {'rank':rank, 'suit':suit}
        pack.append(card)


# shuffle the pack - randomly move cards
for i in range(100):
    cardpos = random.randint(0, len(pack) - 1)
    newpos = random.randint(0, len(pack) - 2)
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
    dealsize = 8
elif players==5:
    dealsize = 7
else:
    dealsize = 6

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

# create some variables to keep track of the sets that get made
# and for the computer players' knowledge of who holds what cards
setsmade = 0
playersetsmade = [0 for x in playernames]
knowledge = [{x : -1 for x in ranks} for y in range(players)]

# show the human their hand, say what order we play in, and ask if they're ready to start
# check if they were dealt a set to start with
print(name, ", this is your hand.  Good luck with it!")
showcards(hand[humanpos], 0)
print()
setfound = checkForSet(hand[humanpos])
if setfound!='':
    setsmade += 1
    playersetsmade[humanpos] += 1
    print ('You already have a set of', setfound+'s.', 'That\'s a great start!')
    if TEST:
        print("--- JUST CHECKING! Your hand is now:")
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
        #if TEST:
            #print('---DECODING : <ASK>+"', movetext, '"', sep='')
        if movetext[1]==' ':
            # match the initial to a player
            for i in range(len(playernames)):
                if movetext[0].upper()==playernames[i][0].upper() and i != humanpos:
                    # found the player the human wants to ask
                    askplayer = i
            #if TEST:
                #print('---DECODING : Player #', askplayer, sep='')
            if askplayer != -1:
                # the next word should be 'for'
                movetext = movetext[2:]
                if movetext[:4].upper()=='FOR ':
                    # finally work out which card the human is asking for
                    movetext = movetext[4:]
                    #if TEST:
                        #print('---DECODING : <ASK>+<Player #', askplayer, '>+"', movetext, '"', sep='')
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

    return {'action':action, 'ask':askplayer, 'card':ranks[askcard]}


# A player needs to pick up from the pack. If it's the human player then tell them the card name
def doPickUpFor(player, ishuman):
    if len(pack)>0:
        # move a card from the pack into the player's hand
        if ishuman:
            print(playernames[player], 'picks up a card. It\'s the', list(pack[0].values()), end='.\n')
        else:
            print(playernames[player], 'picks up a card.')
        hand[player].append(pack.pop(0))
        if len(pack)==1:
            print('There is only one card left in the pack.')
        elif len(pack)==0:
            print('That was the last card.')

    else:
        # announce that there are no cards left in the pack
        print('There are no cards left in the pack,', playernames[player], 'can\'t pick up.')


# Carry out a player's move, where player1 asks player2 if they have any cards
# Find any matching cards in the asked player's hand, and move them to player1's hand if there are any
# Record the revealed knowledge of who now holds the card for the computer players to use
def doTheMove(player1, player2, askfor):
    matchedcards = []
    for card in hand[player2][:]:
        if card['rank']==askfor:
            matchedcards.append(card)
            hand[player2].remove(card)
    if matchedcards==[]:
        # No matching cards - GO FISH! So player 1 must pick up if possible
        print(playernames[player2], 'says "GO FISH!"')
        doPickUpFor(player1, player1==humanpos)
    else:
        # Announce the matching cards and add to player1's hand
        print(playernames[player2], 'passes', len(matchedcards), 'cards to', playernames[player1], end='.\n')
        hand[player1].extend(matchedcards)
    for i
    knowledge[askfor] = player1


# === MAIN GAME LOOP ===
gameover = False
while not gameover:
    for p in range(players):
        if p==humanpos:
            # Human player's turn. Input a move, check it, and repeat until they input a valid move

            # First display the state of the game.
            # !!! work out how to clear the screen to stop cheating by looking back
            # !!! improve the ordering so it starts from the human player's virtual left
            print('Your turn now, this is how things are in the game:')
            for p in range(players):
                if p!=humanpos:
                    print(playernames[p], 'has', len(hand[p]), 'card(s) and', playersetsmade[p], 'sets.')
                else:
                    print('You have', len(hand[p]), 'card(s) and', playersetsmade[p], 'sets.')
            print()

            # Pick up if needed
            if len(hand[p])!=0:
                print('This is your hand:')
                showcards(hand[p], 0)
            else:
                print('Your turn now, and you have no cards.')
                doPickUpFor(p, True)

            # Check if the player now has any cards, and carry out their turn
            if len(hand[p])==0:
                print('Your game is over, no more moves for you.')

            else:
                print('\nPlease enter your move: ', end='')
                while True:
                    movetext = input()
                    if movetext.strip() != '':
                        decodedmove = workOutHumanMove(movetext)
                        if decodedmove['action']>0:
                            # successful input so go on to carry it out
                            break
                    print('Try again, or type Q then ENTER to quit: ', end='')

                # Carry out their move.
                # !!! check it's legal : human must have one of the cards, and player must have some cards
                print()
                if decodedmove['action']==1:
                    gameover = True
                elif decodedmove['action']==2:
                    doTheMove(p, decodedmove['ask'], decodedmove['card'])
                    print()
                    # check if they made a set
                    if checkForSet(hand[p])!='':
                        setsmade += 1
                        playersetsmade[p] += 1
                        print ('You\'ve made a new set. You now have', playersetsmade[p], 'set(s) and', len(hand[p]), 'cards.')
                        if TEST:
                            print("--- JUST CHECKING! Your hand is now:")
                            showcards(hand[p], 0)
                        print()

            # End of human player's turn

        else:
            # computer turn
            print(playernames[p], 'to play next.')

            # Pick up if needed
            if len(hand[p])==0:
                doPickUpFor(p, True)

            # Check if the player now has any cards, and carry out their turn
            if len(hand[p])==0:
                print(playernames[p], 'has no cards and must pass.')

            else:
                # We finally get to the computer player's turn.
                # They choose a random card in their hand, ask a specific player if they know who holds them,
                # and a randomly chosen player otherwise
                if TEST:
                    print("--- JUST CHECKING! Their hand :")
                    showcards(hand[p], 0)
                askcard = hand[p][random.randint(1, len(hand[p])) - 1]['rank']
                if knowledge[askcard]!=-1:
                    askplayer = knowledge[askcard]
                else:
                    # Ask a randomly chosen player, making sure not to try to ask themselves
                    # or a player with no cards.
                    askplayer = random.randint(0, players - 1)
                    while askplayer==p or hand[askplayer]==[]:
                        askplayer = random.randint(0, players - 1)

                # Now carry out the chosen move
                print('"', playernames[askplayer], ', do you have any ', askcard,'s?"', sep='')
                doTheMove(p, askplayer, askcard)

                # check if they made a set
                if checkForSet(hand[p])!='':
                    setsmade += 1
                    playersetsmade[p] += 1
                    print (playernames[p], 'made a new set.')

            # End of computer player's turn.

        # Turn completed so pause before going on to the next player.
        response = input("Press ENTER to continue.")
        print()

        # Before going on to the next player, check if all the sets are made
        # and the game is finished.
        if setsmade==RANKS_IN_PACK:
            print('That\'s all the sets made. Here is the final score:')
            for p in range(players):
                print(playernames[p], ':', setsmade[p])
            print()
            gameover = True

        if gameover:
            break

        # End of player loop.  Continue on to the next player.
    # End of game loop. Continue with another round of turns.

# game finished so say goodbye
print("Game finished, hope you enjoyed it! Play again soon.")
