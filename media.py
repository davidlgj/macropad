from rainbowio import colorwheel
import terminalio
from adafruit_display_text import label
from displayio import Group
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode as kc
from adafruit_hid.consumer_control_code import ConsumerControlCode as ccc
from adafruit_hid.consumer_control import ConsumerControl
import usb_hid


def init(display, pixels, keys, encoder, debounced_switch, init_plugin):
    lbl = label.Label(terminalio.FONT, text="Media")
    lbl.scale = 3
    lbl.x = 25
    lbl.y = 25
    display.show(lbl)
    display.refresh()

    consumer_control = ConsumerControl(usb_hid.devices)
    keyboard = Keyboard(usb_hid.devices)

    colorwheel_step = 256/12
    colors_pressed = (
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

    colors = (
        (0,0,0),
        (0, 0,0),
        (0,0,0),

        (0, 0, 0),
        (10,10,10),
        (50,50,50),

        (50, 30, 50),
        (0, 0, 0),
        (30, 0, 0),

        (50,50,10),
        (10,50,50),
        (50,50,10),
    )

    #178 167

    numpad_mapping = (
        # Nothing yet
        0x00, 0x00, 0x00,

        # screen brightness
        0x70 ,0x00, 0x6F,

                        # mute microphone
        ccc.MUTE, 0x00  ,0xB2,
        ccc.SCAN_PREVIOUS_TRACK, ccc.PLAY_PAUSE, ccc.SCAN_NEXT_TRACK
    )

    for index in range(0,12):
        pixels[index] = colors[index]

    pixels.show()

    class MediaControl:
        def __init__(self):
            self.last_encoder = encoder.position

        def update(self):
            key_event = keys.events.get()
            if key_event:
                if key_event.pressed:
                    pixels[key_event.key_number] = colors_pressed[key_event.key_number]
                    consumer_control.send(numpad_mapping[key_event.key_number])
                else:
                    pixels[key_event.key_number] = colors[key_event.key_number]
                pixels.show()

            # Volume on encoder
            pos = encoder.position
            if pos > self.last_encoder:
                for i in range(abs(pos - self.last_encoder)):
                    consumer_control.send(ccc.VOLUME_DECREMENT)
            elif pos < self.last_encoder:
                for i in range(abs(pos - self.last_encoder)):
                    consumer_control.send(ccc.VOLUME_INCREMENT)
            self.last_encoder = pos


            debounced_switch.update()
            if debounced_switch.fell:
                init_plugin("Main")

        def draw(self):
            pass

        def tear_down(self):
            for index in range(0,12):
                pixels[index] = (0,0,0)
            pixels.show()

    return MediaControl()
