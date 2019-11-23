"""The module contains templates for colour cycles"""
import time
from driver import apa102
import threading


class ColorCycleTemplate:
    """This class is the basis of all color cycles.
    This file is usually used "as is" and not being changed.

    A specific color cycle must subclass this template, and implement at least the
    'update' method.
    """

    def __init__(self, num_led, pause_value=0, num_steps_per_cycle=100,
                 num_cycles=-1, global_brightness=255, order='rbg',
                 color = 'ffffff', end_time = -1, mosi=10, sclk=11):
        self.num_led = num_led  # The number of LEDs in the strip
        self.pause_value = pause_value  # How long to pause between two runs
        self.num_steps_per_cycle = num_steps_per_cycle  # Steps in one cycle.
        self.num_cycles = num_cycles  # How many times will the program run
        self.global_brightness = global_brightness  # Brightness of the strip
        self.order = order  # Strip colour ordering
        self.color = color # The color to display on the strip.
        self.end_time = end_time # The amount of time to dispaly the effect.
        self.mosi = mosi  # Master out slave in of the SPI protocol
        self.sclk = sclk  # Clock line of the SPI protocol
        self.running = threading.Event() # Thread safe way to stop the loop.
        self.do_cleanup = True # If the color cycle should do a full cleanup.

    def init(self, strip, num_led):
        """This method is called to initialize a color program.

        The default does nothing. A particular subclass could setup
        variables, or even light the strip in an initial color.
        """
        pass

    def shutdown(self, strip, num_led):
        """This method is called before exiting.

        The default does nothing
        """
        pass

    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
        """This method paints one subcycle. It must be implemented.

        current_step:  This goes from zero to numStepsPerCycle-1, and then
          back to zero. It is up to the subclass to define what is done in
          one cycle. One cycle could be one pass through the rainbow.
          Or it could be one pixel wandering through the entire strip
          (so for this case, the numStepsPerCycle should be equal to numLEDs).
        current_cycle: Starts with zero, and goes up by one whenever a full
          cycle has completed.
        """

        raise NotImplementedError("Please implement the update() method")

    def cleanup(self, strip):
        """Cleanup method."""
        if(self.do_cleanup):
            self.shutdown(strip, self.num_led)
            strip.clear_strip()
        strip.cleanup()

    def terminate(self, do_cleanup):
        """Method for ending the effect."""
        self.do_cleanup = do_cleanup
        self.running.clear()

    def start(self):
        """This method does the actual work."""
        strip = None
        try:
            self.running.set()
            strip = apa102.APA102(num_led=self.num_led,
                                  global_brightness=self.global_brightness,
                                  mosi=self.mosi, sclk=self.sclk,
                                  order=self.order)  # Initialize the strip
            strip.clear_strip()
            self.init(strip, self.num_led)  # Call the subclasses init method
            strip.show()
            current_cycle = 0
            # Loop while the thread event is set
            while(self.running.is_set()):
                for current_step in range(self.num_steps_per_cycle):
                    need_repaint = self.update(strip, self.num_led,
                                               self.num_steps_per_cycle,
                                               current_step, current_cycle)
                    if need_repaint:
                        strip.show()  # repaint if required
                    if(not self.running.is_set()): break
                    if self.end_time != -1 and self.end_time < time.time():
                        self.terminate(True)
                    time.sleep(self.pause_value)  # Pause until the next step
                current_cycle += 1
                if self.num_cycles != -1:
                    if current_cycle >= self.num_cycles:
                        break
            # Finished, cleanup everything
            self.cleanup(strip)

        except KeyboardInterrupt:  # Ctrl-C can halt the light program
            print('Interrupted...')
            if self.cleanup is not None:
                self.cleanup(strip)
