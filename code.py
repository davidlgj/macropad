import neopixel
import board
import time
from rainbowio import colorwheel
import gc
import keypad
from displayio import Group, Bitmap, TileGrid, Palette
import terminalio
from adafruit_display_text import label
from adafruit_debouncer import Debouncer
import rotaryio
import digitalio
import menu

# Setup display
display = board.DISPLAY
# Let plugins steer refreshing
display.auto_refresh = False

# Setup key scanning
keys = keypad.Keys([getattr(board, "KEY%d" % (num + 1)) for num in range(12)], value_when_pressed=False, pull=True)

# Define rotary encoder and encoder switch:
encoder = rotaryio.IncrementalEncoder(board.ROTA, board.ROTB)
encoder_switch = digitalio.DigitalInOut(board.BUTTON)
encoder_switch.switch_to_input(pull=digitalio.Pull.UP)
debounced_switch = Debouncer(encoder_switch)

# Neopixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 12, auto_write=False)
pixels.brightness = 0.3

offset = 0
last_encoder = encoder.position
last_time = time.monotonic()
current_time = last_time

plugin = None

# Function to load "plugin", i.e. the next code to run
def init_plugin(name):
    global plugin
    print(f"Loading module {name}")
    print(gc.mem_free())
    if plugin != None:
        plugin.tear_down()
    plugin = None
    display.show(Group())
    display.refresh()
    gc.collect()
    print(gc.mem_free())

    if name == "Main":
        plugin = menu.init(display, pixels, keys, encoder, debounced_switch, init_plugin)
    if name == "Numpad":
        import numpad
        plugin = numpad.init(display, pixels, keys, encoder, debounced_switch, init_plugin)
    if name == "Ball":
        import ball
        plugin = ball.init(display, pixels, keys, encoder, debounced_switch, init_plugin)

# Start up with main menu
init_plugin("Main")

# Main loop
while True:
    current_time = time.monotonic()

    # Update plugins
    if plugin != None:
        # Update is called as many times as possible
        plugin.update()

        # Draw we try to call 60fps
        if current_time - last_time >= 0.0166:
            plugin.draw()
            last_time = current_time






