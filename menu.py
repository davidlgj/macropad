from displayio import Group
import terminalio
from adafruit_display_text import label
import math

menu_items = ("Numpad", "Media", "Ball",)


class Menu:
    def __init__(self, items):
        self.group = Group()
        self.items = items

        for txt in items:
            lbl = label.Label(terminalio.FONT, text=txt)
            self.group.append(lbl)
        self.select(0)

    def select(self,selected):
        self.selected = max(0,min(selected, len(self.items) - 1))

        # Hide all to begin with, so everything outside is kept hidden
        for lbl in self.group:
            lbl.hidden = True

        # Setup placement of one

        def setup(index, y, scale):
            if index < 0 or index >= len(self.items):
                return

            lbl = self.group[index]
            txt = self.items[index]
            lbl.scale = scale
            lbl.x = int(70 - (len(txt)/2) * 6 * lbl.scale)
            lbl.y = y
            lbl.hidden = False

        # Always 7 max, 3 above, on in middle and 3 below
        start_index = self.selected-3
        setup(start_index, -4, 1)
        setup(start_index+1, 6, 1)
        setup(start_index+2, 16, 1)

        setup(start_index+3, 28, 2)

        setup(start_index+4, 46, 1)
        setup(start_index+5, 56, 1)
        setup(start_index+6, 66, 1)


    def next(self):
        self.select(self.selected + 1)

    def prev(self):
        self.select(self.selected - 1)

    @property
    def selected_item(self):
        return self.items[self.selected]


def init(display, pixels, keys, encoder, debounced_switch, init_plugin):
    # Offset encoder so we are at zero
    encoder_offset = encoder.position
    def encoder_pos():
        return encoder.position - encoder_offset

    class MainMenu:
        def __init__(self):
            self.menu = Menu(menu_items)
            display.show(self.menu.group)
            display.refresh()
            self.last_encoder = encoder_pos()

        def update(self):
            pos = encoder_pos()
            if self.last_encoder != pos:
                self.menu.select(pos)
                self.last_encoder = pos
                display.refresh()

            debounced_switch.update()
            if debounced_switch.fell:
                init_plugin(self.menu.selected_item)

        def draw(self):
            display.refresh()

        def tear_down(self):
            pass

    return MainMenu()
