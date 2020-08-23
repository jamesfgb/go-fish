# Module of gameplay functions for Go Fish v2

# Game constants and settings. Values may be changed in the main program.
suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
shortranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

NAMES = [['Gertrude', 'Doris', 'Boris', 'Fred', 'Larry'],
            ['Boris', 'Doris', 'Horace', 'Norris', 'Phyllis'],
            ['Barry', 'Carrie', 'Harry', 'Larry', 'Mary']]

TEST = False
RANKS_IN_PACK = 13
PAUSETIME = 0.5

# Global variables. Create here but may be initialised properly in the main program.
pack = []
players = 0
playernames = []
hand = []
humanpos = 0
setsmade = 0
playersetsmade = []
knowledge = []
playermessage = []

# === FUNCTIONS ===

# Print a list of cards.  If num>0 then it will print up to that number of cards rather than the whole list
# !!! probably don't need this anymore
def showcards(cards, num):
    if num==0:
        num = len(cards)
    else:
        num = min(num, len(cards))
    for c in range(num):
        print(list(cards[c].values()))


# Check for sets of 4 cards in a player's hand
# Remove the matching cards if one is found
# It's possible (but unlikely) there could be more than one set at the start of the game
# so allow for that possibility and return a count of sets found
def checkForSet(cards):
    cardcount = {x:0 for x in ranks}
    found = 0
    for c in cards:
        cardcount[c['rank']] += 1
        if cardcount[c['rank']]==4:
            found += 1
    if found>0:
        for c in cards.copy():
            if cardcount[c['rank']]==4:
                cards.remove(c)
    if TEST:
        print('--- CHECKING', cardcount, found)
    return found

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


# A player needs to pick up from the pack. If it's the human player then report the card name.
def AltdoPickUpFor(player, ishuman):
    message = ''
    if len(pack)>0:
        # move a card from the pack into the player's hand
        if ishuman:
            message = f'You pick up a card. It\'s the {pack[0]["rank"]} of {pack[0]["suit"]}.'
        else:
            message = f'{playernames[player]} picks up a card.'
        hand[player].append(pack.pop(0))
        if len(pack) == 0:
            message = message + ' That was the last card.'
    else:
        # announce that there are no cards left in the pack
        message = f'There are no cards for {"you" if ishuman else playernames[player]} to pick up.'
    return message


# Carry out a player's move, where player1 asks player2 if they have any cards.
# Find any matching cards in the asked player's hand, and move them to player1's hand if there are any.
# Record the revealed knowledge of who now holds the card for the computer players to use.
# Returns a 'Go Fish' flag : True if the the move ended in 'Go Fish!'
def AltdoTheMove(player1, player2, askfor):
    matchedcards = []
    for card in hand[player2][:]:
        if card['rank']==askfor:
            matchedcards.append(card)
            hand[player2].remove(card)
    if matchedcards==[]:
        # No matching cards - GO FISH! So player 1 must pick up if possible
        playermessage[player2] = '- GO FISH!'
        #doPickUpFor(player1, player1==humanpos)
    else:
        # Announce the matching cards and add to player1's hand
        playermessage[player2] = f'- Take {len(matchedcards)} {askfor}(s).'
        hand[player1].extend(matchedcards)
    # record in the other players' knowledge that player1 holds these cards
    for p in range(players):
        if p!=player1:
            knowledge[p][askfor] = player1
    return False if len(matchedcards) > 0 else True