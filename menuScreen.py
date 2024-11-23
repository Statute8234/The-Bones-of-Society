import pygame
import pygame_menu
from pygame_menu import themes
import pygame_menu.widgets

# main menu
class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.play = False
        self.create_main_menu()
    
    def create_main_menu(self):
        self.main_menu = pygame_menu.Menu('Welcome', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.loadGame_screen = pygame_menu.Menu('Load Game', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.settings_screen = pygame_menu.Menu('Settings', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.main_menu.add.button('Play', self.Play)
        self.main_menu.add.button('Load Game', self.load_game)
        self.main_menu.add.button('Settings', self.settings)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
    
    def load_game(self):
        self.loadGame_screen.clear()
        saved_games = [
            "Load Game",
            "Load Game",
            "Load Game"
        ]
        for index, save in enumerate(saved_games):
            self.loadGame_screen.add.button(save, lambda index=index: self.load_game(index))
        self.loadGame_screen.add.button('Return to Main Menu', pygame_menu.events.BACK)
        self.main_menu._open(self.loadGame_screen)

    def settings(self):
        self.settings_screen.clear()
        self.music_volume = self.settings_screen.add.range_slider('Music Volume', default=50, range_values=(0, 100), increment=1)
        self.settings_screen.add.range_slider('Sound Effects', default=50, range_values=(0, 100), increment=1)
        self.settings_screen.add.range_slider('Frame Rate', default=60, range_values=(30, 120), increment=1)
        self.settings_screen.add.range_slider('Brightness', default=100, range_values=(0, 100), increment=1)
        self.settings_screen.add.button('Return to Main Menu', pygame_menu.events.BACK)
        self.main_menu._open(self.settings_screen)
    
    def quit_menu(self):
        self.main_menu.disable()

    def Play(self):
        self.play = True

# pause menu
class PauseMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.play = True
        self.restart_game = False
        self.exit_game_varible = False
        self.create_main_menu()
    
    def create_main_menu(self):
        self.pause_menu_screen = pygame_menu.Menu('Pause Menu', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.options_screen = pygame_menu.Menu('Options', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.pause_menu_screen.add.button('Resume', self.resume)
        self.pause_menu_screen.add.button('Restart', self.restart)
        self.pause_menu_screen.add.button('Options', self.options)
        self.pause_menu_screen.add.button('Exit', self.exit_game)
    
    def resume(self):
        self.play = True
    
    def restart(self):
        self.restart_game = True
        self.play = True
    
    def options(self):
        self.options_screen.clear()
        self.music_volume = self.options_screen.add.range_slider('Music Volume', default=50, range_values=(0, 100), increment=1)
        self.options_screen.add.range_slider('Sound Effects', default=50, range_values=(0, 100), increment=1)
        self.options_screen.add.range_slider('Frame Rate', default=60, range_values=(30, 120), increment=1)
        self.options_screen.add.range_slider('Brightness', default=100, range_values=(0, 100), increment=1)
        self.options_screen.add.button('Return to Main Menu', pygame_menu.events.BACK)
        self.pause_menu_screen._open(self.options_screen)
    
    def exit_game(self):
        self.exit_game_varible = True
        self.play = True

    def quit_menu(self):
        self.pause_menu_screen.disable()

# player screen
class PlayerInventory:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.play = True
        self.skills = {
            "XP": {"current": 0, "max": 100},
            "Health": {"current": 100, "max": 100},
            "Weight": {"current": 0, "max": 100},
            "Magic": {"current": 100, "max": 100},
            "Damage": {"current": 0, "max": 100},
            "Speed": {"current": 100, "max": 100},
            "Fortitude": {"current": 0, "max": 100}
        }
        self.create_main_menu()
    
    def create_main_menu(self):
        self.playerInventory = pygame_menu.Menu('Player Inventory', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.playerInventory.add.image(r"Assets\lpc_entry\png\profile_images\skeleton_profile.png", angle=0).set_alignment(pygame_menu.locals.ALIGN_LEFT)
        for skill_name, values in self.skills.items():
            frame = self.playerInventory.add.frame_h(400, 60, background_color=(0, 0, 0))
            progress_bar = self.playerInventory.add.progress_bar(skill_name,default=(values["current"] / values["max"]) * 100,progress_text=f"{skill_name}: {values['current']}/{values['max']}",_relax=True)
            button = self.playerInventory.add.button("+", self.increaseSkill, skill_name)
            frame.pack(progress_bar)
            frame.pack(button)
        self.playerInventory.add.button("Exit", self.quit_menu)

    def increaseSkill(self, skill_name):
        if self.skills[skill_name]["current"] < self.skills[skill_name]["max"]:
            self.skills[skill_name]["current"] += 10
        self.update_progress_bar(skill_name)
    
    def update_progress_bar(self, skill_name):
        """Update the progress bar for a specific skill."""
        progress = (self.skills[skill_name]["current"] / self.skills[skill_name]["max"]) * 100
        widget = self.playerInventory.get_widget(skill_name)
        widget.set_value(progress)
        widget.set_progress_text(f"{skill_name}: {self.skills[skill_name]['current']}/{self.skills[skill_name]['max']}")

    def quit_menu(self):
        self.play=True
