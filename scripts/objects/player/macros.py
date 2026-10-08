# ref : https://github.com/DarkD04/Harmony-Framework/blob/110e1dc3452f049a8f670b1b2b09cce132fff55d/scripts/player_macros/player_macros.gml#L6

G_MODE_FLOOR        = 0
G_MODE_RIGHTWALL    = 1
G_MODE_CEILLING     = 2
G_MODE_LEFTWALL     = 3



# State macros:
ST_NULL         = -1
ST_NORMAL       = 0
ST_JUMP         = 1
ST_ROLL         = 2
ST_LOOKUP       = 3
ST_LOOKDOWN     = 4
ST_SPINDASH     = 5
ST_SKID         = 6
ST_KNOCKOUT     = 7
ST_SPRING_H     = 8
ST_SPRING_D     = 9
ST_PEELOUT      = 10
ST_TAILSFLY     = 11
ST_KNUXGLIDE    = 12
ST_KNUXCLIMB    = 13
ST_KNUXLEDGE    = 14
ST_KNUXFALL     = 15
ST_KNUXSLIDE    = 16
ST_DROPDASH     = 17
ST_HANG         = 18


# Animation macros:
ANIM_STAND          = "Stopped"
ANIM_WAIT           = "Waiting"
ANIM_WALK           = "Walking"
ANIM_RUN            = "Running"
ANIM_MAXRUN         = "Running"
ANIM_ROLL           = "Jumping"
ANIM_LOOKUP         = "Looking Up"
ANIM_LOOKDOWN       = "Looking Down"
ANIM_SPINDASH       = "Spin Dash"
ANIM_SPRING_H       = "Bouncing"
ANIM_SPRING_D       = "Twirl H"
ANIM_SKID           = "Skidding"
ANIM_SKIDTURN       = "Skidding Turn"
ANIM_HURT           = "Hurt"
ANIM_DIE            = "Dying"
ANIM_DROWN          = "Drowning"
ANIM_BREATHE        = "15"
ANIM_VICTORY        = "Victory"
ANIM_PUSH           = "Pushing"
ANIM_LEDGE1         = "Flailing 1"
ANIM_LEDGE2         = "Flailing 2"
ANIM_TAILSFLY       = "Fly Lift Down"
ANIM_TAILSTIRED     = "Fly Lift Tired"
ANIM_TAILSSWIM      = "Swim Lift"
ANIM_TAILSSWIMTIRED = "Swim Lift"
ANIM_KNUXGLIDE      = "Grabbing"
ANIM_KNUXGLIDETURN  = "Gliding"
ANIM_KNUXCLIMBIDLE  = "Climbing Stopped"
ANIM_KNUXCLIMBUP    = "Climbing Up"
ANIM_KNUXCLIMBDOWN  = "Climbing Down"
ANIM_KNUXFALL       = "Gliding Drop"
ANIM_KNUXSLIDE      = "Gliding Slide"
ANIM_KNUXGETUP      = "Gliding Get Up"
ANIM_KNUXLEDGE      = "Ledge Pull Up"
ANIM_KNUXLAND       = ANIM_KNUXGETUP
ANIM_DROPDASH       = "Super Transform"
ANIM_HANG           = "Hanging"

TAIL_1 = "Tails Stopped"
TAIL_2 = "Tails Skidding"
TAIL_3 = "Tails Jumping"
# Shield macros
S_NONE          = -1
S_NORMAL        = 0
S_FIRE          = 1
S_ELECTRIC      = 2
S_BUBBLE        = 3
	
# Player macro
CHAR_SONIC      = 0
CHAR_TAILS      = 1
CHAR_KNUX       = 2

	
# Misc.
K_HURT          = 1
K_DIE           = 2
K_DROWN         = 3


# OTHER non-ref:

TIME_TRANSFORMATION = 20
MAX_SPEED = 64

