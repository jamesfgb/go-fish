# Card game - Go Fish, with graphics
# James Francis, Apr 2020
#
# 29/04/2020 BAF Added in Beth's bit.
# 05/06/2020 JGF Full dummy game loop with everyone passing.
# 14/06/2020 JGF Can type in the human move --- in test.
# 05/07/2020 JGF Full game with AI, plays the game correctly. Various things to improve.
# 17/08/2020 JGF Began adapting to play with a graphical card display.
# 19/08/2020 JGF Moved all the function defs into two custom modules.

#!!! things to fix or improve:
# quit on enter and input
# highlight the current player
# get all functions properly into the defs module
# tidy up the pickup logic
# re-do the TEST functionality
# AI can ask a player for cards twice
# grammar : passes 1 cards
# grammar : use "You"
# tidy up the check for sets logic
# merge the human and AI move logic

# === SETUP : Python libraries and program settings ===

import random
import time

# The custom Go Fish modules.
import gofishvisdefs as vis     # Pygame related defs, which also initialise Pygame
from gofishdefs import *        # Gameplay related defs

# Use tkinter for message and input boxes, and hide the main tkinter window.
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
tk.Tk().withdraw()

vis.pressenter()
vis.drawgame([], [], [], [], 0, 52, '', 'Let\'s get started...')

# Game constants and settings. All defined as globals in the gofishdefs module.
TEST = False
RANKS_IN_PACK = 8

# Functions to simplify the standard call which draws the game screen.
def drawGameUsual(msgtext, turn=-1):
    vis.drawgame(playernames, hand, playermessage, playersetsmade, humanpos, len(pack), packmessage, msgtext, turn)
def drawGameUsualEnter(msgtext, turn=-1):
    vis.drawgame(playernames, hand, playermessage, playersetsmade, humanpos, len(pack), packmessage,
                    f'{msgtext} Press ENTER to continue.', turn)

# === !!! SOME FUNCTIONS WHICH TEMPORARILY LIVE IN THE MAIN PROGRAM NOT THE MODULE ===

# A player needs to pick up from the pack. If it's the human player then report the card name.
def doPickUpFor(player, ishuman):
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
def doTheMove(player1, player2, askfor):
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


# === GET THE GAME STARTED ===

# Create and shuffle the pack.
pack = [{'rank':ranks[i], 'suit':suit} for i in range(8) for suit in suits]
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

# cool bit that Beth originally did here. Ask the player's name and how
# many people they would like to play against.

name = simpledialog.askstring('Go Fish', 'To get started, please type in your name:')
#players = simpledialog.askinteger('Go Fish', 'Hi ' + name + '. How many other players (2, 3 or 4) ' +
#                                'do you want?')
players = int(simpledialog.askstring('Go Fish', 'Hi ' + name + '. How many other players (2, 3 or 4) ' +
                                'do you want?'))
playernames = NAMES[0][0:players]


# add the human into the list of players, then deal all the hands
playernames.append(name)
players += 1
humanpos = players - 1
dealsize = (len(pack) - players*2 - 1) // players

# print('Dealing the cards,', dealsize, 'each.')
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
# and to show the communication between players.
setsmade = 0
playersetsmade = [0 for x in playernames]
knowledge = [{x : -1 for x in ranks} for y in range(players)]
playermessage = ['' for x in playernames]
packmessage = ''

# Show the hands ready to start the game.
drawGameUsualEnter('Ready to play.')
vis.pressenter()

# === MAIN GAME LOOP ===
gameover = False
while not gameover:
    for p in range(players):

        if p==humanpos:
            # Human player's turn. Input a move, check it, and repeat until they input a valid move

            # Check if they already have some sets. This could happen at the start of the game.
            setsfound = checkForSet(hand[humanpos])
            if setsfound!=0:
                setsmade += setsfound
                playersetsmade[humanpos] += setsfound
                if setsfound==1:
                    drawGameUsualEnter('You already made a set, that\'s a great start!')
                else:
                    drawGameUsualEnter(f'You already made {setsfound} sets, that\'s a fantastic start!')
                vis.pressenter()

            # !!! don't run through all this if there are no cards in either the hand or the pack
            # Pick up if needed
            if len(hand[p]) == 0:
                gamemsg = doPickUpFor(p, True)

            # Check if the player now has any cards, and carry out their turn
            if len(hand[p])==0:
                gamemsg = gamemsg + ' Your game is over, no more moves for you.'
                drawGameUsualEnter(gamemsg, turn=p)
                vis.pressenter()

            else:
                time.sleep(PAUSETIME)
                gamemsg = gamemsg + ' Press ENTER to make your move.'
                drawGameUsual(gamemsg, turn=p)
                vis.pressenter()
                while True:
                    movetext = simpledialog.askstring('Go Fish', 'Please type in your move:')
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
                    setsfound = checkForSet(hand[p])
                    if setsfound!=0:
                        setsmade += setsfound
                        playersetsmade[p] += setsfound
                        print ('You\'ve made a new set. You now have', playersetsmade[p], 'set(s) and', len(hand[p]), 'cards.')
                        if TEST:
                            print("--- JUST CHECKING! Your hand is now:")
                            showcards(hand[p], 0)
                        print()

            # End of human player's turn

        else:
            # AI turn. Check for existing sets in their hand. This could happen at the start of the game.
            setsfound = checkForSet(hand[p])
            if setsfound!=0:
                setsmade += setsfound
                playersetsmade[p] += setsfound
                gamemsg = f'{playernames[p]} starts by putting down {"a set." if setsfound==1 else f"{setsfound} sets!"}'
                drawGameUsualEnter(gamemsg, turn=p)
                vis.pressenter()

            # Pick up if needed, and if possible.
            if len(hand[p])==0:
                gamemsg = doPickUpFor(p, False)
                if len(hand[p])==0:
                    drawGameUsualEnter(f'{gamemsg}. {playernames[p]} must pass.', turn=p)
                else:
                    drawGameUsual(f'{gamemsg}. Press ENTER to continue their turn.', turn=p)
                vis.pressenter()

            else:
                # We finally get to the computer player's turn.
                # They choose a random card in their hand, ask a specific player if they know who holds them,
                # and a randomly chosen player otherwise
                if TEST:
                    print("--- JUST CHECKING! Their hand :")
                    showcards(hand[p], 0)
                askcard = hand[p][random.randint(1, len(hand[p])) - 1]['rank']
                if knowledge[p][askcard]!=-1:
                    askplayer = knowledge[p][askcard]
                else:
                    # Ask a randomly chosen player, making sure not to try to ask themselves
                    # or a player with no cards.
                    askplayer = random.randint(0, players - 1)
                    while askplayer==p or hand[askplayer]==[]:
                        askplayer = random.randint(0, players - 1)

                # Now carry out the chosen move
                playermessage[p] = f'- {playernames[askplayer]}, do you have any {askcard}s?'
                drawGameUsual(f'{playernames[p]} playing.', turn=p)
                goFish = doTheMove(p, askplayer, askcard)
                time.sleep(PAUSETIME)
                drawGameUsual(f'{playernames[p]} playing.', turn=p)

                # Pick up if neccessary.
                if goFish:
                    packmessage = doPickUpFor(p, False)
                    time.sleep(PAUSETIME)
                    drawGameUsual(f'{playernames[p]} playing.', turn=p)

                # Check if they made a set. Could be more than one at the start of the game.
                setsfound = checkForSet(hand[p])
                if setsfound!=0:
                    setsmade += setsfound
                    playersetsmade[p] += setsfound
                    gamemsg = f'{playernames[p]} Playing. Puts down {"a set." if setsfound==1 else f"{setsfound} sets!"}'
                    time.sleep(PAUSETIME)
                    drawGameUsualEnter(gamemsg, turn=p)
                else:
                    drawGameUsualEnter(f'{playernames[p]} playing.', turn=p)
                vis.pressenter()

            # End of computer player's turn.

        # Turn completed so go on to the next player. Unless all the sets are now made and the game is finished.
        playermessage = ['' for x in playernames]
        packmessage = ''

        if setsmade==RANKS_IN_PACK:
        # !!! FINISH this bit
            print('That\'s all the sets made. Here is the final score:')
            for p in range(players):
                print(playernames[p], ':', playersetsmade[p])
            print()
            gameover = True

        if gameover:
            break

        # End of player loop.  Continue on to the next player.
    # End of game loop. Continue with another round of turns.

# game finished so say goodbye
print("Game finished, hope you enjoyed it! Play again soon.")
vis.quit()
tk.Tk().destroy()