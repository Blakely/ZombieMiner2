#Filename: ZombieMiner.py
#Author: Ryan Blakely
#Last Modified By: Ryan Blakely
#Last Modified: July 30th, 2013 
#Description: A Simple mining game in which the player must collect mines and avoid zombies.


"""
Revision History:
 001  July 29,2013
      - Original game 
      - fow testing (drawFOW())
      - handlePlayer/Zombies (moved code from game loop)
      - testing various zombie collision logic change (clearing bag, resetting player pos, etc)
      - added resetPlayer
      
 002  July 30,2013
      - added a second "type" of zombie...employs same logic and stats
      - added centerpos constant for player instead of using startpos in scrollmap
      - handleZombie changed to handle different zombie types
      - more on handleZombie to check for sunlight before killing player. also stops zombie from moving
      - fixed handleZombie bug where it wouldnt entirely reach the tile and die...this was fixed with the dirtyPos fix
      - fixed resetPlayer bug where he could keep up after being reset (resets stepDist and act now)
      - "pixel perfect" (uses exact position) vs getPos which uses tilebased posit
      
 003  July 30, 2013
      - Finally fixed that stupid bug where if a zombie was dying it would freeze up (seemingly) random other zombies
        ... the "continue" line in handleZombies, instead of having break there.
      - added title to menu.png!
      - fixed the winningTile bug where it couldnt be broken
      - finally fixed a randomMapTemplate bug where it wasn't always making a full row of tiles (minor change in weighted random algorithm)
        ... added a default tile param
      - fixed scrolling edge bug (not letting you go up and down at the right side)...just a matter of an X where there needed to be a Y
      - changed up the fonts size and styles...gui doesnt entirely line up anymore, but im going to save that for the next iteration
      - fixed startTime to display minutes and seconds when games done
 
 004  July 30, 2013
      - ...fixed dates. everything was june lol
      - added a "fading vision" to the FOW drawing (drawVision)
      - finished off FOW w/ player vision stat
      - can now buy vision at shop
      - MASSIVE gui changes. lots of moving/resizing of labels and buttons
      - changed menu-to-game logic (game actually is started in menu now)
      - implemented multiple levels of difficulty & menu for it
      - implemented menu-to-menu logic (simple change menuWin)

 005  July 31st, 2013
      - slight gui changes - bolded stat font and changed the title font
      - fixed slight bug where it wouldnt update the stat window if cash zombies hit him
      - fixed bug where vision could still be bought at the store, even though there is no FOV
      - can now "disable" buttons - disabling clicks and darkening the buttons image
        ...added changeBrightness(img,factor) to gameFunctions and also added a few related constants
      - fixed a bug where nearby cash zombies would freeze if one was touching me
       ...the line returnWin = WIN_STAT fixed it, instead of instantly returning the window
       
006  July 31st, 2013
      - changed setWinningTile to set handle a "random placement" flag. also setup appropriate constants
      
006  Aug 1st, 2013
      - added game options dict to game() instead of multi-variables
      - massive changes in gameConstants for zombie stats and game options to streamline different level creation w/ different zombies
       ..also some changes to how createZombies works (and how its called), and also the level-menu logic
       ..also some changes to setWinningTile to accept a given tile position instead of using the constant
      - added dmg stat to miners based on strength to better regulate hit dmg
      
006  Aug 2nd, 2013
     - made some changes to Window - no longer uses a drawPos, simply self.pos
     - made some changes to labels to handle multi-line text
     ...this included major change to textImage in gameFunctions to handle multi-line text, since pygame doesnt natively support it
     - first instruction window essentially complete. other windows should be easy with the above changes :D. done 006!
"""


#import needed modules for pygame
import pygame, sys, random
from pygame.locals import *

#initialize pygame
pygame.init()
pygame.font.init()

#import constants, functions, and objects needed for the game
from gameConstants import *
from gameFunctions import *
from gameObjects import *

#Create any constants that require game objects to first be imported
#---------------------------------------------------------------------------------------
#windows image set for drawing windows
WINSET = ImageSet(IMG_WINSET,WINSET_PNLSIZE,TILE_TRANSCOLOR)
#button imageset for drawing buttons
BTNSET=ImageSet(IMG_BTNSET,BTNSET_PNLSIZE,TILE_TRANSCOLOR)


# ui elements for the shops items
SHOP_LBLS=[Label((50,50),   SHOP_LABEL_TEXT[0],WIN_FONT,WIN_FONT_COLOR),
           Label((50,80),   SHOP_LABEL_TEXT[1],WIN_FONT,WIN_FONT_COLOR),
           Label((50,110),  SHOP_LABEL_TEXT[2],WIN_FONT,WIN_FONT_COLOR)]
SHOP_BTNS=[Button(SHOP_BTN_STR,     (270,50),   BTNSET,textImage(SHOP_BTN_TEXT,BTN_FONT,WIN_FONT_COLOR)),
           Button(SHOP_BTN_SP,      (270,80),   BTNSET,textImage(SHOP_BTN_TEXT,BTN_FONT,WIN_FONT_COLOR)),
           Button(SHOP_BTN_VISION,  (270,110),  BTNSET,textImage(SHOP_BTN_TEXT,BTN_FONT,WIN_FONT_COLOR))]
#window for shopping in the game
SHOP_WIN=Window((ALIGN_CENTER,5),WINSET,len(SHOP_LBLS),SHOP_TITLE,SHOP_LBLS,SHOP_BTNS)


# ui elements for the main menu buttons
MENU_BTNS=[Button(MENU_BTN_PLAY,    (ALIGN_CENTER,50),  BTNSET,textImage(MENU_BTN_PLAY,BTN_FONT,WIN_FONT_COLOR)),
           Button(MENU_BTN_HOW,     (ALIGN_CENTER,80),  BTNSET,textImage(MENU_BTN_HOW,BTN_FONT,WIN_FONT_COLOR)),
           Button(MENU_BTN_EXIT,    (ALIGN_CENTER,110), BTNSET,textImage(MENU_BTN_EXIT,BTN_FONT,WIN_FONT_COLOR))]
#window for the main menu  
MENU_WIN=Window((ALIGN_CENTER,ALIGN_CENTER),WINSET,len(MENU_BTNS),MENU_TITLE,None,MENU_BTNS)


# ui elements for the level select menu buttons
LVL_BTNS=[Button(MENU_LVL_BTN_FREE, (ALIGN_CENTER,55),  BTNSET,textImage(MENU_LVL_BTN_FREE,BTN_FONT,WIN_FONT_COLOR)),
          Button(MENU_LVL_BTN_EZ,   (ALIGN_CENTER,85),  BTNSET,textImage(MENU_LVL_BTN_EZ,BTN_FONT,WIN_FONT_COLOR)),
          Button(MENU_LVL_BTN_MED,  (ALIGN_CENTER,115), BTNSET,textImage(MENU_LVL_BTN_MED,BTN_FONT,WIN_FONT_COLOR)),
          Button(MENU_LVL_BTN_HARD, (ALIGN_CENTER,145), BTNSET,textImage(MENU_LVL_BTN_HARD,BTN_FONT,WIN_FONT_COLOR)),
          Button(MENU_BTN,          (ALIGN_CENTER,185), BTNSET,textImage(MENU_BTN,BTN_FONT,WIN_FONT_COLOR))]
#window for level/difficulty select menu
LVL_WIN = Window((ALIGN_CENTER,ALIGN_CENTER),WINSET,len(LVL_BTNS)+1,MENU_LVL_TITLE,None,LVL_BTNS)


#text for the main instructions window
HOW_TXT =\
"""
You're just been robbed! A gang of zombies mugged
you and made off with your stash of beloved meth.

There's no way in hell you're going to part with
that sweet, precious meth, so you decide to follow
the zombies and track them back to a nearby cave.

Your objective is to venture into the cave and 
recover your stolen meth as fast as possible!

...and probably best try to avoid those zombies, too!
"""

# ui elements for the instruction windows
HOW_LBLS=[Label((ALIGN_CENTER,ALIGN_CENTER),HOW_TXT,WIN_FONT,WIN_FONT_COLOR,LBL_LINE_DLIM,True)]
HOW_BTNS=[Button(HOW_BTN_MECH,  (30,ALIGN_BOTTOM),  BTNSET,textImage(HOW_BTN_MECH,BTN_FONT,WIN_FONT_COLOR)),
          Button(MENU_BTN,      (200,ALIGN_BOTTOM), BTNSET,textImage(MENU_BTN,BTN_FONT,WIN_FONT_COLOR))]
#window for instructions
HOW_WIN=Window((ALIGN_CENTER,ALIGN_CENTER),WINSET,len(HOW_LBLS[0].text.split(LBL_LINE_DLIM))+1,HOW_TITLE,HOW_LBLS,HOW_BTNS)


#text for the mechanics window
HOW_MECH_TXT =\
"""
There is a small prospecting shop outside that will
purchase any minerals you may come across while
exploring and train you to navigate
the cave more efficiently.

From your understanding of modern day zombies, they
should burst into flames once the sun touches them,
so your best bet if you run into any zombies is to
lead them out and into the sun.

P.S. Use the arrow keys to move your character!
"""
# ui elements for the game mechanics window
HOW_MECH_LBLS=[Label((ALIGN_CENTER,ALIGN_CENTER),HOW_MECH_TXT,WIN_FONT,WIN_FONT_COLOR,LBL_LINE_DLIM,True)]
HOW_MECH_BTNS=[Button(HOW_BTN_ZOMBIES,  (30,ALIGN_BOTTOM),  BTNSET,textImage(HOW_BTN_ZOMBIES,BTN_FONT,WIN_FONT_COLOR)),
               Button(MENU_BTN,         (200,ALIGN_BOTTOM), BTNSET,textImage(MENU_BTN,BTN_FONT,WIN_FONT_COLOR))]
HOW_MECH_WIN=Window((ALIGN_CENTER,ALIGN_CENTER),WINSET,len(HOW_MECH_LBLS[0].text.split(LBL_LINE_DLIM))+1,HOW_MECH_TITLE,HOW_MECH_LBLS,HOW_MECH_BTNS)


#text for the zombies window
HOW_ZOMBIES_TXT =\
"""
There is a small prospecting shop outside that will
purchase any minerals you may come across while
exploring and train you to navigate
the cave more efficiently.

From your understanding of modern day zombies, they
should burst into flames once the sun touches them,
so your best bet if you run into any zombies is to
lead them out and into the sun.

P.S. Use the arrow keys to move your character!
"""
# ui elements for the zombies window
HOW_ZOMBIES_LBLS=[Label((ALIGN_CENTER,ALIGN_CENTER),HOW_ZOMBIES_TXT,WIN_FONT,WIN_FONT_COLOR,LBL_LINE_DLIM,True)]
HOW_ZOMBIES_BTNS=[Button(HOW_BTN_MINES,  (30,ALIGN_BOTTOM),  BTNSET,textImage(HOW_BTN_ZOMBIES,BTN_FONT,WIN_FONT_COLOR)),
                  Button(MENU_BTN,         (200,ALIGN_BOTTOM), BTNSET,textImage(MENU_BTN,BTN_FONT,WIN_FONT_COLOR))]
HOW_ZOMBIES_WIN=Window((ALIGN_CENTER,ALIGN_CENTER),WINSET,len(HOW_ZOMBIES_LBLS[0].text.split(LBL_LINE_DLIM))+1,HOW_ZOMBIES_TITLE,HOW_ZOMBIES_LBLS,HOW_ZOMBIES_BTNS)


#text for the minerals window
HOW_MINES_TXT =\
"""
There is a small prospecting shop outside that will
purchase any minerals you may come across while
exploring and train you to navigate
the cave more efficiently.

From your understanding of modern day zombies, they
should burst into flames once the sun touches them,
so your best bet if you run into any zombies is to
lead them out and into the sun.

P.S. Use the arrow keys to move your character!
"""
# ui elements for the minerals window
HOW_MINES_LBLS=[Label((ALIGN_CENTER,ALIGN_CENTER),HOW_MINES_TXT,WIN_FONT,WIN_FONT_COLOR,LBL_LINE_DLIM,True)]
HOW_MINES_BTNS=[Button(MENU_BTN,(ALIGN_CENTER,ALIGN_BOTTOM), BTNSET,textImage(MENU_BTN,BTN_FONT,WIN_FONT_COLOR))]
HOW_MINES_WIN=Window((ALIGN_CENTER,ALIGN_CENTER),WINSET,len(HOW_MINES_LBLS[0].text.split(LBL_LINE_DLIM))+1,HOW_MINES_TITLE,HOW_MINES_LBLS,HOW_MINES_BTNS)
                
#=========================================================================================
#                     MAIN/GAME FUNCTIONS
#=========================================================================================            

#attempts to perform an action for a Miner in a particular direction
#screen (pygame Surface) - the screen for the game
#miner (Miner) - the acting miner
#direction (int) - the direction being acted in
#tilemap (TileMap) - the tilemap the action is taking place on
#returns - the next tile in the specified direction from the miner on the tilemap, if it can be acted on. otherwise dont return anything
def tryAction(screen,miner,direction,tilemap):
    #get the direction vector for the desired action
    if(direction==DIR_RIGHT):
        move=(1,0)
    elif(direction==DIR_LEFT):
        move=(-1,0)
    elif(direction==DIR_UP):
        move=(0,-1)
    elif(direction==DIR_DOWN):
        move=(0,1)
    
    #determine the next tile position in the desired direction
    nextPos = (miner.getPos()[X]+move[X],miner.getPos()[Y]+move[Y])
    
    #make sure the next position to be acted towards is within the screens dimensions
    if(nextPos[X]>=0 and nextPos[X]<tilemap.getSize()[X] and
       nextPos[Y]>=0 and nextPos[Y]<tilemap.getSize()[Y]):
        nextTile = tilemap.getTile(nextPos) #get the next tile in the chosen direction
        
        #if new direction next tileis blocked...
        if(nextTile.attributes['type']==MINE_BLOCK_FULL):
            return None #can't walk in that direction
        
        #if new direction is up, but up is blocked...
        elif (direction==DIR_UP and tilemap.getTile(nextPos).attributes['type']==MINE_BLOCK_UP):
            return None #can't act in that direction
        
        #if the new direction is diggable
        elif (nextTile.attributes['type']==MINE_DIGGABLE):
            if(miner.doAction(ACT_DIG)): #dig it and return the tile being dug
                return nextTile
        
        else: #if the new direction is free and the player is trying to move
            if(miner.doAction(ACT_WALK,(move[X]*tilemap.tileSize[X],move[Y]*tilemap.tileSize[Y]))):
                return nextTile

#BUG - this seems to have some issues on the right side and the bottom :( I thought I had it fixed until last minute
#scrolls the map if necessary
#screen (pygame Surface) - screen to move the map on
#player (Miner) - the player (needed for position)
#tilemap (TileMap) - the tilemap to scroll
#moveVect (tuple) - the scroll vector
def scrollMap(screen,player,tilemap,moveVect):
    #if the player has reached an edge of the map on the x-axis, dont move the map in that direction anymore
    if (player.getPos()[X]<PLAYER_CENTERPOS[X]
        or player.getPos()[X]>tilemap.getSize()[X]-PLAYER_CENTERPOS[X]-1
        or player.getPos()[X]==PLAYER_CENTERPOS[X] and player.dir==DIR_RIGHT):
        moveVect=(0,moveVect[Y])
    
    #if the player has reached an edge of the map on the y-axis, dont move the map in that direction anymore (FIXED)
    if (player.getPos()[Y]<PLAYER_CENTERPOS[Y]
        or player.getPos()[Y]>tilemap.getSize()[Y]-PLAYER_CENTERPOS[Y]-1
        or player.getPos()[Y]==PLAYER_CENTERPOS[Y] and player.dir==DIR_DOWN):
        moveVect=(moveVect[X],0)
    
    tilemap.move((-moveVect[X],-moveVect[Y]),(0,0),screen.get_size())

#creates the zombies!
#zData (dict) - zombie data for the to-be-created zombies. contains img, stats, and number of zombies
#tilemap (TileMap) - the tilemap to create the zombies on (only needed to replace tiles for zombie space)
#tileset (ImageSet) - the tileset for the tilemap (again, only needed for replace tiles for zombie space)
#spriteTemplate (3d list) - the sprite template for the zombies
#player (Miner) - the player, AKA the zombies (ai's) target
#startPos (tuple) - the start position on the tilemap to start allowing zombies (wont allow placement < startPos)
def createZombies(zData,tilemap,tileset,spriteTemplate,target,startPos=(0,0)):
    zombieImg=loadImage(zData[ZOMBIE_IMG],TILE_TRANSCOLOR) #load spriteset image for zombies
    zombieAI = AI(target) #setup a simple AI that targets the player
    
    zombies=list() #holder list for zombies
    
    #create given # of zombies
    for z in range(0,zData[GAME_OPT_ZOMBIE_NUM]):
        #randomly choose a position for the zombie to start -- goes to width -1 and height - 1, to account for border
        randomPos = (random.randint(startPos[X],tilemap.getSize()[X]-2),random.randint(startPos[Y],tilemap.getSize()[Y]-2))
        
        zombieStats = zData[ZOMBIE_STATS].copy() #make a copy of the stats soas not to effect other zombies
        
        #mod base stats based on the random position - further away zombies will be harder/faster
        for stat in zombieStats.keys():
            zombieStats[stat]=zombieStats[stat]*(randomPos[X]+randomPos[Y])/2
        
        #create a new zombie and add it to the list of zombies
        zombie = Mob(randomPos,SpriteSet(zombieImg,SPRITE_SIZE,spriteTemplate),zombieStats,zombieAI)
        zombies.append(zombie)
        
        #change the tile to be a "broken" one at the randomly chosen position
        tilemap.getTile(randomPos).change(mines[MINE_DUG],tileset[MINE_DUG])
    
    return zombies

#attempts to get the player to buy a stat at a particular cost
#player (Miner) - the player
#stat (str) - the stat being bought
#cost (int) - the cost of the stat
#returns - True if it could be afforded, false otherwise
def buyStat(player,stat,cost):
    #if the player can afford the stat
    if (player.stats[STAT_MONEY]>=cost):
        player.addStat(stat,1)
        player.subStat(STAT_MONEY,cost)
        return True
    else:
        return False

#creates the players statistics window
#player (Miner) - the player
#returns - the statistics window
def createStatWin(player):
    #ui elements for stats window
    statLbls = [Label((50,5),"Strength : " + str(player.stats[STAT_STR]),WIN_STAT_FONT,WIN_FONT_COLOR),
                Label((50,25),"Speed       : " + str(player.stats[STAT_SP]),WIN_STAT_FONT,WIN_FONT_COLOR),
                Label((230,5), "Bag    : " + str(len(player.stats[STAT_BAG])) + " / " + str(player.stats[STAT_MAXBAG]),
                      WIN_STAT_FONT,WIN_FONT_COLOR),
                Label((230,25),"Cash  : " + str(player.stats[STAT_MONEY]),WIN_STAT_FONT,WIN_FONT_COLOR)]
    
    #create the stat window
    statWin = Window((ALIGN_CENTER,ALIGN_BOTTOM),WINSET,0,None,statLbls)
    
    return statWin

#creates the end-game screen, win or lose
#title (str) - the title for the window
#msg (str) - the inner msg for the window
#returns- the end game window
def createEndWin(title, msg):
    # ui elements for the shops items
    endLbls=[Label((ALIGN_CENTER,48),msg,WIN_FONT,WIN_FONT_COLOR)]
    endBtns=[Button(MENU_BTN,(ALIGN_CENTER,82),BTNSET,textImage(MENU_BTN,BTN_FONT,WIN_FONT_COLOR))]
    
    #setup window for shopping    
    return Window((ALIGN_CENTER,ALIGN_CENTER),WINSET,len(endLbls)+len(endBtns),title,endLbls,endBtns)

#sets a particular tile on the tilemap to be the winning tile
#tilemap (TileMap) - tilemap to place the mine on
#tileset (TileSet) - the tileset to choose the mine from
def setWinningTile(pos,tilemap,tileset):
    (tileX,tileY)=pos
    
    if(pos[X]==WIN_POS_RAND):
        tileX=random.randint(1,tilemap.size[X]-1)
    if(pos[Y]==WIN_POS_RAND):
        tileY=random.randint(1,tilemap.size[Y]-1)
        
    tilemap.getTile((tileX,tileY)).change(mines[MINE_WIN],tileset[MINE_WIN])

#draws a "fading" vision circle around the player
def drawVision(fowImg,tilemap,player):
    vision=(player.pos[X]+VISION_OFFSET[X],player.pos[Y]+VISION_OFFSET[Y],player.stats[STAT_RANGE])
    alpha=FADE_MAX_ALPHA
    steps=0 #no fading steps

    #loop through each fading step of the circle fade until its untirely faded (base circle, faded ring, more faded ring, etc until black)
    while alpha>=FADE_MIN_ALPHA:
        #determine the vision radius based on the players vision & current fade step
        visionRadius=vision[R]-steps*FADE_STEP_DIST
        if visionRadius<0:
            visionRadius=0
        
        pygame.draw.circle(fowImg,Color(0,0,0,alpha),
                           (vision[X]+tilemap.shift[X],
                            vision[Y]+tilemap.shift[Y]),
                           visionRadius)
        
        alpha-=FADE_STEP_ALPHA
        steps+=1
            
    
def drawFOW(screen,tilemap,player,clearings=None):
    #create a new surface to paint the fow onto
    fowImg = pygame.Surface(screen.get_size())
    fowImg=fowImg.convert_alpha()
    fowImg.fill(Color(0,0,0,255))
    
    #draw the circle around the player - MUST be called before other clearings, as the fade messes with things
    drawVision(fowImg,tilemap,player)
    
    #if theres any "clearings" (fow-clear areas), loop through the areas and clear them of FOW
    if(clearings):
        for area in clearings:
            for area in clearings:
                if (len(area)==3):
                    #draw a circle
                    pygame.draw.circle(fowImg,Color(0,0,0,0),(area[X]+tilemap.shift[X],area[Y]+tilemap.shift[Y]),area[R])
                if (len(area)==4):
                    #draw a rectangle
                    pygame.draw.rect(fowImg,Color(0,0,0,0),(area[X]+tilemap.shift[X],area[Y]+tilemap.shift[Y],area[W],area[H]))
    
    #draw the fow image to the screen
    screen.blit(fowImg,(0,0))


def resetPlayer(player):
    player.setPos(PLAYER_STARTPOS)
    #player.lastMod+= 3000 #FIX?? delay after reset
    player.frame=0
    player.act=ACT_NONE
    player.stepDist=(0,0)
    player.actTile=None
    player.updateFrame()


def handlePlayer(screen,tilemap,tileset,player):
    #update the player and get the returned action data
    playerAct=player.update()
    
    #if the finished act is a tuple (e.g. a move vector)
    if (type(playerAct) is tuple):
        moveVect = playerAct
        #scroll the map the distance that the player has moved
        scrollMap(screen,player,tilemap,moveVect)
        
    # if the player is done hitting
    elif (playerAct==ACT_DIG):
        pHitTile = player.actTile
        pHitResult = pHitTile.hit(STAT_DMG_BASE+player.stats[STAT_DMG])

        #if the hit returned a result (broke?)
        if(pHitResult!=None):
            pHitTile.change(mines[MINE_DUG],tileset[MINE_DUG]) #set the dug-out tiles attributes and image to "dug" tile
            
            #if the player just broke the winning mine, show the winning game screen
            if(pHitResult==MINE_VAL_WIN):
                return WIN_END
                
            else: #otherwise, if it was a normal tile...
                player.addToBag(pHitResult) #add the tiles value to the players bag
                return WIN_STAT #create a new stat window (basically an update, but i never wrote an update)
    
    return None

def handleZombies(screen,tilemap,tileset,zombies,player,fireSet):
    returnWin=None
    
    #loop through each zombie to update
    for z in range(0,len(zombies)):
        zombie=zombies[z]
        
        #if the zombie is outside...
        if (tilemap.getTile(zombie.getPos()).attributes['type']==MINE_BLOCK_UP):
            #dying animation. when the animation is complete, remove the zombie from the tilemap and the game
            if(zombie.dying(fireSet,SPRITE_MASK_DELAY)):
                tilemap.clearMob(z)
                zombies.remove(zombie)
                break
            continue #go to next zombie!
        
        #otherwise if the zombie is touching the player - perform special zombie action!
        elif (zombie.pos == player.pos):
            #if its a killer zombie, end the game.
            if(zombie.stats[STAT_TYPE]==ZOMBIE_TYPE_KILL):
                #return instantly and end the game
                return WIN_END
            
            #if its a cash zombie, steal the players cash and bag
            elif(zombie.stats[STAT_TYPE]==ZOMBIE_TYPE_CASH):
                player.stats[STAT_MONEY]=0
                player.clearBag()
            
            #if its an easy zombie, steal the bag and send player
            elif (zombie.stats[STAT_TYPE]==ZOMBIE_TYPE_EZ):
                #basic zombie - clear the players bag and return him to home
                resetPlayer(player)
                player.clearBag()
                tilemap.shift=(0,0)
            
            #if the game didn't end, the stat window needs to be updated, so set the return flag (FIXED)
            returnWin = WIN_STAT
        
        #let the AI kick in to choose a direction,then try and act in that direction
        nearTiles=tilemap.getNearTiles(zombie.getPos()) #get tiles around zombie
        newDir=zombie.runAI(nearTiles)#get ai to choose path based on nearby tiles
        
        #try to act in the direction chosen
        zTryResult = tryAction(screen,zombie,newDir,tilemap)
        if(zTryResult):
            zombie.actTile=zTryResult
                
        #update the zombie and get the returned action data
        zombieAct=zombie.update()
        
        #if the zombie is hitting
        if (zombieAct==ACT_DIG):
            zHitTile = zombie.actTile #get the tile the zombie is trying to hit
            zHitResult = zHitTile.hit(zombie.stats[STAT_STR])
            
            #if the hit returned a result (broke?)
            if(zHitResult!=None):
                #set the dug-out tiles attributes and image to "dug" tile
                zHitTile.change(mines[MINE_DUG],tileset[MINE_DUG])
                
    return returnWin

#main game loop - handles all game logic - runs until the user quits or returns to main menu
# screen (pygame Surface) - the game screen!
def game(screen,options):
    startTime = pygame.time.get_ticks()
    
    #setup and create the player
    playerImg=loadImage(IMG_PLAYER,TILE_TRANSCOLOR) #load the spriteset image for the player (miner)
    player = Miner(PLAYER_STARTPOS,SpriteSet(playerImg,SPRITE_SIZE,SPRITE_TEMPLATE),PLAYER_STATS)

    #create the template for the mine map
    template=randomMapTemplate(options[GAME_OPT_MAP_SIZE],mines,MINE_ROCK) #create random map template of mines
    template.setBorder(MINE_ROCK) #set the border to be all unbreakable bricks
    aboveground=mapReader(MAP_FILE,MAP_FILE_DLIM) #load in custom map for aboveground
    template.setArea((0,0),aboveground) #combine random minemap with aboveground map @ top left corner
        
    #load in the tileset and tile maskset for the game 
    tileset = ImageSet(IMG_TILESET,TILE_SIZE,TILE_TRANSCOLOR)
    maskSet = ImageSet(IMG_CRACKS,TILE_SIZE,TILE_TRANSCOLOR)

    #create the TileMap for the game and create/add zombies
    tilemap=TileMap(template,tileset,TILE_SIZE,player,maskSet)
    
    #create all the zombies for the level (type by type) & add them to the map
    zombies=list()
    for zData in options[GAME_OPT_ZOMBIES]:
        zombies = zombies + createZombies(zData.copy(),tilemap,tileset,SPRITE_TEMPLATE,player,(1,len(aboveground))) #copy zombie data (zData) so it doesnt overwrite later plays
    tilemap.addMobs(zombies) #add zombies to the tilemap
    
    setWinningTile(options[GAME_OPT_WIN_POS],tilemap,tileset)#place the winning tile!

    #setup the fire spriteset for any zombies that need to burn!
    fireImg=loadImage(IMG_FIRE,TILE_TRANSCOLOR)
    fireSet=SpriteSet(fireImg,SPRITE_SIZE,FIRE_TEMPLATE)[0][0] #spritesets are dicts, but we only need the first "act"+"dir" of it for this (which is a list)
    
    #setup windows
    shopWin = SHOP_WIN  #setup the shop window
    statWin = createStatWin(player) #setup window for stats
    endWin = None #initialize the "end game" window - if this is set, the game is over
    
    #if fow is set, and the vision button exists (though why wouldnt it??), disable the button
    if (not options[GAME_OPT_FOW] and shopWin.getButton(SHOP_BTN_VISION)):
        shopWin.getButton(SHOP_BTN_VISION).disable()
    
    #set pygame to "repeat" key-presses (basically key toggling)
    pygame.key.set_repeat(50,50)
    
    #play the game for as long as this is true
    play=True
    
    #begin game loop
    while play:
        
        #check all of the events that have occured since last loop
        for event in pygame.event.get():
            #if users quits, exit the game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            #if a key was pressed and the game isnt over yet...
            elif (event.type == KEYDOWN and not endWin):
                #determine which direction to act based on what key was pressed
                if (event.key==K_UP):
                    direction = DIR_UP
                elif (event.key==K_DOWN):
                    direction = DIR_DOWN
                elif (event.key==K_LEFT):
                    direction = DIR_LEFT
                    player.setDir(DIR_LEFT) #change the visual direction of the player sprite
                elif (event.key==K_RIGHT):
                    direction = DIR_RIGHT
                    player.setDir(DIR_RIGHT) #change the visual direction of the player sprite
                else:
                    continue #ignore other keyboard inputs (go to next event)
                
                #try to act on the next tile in the chosen direction
                pTryResult=tryAction(screen,player,direction,tilemap)
                if(pTryResult): #if the action went through, get which tile was affected (or the move vector)
                    player.actTile=pTryResult
            
            #if the mouse was clicked, check if any buttons were clicked
            elif event.type == MOUSEBUTTONDOWN:
                #if ending window is shown (game is over), detect clicks for ending window
                if(endWin):
                    clicked=endWin.click(screen,event.pos)
                
                #otherwise, check shop window for clicks
                else:
                    clicked=shopWin.click(screen,event.pos)
                
                #if a button was infact clicked, determine which button and take appropriate actions
                if(clicked):
                    if(clicked==SHOP_BTN_STR):
                        buyStat(player,STAT_STR,SHOP_COST_STR) #player bought str
                    elif (clicked==SHOP_BTN_SP):
                        buyStat(player,STAT_SP,SHOP_COST_SP) #player bought sp
                    elif (clicked==SHOP_BTN_VISION):
                        print 'test'
                        buyStat(player,STAT_VISION,SHOP_COST_VISION) #player bought vision
                    elif (clicked==MENU_BTN):
                        play=False #game is over (exits game loop) and player returned to main menu
                        break
                        
                    #update the stat window  
                    statWin=createStatWin(player)

        #always clear screen and redraw tilemap - doesn't matter if game is over or not
        
        screen.fill(Color(0,0,0))
        tilemap.draw(screen)
        
        #if the game isn't over yet, run updates for players and zombies and draw any necessary windows/fow
        if (not endWin):
            #draw the "fog of war" (or lackthereof) if its set as a game option
            if (options[GAME_OPT_FOW]):
                #aboveground is in the within the fog of war
                drawFOW(screen,tilemap,player,[[0 , 0 , len(aboveground[0])*tilemap.tileSize[X] , len(aboveground)*tilemap.tileSize[Y]]])
                
            
            #HANDLE PLAYER
            #work horse function for handling the player
            updateUI=handlePlayer(screen,tilemap,tileset,player)
            
            #if any UI updates need to take place from handling the player, do them
            if(updateUI==WIN_STAT):
                statWin = createStatWin(player)
            if (updateUI==WIN_END):
                minutes= str((pygame.time.get_ticks() - startTime)/1000/60)
                seconds=str(((pygame.time.get_ticks() - startTime)/1000) % 60)
                endWin=createEndWin("You Win!","Time : " + minutes + " minutes, " + seconds + " seconds")
            
            
            #HANDLE ZOMBIES
            #work horse function for handling the zombies
            updateUI=handleZombies(screen,tilemap,tileset,zombies,player,fireSet)
            
            #if any UI updates need to take place from handling the zombies, do them.
            if(updateUI==WIN_STAT):
                statWin = createStatWin(player)
            elif(updateUI==WIN_END):
                endWin = createEndWin("Game Over","You have died!")
            
            
            #HANDLE WINDOW DRAWING 
            #if the player is sitting on a shop tile, show shop!
            if(tilemap.getTile(player.getPos()).attributes['type']==MINE_SHOP):
                player.addStat(STAT_MONEY,player.clearBag()) #exchange bag for moneys
                statWin=createStatWin(player) #update the stat window
                shopWin.visible=True
            else: #otherwise....dont!
                shopWin.visible=False
            
            #draw the stat window and shop window...they will only draw if visible
            statWin.draw(screen)
            shopWin.draw(screen) 
        
        #if the game is over(endWin is defined), show the end game window
        else:
            endWin.draw(screen)
#WINDOW DRAWING DONE ==========================================================================

        #update the display
        pygame.display.flip()

   
#creates, displays, and handles events for the main menu for the game
#screen (pygame Surface) - the game screen to draw to
def menu(screen):
    menuWin = MENU_WIN #creates the menu window
    bgImg = loadImage(IMG_MENUBG) #menus background image
    
    #keep showing the menu until the user decides to go elsewhere
    while True:
        for event in pygame.event.get():
            #if users quits, exit the game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            #if the mouse was clicked, check if any buttons were clicked
            elif event.type == MOUSEBUTTONDOWN:
                clicked=menuWin.click(screen,event.pos)
                if(clicked):
                    #MISC Clicks- can occur on various windows -----------------------------
                    #return to main menu button
                    if(clicked==MENU_BTN):
                        menuWin= MENU_WIN
                        
                    #The "Main Menu" Clicks ------------------------------------------------
                    #if the "play" button was clicked, exit the main menu and start the game
                    elif(clicked==MENU_BTN_PLAY):
                        menuWin= LVL_WIN
                        
                    #if the instructions button was clicked, show the instructions window
                    elif (clicked==MENU_BTN_HOW):
                        menuWin=HOW_WIN
                    
                    #if the exit button was clicked, close the game
                    elif (clicked==MENU_BTN_EXIT):
                        pygame.quit()
                        sys.exit()
                    
                    #The "Level Menu" Clicks ------------------------------------------------
                    #if a game-level button was clicked, start the game with the selected difficulty
                    else:
                        #start game based on which difficulty buttonw as selected
                        if (clicked):
                            game(screen,GAME_LVLS[clicked]) #btn name should has to match up with game difficulty name for this to work
                        menuWin=MENU_WIN #go back to main menu after game
                    
        #draw the background image & menu window
        screen.blit(bgImg,(0,0))
        menuWin.draw(screen)
        
        pygame.display.flip() #update the display

#main program - sets up the display & controls between-screen flow (mainmenu, game)
def main():
    #setup game screen
    gameScreen = pygame.display.set_mode(SCREEN_SIZE)
    
    #continue to loop through the menu & game until the program is exited
    while True:
        #start the menu
        menu(gameScreen)
    
        #start the game (if "play" was clicked in menu)
        #game(gameScreen)

#Start the program
if __name__ == "__main__":
    main()