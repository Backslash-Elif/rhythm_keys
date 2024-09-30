try:
    import pygame, tkinter
except:
    import platform, subprocess
    print("\n\nIt seems like you're running this script in a custom environment.")
    print("This is fine, however not all required modules are installed.\n")
    install = ""
    while install.lower() not in ("y", "n"):
        install = input("Would you like to attempt to auto-install the missing modules? [Y/N] >")
    if install.lower() == "y":
        print("Attempting to install pygame...")
        subprocess.run(['pip', 'install', 'pygame'])
        subprocess.run(['pip', 'install', 'tk'])
        if platform.system() == "Linux":
            subprocess.run(['sudo', 'apt', 'install', 'python3-pygame', '-y'])
            subprocess.run(['sudo', 'apt', 'install', 'python3-tk', '-y'])
    else:
        print("Please install modules:\ntkinter (alias: tk)\npygame")
    print("Please restart this script.")
    input("Press ENTER to exit...")
    exit()

import screen_manager

# Initialize Pygame
pygame.init()

screen_mgr = screen_manager.ScreenManager()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        screen_mgr.handle_event(event)
    
    screen_mgr.draw()
    screen_mgr.flip_screen()
    screen_mgr.tick(60)