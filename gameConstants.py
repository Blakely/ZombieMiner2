#Filename: gameConstants.py
#Author: Ryan Blakely
#Last Modified By: Ryan Blakely
#Last Modified: July 30th, 2013
#Description: Constants required for the ZombieMiner.py game

#Revision History:
# July 29,13 - fixed constants to speed up game
# July 30,13 - added zombie stats variables for various zombies. also new imgs
#            - added player centerpos
#            - added constants for different types of zombies
#            - added constants for tile(mine) attributes
#            - added some new constants for fonts, changed up sizes and styles, etc.
# Aug 1,13   - massive changes to zombie stats and game options to streamline different level creation w/ different zombies

import pygame
from pygame.locals import *

#x,y,width,height in position tuples and Rect's, etc etc...
X=0
Y=1
W=2
H=3
R=2 #radius (for circles - x,y,r)

#direction constants...
DIR_RIGHT=0
DIR_LEFT=1
DIR_UP=2
DIR_DOWN=3

#action constants
ACT_NONE=0
ACT_WALK=1
ACT_DIG=2

#general constants
SCREEN_SIZE=(500,500)
FLIPVAL="^"
FOV_OFFSET=(15,15) #offset to center the FOV on the character

#map constants
MAP_FILE = "above.txt" #name of the aboveground map file
MAP_FILE_DLIM='\t' #file delimiter for aboveground map file

#tile constants
TILE_TRANSCOLOR = Color(255,0,255,0)
TILE_SIZE=(48,48)

#return variables from the handler functions
WIN_STAT = 0 #stat window needs to be updated
WIN_END = 1 #end-game window needs to be updated


#image file locations
IMG_DIR = 'images/'
IMG_ZOMBIE_EZ=IMG_DIR+'zombie.png'
IMG_ZOMBIE_MED=IMG_DIR+'zombie4.png'
IMG_ZOMBIE_HARD=IMG_DIR+'zombie3.png'
IMG_PLAYER=IMG_DIR+'player.png'
IMG_CRACKS=IMG_DIR+'cracks.png'
IMG_TILESET=IMG_DIR+'mines.png'
IMG_FIRE=IMG_DIR+'fire.png'
IMG_BTNSET=IMG_DIR+'buttonset2.png'
IMG_WINSET=IMG_DIR+'winset.png'
IMG_MENUBG=IMG_DIR+"menu.png"

#spriteset template (RL) for both player and zombiea
SPRITE_SIZE = TILE_SIZE #currently, changing this might mess things up
SPRITE_TEMPLATE=[[['0'],['^0']], #standing
                [['0','1','2','3'],['^0','^1','^2','^3']], #walking
                [['4','5','6','7'],['^4','^5','^6','^7']]] #axing
FIRE_TEMPLATE=[[['0','1','2','^1','3','^2','0','3','2']]] #uses a template/spriteset so it can have duplicates of frames 
#sprite animation delay "bases"
SPRITE_FRAME_DELAY = 50 #delay between frames
SPRITE_ACT_DELAY = 50 #delay between acts
SPRITE_MASK_DELAY = 200 #delay between mask ani frames

#miner statistic constants
STAT_SP='sp' #miners speed
STAT_STR='str' #miners strength 
STAT_MAXBAG='maxBag' #the current maximum bag size
STAT_MONEY='money' #the players money 
STAT_BAG = 'bag' #players current bag (list)
STAT_ORIGINAL_BAG='origBag' #the original bag size assigned to the player at game runtime
STAT_VISION='vision' #the stat for range of vision of the player
STAT_RANGE='range' #actual range of vision fior the player (behind the scenes)
STAT_DMG='dmg' #actual damage stat for how much dmg the player does - works behind the scenes

#base stat constants
STAT_RANGE_BASE = 30 #base vision range
STAT_DMG_BASE=1 #base dng


#player constants
PLAYER_STATS = {STAT_SP:3,STAT_STR:8,STAT_MAXBAG:4,STAT_MONEY:0,STAT_VISION:1} #player initial stats
PLAYER_CENTERPOS = (4,4) #players "center" position on the screen - FIX (dynamic?)
PLAYER_STARTPOS = (1,4) #players starting position

#order the AI will check in order to choose which direction to move in
AI_CHECKORDER = {DIR_UP:    [DIR_UP,DIR_RIGHT,DIR_LEFT,DIR_DOWN],
                 DIR_RIGHT: [DIR_RIGHT,DIR_UP,DIR_DOWN,DIR_LEFT],
                 DIR_LEFT:  [DIR_LEFT,DIR_UP,DIR_DOWN,DIR_RIGHT],
                 DIR_DOWN:  [DIR_DOWN,DIR_RIGHT,DIR_LEFT,DIR_UP]}

#zombie constants for types of zombies and zombie-specific stats
ZOMBIE_TYPE="zType" #mob stat for the type of mob
ZOMBIE_TYPE_EZ='ez'
ZOMBIE_TYPE_MED='med'
ZOMBIE_TYPE_HARD='hard'
ZOMBIE_IMG ="zImg" #img for mob
ZOMBIE_STATS = "zStats"

#dictionaries containing all info for different types of zombies
ZOMBIE_EZ  = {ZOMBIE_TYPE:ZOMBIE_TYPE_EZ,  ZOMBIE_IMG: IMG_ZOMBIE_EZ ,
              ZOMBIE_STATS:{STAT_SP:0.008, STAT_STR:0.005}}
ZOMBIE_MED = {ZOMBIE_TYPE:ZOMBIE_TYPE_MED, ZOMBIE_IMG: IMG_ZOMBIE_MED,
              ZOMBIE_STATS:{STAT_SP:0.012, STAT_STR:0.008}}
ZOMBIE_HARD= {ZOMBIE_TYPE:ZOMBIE_TYPE_HARD,ZOMBIE_IMG: IMG_ZOMBIE_HARD,
              ZOMBIE_STATS:{STAT_SP:0.02,  STAT_STR:0.01}}


#game constants/option flags for various game levels/difficulties
GAME_LVL_FREE="Free Play"
GAME_LVL_EZ="Easy"
GAME_LVL_MED="Medium"
GAME_LVL_HARD="Hard" 
GAME_OPT_FOW="fow" #game option for fog of war
GAME_OPT_ZOMBIES="z" #game option to hold list of zombies (stats, etc)
GAME_OPT_ZOMBIE_NUM="zNum" #game option for the number of zombies
GAME_OPT_MAP_SIZE="mapSize" #game option for size of the map
GAME_OPT_WIN_POS="winPos" #game option for winning position on a map
WIN_POS_RAND='?' #flag for a random winning position, within the bounds of the map


GAME_LVLS = {
                #free play level options
                GAME_LVL_FREE :{GAME_OPT_MAP_SIZE:(75,75),
                                GAME_OPT_WIN_POS :(73,73), #last row, last col
                                GAME_OPT_FOW     :False, #no fow
                                GAME_OPT_ZOMBIES :[]}, #no zombies
                #easy level options
                GAME_LVL_EZ   :{GAME_OPT_MAP_SIZE:(100,100),
                                GAME_OPT_WIN_POS :(98,98), #alst row, last col
                                GAME_OPT_FOW     :False, #no fow
                                GAME_OPT_ZOMBIES :[ #10 ez zombies
                                                     dict(ZOMBIE_EZ.items() +  [(GAME_OPT_ZOMBIE_NUM,10)])
                                                  ]},
                #medium level options
                GAME_LVL_MED  :{GAME_OPT_MAP_SIZE:(150,150),
                                GAME_OPT_WIN_POS :(WIN_POS_RAND,148), #winning tile position (random, but on the last row!)
                                GAME_OPT_FOW     :False,  #fow
                                GAME_OPT_ZOMBIES :[ #10 ez, and 10 medium zombies
                                                     dict(ZOMBIE_EZ.items() +  [(GAME_OPT_ZOMBIE_NUM,10)]),
                                                     dict(ZOMBIE_MED.items() + [(GAME_OPT_ZOMBIE_NUM,10)])
                                                  ]},
                #hard level options
                GAME_LVL_HARD :{GAME_OPT_MAP_SIZE:(200,200),
                                GAME_OPT_WIN_POS :(WIN_POS_RAND,198), #winning tile position (random, but on the last row!)
                                GAME_OPT_FOW     :False,  #fow
                                GAME_OPT_ZOMBIES :[ #15 ez, 10 medium, and 5 hard zombies
                                                     dict(ZOMBIE_EZ.items() +  [(GAME_OPT_ZOMBIE_NUM,15)]),
                                                     dict(ZOMBIE_MED.items() + [(GAME_OPT_ZOMBIE_NUM,10)]),
                                                     dict(ZOMBIE_HARD.items() +[(GAME_OPT_ZOMBIE_NUM,5)])
                                                  ]}
            }

#------------------------------------------------------------------------------------------------------
#MINE/TILE CONSTANTS
#------------------------------------------------------------------------------------------------------

#special mines (tiles)
MINE_DUG = 21
MINE_ROCK=0
MINE_BLANK=1
MINE_WIN=17

#types of mines
MINE_BLOCK_FULL=2
MINE_BLOCK_UP=1
MINE_BLOCK_NONE = 0
MINE_DIGGABLE = 4 #just for readability
MINE_SHOP=3

MINE_VAL_WIN=-1 #special winning mine value

#tile(mine) attributes
ATTR_HITS='hits'
ATTR_HP='hp'
ATTR_VAL='value'
ATTR_CHANCE='chance'
ATTR_TYPE='type'

#all of the available "mines" (tiles) in the game, and their associated properties
mines={ #diggable tiles - first is blank, last is win, others are minable
        MINE_BLANK: {ATTR_CHANCE:80, ATTR_VAL:0,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:5}, #"blank" tile
        2:          {ATTR_CHANCE:22, ATTR_VAL:1,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:7},
        3:          {ATTR_CHANCE:17, ATTR_VAL:2,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:9},
        4:          {ATTR_CHANCE:15, ATTR_VAL:3,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:10},
        5:          {ATTR_CHANCE:14, ATTR_VAL:4,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:13},
        6:          {ATTR_CHANCE:12, ATTR_VAL:5,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:15},
        7:          {ATTR_CHANCE:10, ATTR_VAL:6,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:20},
        8:          {ATTR_CHANCE:9,  ATTR_VAL:7,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:22},
        9:          {ATTR_CHANCE:8,  ATTR_VAL:8,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:25},
        10:         {ATTR_CHANCE:7,  ATTR_VAL:9,           ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:30},
        11:         {ATTR_CHANCE:6,  ATTR_VAL:10,          ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:32},
        12:         {ATTR_CHANCE:5,  ATTR_VAL:11,          ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:35},
        13:         {ATTR_CHANCE:4,  ATTR_VAL:12,          ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:48},
        14:         {ATTR_CHANCE:3,  ATTR_VAL:13,          ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:55},
        15:         {ATTR_CHANCE:2,  ATTR_VAL:14,          ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:65},
        16:         {ATTR_CHANCE:1,  ATTR_VAL:15,          ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:75},
        MINE_WIN:   {ATTR_CHANCE:0,  ATTR_VAL:MINE_VAL_WIN,ATTR_TYPE:MINE_DIGGABLE, ATTR_HITS:100}, #winning tile
        
        #misc tiles
        MINE_ROCK:  {ATTR_CHANCE:18, ATTR_VAL:0,           ATTR_TYPE:MINE_BLOCK_FULL}, #rock
        18:         {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_BLOCK_UP}, #outside tile
        19:         {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_BLOCK_FULL}, #cave-outside (side)
        20:         {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_BLOCK_FULL}, #cave-outside (bottom)
        MINE_DUG:   {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_BLOCK_NONE}, #dug out tile
            
        #house tiles (roof x3, then floor x3)
        22:         {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_BLOCK_UP},
        23:         {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_BLOCK_UP},
        24:         {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_BLOCK_UP},
        
        25:         {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_SHOP},
        26:         {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_SHOP},
        27:         {ATTR_CHANCE:0,  ATTR_VAL:0,           ATTR_TYPE:MINE_SHOP},               
      }


#------------------------------------------------------------------------------------------------------
#UI CONSTANTS
#------------------------------------------------------------------------------------------------------
#special window position constants
ALIGN_CENTER=-1 #position value used for window-UI centering
ALIGN_BOTTOM=-2 #position value used for window-UI bottom-alignment

#fov/vision constants
FADE_MAX_ALPHA=255 #maximum alpha color value
FADE_MIN_ALPHA=0 #minumum alpha color value
FADE_STEP_NUM=17 #number of fading steps
FADE_STEP_ALPHA=FADE_MAX_ALPHA/FADE_STEP_NUM #amount of alpha to fade with each step
FADE_STEP_DIST=3 #amount to move away from center for each fade-step
VISION_OFFSET=(24,14) #random offset needed to center vision circle around the player

#changing RBG constants
BTN_DISABLE_RGB = 0.6 #percent to darken disabled buttons
MIN_RGB=0 #minimum r,g, or b values
MAX_RGB=255 #maximum r,g or b values

#font file constants
FONT_DIR = "fonts/"
WIN_FONT_FILE = FONT_DIR + "EuphoriaScript.ttf"
WIN_GAME_FONT_FILE = FONT_DIR + "Ewert.ttf"
WIN_BTN_FONT_FILE = FONT_DIR + "Ewert.ttf"

#font constants for UI
WIN_TITLE_FONT_SIZE = 50
WIN_SUB_FONT_SIZE = 30
WIN_FONT_SIZE = 23
WIN_FONT_STAT_SIZE=18
WIN_FONT_BTN_SIZE = 18
WIN_FONT_COLOR = pygame.Color(90,70,55) #brownish

#create fonts for the windows
WIN_TITLE_FONT = pygame.font.Font(WIN_FONT_FILE,WIN_TITLE_FONT_SIZE)
WIN_SUB_FONT = pygame.font.Font(WIN_FONT_FILE,WIN_SUB_FONT_SIZE)
WIN_FONT = pygame.font.Font(WIN_FONT_FILE,WIN_FONT_SIZE) #general font (mainly insutrction screen)
WIN_STAT_FONT = pygame.font.Font(WIN_GAME_FONT_FILE,WIN_FONT_STAT_SIZE); WIN_STAT_FONT.set_bold(True) #bold the stat font
BTN_FONT = pygame.font.Font(WIN_BTN_FONT_FILE,WIN_FONT_BTN_SIZE)

#size of the panels for the windowset and button set images
WINSET_PNLSIZE=(438,25)
BTNSET_PNLSIZE=(25,25)

#window image sets ui order
WINSET_IMG_TOP=0 
WINSET_IMG_BTM=2
WINSET_IMG_PNL=1

#button image sets ui order
BTNSET_IMG_LEFT=0
BTNSET_IMG_RIGHT=2
BTNSET_IMG_MID=1

#general label constants
LBL_LINE_DLIM="\n"

#shop constants
SHOP_COST_STR=20 #cost of str
SHOP_COST_SP=30 #cost of sp
SHOP_COST_VISION=20
SHOP_BTN_TEXT="Buy" #button text for shop buttons
SHOP_BTN_STR="shopStr" #id for buy str button
SHOP_BTN_SP="shopSp" #id for buy sp button
SHOP_BTN_VISION="shopVision" #id for buy vision button
#label text for the shop items
SHOP_LABEL_TEXT=["Strength  $"+str(SHOP_COST_STR),
                 "Speed        $"+str(SHOP_COST_SP),
                 "Vision       $"+str(SHOP_COST_VISION)]

#window titles
MENU_TITLE = "Main Menu" #main menu title
MENU_LVL_TITLE = "Difficulty" #level selection menu title
SHOP_TITLE="Ye Olde Shop" #title for the shop
HOW_TITLE="Overview"
HOW_MECH_TITLE = "Mechanics"
HOW_ZOMBIES_TITLE = "Zombies"
HOW_MINES_TITLE = "Minerals"


#menu buttons - button id's and button text
MENU_BTN_PLAY = "Play"
MENU_BTN_HOW = "How To Play"
MENU_BTN_EXIT = "Exit"
MENU_BTN = "Main Menu"

#level selection buttons - buttons ids and text
MENU_LVL_BTN_FREE=GAME_LVL_FREE
MENU_LVL_BTN_EZ = GAME_LVL_EZ
MENU_LVL_BTN_MED = GAME_LVL_MED
MENU_LVL_BTN_HARD = GAME_LVL_HARD


#
# DONT FORGET - THERE IS A FEW CONSTANTS AT THE TOP OF ZOMBIEMINER 
#