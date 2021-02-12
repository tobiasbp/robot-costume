import neopixel, utime
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
        self._leds = neopixel.NeoPixel(data_pin, self._ph * self._pw * self._panels)

    def set_pixel(self, x, y, v=(0x0F, 0x00, 0x00)):
        """ Set the value of a pixel """
        # What panel is the pixel on? (0 indexed)
        panel_no = int((x - 1) / self._pw)
        # Calculate led index, as if the pixel was on first panel (0)
        led_index = (x - 1 - panel_no * self._pw) + ((y - 1) * self._pw)
        # Update value of LED
        self._leds[led_index + panel_no * self._pw * self._ph] = v

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
# matrix.set_pixel(16,8)
matrix.show()

# Calculate initial color
led_color = calculate_color()


while True:
    pass

    for x in range(matrix.width):
        for y in range(matrix.height):
            matrix.set_pixel(x + 1, y + 1)
            matrix.show()
            utime.sleep_ms(1)
            matrix.clear_pixel(x + 1, y + 1)
            matrix.show()
            utime.sleep_ms(1)

    matrix.clear()
    matrix.show()
    utime.sleep_ms(10)

    """
    # Change LED color
    if CHANGE_COLOR_BUTTON.was_pressed():
        if LED_COLOR_INDEX == len(LED_COLORS) - 1:
            LED_COLOR_INDEX = 0
        else:
            LED_COLOR_INDEX += 1
        led_color = calculate_color()
        # Display color number
        mb.display.show(LED_COLOR_INDEX + 1)
        ts_display_on = utime.ticks_ms()
        led_strip.clear()

    # Change overall LED intensity
    if CHANGE_INTENSITY_BUTTON.was_pressed():
        if LED_INTENSITY_INDEX == len(LED_INTENSITIES) - 1:
            LED_INTENSITY_INDEX = 0
        else:
            LED_INTENSITY_INDEX += 1
        led_color = calculate_color()
        # Display intensity index
        mb.display.show(LED_INTENSITY_INDEX + 1)
        ts_display_on = utime.ticks_ms()
        led_strip.clear()

    # Advance to next LED
    if utime.ticks_diff(utime.ticks_ms(), ts_led_advance) > LED_ADVANCE_RATE_MS:
        ts_led_advance = utime.ticks_ms()
        # Update LED
        led_strip[led_index] = led_color
        # Calculate index of next LED
        if led_index == LED_STRIP_LENGTH - 1:
            led_index = 0
        else:
            led_index += 1

    # Lower intensity of all LEDs and write data to strip
    if utime.ticks_diff(utime.ticks_ms(), ts_led_update) > LED_UPDATE_RATE_MS:
        LED_UPDATE_RATE_PIN.write_digital(1)
        ts_led_update = utime.ticks_ms()
        for i in range(LED_STRIP_LENGTH):
            led_strip[i] = [int(v * LED_FADE_SPEED) for v in led_strip[i]]
        led_strip.show()
        LED_UPDATE_RATE_PIN.write_digital(0)

    # Clear display after time out
    if utime.ticks_diff(utime.ticks_ms(), ts_display_on) > DISPLAY_CLEAR_MS:
        mb.display.clear()
    """
