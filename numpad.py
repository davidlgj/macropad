from rainbowio import colorwheel
import terminalio
from adafruit_display_text import label
from displayio import Group
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode as kc
import usb_hid




def init(display, pixels, keys, encoder, debounced_switch, init_plugin):
    lbl = label.Label(terminalio.FONT, text="Numpad")
    lbl.scale = 3
    lbl.x = 10
    lbl.y = 25
    display.show(lbl)
    display.refresh()

    keyboard = Keyboard(usb_hid.devices)

    colorwheel_step = 256/12
    colors = (
        colorwheel(0),
        colorwheel(1*colorwheel_step),
        colorwheel(2*colorwheel_step),
        colorwheel(3*colorwheel_step),
        colorwheel(4*colorwheel_step),
        colorwheel(5*colorwheel_step),
        colorwheel(6*colorwheel_step),
        colorwheel(7*colorwheel_step),
        colorwheel(8*colorwheel_step),
        colorwheel(9*colorwheel_step),
        colorwheel(10*colorwheel_step),
        colorwheel(11*colorwheel_step),
    )

    numpad_mapping = (
        kc.KEYPAD_SEVEN,kc.KEYPAD_EIGHT,kc.KEYPAD_NINE,
        kc.KEYPAD_FOUR ,kc.KEYPAD_FIVE ,kc.KEYPAD_SIX,

        kc.KEYPAD_ONE, kc.KEYPAD_TWO  ,kc.KEYPAD_THREE,
        kc.KEYPAD_ZERO, kc.KEYPAD_FORWARD_SLASH, kc.KEYPAD_ENTER
    )

    for index in range(0,10):
        pixels[index] = (10,10,10)
    pixels[10] = (0,10,0)
    pixels[11] = (10,0,10)

    pixels.show()

    class Numpad:
        def update(self):
            key_event = keys.events.get()
            if key_event:
                if key_event.pressed:
                    pixels[key_event.key_number] = colors[key_event.key_number]
                    keyboard.send(numpad_mapping[key_event.key_number])
                else:
                    pixels[key_event.key_number] = (10,10,10)
                    if key_event.key_number == 10:
                        pixels[10] = (0,10,0)
                    elif key_event.key_number == 11:
                        pixels[11] = (10,0,10)
                pixels.show()

            debounced_switch.update()
            if debounced_switch.fell:
                init_plugin("Main")

        def draw(self):
            pass

        def tear_down(self):
            for index in range(0,12):
                pixels[index] = (0,0,0)
            pixels.show()

    return Numpad()
