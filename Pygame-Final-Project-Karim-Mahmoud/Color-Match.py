import pygame
import random

# Setup and Constants 
WIDTH, HEIGHT, FPS = 400, 600, 60
CENTER_X = WIDTH // 2

COLORS = [(255, 60, 60), (60, 255, 120), (60, 140, 255)] # 0: Red, 1: Green, 2: Blue
KEYS = {pygame.K_a: 0, pygame.K_s: 1, pygame.K_d: 2}      # A=Red, S=Green, D=Blue

# Classes

class Background:
    def draw(self, surface):
        """Draws the dark gray background and the central dividing line."""
        surface.fill((20, 20, 30)) # Dark gray
        pygame.draw.line(surface, (80, 80, 100), (CENTER_X, 0), (CENTER_X, HEIGHT), 4)

class Player:
    #the user-controlled orb at the bottom of the screen.
    def __init__(self):
        """Initializes the player with a starting position, size, and default color."""
        self.color = 0 # Starts as Red
        self.y = 500
        self.radius = 30

    def draw(self, surface):
        """Draws a filled colored circle and a white outline."""
        pygame.draw.circle(surface, COLORS[self.color], (CENTER_X, self.y), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (CENTER_X, self.y), self.radius, 3)

class Block:
    """Deals with the falling colored blocks that fall from the top of the screen to collide with the player's orb."""
    def __init__(self, speed):
        ''' Initializes a block with a random color and given speed.
        Argument "speed" (float) : How many pixels the block moves per frame.'''
        self.color = random.randint(0, 2)
        self.y = -50
        self.speed = speed
        self.size = 40

    def move(self):
        """Updates the block's Y coordinate to make it fall."""
        self.y += self.speed

    def draw(self, surface):
        """Draws a rounded colored square with a white outline."""
        rect = (CENTER_X - 20, self.y - 20, self.size, self.size)
        pygame.draw.rect(surface, COLORS[self.color], rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), rect, 3, border_radius=8)

class ScoreBoard:
    """Deals with the score display and game over messaging."""
    def __init__(self):
        """Initializes the scoreboard with a starting score of 0."""
        self.score = 0
        self.font = pygame.font.SysFont(None, 42)

    def draw(self, surface, game_over):
        # Draw Score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10))
        
        # Draw Game Over
        if game_over:
            msg = self.font.render("GAME OVER", True, (255, 60, 60))
            surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

class Game:
    """The main game engine class. It initializes Pygame, manages the main game loop, handles collision detection, 
    accelerates the game difficulty, and ties all other classes together."""
    def __init__(self):
        """Initializes the Pygame library, the display window, and the clock."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Color Match")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        """
        Resets all game objects and variables to their starting state.
        Called at launch and whenever the player restarts after a Game Over.
        """
        self.bg, self.player, self.ui = Background(), Player(), ScoreBoard()
        self.blocks = []
        self.timer = 0
        self.speed = 5.0 # Starting speed
        self.game_over = False

    def run(self):
        """
        The main game loop. Runs continuously, handling events, updating logic, 
        and drawing frames until the application is closed.
        """
        while True:
            # 1. Handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return # Safely exits the program
                
                if event.type == pygame.KEYDOWN:
                    #Handles restart 
                    if self.game_over and event.key == pygame.K_SPACE:
                        self.reset()
                    #Handles color switching 
                    elif not self.game_over and event.key in KEYS:
                        self.player.color = KEYS[event.key] # update player attribute

            # 2. Game Logic (Physics and collisions)
            if not self.game_over:
                self.timer += 1
                
                # Spawn Rate Acceleration
                if self.timer >= max(30, 80 - self.ui.score):
                    self.blocks.append(Block(self.speed)) #Create new instance of block
                    self.timer = 0

                # Iterate over a *copy* of the list ([:]) so we can safely remove items
                for b in self.blocks[:]:
                    b.move()
                    
                    # Collision Detection
                    if b.y >= self.player.y - self.player.radius:
                        if b.color == self.player.color:
                            # Colors match, increment score and speed up
                            self.ui.score += 1
                            self.speed += 0.05 # Speed Acceleration
                            self.blocks.remove(b)
                        else:
                            # Color mismatch, game over
                            self.game_over = True

            # 3. Draw Everything (Render)
            self.bg.draw(self.screen)
            self.player.draw(self.screen)
            for b in self.blocks:
                b.draw(self.screen)
            self.ui.draw(self.screen, self.game_over)

            # Update the full display Surface to the screen
            pygame.display.flip()

            # Regulate frame rate to exactly FPS (60 frames per second)
            self.clock.tick(FPS)

# Start Game
if __name__ == "__main__":
    Game().run()