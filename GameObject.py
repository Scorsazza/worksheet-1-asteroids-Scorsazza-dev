import pyasge
import math
import random

class GameObject:

    def __init__(self):
        self.sprite = pyasge.Sprite()
        self.move_direction = [0.0, 0.0]


class Asteroid(GameObject):

    def __init__(self):
        super().__init__()
        self.move_speed = random.uniform(1, 5)
        dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
        norm = math.sqrt(dx**2 + dy**2)
        self.move_direction = [dx/norm, dy/norm]
        self.sprite.scale = random.uniform(0.5, 2)
        self.collisionSprite = pyasge.Sprite()
    def Move(self):
        self.sprite.x += self.move_direction[0] * self.move_speed
        self.sprite.y += self.move_direction[1] * self.move_speed


class Ship(GameObject):
    def __init__(self):
        super().__init__()
        self.move_speed = 0.0
        self.lives = 3 
        self.collisionSprite = pyasge.Sprite()
    def update_move_direction(self, direction):
        self.move_direction = direction
        self.update_rotation()
    
    def update_rotation(self):
        dx, dy = self.move_direction

        if dx != 0 or dy != 0:
            # Calculate the angle in radians using atan2, with dy and dx as is
            angle_radians = math.atan2(dy, dx)

            # Convert radians to degrees
            angle_degrees = math.degrees(angle_radians)

            # Adjust for sprite's default up-facing orientation by subtracting 90 degrees
            # This aligns the 0 degrees (right) to the sprite's up direction
            adjusted_angle = (angle_degrees + 90) % 360

            # Apply the calculated rotation to the sprite, converting to radians if necessary
            self.sprite.rotation = math.radians(adjusted_angle)







    def Move(self):
  
        
        
        self.sprite.x += self.move_direction[0] * self.move_speed
        self.sprite.y += self.move_direction[1] * self.move_speed
        self.collisionSprite.x = self.sprite.x
        self.collisionSprite.y = self.sprite.y
        pass


class Projectile(GameObject):

    def __init__(self):
        super(Projectile, self).__init__()
    def Move(self):
        self.sprite.x += self.move_direction[0] * self.move_speed
        self.sprite.y += self.move_direction[1] * self.move_speed