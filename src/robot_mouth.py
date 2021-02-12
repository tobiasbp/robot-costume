import neopixel
import utime
import random
import microbit as mb

# from neomatrix import NeoMatrix

# Configuration variables

# NUmber of LEDs on the strip
LED_STRIP_LENGTH = 24

# Speed of fade (0.0 - 1.0). Higher value, slower fade.
LED_FADE_SPEED = 0.7

# How often to advance the "head" LED
LED_ADVANCE_RATE_HZ = 20

# How often to update/refresh the LED strip
# Tests seem to indicate, a maximum rate of 30 HZ
LED_UPDATE_RATE_HZ = 20

# This pin is high when update pin (Use for bebugging)
LED_UPDATE_RATE_PIN = mb.pin1

# The pin sending the data to the LED strip
LED_STRIP_DATA_PIN = mb.pin0

# Clear display on MB after this many milliseconds
DISPLAY_CLEAR_MS = 1500

# The LED colors
LED_COLORS = ((250, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (0, 0, 0))

# The LED intensity levels
LED_INTENSITIES = (0.1, 0.2, 0.35, 0.5, 1.0)

# Index of currently used color
LED_COLOR_INDEX = 0

# Index of currently used intensity
LED_INTENSITY_INDEX = 2

# The buttons to use
CHANGE_COLOR_BUTTON = mb.button_a
CHANGE_INTENSITY_BUTTON = mb.button_b

###################
# Here be dragons #
###################

# Pause between advancing head LED
LED_ADVANCE_RATE_MS = 1000 / LED_ADVANCE_RATE_HZ

# Pause between refreshes of the LED strip
LED_UPDATE_RATE_MS = 1000 / LED_UPDATE_RATE_HZ

# The LED strip
led_strip = neopixel.NeoPixel(LED_STRIP_DATA_PIN, LED_STRIP_LENGTH)

# make sure all LEDs are off.
led_strip.clear()

# Time stamps
ts_led_advance = 0
ts_led_update = 0
ts_display_on = 0

# Index of current "head" LED
led_index = 0


def calculate_color():
    """ Calculate current color data """
    global LED_COLORS, LED_COLOR_INDEX
    global LED_INTENSITIES, LED_INTENSITY_INDEX
    # Get color to use
    c = LED_COLORS[LED_COLOR_INDEX]
    # Update with intensity
    c = [int(v * LED_INTENSITIES[LED_INTENSITY_INDEX]) for v in c]
    return c


class NeoMatrix:
    """ An LED matrix made up of horizontally arranged panels. """

    def __init__(self, data_pin, panel_width=8, panel_height=8, no_of_panels=1):
        self.width = panel_width * no_of_panels
        self.height = panel_height
        self._pw = panel_width
        self._ph = panel_height
        self._panels = no_of_panels
        self._pixels_pr_panel = self._pw * self._pw
        self._leds = neopixel.NeoPixel(data_pin, self._ph * self._pw * self._panels)

    def _coordinate_to_index(self, x, y):
        """ Translate a coordinate to a pixel index """
        # What panel is the pixel on? (0 indexed)
        panel_no = int(x / self._pw)
        # Calculate led index, as if the pixel was on first panel (0)
        led_index = (x - panel_no * self._pw) + (y * self._pw)
        # Pad the index with number of pixels in a panel
        # return led_index + panel_no * self._pw * self._ph
        return led_index + panel_no * self._pixels_pr_panel

    def fade(self, percent_to_keep=0.8):
        """ Change intensity of all pixels """
        for i in range(self.width * self.height):
            self._leds[i] = [int(v * percent_to_keep) for v in self._leds[i]]

    def set_pixel(self, x, y, v=(0x0F, 0x00, 0x00)):
        """ Set the value of a pixel """
        self._leds[self._coordinate_to_index(x, y)] = v

    def get_pixel(self, x, y):
        """ Get the value of a pixel """
        return self._leds[self._coordinate_to_index(x, y)]

    def scroll_left(self):
        """ Scroll all pixels to the left. Right most column cleared. """
        for x in range(1, self.width):
            for y in range(self.height):
                self.set_pixel(x - 1, y, self.get_pixel(x, y))
        # Clear pixels in right most column
        for y in range(self.height):
            self.clear_pixel(self.width - 1, y)

    def clear_pixel(self, x, y):
        """ Turn off pixel """
        self.set_pixel(x, y, v=(0x00, 0x00, 0x00))

    def show(self):
        """ Push data to the LEDs """
        self._leds.show()

    def clear(self):
        """ Turn all LEDs off """
        self._leds.clear()


# Set up a an LED matrix
matrix = NeoMatrix(LED_STRIP_DATA_PIN, no_of_panels=2)
matrix.clear()
matrix.set_pixel(1, 1)
# matrix.scroll_left()
matrix.show()

# Calculate initial color
led_color = calculate_color()


while True:

    # matrix.set_pixel(15, random.randint(0,7))
    for i in range(matrix.width):
        matrix.set_pixel(random.randint(0, 15), random.randint(0, 7))
        # matrix.scroll_left()
        # matrix.set_pixel(i+1, 4)
        matrix.fade()
        matrix.show()
        # utime.sleep_ms(1000)
        # utime.sleep_ms(10)
    # matrix.clear()

    """
    for x in range(matrix.width):
        for y in range(matrix.height):
            matrix.set_pixel(x + 1, y + 1)
            # matrix.show()
            utime.sleep_ms(1)
            matrix.clear_pixel(x + 1, y + 1)
            # matrix.show()
            utime.sleep_ms(1)

    # matrix.clear()
    # matrix.show()
    utime.sleep_ms(10)
    """
