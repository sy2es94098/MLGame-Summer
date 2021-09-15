
def _init():
    global pixels
    pixels = []

def set_value(pix):
    global pixels
    pixels = pix
    
def get_value():
    return pixels
