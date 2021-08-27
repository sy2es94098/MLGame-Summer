from .game.star_gummer import Star_Gummer

GAME_VERSION = "1.0"
GAME_PARAMS = {
    "()": {
        "prog": "star_gummer",
        "game_usage": "%(prog)s <level>"
    },
    "level": {
        "choices": ("EASY", "NORMAL", "HARD"),
        "metavar": "param1",
        "help": "Specify the game style. Choices: %(choices)s"
    },
}

# will be equal to config. GAME_SETUP["ml_clients"][0]["name"]

GAME_SETUP = {
    "game": Star_Gummer,
    "ml_clients": Star_Gummer.ai_clients(),
}