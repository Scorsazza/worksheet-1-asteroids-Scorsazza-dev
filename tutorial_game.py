import random
import pyasge
import GameObject
import time
import math
from gamedata import GameData
from GameObject import Asteroid, Ship, Projectile

class LeaderboardEntry:
    def __init__(self, name, score):
        self.name = name
        self.score = score

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
        self.leaderboard = []
        self.renderer.setClearColour(pyasge.COLOURS.BLACK)
        self.direction_vector = [0, 0]
        self.projectiles = []
        self.last_shot_time = 0
        self.score = 0
        self.game_over = False

        self.cooldown_time = 0.25
        self.max_asteroids = 3

        self.data = GameData()
        self.data.renderer = self.renderer
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 24)
        self.initScoreDisplay()
        self.initGameOverScreen()

        self.key_states = {"up": False, "down": False, "left": False, "right": False}
        self.data.inputs = self.inputs

        self.data.game_res = [settings.window_width, settings.window_height]

        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.keyHandler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.clickHandler)

        self.menu = True
        self.play_option = None
        self.exit_option = None
        self.menu_option = 0

        self.data.background = pyasge.Sprite()
        self.initBackground()

        self.menu_text = None
        self.start_text = None
        self.initMenu()

        self.scoreboard = None
        self.initScoreboard()

        self.asteroid = GameObject.Asteroid()
        self.initAsteroid()
        self.asteroids = []
        self.spawn_asteroids(5)

        self.player = GameObject.Ship()
        self.initPlayer()
        self.initLivesDisplay()
        self.projectile = GameObject.Projectile()
        self.initProjectile()
        self.resetGame()

    def initBackground(self) -> bool:
        pass

    def initScoreDisplay(self):

        if "MainFont" in self.data.fonts:
            self.score_text = pyasge.Text(self.data.fonts["MainFont"], "Score: 0")
            self.score_text.position = pyasge.Point2D(20, 20)
            self.score_text.scale = 1
            self.score_text.colour = pyasge.COLOURS.WHITE
        else:
            print("Error: MainFont not loaded. Check the font path and ensure it's loaded before initScoreDisplay is called.")

    def initGameOverScreen(self):
        self.game_over_text = pyasge.Text(self.data.fonts["MainFont"], f"GAME OVER - Score: {self.score}, PRESS R TO PLAY AGAIN")
        self.end_game()
        leaderboard_text = pyasge.Text(self.data.renderer.getDefaultFont(), "Leaderboard", 400, 350)
        leaderboard_text.colour = pyasge.COLOURS.WHITE
        self.data.renderer.render(leaderboard_text)

        y_offset = 400
        for idx, entry in enumerate(self.leaderboard[:5]):
            entry_text = pyasge.Text(self.data.renderer.getDefaultFont(), f"{idx + 1}. {entry.name}: {entry.score}",400, y_offset)
            entry_text.colour = pyasge.COLOURS.WHITE
            self.data.renderer.render(entry_text)
            y_offset += 50
        self.game_over_text.position = pyasge.Point2D(550, 500)
        self.game_over_text.colour = pyasge.COLOURS.RED

    def handle_asteroid_collision(self, asteroid_index):
        asteroid = self.asteroids[asteroid_index]
        if asteroid.sprite.scale > 1:
            scale_factor = 0.5
            for _ in range(2):
                new_asteroid = Asteroid()
                new_asteroid.sprite.x = asteroid.sprite.x
                new_asteroid.sprite.y = asteroid.sprite.y
                new_asteroid.sprite.scale = asteroid.sprite.scale * scale_factor
                new_asteroid.sprite.loadTexture("/data/images/kenney_simple-space/PNG/Retina/meteor_detailedLarge.png")
                dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
                norm = math.sqrt(dx ** 2 + dy ** 2)
                new_asteroid.move_direction = [dx / norm, dy / norm]
                new_asteroid.move_speed = random.uniform(1, 5)
                self.asteroids_to_add.append(new_asteroid)
        self.asteroids_to_remove.append(asteroid_index)

    def create_smaller_asteroid(self, parent_asteroid):
        new_asteroid = GameObject.Asteroid()
        new_asteroid.sprite.x = parent_asteroid.sprite.x
        new_asteroid.sprite.y = parent_asteroid.sprite.y
        new_asteroid.sprite.scale = parent_asteroid.sprite.scale / 2

        dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
        norm = math.sqrt(dx ** 2 + dy ** 2)
        new_asteroid.move_direction = [dx / norm, dy / norm]
        new_asteroid.move_speed = parent_asteroid.move_speed + random.uniform(0.5, 1.5)

        return new_asteroid

    def resetGame(self):
        self.player.lives = 3
        self.score = 0
        self.game_over = False
        self.menu = True
        self.projectiles.clear()
        self.asteroids.clear()
        self.spawn_asteroids(5)

        self.score_text.string = f"Score: {self.score}"

        self.lives_text.string = f"Lives: {self.player.lives}"

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

        if self.player.sprite.loadTexture("data/images/kenney_simple-space/PNG/Retina/ship_G.png"):
            self.player.move_speed = 8.0
            self.player.sprite.x = self.data.game_res[0] / 2 - self.player.sprite.width / 2
            self.player.sprite.y = self.data.game_res[1] / 2 - self.player.sprite.height / 2
            self.player.sprite.scale = 0.5

            self.player.collisionSprite.loadTexture("data/images/kenney_simple-space/PNG/Retina/ship_G.png")
            self.player.collisionSprite.x = self.data.game_res[0] / 2 - self.player.sprite.width / 2
            self.player.collisionSprite.y = self.data.game_res[1] / 2 - self.player.sprite.height / 2
            self.player.collisionSprite.scale = 0.5
            return True
        return False

    def initLivesDisplay(self):

        if "MainFont" in self.data.fonts:
            self.lives_text = pyasge.Text(self.data.fonts["MainFont"], f"Lives: {self.player.lives}")

            self.lives_text.position = pyasge.Point2D(self.score_text.position.x + 150, 20)
            self.lives_text.scale = 0.5
            self.lives_text.colour = pyasge.COLOURS.WHITE
        else:
            print("Error: MainFont not loaded. Check the font path and ensure it's loaded before calling initLivesDisplay.")

    def initProjectile(self) -> bool:

        self.projectile.sprite.loadTexture("/data/images/kenney_simple-space/PNG/Retina/star_tiny.png")
        pass

    def spawn(self, gameObject: GameObject) -> None:
        pass

    def initScoreboard(self) -> None:
        pass

    def FireBullet(self):
        new_projectile = GameObject.Projectile()
        if time.time() - self.last_shot_time < self.cooldown_time:
            return

        offset_distance = 50
        ship_front_x = self.player.sprite.x - 30
        ship_front_y = self.player.sprite.y - 30

        angle_offset = math.pi / 2
        spawn_x = ship_front_x + offset_distance * math.cos(self.player.sprite.rotation - angle_offset)
        spawn_y = ship_front_y + offset_distance * math.sin(self.player.sprite.rotation - angle_offset)

        new_projectile.sprite.x = spawn_x
        new_projectile.sprite.y = spawn_y
        new_projectile.sprite.loadTexture("/data/images/kenney_simple-space/PNG/Retina/star_tiny.png")

        new_projectile.move_direction = [math.cos(self.player.sprite.rotation - angle_offset),
                                         math.sin(self.player.sprite.rotation - angle_offset)]
        new_projectile.move_speed = 10
        self.projectiles.append(new_projectile)
        self.last_shot_time = time.time()

    def initMenu(self) -> bool:

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

    def clickHandler(self, event: pyasge.ClickEvent) -> None:
        if event.button == pyasge.MOUSE.MOUSE_BTN1:

            if not self.menu:

                self.FireBullet()

    def keyHandler(self, event: pyasge.KeyEvent) -> None:
        if self.game_over and event.key == pyasge.KEYS.KEY_R and event.action == pyasge.KEYS.KEY_PRESSED:
            self.resetGame()

        if event.action == pyasge.KEYS.KEY_PRESSED:

            if event.key == pyasge.KEYS.KEY_ESCAPE:
                exit()

            if self.menu == True:

                if event.key == pyasge.KEYS.KEY_SPACE:

                    self.menu = False

            else:
                if event.key in [pyasge.KEYS.KEY_W, pyasge.KEYS.KEY_UP]:
                    self.key_states["up"] = True
                if event.key in [pyasge.KEYS.KEY_S, pyasge.KEYS.KEY_DOWN]:
                    self.key_states["down"] = True
                if event.key in [pyasge.KEYS.KEY_A, pyasge.KEYS.KEY_LEFT]:
                    self.key_states["left"] = True
                if event.key in [pyasge.KEYS.KEY_D, pyasge.KEYS.KEY_RIGHT]:
                    self.key_states["right"] = True

                pass

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

                pass

    def check_collision(self, sprite_1: pyasge.Sprite, sprite_2: pyasge.Sprite) -> bool:

        sprite_1_width_scaled = sprite_1.width * sprite_1.scale
        sprite_1_height_scaled = sprite_1.height * sprite_1.scale

        sprite_2_width_scaled = sprite_2.width * sprite_2.scale
        sprite_2_height_scaled = sprite_2.height * sprite_2.scale

        if sprite_1.x + sprite_1_width_scaled < sprite_2.x:
            return False

        if sprite_1.x > sprite_2.x + sprite_2_width_scaled:
            return False

        if sprite_1.y + sprite_1_height_scaled < sprite_2.y:
            return False

        if sprite_1.y > sprite_2.y + sprite_2_height_scaled:
            return False

        return True

    def update(self, game_time: pyasge.GameTime) -> None:
        self.asteroids_to_add = []
        self.asteroids_to_remove = []
        self.score_text.string = f"Score: {self.score}"

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

            self.player.update_move_direction([x_dir, y_dir])
            self.player.Move()
            self.lives_text.string = f"Lives: {self.player.lives}"

            for asteroid in self.asteroids:
                self.AsteroidScreenWrap(asteroid)
                asteroid.Move()
            self.ShipScreenWrap()

            for projectile in self.projectiles[:]:
                projectile.Move()
                for i, asteroid in enumerate(self.asteroids):
                    if self.check_collision(projectile.sprite, asteroid.sprite):
                        self.handle_asteroid_collision(i)
                        self.projectiles.remove(projectile)
                        self.score += 1
                        self.score_text.string = f"Score: {self.score}"
                        break

            for asteroid in self.asteroids[:]:
                if self.check_collision(self.player.sprite, asteroid.sprite):
                    self.asteroids.remove(asteroid)
                    self.reset_player_position()
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        self.game_over = True
                        self.end_game()
                        self.bubble_sort_leaderboard()
                    break

            for i in sorted(self.asteroids_to_remove, reverse=True):
                del self.asteroids[i]
            self.asteroids.extend(self.asteroids_to_add)

            while len(self.asteroids) < self.max_asteroids:
                self.spawn_asteroids(1)

    def generate_unique_leaderboard_entry(self, base_name):
        count = 1
        new_name = base_name
        while any(entry.name == new_name for entry in self.leaderboard):
            count += 1
            new_name = f"{base_name}{count}"
        return new_name

    def generate_random_leaderboard_entries(self):
        possible_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Steve", "Quinn", "Richard", "Wojciech"]
        for _ in range(5):
            name = random.choice(possible_names)
            unique_name = self.generate_unique_leaderboard_entry(name)
            score = random.randint(5, 20)
            self.leaderboard.append(LeaderboardEntry(unique_name, score))

    def bubble_sort_leaderboard(self):

        n = len(self.leaderboard)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.leaderboard[j].score < self.leaderboard[j + 1].score:
                    self.leaderboard[j], self.leaderboard[j + 1] = self.leaderboard[j + 1], self.leaderboard[j]
                elif self.leaderboard[j].score == self.leaderboard[j + 1].score:

                    if self.leaderboard[j].name > self.leaderboard[j + 1].name:
                        self.leaderboard[j], self.leaderboard[j + 1] = self.leaderboard[j + 1], self.leaderboard[j]

    def end_game(self):

        self.leaderboard.clear()

        self.leaderboard.insert(0, LeaderboardEntry("YOU", self.score))

        self.generate_random_leaderboard_entries()

    def AsteroidScreenWrap(self, asteroid: GameObject.Asteroid):

        if asteroid.sprite.x > self.data.game_res[0]:
            asteroid.sprite.x = -asteroid.sprite.width

        elif asteroid.sprite.x < -asteroid.sprite.width:
            asteroid.sprite.x = self.data.game_res[0]

        if asteroid.sprite.y > self.data.game_res[1]:
            asteroid.sprite.y = -asteroid.sprite.height

        elif asteroid.sprite.y < -asteroid.sprite.height:
            asteroid.sprite.y = self.data.game_res[1]

    def reset_player_position(self):
        self.player.sprite.x = self.data.game_res[0] / 2 - self.player.sprite.width / 2
        self.player.sprite.y = self.data.game_res[1] / 2 - self.player.sprite.height / 2

    def spawn_asteroids(self, number_of_asteroids: int):
        for _ in range(number_of_asteroids):
            new_asteroid = GameObject.Asteroid()

            new_asteroid.sprite.x = random.uniform(0, self.data.game_res[0] - new_asteroid.sprite.width)
            new_asteroid.sprite.y = random.uniform(0, self.data.game_res[1] - new_asteroid.sprite.height)

            angle = random.uniform(0, 2 * math.pi)
            new_asteroid.move_direction = [math.cos(angle), math.sin(angle)]
            new_asteroid.move_speed = random.uniform(5, 10)

            new_asteroid.sprite.loadTexture("/data/images/kenney_simple-space/PNG/Retina/meteor_detailedLarge.png")
            new_asteroid.sprite.z_order = -10

            self.asteroids.append(new_asteroid)

    def render(self, game_time: pyasge.GameTime) -> None:
        if self.menu:
            self.data.renderer.render(self.menu_text)
            self.data.renderer.render(self.start_text)
        elif self.game_over:
            self.game_over_text.string = f"GAME OVER - Score: {self.score}, PRESS R TO PLAY AGAIN"
            self.data.renderer.render(self.game_over_text)
            self.bubble_sort_leaderboard()

            leaderboard_text = pyasge.Text(self.data.fonts["MainFont"], "Leaderboard")
            leaderboard_text.position = pyasge.Point2D(620, 100)
            leaderboard_text.colour = pyasge.COLOURS.WHITE
            leaderboard_text.scale = 0.8
            self.data.renderer.render(leaderboard_text)

            y_offset = 150
            for idx, entry in enumerate(self.leaderboard[:5]):
                entry_text = pyasge.Text(self.data.fonts["MainFont"], f"{idx + 1}. {entry.name}: {entry.score}")
                entry_text.position = pyasge.Point2D(600, y_offset + idx * 50)
                entry_text.colour = pyasge.COLOURS.WHITE
                entry_text.scale = 0.8
                self.data.renderer.render(entry_text)
        else:

            self.data.renderer.render(self.score_text)
            self.data.renderer.render(self.lives_text)
            for asteroid in self.asteroids:
                self.data.renderer.render(asteroid.sprite)
            self.data.renderer.render(self.player.sprite)
            for projectile in self.projectiles:
                self.data.renderer.render(projectile.sprite)

    def ShipScreenWrap(self):

        if self.player.sprite.x > self.data.game_res[0]:
            self.player.sprite.x = -self.player.sprite.width

        elif self.player.sprite.x + self.player.sprite.width < 0:
            self.player.sprite.x = self.data.game_res[0]

        if self.player.sprite.y > self.data.game_res[1]:
            self.player.sprite.y = -self.player.sprite.height

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