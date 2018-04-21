import arcade
import os

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = SPRITE_SIZE * 14
SCREEN_HEIGHT = SPRITE_SIZE * 10

MOVEMENT_SPEED = 5

class PlatformerGame(arcade.Window):
    ''' Class that holds main application functions: initializer, update, draw, etc... '''

    def __init__(self, width, height):
        ''' Initializer '''
        super().__init__(width, height)

        # Set working directory to same folder this file is in
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite Lists
        self.current_screen = 0


    def setup(self):
        ''' Set up the game and initialize the variables '''

        # set up the player
        self.life = 3
        self.player_sprite  = arcade.Sprite("images/character.jpg", SPRITE_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100

        # setup screens
        self.screens = []
        screen = setup_screen_1()
        self.screens.append(screen)
        screen = setup_screen_2()
        self.screens.append(screen)
        screen = setup_screen_3()
        self.screens.append(screen)

        # choose starting room
        self.current_screen = 0

    def on_draw(self):
        ''' Actually render the screen '''

        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.screens[self.current_screen].background)
        self.screens[self.current_screen].wall_list.draw()

        self.player_sprite.draw()

        def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
