from rainbowio import colorwheel
import terminalio
from adafruit_display_text import label
from rainbowio import colorwheel
from displayio import Group, Bitmap, TileGrid, Palette
import board
import math
import time


def init(display, pixels, keys, encoder, debounced_switch, init_plugin):

    # Offset encoder so we are at zero
    encoder_offset = encoder.position
    def encoder_pos():
        return encoder.position - encoder_offset


    class Ball:
        def __init__(self):
            # ball variables
            self.x = 10
            self.y = 32
            self.dx = 0.124
            self.dy = 0.78

            #setup display
            # Create a 1x1 bitmap with two colors
            bitmap = Bitmap(1, 1, 2)
            bitmap[0] = 1
            # Create a two color palette
            palette = Palette(2)
            palette[0] = 0x000000
            palette[1] = 0xffffff

            # Create a TileGrid using the Bitmap and Palette
            tile_grid = TileGrid(bitmap, pixel_shader=palette)

            # Create a Group
            self.ball_group = Group()

            # Add the TileGrid to the Group
            self.ball_group.append(tile_grid)
            self.ball_group.x = self.x
            self.ball_group.y = self.y

            # Pad
            pad_bitmap = Bitmap(12, 2, 2)
            pad_bitmap.fill(1)

            # Create a TileGrid using the Bitmap and Palette
            pad_tile_grid = TileGrid(pad_bitmap, pixel_shader=palette)
            self.pad_group = Group()
            self.pad_group.append(pad_tile_grid)
            self.pad_group.x = 58
            self.pad_group.y = 58

            # Main group of the display
            group = Group()
            group.append(self.ball_group)
            group.append(self.pad_group)
            display.show(group)

        def update(self):
            debounced_switch.update()
            if debounced_switch.fell:
                init_plugin("Main")

            self.pad_group.x = max(min(64 + encoder_pos()*3,115), 0)


        def draw(self):
            # update ball
            self.x += self.dx
            self.y += self.dy

            # Collision with wall
            if self.y <= 0:
                self.y = 0
                self.dy = self.dy * -1
            elif self.y >= 63:
                self.y = 63
                self.dy = self.dy * -1

            if self.x <= 0:
                self.x = 0
                self.dx = self.dx * -1
            elif self.x >= 127:
                self.x = 127
                self.dx = self.dx * -1

            # Collision with pad
            if self.y >= 58 and self.x >= self.pad_group.x and self.x < (self.pad_group.x + 12):
                print("hit!")
                self.dy = self.dy * -1

                # Depending on where on the padel we get some dx action as well!
                offset = self.x - self.pad_group.x
                if offset == 0:
                    self.dx -= 0.5
                    print("lcorner")
                elif offset == 11:
                    self.dx += 0.5
                    print("rcorner")
                elif offset < 4:
                    self.dx -= 0.3
                    print("lside")
                elif offset > 7:
                    self.dx += 0.3
                    print("rside")

                # TODO:
                # tweak so middle lessen x movement so it goes upwards more
                # also set max/min dx
                # math function to get sign of dx would help

            self.ball_group.x = math.floor(self.x)
            self.ball_group.y = math.floor(self.y)
            display.refresh()


        def tear_down(self):
            pass

    return Ball()
