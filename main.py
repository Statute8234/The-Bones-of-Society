import pygame
import random, sys, math, os, time
import character, menuScreen
# Initialize Pygame and setup display
pygame.init()
current_time = time.time()
random.seed(current_time)

screenWidth, screenHeight = 700, 700
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Project")
clock = pygame.time.Clock()
# menus
def on_resize() -> None:
    window_size = screen.get_size()
    new_w, new_h = window_size[0], window_size[1]
    # main menu
    menu_menu.main_menu.resize(new_w, new_h)
    menu_menu.loadGame_screen.resize(new_w, new_h)
    menu_menu.settings_screen.resize(new_w, new_h)
    # pause menu
    pause_menu.pause_menu_screen.resize(new_w, new_h)
    pause_menu.options_screen.resize(new_w, new_h)
    # player inventory
    player_inventory.playerInventory.resize(new_w, new_h)

menu_menu = menuScreen.MainMenu(screen, screenWidth, screenHeight)
pause_menu = menuScreen.PauseMenu(screen, screenWidth, screenHeight)
player_inventory = menuScreen.PlayerInventory(screen, screenWidth, screenHeight)
on_resize()

# randomized clothing
base_path = "Assets/lpc_entry/png/walkcycle"

clothing_items = { 
    'BELT': ['leather', 'rope'], 
    'FEET': ['plate_armor_shoes', 'shoes_brown'], 
    'HANDS': ['plate_armor_gloves'], 
    'HEAD': ['chain_armor_helmet', 'chain_armor_hood', 'hair_blonde', 'leather_armor_hat', 'plate_armor_helmet', 'robe_hood'], 
    'LEGS': ['pants_greenish', 'plate_armor_pants', 'robe_skirt'], 
    'TORSO': ['chain_armor_jacket_purple', 'chain_armor_torso', 'leather_armor_bracers', 'leather_armor_shirt_white', 'leather_armor_shoulders', 'leather_armor_torso', 'plate_armor_arms_shoulders', 'plate_armor_torso', 'robe_shirt_brown'], 
}

def pick_random_clothing(clothing_items):
    return {category: random.choice(items) for category, items in clothing_items.items()}


def get_valid_image_paths(selected_items, base_path): 
    image_paths = {}
    for category, item in selected_items.items():
        path = os.path.join(base_path, f"{category}_{item}.png")
        if os.path.exists(path):  # Check if the file exists
            image_paths[category] = path
        else:
            print(f"Warning: Missing file for {category} - {path}")
    return image_paths

def assemble_clothing_list(clothing_items, base_path):
    # Pick random clothing items
    random_clothing = pick_random_clothing(clothing_items)
    # Get file paths for the selected clothing items
    valid_image_paths = get_valid_image_paths(random_clothing, base_path)
    # Return the paths as a list
    return list(valid_image_paths.values())

clothing = []
image_paths = []
image_paths = assemble_clothing_list(clothing_items, base_path)
print(image_paths)

for path in image_paths:
    clothing.append(path)

armor_image = []
def add_armor(armor_images):
    for path in armor_images:
        armor_image_path = pygame.image.load(path)
        armor_image.append(character.ObjectSprites(armor_image_path, (10, 10), (40, 55), (25, 10), 1))
add_armor(clothing)

playerSprite_defult = pygame.image.load(r"Assets\lpc_entry\png\walkcycle\BODY_skeleton.png")
citizenSprite_defult = pygame.image.load(r"Assets\lpc_entry\png\walkcycle\BODY_male.png")
player = character.CharacterSprites(playerSprite_defult, (10, 10), (40, 55), (25, 10), (0, 0), 1)
playerX, playerY = 0, 0
playerFrame=18
player.position = [playerX, playerY]
citizen = character.CharacterSprites(citizenSprite_defult, (10, 10), (40, 55), (25, 10), (screenHeight//2,screenWidth//2), 1)
citizenX, citizenY = screenHeight//2,screenWidth//2
citizenFrame=18

directions = {
    pygame.K_UP: {"frame_start": 0, "frame_end": 9, "delta_x": 0, "delta_y": -1},
    pygame.K_DOWN: {"frame_start": 18, "frame_end": 27, "delta_x": 0, "delta_y": 1},
    pygame.K_LEFT: {"frame_start": 9, "frame_end": 18, "delta_x": -1, "delta_y": 0},
    pygame.K_RIGHT: {"frame_start": 27, "frame_end": 35, "delta_x": 1, "delta_y": 0},
}

def main():
    global playerFrame, screen, playerX, playerY, directions, citizenFrame, citizenX, citizenY
    running = True
    while running:
        events = pygame.event.get()
        pressed = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                on_resize()
            if pressed[pygame.K_ESCAPE]:
                if menu_menu.play:
                    pause_menu.play = not(pause_menu.play)
            if pressed[pygame.K_i]:
                if player_inventory.play:
                    player_inventory.play = not(player_inventory.play)
        # player movments
        for key, values in directions.items():
            if pressed[key]:
                # Update player frame
                if playerFrame < values["frame_end"]:
                    playerFrame += 1
                else:
                    playerFrame = values["frame_start"]
                
                # Update player position
                playerX += values["delta_x"]
                playerY += values["delta_y"]
                player.position = [playerX, playerY]
        
        screen.fill((255, 255, 255))
        if not menu_menu.play:
            menu_menu.main_menu.update(events)
            menu_menu.main_menu.draw(screen)
        elif not pause_menu.play:
            pause_menu.pause_menu_screen.update(events)
            pause_menu.pause_menu_screen.draw(screen)
        elif not player_inventory.play:
            player_inventory.playerInventory.update(events)
            player_inventory.playerInventory.draw(screen)
        else:
            player.showSprite(screen, playerFrame)
            citizen.showSprite(screen, citizenFrame)
            citizen.roamAround(screen, 1)
            for obj in armor_image:
                obj.showSprite(screen, citizenFrame, citizen.position[0], citizen.position[1])
            # move
            if citizen.position[0] > citizenX:
                if citizenFrame<35:
                    citizenFrame+=1
                else:
                    citizenFrame=27
            if citizen.position[0] < citizenX:
                if citizenFrame<18:
                    citizenFrame+=1
                else:
                    citizenFrame=9
            if citizen.position[1] > citizenY:
                if citizenFrame<35:
                    citizenFrame+=1
                else:
                    citizenFrame=27
            if citizen.position[1] < citizenY:
                if citizenFrame<9:
                    citizenFrame+=1
                else:
                    citizenFrame=0
            citizenX, citizenY = citizen.position[0], citizen.position[1]
        clock.tick(64)
        pygame.display.flip()
        pygame.display.update()

if __name__ == "__main__":
    main()