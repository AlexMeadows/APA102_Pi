import colorschemes
import threading
import time

class server(threading.Thread):

   # define the function blocks
   def strandTest(self, thread_ID, cycles, end_time, num_LEDs,
                  brightness, strip_color, pause_time = 0.04):
      self.my_cycle = colorschemes.StrandTest(
                     num_led = num_LEDs,
                     pause_value = pause_time,
                     num_steps_per_cycle = num_LEDs,
                     num_cycles = cycles,
                     end_time = end_time,
                     global_brightness = brightness,
                     order='rgb')
      self.my_cycle.start()

   def chase(self, thread_ID, cycles, end_time, num_LEDs,
             brightness, strip_color, pause_time = 0.04):
      self.my_cycle = colorschemes.TheaterChase(
                     num_led = num_LEDs,
                     pause_value = pause_time,
                     num_steps_per_cycle = 35,
                     num_cycles = cycles,
                     end_time = end_time,
                     global_brightness = brightness,
                     order='rgb')
      self.my_cycle.start()

   def roundAndRound(self, thread_ID, cycles, end_time, num_LEDs,
                     brightness, strip_color, pause_time = 0.1):
      self.my_cycle = colorschemes.RoundAndRound(
                     num_led = num_LEDs,
                     pause_value = pause_time,
                     num_steps_per_cycle = num_LEDs,
                     num_cycles = cycles,
                     end_time = end_time,
                     global_brightness = brightness,
                     order='rgb')
      self.my_cycle.start()

   def solid(self, thread_ID, cycles, end_time, num_LEDs,
             brightness, strip_color, pause_time = 1):
      self.my_cycle = colorschemes.Solid(
                     num_led = num_LEDs,
                     pause_value = pause_time,
                     num_steps_per_cycle = 1,
                     num_cycles = cycles,
                     end_time = end_time,
                     global_brightness = brightness,
                     order='rgb',
                     color = strip_color)
      self.my_cycle.start()

   def strobe(self, thread_ID, cycles, end_time, num_LEDs,
              brightness, strip_color, pause_time = 0.05):
      self.my_cycle = colorschemes.Strobe(
                     num_led = num_LEDs,
                     pause_value = pause_time,
                     num_steps_per_cycle = 4,
                     num_cycles = cycles,
                     end_time = end_time,
                     global_brightness = brightness,
                     order='rgb',
                     color = strip_color)
      self.my_cycle.start()

   def fade(self, thread_ID, cycles, end_time, num_LEDs,
            brightness, strip_color, pause_time = 0.028):
      self.my_cycle = colorschemes.Fade(
                     num_led = num_LEDs,
                     pause_value = pause_time,
                     num_steps_per_cycle = 200,
                     num_cycles = cycles,
                     end_time = end_time,
                     global_brightness = brightness,
                     order='rgb',
                     color = strip_color)
      self.my_cycle.start()

   def rainbow(self, thread_ID, cycles, end_time, num_LEDs,
               brightness, strip_color, pause_time = 0.005):
      self.my_cycle = colorschemes.Rainbow(
                     num_led = num_LEDs,
                     pause_value = pause_time,
                     num_steps_per_cycle = 255,
                     num_cycles = cycles,
                     end_time = end_time,
                     global_brightness = brightness,
                     order='rgb')
      self.my_cycle.start()

   def __init__(self, thread_ID, effect,
                brightness = 15,
                cycles = 999999,
                strip_color = "ffffff",
                pause_time = -1,
                run_time = -1,
                num_LEDs = 160):
      threading.Thread.__init__(self)


      self.brightness = brightness
      self.cycles = cycles
      self.effect = effect
      self.num_LEDs = num_LEDs
      self.my_cycle = 1
      self.pause_time = pause_time
      self.strip_color = strip_color
      self.thread_ID = thread_ID

      if(str(run_time) != "-1.0"):
         self.end_time = int(time.time()) + (float(run_time)*60)
      else:
         self.end_time = -1

      # map the inputs to the function blocks
      self.effects = {
                     "strandTest"    : self.strandTest,
                     "chase"         : self.chase,
                     "roundAndRound" : self.roundAndRound,
                     "solid"         : self.solid,
                     "strobe"        : self.strobe,
                     "fade"          : self.fade,
                     "rainbow"       : self.rainbow,
                     }

   def run(self):
      if(self.pause_time != -1):
         self.effects[self.effect](
               self.thread_ID,
               self.cycles,
               self.end_time,
               self.num_LEDs,
               self.brightness,
               self.strip_color,
               self.pause_time)
      else:
         self.effects[self.effect](
               self.thread_ID,
               self.cycles,
               self.end_time,
               self.num_LEDs,
               self.brightness,
               self.strip_color)

   def terminate(self, do_cleanup = True):
      self.my_cycle.terminate(do_cleanup)
