"""ST7789V Display plugin for PiDi (Mopidy)."""
import RPi.GPIO as GPIO
from st7789v.interface import RaspberryPi
from st7789v import Display
from pidi_display_pil import DisplayPIL

__version__ = "0.1.0"


class DisplayST7789V(DisplayPIL):
    """PiDi display output plugin for the ST7798V 1.3" 320x240 SPI LCD."""

    option_name = "st7789v"

    def __init__(self, args):
        super().__init__(args)

        # Set GPIO numbering mode
        GPIO.setmode(GPIO.BCM)  # use BCM numbering (GPIO numbers, not pins)

        # Open SPI interface
        self._rpi = RaspberryPi()
        self._rpi.open()

        # Initialize display
        self._st7789v = Display(self._rpi)
        self._st7789v.initialize(90) #rotation=args.rotation or 0)

    def start(self):
        """Called when PiDi starts."""
        # Optionally, turn backlight fully on
        self._st7789v.set_backlight(100)

    def stop(self):
        """Called when PiDi stops."""
        self._st7789v.set_backlight

    def redraw(self):
        """Draw the current Pillow image to the ST7789V."""
        if DisplayPIL.redraw(self):
            # Convert Pillow image to RGB bytes
            data = list(self._output_image.convert("RGB").getdata())
            self._st7789v.draw_rgb_bytes(data)
