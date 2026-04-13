# ASTEROIDE SINGLEPLAYER v1.0
# This file stores the gameplay, rendering, and balancing constants.

WIDTH = 960
HEIGHT = 720
FPS = 60

START_LIVES = 3
SAFE_SPAWN_TIME = 2.0
WAVE_DELAY = 2.0

SHIP_RADIUS = 15
SHIP_TURN_SPEED = 220.0
SHIP_THRUST = 220.0
SHIP_FRICTION = 0.995
SHIP_FIRE_RATE = 0.2
SHIP_BULLET_SPEED = 420.0
HYPERSPACE_COST = 250

SHIELD_DURATION = 3.0
SHIELD_PICKUP_RADIUS = 14
SHIELD_COLOR = (120, 220, 255)
SHIELD_MAX_PICKUPS = 2
SHIELD_PICKUP_SEPARATION = 100
SHIELD_PICKUP_LIFETIME = 10.0
SHIELD_PICKUP_WARN_TIME = 3.0
SHIELD_SPAWN_DELAY_MIN = 1.5
SHIELD_SPAWN_DELAY_MAX = 14.0

COMBO_WINDOW = 3.0
COMBO_MAX_MULT = 8

AST_VEL_MIN = 30.0
AST_VEL_MAX = 90.0
AST_SIZES = {
    "L": {"r": 46, "score": 20, "split": ["M", "M"]},
    "M": {"r": 24, "score": 50, "split": ["S", "S"]},
    "S": {"r": 12, "score": 100, "split": []},
}

BULLET_RADIUS = 2
BULLET_TTL = 1.0
MAX_BULLETS = 4

UFO_SPAWN_EVERY = 15.0
UFO_SPEED = 80.0
UFO_FIRE_EVERY = 1.2
UFO_BULLET_SPEED = 260.0
UFO_BULLET_TTL = 1.8
UFO_BIG = {"r": 18, "score": 200, "aim": 0.2}
UFO_SMALL = {"r": 12, "score": 1000, "aim": 0.6}

WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)
COMBO_COLOR = (255, 210, 90)

# Asteroide explosivo
EXPLOSIVE_CHANCE   = 0.25        # Probabilidade de um asteroide ser explosivo
EXPLOSION_RADIUS   = 110         # Raio da onda de choque
EXPLOSION_DURATION = 0.35        # Duração visual da explosão 
EXPLOSION_COLOR    = (255, 160, 40)
EXPLOSIVE_COLOR    = (255, 130, 50)  # Cor do contorno do asteroide explosivo

RANDOM_SEED = None

# Duração do fade-in da tela de game over (segundos)
GAME_OVER_FADE_DURATION = 1.5
