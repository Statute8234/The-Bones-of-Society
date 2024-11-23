import pygame
import random

class CharacterSprites:
    def __init__(self, sheet, frame_position, frame_size, frame_space, position, scale):
        self.sheet = sheet
        self.frame_width, self.frame_height = frame_size
        self.frameX, self.frameY = frame_position
        self.frame_spaceX, self.frame_spaceY = frame_space
        self.scale = scale
        self.color = (0, 0, 0)  # Default transparency color (black)
        self.frames = []
        self.speed = 1
        self.flipped = False
        self.position = position
        self.targetPosition = [0, 0]
        self._extractFrames()
        
    def _extractFrames(self):
        """Private method to extract frames from the sprite sheet."""
        self.frames = []  # Clear any existing frames
        sheet_width = self.sheet.get_width()
        sheet_height = self.sheet.get_height()

        for y in range(self.frameY, sheet_height, self.frame_height + self.frame_spaceY):
            for x in range(self.frameX, sheet_width, self.frame_width + self.frame_spaceX):
                # Create a new surface for each frame
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(self.sheet, (0, 0), (x, y, self.frame_width, self.frame_height))
                frame.set_colorkey(self.color)  # Set transparency
                frame = pygame.transform.scale(frame, (int(self.frame_width * self.scale), int(self.frame_height * self.scale)))
                self.frames.append(frame)

    def changeSpriteSheet(self, new_sheet, frame_position=None, frame_size=None, frame_space=None, scale=None):
        """
        Change the sprite sheet and optionally update other parameters.
        """
        self.sheet = new_sheet
        # Update optional parameters if provided
        if frame_position:
            self.frameX, self.frameY = frame_position
        if frame_size:
            self.frame_width, self.frame_height = frame_size
        if frame_space:
            self.frame_spaceX, self.frame_spaceY = frame_space
        if scale:
            self.scale = scale
        # Extract frames from the new sprite sheet
        self._extractFrames()

    def showSprite(self, screen, frame_index, blend=False, alpha=0.5):
        """Display a specific frame or blend between two frames."""
        if 0 <= frame_index < len(self.frames):
            frame = self.frames[frame_index]
            if self.flipped:
                frame = pygame.transform.flip(frame, True, False)
            if blend and 0 <= frame_index + 1 < len(self.frames):
                next_frame = self.frames[frame_index + 1]
                blended_frame = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
                blended_frame.blit(frame, (0, 0))
                blended_frame.blit(next_frame, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                screen.blit(blended_frame, (self.position[0], self.position[1]))
            else:
                screen.blit(frame, (self.position[0], self.position[1]))
            
    def roamAround(self, screen, dt):
        size = screen.get_size()
        px, py = self.position[0], self.position[1]
        self.roamNum = 0
        # Set a new target position if the current one is reached
        if abs(self.position[0] - self.targetPosition[0]) < 1 and abs(self.position[1] - self.targetPosition[1]) < 1:
            self.targetPosition = [
                random.randint(0, size[0] - int(self.frame_width * self.scale)),
                random.randint(0, size[1] - int(self.frame_height * self.scale))
            ]
        
        # Calculate movement and direction
        delta_x = self.targetPosition[0] - self.position[0]
        delta_y = self.targetPosition[1] - self.position[1]
        # ----
        px += self.speed * (delta_x / max(1, abs(delta_x))) * dt
        py += self.speed * (delta_y / max(1, abs(delta_y))) * dt
        self.position = [px, py]
                
class ObjectSprites:
    def __init__(self, sheet, frame_position, frame_size, frame_space, scale):
            self.sheet = sheet
            self.frame_width, self.frame_height = frame_size
            self.frameX, self.frameY = frame_position
            self.frame_spaceX, self.frame_spaceY = frame_space
            self.scale = scale
            self.color = (0, 0, 0)  # Default transparency color (black)
            self.frames = []
            self.speed = 1
            self.flipped = False
            self._extractFrames()
    
    def _extractFrames(self):
        """Private method to extract frames from the sprite sheet."""
        self.frames = []  # Clear any existing frames
        sheet_width = self.sheet.get_width()
        sheet_height = self.sheet.get_height()

        for y in range(self.frameY, sheet_height, self.frame_height + self.frame_spaceY):
            for x in range(self.frameX, sheet_width, self.frame_width + self.frame_spaceX):
                # Create a new surface for each frame
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(self.sheet, (0, 0), (x, y, self.frame_width, self.frame_height))
                frame.set_colorkey(self.color)  # Set transparency
                frame = pygame.transform.scale(frame, (int(self.frame_width * self.scale), int(self.frame_height * self.scale)))
                self.frames.append(frame)

    def changeSpriteSheet(self, new_sheet, frame_position=None, frame_size=None, frame_space=None, scale=None):
        """
        Change the sprite sheet and optionally update other parameters.
        """
        self.sheet = new_sheet
        # Update optional parameters if provided
        if frame_position:
            self.frameX, self.frameY = frame_position
        if frame_size:
            self.frame_width, self.frame_height = frame_size
        if frame_space:
            self.frame_spaceX, self.frame_spaceY = frame_space
        if scale:
            self.scale = scale
        # Extract frames from the new sprite sheet
        self._extractFrames()

    def showSprite(self, screen, frame_index, x, y):
        """Display a specific frame on the screen at a given position."""
        if 0 <= frame_index < len(self.frames):
            frame = self.frames[frame_index]
            if self.flipped:
                frame = pygame.transform.flip(frame, True, False)
            screen.blit(frame, (x, y))