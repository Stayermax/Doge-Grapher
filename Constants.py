from random import randrange as rr
from math import log10
# App window size
STARTED = False
if(not STARTED):
    STARTED = True
    SIZE_X = 1000
    SIZE_Y = 1000

    # Node's velocity coef
    SPEED = 5

    # Minimum starting distance between nodes
    TOLERANCE = 15

    # Size of random graph
    RANDOMGRAPHSIZE = 60

    # Number of CC
    CC_NUMBER = 8

    # Probability of existance connection between two nodes
    PROBABILITY_FACTOR = 0.5

    # Predict collisions (No cat image)
    COLLISIONS = False

    # Allows nodes to go through walls
    TRANSPARENCY = False

    # Connect nodes
    CONNECTIONS = True

    # Don't remember what is it
    FRACTAL = False

    # Each node leaves trase
    TRASE = False

    # Fill figure
    FILL = False

    # Adds colors
    COLORS = False

    # Random colors
    COLOR_PARTY = True

    # Each node can be rotated
    ROTATION = False

    # Connected components can be round or not
    SIRCLESTRUCTURE = True

    # 0 no motion
    # 1 regular
    # 2 cardioida
    # 3 limacon
    # 4 heart
    # 5 SCC_circle
    # 6 circle with center in window center
    MOTIONTYPE = 0

    # 0 linear
    # 1 round
    SEPARATION = 1

    # Adds connected components area
    VISIBLE_SEP = True

    # Sets directions
    DIRECTED = False

    # Create new random graph or work with the old one
    NEWRANDOM = True

    # SCC radius coef
    CC_RADIUS_COEF = 2

    def coef_funk(n):
        return 1/3

    # 0 from graph.txt
    # 1 random graph
    # 2 random k graph
    GRAPHTYPE = 2

    DOGS = False

    # Serious staff
    SIRIUS_STAFF = True
    if(SIRIUS_STAFF):
        SIZE_X = 1000
        SIZE_Y = 1000
        SPEED = 5
        TOLERANCE = 15
        RANDOMGRAPHSIZE = 52
        CC_NUMBER = 8
        PROBABILITY_FACTOR = 0.5
        COLLISIONS = False
        TRANSPARENCY = False
        CONNECTIONS = True
        FRACTAL = False
        TRASE = False
        FILL = False
        COLORS = False
        ROTATION = False
        SIRCLESTRUCTURE = True
        MOTIONTYPE = 0
        SEPARATION = 1
        VISIBLE_SEP = True
        DIRECTED = False
        NEWRANDOM = True
        CC_RADIUS_COEF = coef_funk
        GRAPHTYPE = 2
        DOGS = False
        COLOR_PARTY = False

    ANOTHER_CONFIG = False
    if(ANOTHER_CONFIG):
        RANDOMGRAPHSIZE = 40
        CC_NUMBER = 1
        PROBABILITY_FACTOR = 0.05
        SEPARATION = 1