import keyboard  # Install this package using: pip install keyboard

def handle_key_press():
    while True:
        if keyboard.is_pressed('left'):
            while keyboard.is_pressed('left'):
                pass  # Wait until the key is released
            return "left"
        elif keyboard.is_pressed('right'):
            while keyboard.is_pressed('right'):
                pass
            return "right"
        elif keyboard.is_pressed('up'):
            while keyboard.is_pressed('up'):
                pass
            return "up"
        elif keyboard.is_pressed('down'):
            while keyboard.is_pressed('down'):
                pass
            return "down"        

while True:
    
    direction=handle_key_press()
    print(direction)
