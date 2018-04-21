import arcade
import os

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = SPRITE_SIZE * 14
SCREEN_HEIGHT = SPRITE_SIZE * 10

MOVEMENT_SPEED = 5

class TextButton:
    """ Text-based button """
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Futura-Medium",
                 face_color=arcade.color.RED,
                 highlight_color=arcade.color.ORANGE,
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
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
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

def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
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
        super().__init__(center_x, center_y, 200, 50, "Play", 24, "Futura-Medium")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class CreditsTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 200, 50, "Credits", 24, "Futura-Medium")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class StopTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 200, 50, "Quit", 24, "Futura-Medium")
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
    main_screen.button_list = []
    play_button = StartTextButton(448, 360, start_selection_screen)
    main_screen.button_list.append(play_button)
    credits_button = CreditsTextButton(448, 280, start_selection_screen)
    main_screen.button_list.append(credits_button)
    quit_button = StopTextButton(448, 200, os._exit)
    main_screen.button_list.append(quit_button)

    return main_screen

def start_selection_screen():
    window.current_screen = 1

def CreditsScreen():
    ''' Create and return the screen for the credits screen '''
    var = 1
def setup_screen_1():
    # Level 1: College Bully
    var = 2
def setup_screen_2():
    # Level 2: Midterms
    var = 3
def setup_screen_3():
    # Level 3: Finals
    var = 4
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
        self.button_list = None

    def setup(self):
        ''' Set up the game and initialize the variables '''

        # set up the player
        self.life = 3
        self.player_sprite  = arcade.Sprite("images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100

        # setup screens
        self.screens = []
        screen = MainScreen()
        self.screens.append(screen)
        screen = CreditsScreen()
        self.screens.append(screen)
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

        if self.screens[self.current_screen].wall_list != None:
            self.screens[self.current_screen].wall_list.draw()
            self.player_sprite.draw()
        if self.current_screen == 0:
            if self.screens[self.current_screen].button_list != None:
                for button in self.screens[self.current_screen].button_list:
                    button.draw()

        def on_key_press(self, key, modifiers):
            ''' Called whenever a key is pressed. '''

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
        def on_mouse_press(self, x, y, button, key_modifiers):
            """
            Called when the user presses a mouse button.
            """
            check_mouse_press_for_buttons(x, y, self.screens[self.current_screen].button_list)

        def on_mouse_release(self, x, y, button, key_modifiers):
            """
            Called when a user releases a mouse button.
            """
            check_mouse_release_for_buttons(x, y, self.screens[self.current_screen].button_list)



    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
    #self.physics_engine.update()

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
    window = PlatformerGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
