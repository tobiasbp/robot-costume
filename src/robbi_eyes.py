import neopixel, utime
import microbit as mb

# Configuration variables
LED_STRIP_LENGTH = 24

# Speed of advancing LED
LED_ADVANCE_RATE_MS = 1000 / 20  # 1000/HZ

# Speed of fade (0.0 - 1.0). Higher value, slower fade.
LED_FADE_SPEED = 0.6

# How often to fade (refresh) the LED strip
LED_FADE_RATE_MS = 1000 / 20  # 1000/HZ

# The pin sending the data to the LED strip
LED_STRIP_PIN = mb.pin0

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

# The LED strip
led_strip = neopixel.NeoPixel(LED_STRIP_PIN, LED_STRIP_LENGTH)

# make sure all LEDs are off.
led_strip.clear()

# Time stamps
ts_led_advance = 0
ts_led_fade = 0
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

# Calculate initial color
led_color = calculate_color()

while True:

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
    if utime.ticks_diff(utime.ticks_ms(), ts_led_fade) > LED_FADE_RATE_MS:
        ts_led_fade = utime.ticks_ms()
        for i in range(LED_STRIP_LENGTH):
            led_strip[i] = [int(v * LED_FADE_SPEED) for v in led_strip[i]]
        led_strip.show()

    # Clear display after time out
    if utime.ticks_diff(utime.ticks_ms(), ts_display_on) > DISPLAY_CLEAR_MS:
        mb.display.clear()
