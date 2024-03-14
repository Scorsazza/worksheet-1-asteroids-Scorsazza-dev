import random
import pyasge
import GameObject
import time
import math
from gamedata import GameData





def isInside(sprite_1: pyasge.Sprite, sprite_2: pyasge.Sprite) -> bool:
    pass


class MyASGEGame(pyasge.ASGEGame):
    
    """
    The main game class
    """

        

    def __init__(self, settings: pyasge.GameSettings):
        """
        Initialises the game and sets up the shared data.

        Args:
            settings (pyasge.GameSettings): The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        
        self.renderer.setClearColour(pyasge.COLOURS.BLACK)
        self.direction_vector = [0, 0]
        self.projectiles = []
        self.last_shot_time = 0
        self.score = 0
        self.game_over = False  # Add a game over flag
 
        self.cooldown_time = 0.25
        self.max_asteroids = 3
        # create a game data object, we can store all shared game content her
        # e
        self.data = GameData()
        self.data.renderer = self.renderer
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 24)
        self.initScoreDisplay()
        self.initGameOverScreen()
        self.initLivesDisplay()
        self.key_states = {"up": False, "down": False, "left": False, "right": False}
        self.data.inputs = self.inputs
     
        self.data.game_res = [settings.window_width, settings.window_height]

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.keyHandler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.clickHandler)

        # set the game to the menu
        self.menu = True
        self.play_option = None
        self.exit_option = None
        self.menu_option = 0

        # This is a comment
        self.data.background = pyasge.Sprite()
        self.initBackground()

        #
        self.menu_text = None
        self.start_text = None
        self.initMenu()

        #
        self.scoreboard = None
        self.initScoreboard()

        # Initialising the asteroid
        self.asteroid = GameObject.Asteroid()
        self.initAsteroid()
        self.asteroids = []
        self.spawn_asteroids(5)

        # Initialising player ship
        self.player = GameObject.Ship()
        self.initPlayer()

        self.projectile = GameObject.Projectile()
        self.initProjectile()

    def initBackground(self) -> bool:
        pass
    
    def initScoreDisplay(self):
        if "MainFont" in self.data.fonts:
            # Adjust instantiation to match the constructor's expectations
            self.score_text = pyasge.Text(self.data.fonts["MainFont"], "Score: 0", self.data.game_res[0] - 0, 30)
            self.score_text.colour = pyasge.COLOURS.WHITE
        else:
            print("Error: MainFont not loaded. Check the font path and ensure it's loaded before initScoreDisplay is called.")
    def initGameOverScreen(self):
        self.game_over_text = pyasge.Text(self.data.fonts["MainFont"], "GAME OVER, Press R to restart")
        self.game_over_text.position = pyasge.Point2D(550, 500)  # Start at 0,0 for manual adjustment
        self.game_over_text.colour = pyasge.COLOURS.RED





    def initAsteroid(self) -> bool:

        if self.asteroid.sprite.loadTexture("/data/images/kenney_simple-space/PNG/Retina/meteor_detailedLarge.png"):
            self.asteroid.move_speed = 8
            self.asteroid.sprite.z_order = -10
            self.asteroid.sprite.x = 100
            self.asteroid.sprite.y = 100
            self.asteroid.move_direction = [1, 0]
            self.spawn(self.asteroid)
            return True
        pass

    def initPlayer(self) -> bool:
        # This code initialises the spaceship code, similar to how the fish were loaded in,
        # and positions it at the centre of the screen
        if self.player.sprite.loadTexture("data/images/kenney_simple-space/PNG/Retina/ship_G.png"):
            self.player.move_speed = 8.0
            self.player.sprite.x = self.data.game_res[0] / 2 - self.player.sprite.width / 2
            self.player.sprite.y = self.data.game_res[1] / 2 - self.player.sprite.height / 2
            self.player.sprite.scale = 0.5

            # This code will ensure that player ship collisions remain consistent, you can leave it how it is
            self.player.collisionSprite.loadTexture("data/images/kenney_simple-space/PNG/Retina/ship_G.png")
            self.player.collisionSprite.x = self.data.game_res[0] / 2 - self.player.sprite.width / 2
            self.player.collisionSprite.y = self.data.game_res[1] / 2 - self.player.sprite.height / 2
            self.player.collisionSprite.scale = 0.5
            return True
        return False

    def initProjectile(self) -> bool:
        # This is where you should initialise your projectiles
        self.projectile.sprite.loadTexture("/data/images/kenney_simple-space/PNG/Retina/star_tiny.png")
        pass

    def spawn(self, gameObject: GameObject) -> None:
        # This is where you will set up your asteroid spawn
        # Think about both the starting position of your asteroid
        # and the starting movement direction
        # make a plan for proggramatic approach

        pass

        
    def initScoreboard(self) -> None:
        pass
    
    def FireBullet(self):
        new_projectile = GameObject.Projectile()
        if time.time() - self.last_shot_time < self.cooldown_time:
            return 
        # Calculate the front of the ship based on its rotation
        # Assuming the ship's rotation is correctly centered and in radians
        offset_distance = 50  # Adjust based on your ship's size and desired spawn point
        ship_front_x = self.player.sprite.x - 30
        ship_front_y = self.player.sprite.y - 30

        # Adjust the angle if the ship's default facing direction is not upwards
        angle_offset = math.pi / 2  # Adjust this if your ship's default orientation is not upwards
        spawn_x = ship_front_x + offset_distance * math.cos(self.player.sprite.rotation - angle_offset)
        spawn_y = ship_front_y + offset_distance * math.sin(self.player.sprite.rotation - angle_offset)

        new_projectile.sprite.x = spawn_x
        new_projectile.sprite.y = spawn_y
        new_projectile.sprite.loadTexture("/data/images/kenney_simple-space/PNG/Retina/star_tiny.png")
    
        new_projectile.move_direction = [math.cos(self.player.sprite.rotation - angle_offset), 
                                         math.sin(self.player.sprite.rotation - angle_offset)]
        new_projectile.move_speed = 10  # Adjust speed as necessary
        self.projectiles.append(new_projectile)
        self.last_shot_time = time.time()

    def initMenu(self) -> bool:
        # Initialising the title text
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 80)
        self.menu_text = pyasge.Text(self.data.fonts["MainFont"])
        self.menu_text.string = "The Space Game"
        self.menu_text.position = [375, 200]
        self.menu_text.colour = pyasge.COLOURS.CADETBLUE

        self.data.fonts["SubFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 48)
        self.start_text = pyasge.Text(self.data.fonts["SubFont"])
        self.start_text.string = "Press Space to Start"
        self.start_text.position = [475, 600]
        self.start_text.colour = pyasge.COLOURS.WHITE

        return True
    def resetGame(self):
     # Reset game state
     self.player.lives = 3  # Reset lives to the initial value
     self.score = 0  # Reset score
     self.game_over = False  # Clear the game over flag
    def clickHandler(self, event: pyasge.ClickEvent) -> None:
           if event.button == pyasge.MOUSE.MOUSE_BTN1:  # MOUSE_BTN1 usually represents the left mouse button
        # Check if the game is not in the menu state
             if not self.menu:
            # Fire a bullet
               self.FireBullet()

    def keyHandler(self, event: pyasge.KeyEvent) -> None:
        if self.game_over and event.key == pyasge.KEYS.KEY_R and event.action == pyasge.KEYS.KEY_PRESSED:
         self.resetGame()

        # Act only if a button has been pressed
        if event.action == pyasge.KEYS.KEY_PRESSED:

            # Closes the game whenever Escape is pressed regardless of game state
            if event.key == pyasge.KEYS.KEY_ESCAPE:
                exit()

            # If we are currently on the main menu screen
            if self.menu == True:
                # we check whether specific button (Spacebar in this case)
                # have been pressed
                if event.key == pyasge.KEYS.KEY_SPACE:
                    # We change the state from main menu to game screen
                    self.menu = False

            # If we are not in menu that means we are in main game screen
            else:
                if event.key in [pyasge.KEYS.KEY_W, pyasge.KEYS.KEY_UP]:
                     self.key_states["up"] = True
                if event.key in [pyasge.KEYS.KEY_S, pyasge.KEYS.KEY_DOWN]:
                    self.key_states["down"] = True
                if event.key in [pyasge.KEYS.KEY_A, pyasge.KEYS.KEY_LEFT]:
                    self.key_states["left"] = True
                if event.key in [pyasge.KEYS.KEY_D, pyasge.KEYS.KEY_RIGHT]:
                    self.key_states["right"] = True
                    
         
                # This is where you will implement your in-game inputs
                pass

        # This event is triggered whenever a button is released
        if event.action == pyasge.KEYS.KEY_RELEASED:
            if self.menu == True:
                pass
            else:
                if event.key in [pyasge.KEYS.KEY_W, pyasge.KEYS.KEY_UP]:
                 self.key_states["up"] = False
                if event.key in [pyasge.KEYS.KEY_S, pyasge.KEYS.KEY_DOWN]:
                    self.key_states["down"] = False
                if event.key in [pyasge.KEYS.KEY_A, pyasge.KEYS.KEY_LEFT]:
                    self.key_states["left"] = False
                if event.key in [pyasge.KEYS.KEY_D, pyasge.KEYS.KEY_RIGHT]:
                    self.key_states["right"] = False
                # You can track which buttons have been released here
                pass
            


    def check_collision(self, sprite_1: pyasge.Sprite, sprite_2: pyasge.Sprite) -> bool:
        # Check if the right edge of sprite_1 is left of the left edge of sprite_2
        if sprite_1.x + sprite_1.width < sprite_2.x:
            return False
        # Check if the left edge of sprite_1 is right of the right edge of sprite_2
        if sprite_1.x > sprite_2.x + sprite_2.width:
            return False
        # Check if the bottom edge of sprite_1 is above the top edge of sprite_2
        if sprite_1.y + sprite_1.height < sprite_2.y:
            return False
        # Check if the top edge of sprite_1 is below the bottom edge of sprite_2
        if sprite_1.y > sprite_2.y + sprite_2.height:
            return False
        return True
    def initLivesDisplay(self):
    # Assuming "MainFont" is already loaded as in initScoreDisplay
        self.lives_text = pyasge.Text(self.data.fonts["MainFont"], "Lives: 3")
        self.lives_text.position = pyasge.Point2D(self.data.game_res[0] - 0, 60)  # Adjust position as needed
        self.lives_text.colour = pyasge.COLOURS.WHITE
    
    def update(self, game_time: pyasge.GameTime) -> None:

        if self.menu:

            pass
        elif self.game_over:
         return
    
        else:
            x_dir = 0
            y_dir = 0
            if self.key_states["up"]:
                y_dir -= 1
            if self.key_states["down"]:
                y_dir += 1
            if self.key_states["left"]:
                x_dir -= 1
            if self.key_states["right"]:
                x_dir += 1
                
   
        
      
            
               
         
            # update the game here
            self.player.update_move_direction([x_dir, y_dir])
            self.player.Move()
            self.lives_text.string = f"Lives: {self.player.lives}"  # Update lives display

            for asteroid in self.asteroids:
             self.AsteroidScreenWrap(asteroid)
             
             asteroid.Move() 
             self.ShipScreenWrap()
            for asteroid in self.asteroids[:]:  # Use a copy of the list to avoid modification issues
             if self.check_collision(self.player.sprite, asteroid.sprite):
                self.asteroids.remove(asteroid)  # Remove the collided asteroid
                self.reset_player_position()  # Reset player's position or handle life loss
                self.player.lives -= 1  # Assuming you have a lives attribute
                if self.player.lives <= 0:
                 self.game_over = True
                break            
             for projectile in self.projectiles:
               projectile.Move()
            for projectile in self.projectiles[:]:
             for asteroid in self.asteroids[:]:
                if self.check_collision(projectile.sprite, asteroid.sprite):
                    self.asteroids.remove(asteroid)
                    self.projectiles.remove(projectile)
                    self.score += 1  # Increase the score by 1
                    self.score_text.string = f"Score: {self.score}"  # Update score text
                    break

            while len(self.asteroids) < self.max_asteroids:
                self.spawn_asteroids(1) 

  

            pass
    def AsteroidScreenWrap(self, asteroid: GameObject.Asteroid):
        # Right boundary
        if asteroid.sprite.x > self.data.game_res[0]:
            asteroid.sprite.x = -asteroid.sprite.width

        # Left boundary
        elif asteroid.sprite.x < -asteroid.sprite.width:
            asteroid.sprite.x = self.data.game_res[0]

        # Bottom boundary
        if asteroid.sprite.y > self.data.game_res[1]:
            asteroid.sprite.y = -asteroid.sprite.height

        # Top boundary
        elif asteroid.sprite.y < -asteroid.sprite.height:
            asteroid.sprite.y = self.data.game_res[1]

    def reset_player_position(self):
        self.player.sprite.x = self.data.game_res[0] / 2 - self.player.sprite.width / 2
        self.player.sprite.y = self.data.game_res[1] / 2 - self.player.sprite.height / 2




    def spawn_asteroids(self, number_of_asteroids: int):
        for _ in range(number_of_asteroids):
            new_asteroid = GameObject.Asteroid()
        
            # Randomly position the asteroid, ensuring it's within screen bounds
            new_asteroid.sprite.x = random.uniform(0, self.data.game_res[0] - new_asteroid.sprite.width)
            new_asteroid.sprite.y = random.uniform(0, self.data.game_res[1] - new_asteroid.sprite.height)
        
            # Set a random movement direction
            angle = random.uniform(0, 2 * math.pi)
            new_asteroid.move_direction = [math.cos(angle), math.sin(angle)]
            new_asteroid.move_speed = random.uniform(5, 10)  # Example speed range
        
            # Load texture, set z_order, etc.
            new_asteroid.sprite.loadTexture("/data/images/kenney_simple-space/PNG/Retina/meteor_detailedLarge.png")
            new_asteroid.sprite.z_order = -10
        
            self.asteroids.append(new_asteroid)



    def render(self, game_time: pyasge.GameTime) -> None:
        """
        This is the variable time-step function. Use to update
        animations and to render the game-world. The use of
        ``frame_time`` is essential to ensure consistent performance.
        @param game_time: The tick and frame deltas.
        """

        if self.menu:
            # Render the menu screen here
            self.data.renderer.render(self.menu_text)

            self.data.renderer.render(self.start_text)

            pass
        elif self.game_over:
            self.data.renderer.render(self.game_over_text)
        else:
            # render the game here
            self.data.renderer.render(self.score_text)
            for asteroid in self.asteroids:
             self.data.renderer.render(asteroid.sprite)
            self.data.renderer.render(self.player.sprite)
            for projectile in self.projectiles:
             self.data.renderer.render(projectile.sprite)
            self.data.renderer.render(self.lives_text)
            
        
    def ShipScreenWrap(self):
        # Right boundary
        if self.player.sprite.x > self.data.game_res[0]:
            self.player.sprite.x = -self.player.sprite.width

        # Left boundary
        elif self.player.sprite.x + self.player.sprite.width < 0:
            self.player.sprite.x = self.data.game_res[0]

        # Bottom boundary
        if self.player.sprite.y > self.data.game_res[1]:
            self.player.sprite.y = -self.player.sprite.height

        # Top boundary
        elif self.player.sprite.y + self.player.sprite.height < 0:
            self.player.sprite.y = self.data.game_res[1]







def main():
    """
    Creates the game and runs it
    For ASGE Games to run they need settings. These settings
    allow changes to the way the game is presented, its
    simulation speed and also its dimensions. For this project
    the FPS and fixed updates are capped at 60hz and Vsync is
    set to adaptive.
    """
    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.BORDERLESS_WINDOW
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()
