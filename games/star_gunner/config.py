from .src.game import StarGunner

GAME_VERSION = "1.1"
GAME_PARAMS = {
    "()": {
        "prog": "star-gunner",
        "game_usage": "%(prog)s <param1> [param2] [param3]"
    },
    "param1": {
        "choices": ("EASY", "NORMAL", "HARD"),
        "metavar": "param1",
        "help": "Specify the game style. Choices: %(choices)s"
    },
    "param2": {
        "type": int,
        "nargs": "?",
        "metavar": "param2",
        "default": 1,
        "help": ("[Optional] The score that the game will be exited "
                 "when either side reaches it.[default: %(default)s]")
    },
    "param3": {
        "nargs": "?",
        "metavar": "param3",
        "default": "blabla",
        "help": ("[Optional] The score that the game will be exited "
                 "when either side reaches it.[default: %(default)s]")
    }
}

# will be equal to config. GAME_SETUP["ml_clients"][0]["name"]

GAME_SETUP = {
    "game": StarGunner,
    "ml_clients": StarGunner.ai_clients(),
    # "dynamic_ml_clients":True
}