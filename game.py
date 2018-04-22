import arcade
import os
import math

SPRITE_SCALING = 0.75
PLAYER_SCALING = 0.55
SPRITE_NATIVE_SIZE = 64
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)
SPRITE_SCALING_LASER = 0.3
BULLET_SPEED = 10
SCREEN_WIDTH = SPRITE_SIZE * 32
SCREEN_HEIGHT = SPRITE_SIZE * 20

MOVEMENT_SPEED = 6
JUMP_SPEED = 14
ENEMY_JUMP_SPEED = 25
GRAVITY = 0.5

class Bullet(arcade.Sprite):
    def update(self):
        self.center_x += BULLET_SPEED
class Enemy_Bullet(arcade.Sprite):
    def update(self):
        self.center_x -= BULLET_SPEED
class TextButton:
    """ Text-based button """
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Futura-Medium",
                 face_color=arcade.color.BLACK,
                 highlight_color=arcade.color.BLACK,
                 shadow_color=arcade.color.BLACK,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color, 6)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

def check_mouse_press_for_buttons(x, y, button_list, game):
    """ Given an x, y, see if we need to register any button clicks. """
    for index, button in enumerate(button_list):
        if game.current_screen == 1 and index != 3:
            continue
        if game.current_screen == 2:
            continue
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(x, y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()

class StartTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 400, 100, "Play", 24, "Futura-Medium")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class CreditsTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 400, 100, "Credits", 24, "Futura-Medium")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class BackTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 400, 100, "Back to Main Screen", 24, "Futura-Medium")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class StopTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 400, 100, "Quit", 24, "Futura-Medium")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class Screen:
    '''
    This class holds information about the screens.
    '''
    def __init__(self):
        self.wall_list = None
        self.background = None
        self.button_list = None




def MainScreen():
    ''' Create and return the screen for the main screen '''
    main_screen = Screen()
    main_screen.background = arcade.load_texture("images/main_background.png")

    return main_screen


def CreditsScreen():
    ''' Create and return the screen for the credits screen '''
    credits_screen = Screen()
    credits_screen.background = arcade.load_texture("images/credits.png")

    return credits_screen

def setup_screen_1():
    # Level 1: College Bully
    level1 = Screen()
    level1.background = arcade.load_texture("images/level1background.jpg")

    level1.wall_list = arcade.SpriteList()
    # Create top and bottom column of boxes
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if y < 20:
                wall = arcade.Sprite("images/grass_floor.png", SPRITE_SCALING)
            # else:
            #     wall = arcade.Sprite("images/brick_wall.png", SPRITE_SCALING)

                wall.left = x
                wall.bottom = y
                level1.wall_list.append(wall)
    for x in range(6,10):
        wall1 = arcade.Sprite("images/grass_floor.png", SPRITE_SCALING)
        wall1.left = x * SPRITE_SIZE
        wall1.bottom = 3 * SPRITE_SIZE
        level1.wall_list.append(wall1)

    for x in range(0,3):
        wall1 = arcade.Sprite("images/grass_floor.png", SPRITE_SCALING)
        wall1.left = x * SPRITE_SIZE
        wall1.bottom = 5 * SPRITE_SIZE
        level1.wall_list.append(wall1)
    level1.background = arcade.load_texture("images/level1background.jpg")

    for x in range(7,10):
        wall1 = arcade.Sprite("images/grass_floor.png", SPRITE_SCALING)
        wall1.left = x * SPRITE_SIZE
        wall1.bottom = 7 * SPRITE_SIZE
        level1.wall_list.append(wall1)
    level1.background = arcade.load_texture("images/level1background.jpg")

    for x in range(0,2):
        wall1 = arcade.Sprite("images/grass_floor.png", SPRITE_SCALING)
        wall1.left = x * SPRITE_SIZE
        wall1.bottom = 10 * SPRITE_SIZE
        level1.wall_list.append(wall1)
    level1.background = arcade.load_texture("images/level1background.jpg")

    return level1


def setup_screen_2():
    # Level 2: Midterms
    var = 3
def setup_screen_3():
    # Level 3: Finals
    var = 4
class PlatformerGame(arcade.Window):
    ''' Class that holds main application functions: initializer, update, draw, etc... '''
    def quit(self):
        os._exit(0)
    def play(self):
        self.current_screen = 2
    def credits(self):
        self.current_screen = 1
    def main(self):
        self.current_screen = 0
    def __init__(self, width, height):
        ''' Initializer '''
        super().__init__(width, height)

        # Set working directory to same folder this file is in
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite Lists
        self.current_screen = 0
        self.button_list = None
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.all_sprites_list = None
        self.enemy_sprite = None

    def setup(self):
        self.all_sprites_list = arcade.SpriteList()
        ''' Set up the game and initialize the variables '''
        # set up the player
        self.enemy_bullet_counter = 0

        self.player_sprite  = arcade.AnimatedWalkingSprite()
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 73

        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_right_textures.append(arcade.load_texture("images/character_sprites/character0.png", scale=PLAYER_SCALING))
        self.player_sprite.stand_left_textures = []
        self.player_sprite.stand_left_textures.append(arcade.load_texture("images/character_sprites/character0.png",scale=PLAYER_SCALING, mirrored=True))

        self.player_sprite.walk_right_textures = []
        self.player_sprite.walk_right_textures.append(arcade.load_texture("images/character_sprites/characterw0.png",scale=PLAYER_SCALING))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("images/character_sprites/characterw1.png",scale=PLAYER_SCALING))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("images/character_sprites/characterw2.png",scale=PLAYER_SCALING))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("images/character_sprites/characterw3.png",scale=PLAYER_SCALING))

        self.player_sprite.walk_left_textures = []
        self.player_sprite.walk_left_textures.append(arcade.load_texture("images/character_sprites/characterw0.png",scale=PLAYER_SCALING, mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("images/character_sprites/characterw1.png",scale=PLAYER_SCALING, mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("images/character_sprites/characterw2.png",scale=PLAYER_SCALING, mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("images/character_sprites/characterw3.png",scale=PLAYER_SCALING, mirrored=True))

        self.player_sprite.texture_change_distance = 35
        self.enemy_health = 100
        self.player_health = 100
        self.all_sprites_list.append(self.player_sprite)
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.move_right = False
        self.move_left = False
        self.moving_up = False
        self.last_y = self.player_sprite.center_y

        self.enemy_sprite = arcade.Sprite("images/bully1.png", 0.65)
        self.enemy_sprite.center_x = 1400
        self.enemy_sprite.center_y = 77
        self.all_sprites_list.append(self.enemy_sprite)
        # setup screens
        self.screens = []
        screen1 = MainScreen()
        self.screens.append(screen1)
        screen2 = CreditsScreen()
        self.screens.append(screen2)
        screen3 = setup_screen_1()
        self.screens.append(screen3)
        screen4 = setup_screen_2()
        self.screens.append(screen4)
        screen5 = setup_screen_3()
        self.screens.append(screen5)

        # choose starting room
        self.current_screen = 0
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.screens[2].wall_list, GRAVITY)
        self.physics_engine2 = arcade.PhysicsEnginePlatformer(self.enemy_sprite, self.screens[2].wall_list, GRAVITY)
        self.button_list = []
        play_button = StartTextButton(784, 605, self.play)
        self.button_list.append(play_button)
        credits_button = CreditsTextButton(784, 465, self.credits)
        self.button_list.append(credits_button)
        quit_button = StopTextButton(784, 325, self.quit)
        self.button_list.append(quit_button)
        back_button = BackTextButton(784,683, self.main)
        self.button_list.append(back_button)


    def on_draw(self):
        ''' Actually render the screen '''

        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.screens[self.current_screen].background)
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()
        if self.screens[self.current_screen].wall_list != None:
            self.screens[self.current_screen].wall_list.draw()
            self.player_sprite.draw()
            if self.enemy_health > 0:
                self.enemy_sprite.draw()
            else:
                arcade.draw_text("Congrats, you have defeated the bully!!", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.BLACK, 35, width=250, align="center",
                                             anchor_x="center", anchor_y="center")
        if self.current_screen == 0:
            for index, button in enumerate(self.button_list):
                if index != 3:
                    button.draw()
        if self.current_screen == 1:
            self.button_list[3].draw()
        if self.current_screen == 2:

            arcade.draw_text("Player Health: " + str(self.player_health), self.player_sprite.center_x, self.player_sprite.center_y +50, arcade.color.BLACK, 14, width=150, align="center",
                             anchor_x="center", anchor_y="center")
            if self.enemy_health > 0:
                arcade.draw_text("Enemy Health: " + str(self.enemy_health), self.enemy_sprite.center_x, self.enemy_sprite.center_y +50, arcade.color.BLACK, 14, width=150, align="center",
                                 anchor_x="center", anchor_y="center")
    def on_key_press(self, key, modifiers):
        ''' Called whenever a key is pressed. '''

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        if key == arcade.key.LEFT:
            self.move_left = True
        if key == arcade.key.RIGHT:
            self.move_right = True
        if key == arcade.key.SPACE:
            bullet = Bullet("images/bullet.png", SPRITE_SCALING_LASER)
            bullet2 = Enemy_Bullet("images/enemy_bullet.png", SPRITE_SCALING_LASER)
            bullet.angle = 270
            bullet2.angle = 90
            # Position the bullet
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.center_y
            bullet2.center_x = self.enemy_sprite.center_x
            bullet2.bottom = self.enemy_sprite.center_y
            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)
            self.enemy_bullet_list.append(bullet2)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT:
            self.move_left = False
        if key == arcade.key.RIGHT:
            self.move_right = False

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        check_mouse_press_for_buttons(x, y, self.button_list, self)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        self.on_mouse_press(x,y,button, key_modifiers)
        check_mouse_release_for_buttons(x, y, self.button_list)

    def update(self, delta_time):

        if self.physics_engine2.can_jump():
            self.enemy_sprite.change_y = ENEMY_JUMP_SPEED

        """ Movement and game logic """
        if self.move_right == True and self.move_left == False:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif self.move_left == True and self.move_right == False:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.move_left == True and self.move_right == True:
            self.player_sprite.change_x = 0
        elif self.move_right == False and self.move_left == False:
            self.player_sprite.change_x = 0
        if self.current_screen == 2 and self.physics_engine != None:
            self.physics_engine.update()
            self.physics_engine2.update()
            self.bullet_list.update()
            self.enemy_bullet_list.update()
            self.player_sprite.update_animation()
        if self.player_sprite.center_x < 31:
            self.player_sprite.center_x = 32
        if self.player_sprite.center_x > 1510:
            self.player_sprite.center_x = 1509
        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_screen == 2:
            self.current_screen = 1
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.screens[self.current_screen].wall_list, GRAVITY)
            self.player_sprite.center_x = 0




        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.screens[self.current_screen].wall_list)
            enemy = arcade.SpriteList()
            enemy.append(self.enemy_sprite)
            enemy_hit = arcade.check_for_collision_with_list(bullet, enemy)
            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.kill()
            if len(enemy_hit) > 0:
                bullet.kill()
                self.enemy_health -= 5
                            # For every coin we hit, add to the score and remove the coin

            # If the bullet flies off-screen, remove it.
            if bullet.left > SCREEN_WIDTH:
                bullet.kill()
        for bullet in self.enemy_bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.screens[self.current_screen].wall_list)
            enemy = arcade.SpriteList()
            enemy.append(self.player_sprite)
            enemy_hit = arcade.check_for_collision_with_list(bullet, enemy)
            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.kill()
            if len(enemy_hit) > 0:
                bullet.kill()
                self.player_health -= 5
                            # For every coin we hit, add to the score and remove the coin

            # If the bullet flies off-screen, remove it.
            if bullet.left > SCREEN_WIDTH:
                bullet.kill()

def main():
    """ Main method """
    window = PlatformerGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.set_update_rate(1/60)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
