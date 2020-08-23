# Go Fish visual module.
# All the detailed Pygame defs to display the card table.

import pygame
from pygame.locals import *

# Set up pygame.
pygame.init()

# Set up the colors.
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
RED = (196, 0, 0)
BLUEGREEN = (0, 128, 196)
TABLECOLOUR = GREEN
PNAMECOLOUR = BLACK
MSGCOLOUR = WHITE
BACKCOLOUR = BLUEGREEN

# Define some sizes and dimensions
HCARD = 64
WCARD = 40
PNAMETOP = 30
PNAMELEFT = 30
PGAP = 90
PCARDLEFT = 200
PCARDGAP = 45
PSETSLEFT = 950
TABLEWIDTH = 1100
TABLEHEIGHT = 650
TITLE = 'Go Fish'

# Define some fonts we'll use.
suitFont = pygame.font.SysFont('arial', 36)
rankFont = pygame.font.SysFont('arial', 20)
pnameFont = pygame.font.SysFont('arial', 32)
msgFont = pygame.font.SysFont('arial', 20)

# Set up the window.
windowSurface = pygame.display.set_mode((TABLEWIDTH, TABLEHEIGHT), 0, 32)
windowSurface.fill(TABLECOLOUR)
textImg = pnameFont.render('Welcome to Go Fish! Press ENTER to play.', True, WHITE, TABLECOLOUR)
textRect = textImg.get_rect()
textRect.centerx, textRect.centery = TABLEWIDTH / 2, TABLEHEIGHT / 2
windowSurface.blit(textImg, textRect)
pygame.display.set_caption(TITLE)
pygame.display.update()

# Create an image for the four suits
suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
suitchars = ['\u2660', '\u2665', '\u2666', '\u2663']
suitImages = {suit :
                suitFont.render(char, True,
                                BLACK if suit in ['Spades', 'Clubs'] else RED,
                                WHITE)
                for (suit, char) in zip(suits, suitchars)}

# Draw a specified card.
def drawcard(card, xpos, ypos):
    # Create the card.
    cardSurf = pygame.Surface((WCARD, HCARD))
    cardSurf.fill(WHITE)
    cardRect = cardSurf.get_rect()
    # Draw the rank on the card.
    rankImg = rankFont.render(card['rank'], True,
                BLACK if card['suit'] in ['Spades', 'Clubs'] else RED,
                WHITE)
    textRect = rankImg.get_rect()
    textRect.left, textRect.top = 2, 0
    cardSurf.blit(rankImg, textRect)
    textRect.right = cardRect.right - 2
    textRect.bottom = cardRect.bottom
    cardSurf.blit(rankImg, textRect)
    # Draw the suit on the card.
    suitImg = suitImages[card['suit']]
    textRect = suitImg.get_rect()
    textRect.centerx = cardRect.centerx
    textRect.centery = cardRect.centery - 5
    cardSurf.blit(suitImg, textRect)
    # Draw the card on the card table.
    windowSurface.blit(cardSurf, (xpos, ypos))

# Draw a face-down card with an optional number on the back.
def drawback(xpos, ypos, num=0):
    # Create the card.
    cardSurf = pygame.Surface((WCARD, HCARD))
    cardSurf.fill(BACKCOLOUR)
    cardRect = cardSurf.get_rect()
    # Draw the number on the card.
    if num != 0:
        textImg = rankFont.render(str(num), True, MSGCOLOUR, BACKCOLOUR)
        textRect = textImg.get_rect()
        textRect.centerx = cardRect.centerx
        textRect.centery = cardRect.centery
        cardSurf.blit(textImg, textRect)
    # Draw the card on the card table.
    windowSurface.blit(cardSurf, (xpos, ypos))

# Draw some text at a specific x,y location.
def drawtext(text, Font, fgcolour, bgcolour, xpos, ypos):
    textImg = Font.render(text, True, fgcolour, bgcolour)
    windowSurface.blit(textImg, (xpos, ypos))

# Redraw the game window and clear the event queue.
def drawgame(pnames, hands, messages, sets, humanpos, packnum, packmsg, prompt, turn=-1):
    # Clear the window.
    windowSurface.fill(TABLECOLOUR)

    # Display each player.
    for p, name in enumerate(pnames):
        drawtext(name, pnameFont, PNAMECOLOUR, TABLECOLOUR, PNAMELEFT, PNAMETOP + p*PGAP)
        # Draw the cards in the player's hand.
        for c, card in enumerate(hands[p]):
            if p == humanpos:
                drawcard(card, PCARDLEFT + c*PCARDGAP, PNAMETOP + p*PGAP)
            else:
                drawback(PCARDLEFT + c*PCARDGAP, PNAMETOP + p*PGAP)
        # Show the player's message.
        if messages[p] != '':
            textImg = msgFont.render(messages[p], True, MSGCOLOUR, TABLECOLOUR)
            textRect = textImg.get_rect()
            textRect.left, textRect.top = PCARDLEFT, PNAMETOP + p*PGAP + HCARD
            windowSurface.blit(textImg, textRect)

        # Show the player's score if they have one.
        if sets[p] > 0:
            drawback(PSETSLEFT, PNAMETOP + p*PGAP, num=sets[p])

    # Show the pack if there are any remaining cards, and any message text next to the pack.
    textImg = msgFont.render(packmsg, True, MSGCOLOUR, TABLECOLOUR)
    if packnum > 0:
        drawback(PCARDLEFT, PNAMETOP + len(pnames)*PGAP, packnum)
        windowSurface.blit(textImg, (PCARDLEFT + PCARDGAP, PNAMETOP + len(pnames)*PGAP))
    else:
        windowSurface.blit(textImg, (PCARDLEFT, PNAMETOP + len(pnames)*PGAP, packnum))


    # Write the prompt message at the bottom of the window.
    textImg = msgFont.render(prompt, True, MSGCOLOUR, TABLECOLOUR)
    textRect = textImg.get_rect()
    textRect.left, textRect.bottom = PNAMELEFT, TABLEHEIGHT
    windowSurface.blit(textImg, textRect)
    # Redisplay the window and clear the event queue.
    pygame.display.update()
    for event in pygame.event.get():
        pass

# Wait until ENTER is pressed.
def pressenter():
    enter = False
    while not enter:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                enter = True

# Close pygame.
def quit():
    pygame.quit()