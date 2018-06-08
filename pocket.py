import sys
import time
import subprocess
import pyautogui
from argparse import ArgumentParser
from sys import exit

START_DIMS = {'x': 125, 'y': 53}
RESOLUTION = {'x': 1687, 'y': 951}

class Pocket(object):
  def __init__(self, args):
    self.args = args
    print(self.args.start_dims)
    if self.args.start_dims:
      self.start_dims = dict(item.split("=") 
                             for item in args.start_dims.split(","))
    else:
      self.start_dims = START_DIMS
      
    if self.args.resolution:
      self.resolution = dict(item.split("=") 
                             for item in args.resolution.split(","))
    else:
      self.resolution = RESOLUTION
      
  def click(self, x, y, button=None):
    pyautogui.click(*self.transform_position(x, y), button=button)

  def moveTo(self, x, y):
    pyautogui.moveTo(*self.transform_position(x, y))
      
  def transform_position(self, x, y):
    new_x = x - (START_DIMS['x'] - int(self.start_dims['x']))
    new_x = round(new_x * (float(self.resolution['x'])/float(RESOLUTION['x'])))
    new_y = y - (START_DIMS['y'] - int(self.start_dims['y']))
    new_y = round(new_y * (float(self.resolution['y'])/float(RESOLUTION['y'])))
    return (new_x, new_y)
    
  def wait_until_loaded(self, x, y, pixels=[], timeout=None):
    x, y = self.transform_position(x, y)
    im = pyautogui.screenshot(region=(x, y, 5, 5))
    count = 0
    current_pixel = im.getpixel((0, 0))
    
    condition = not [p for p in pixels 
                     if ((current_pixel[0] in range(p[0]-10, p[0]+10)) and 
                     (current_pixel[1] in range(p[1]-10, p[1]+10)) and
                     (current_pixel[2] in range(p[2]-10, p[2]+10)))]
    if timeout is not None:
      current_time = time.time()
      condition = condition and time.time() < current_time + timeout 
    
    while condition:
      time.sleep(0.1)
      im = pyautogui.screenshot(region=(x, y, 5, 5))
      current_pixel = im.getpixel((0, 0))
      
      condition = not [p for p in pixels 
                       if ((current_pixel[0] in range(p[0]-10, p[0]+10)) and 
                       (current_pixel[1] in range(p[1]-10, p[1]+10)) and
                       (current_pixel[2] in range(p[2]-10, p[2]+10)))]
      if timeout is not None:
        condition = condition and time.time() < current_time + timeout
        
      count += 1
      if count % 50 == 0:
        print('have waited for %s iterations' % count)
        print('position is: %s,%s' % (x,y))
        print('current_pixel is: %s,%s,%s' % current_pixel)
        number = 1
        for pixel in pixels:
          print('expected %s pixel is: %s,%s,%s' % (number, pixel[0], pixel[1], pixel[2]))
          number += 1
        
      if count > 1200:
        print('Failed after %s attempts' % count)
        sys.exit()
        
    number = 1
    for p in pixels:
      if ((current_pixel[0] in range(p[0]-10, p[0]+10)) and 
          (current_pixel[1] in range(p[1]-10, p[1]+10)) and
          (current_pixel[2] in range(p[2]-10, p[2]+10))):
        return number
      else:
        number += 1      
   
  def repeat_until_loaded(self, x1, y1, x2, y2, pixels=[], timeout=None, max_attempts=2, attempts=0):
    self.moveTo(x1, y1)
    time.sleep(0.3)
    
    self.click(x1, y1, button='left')
    time.sleep(0.5)
    
    if attempts >= max_attempts:
      match = self.wait_until_loaded(x2, y2, pixels=pixels)
    else:  
      match = self.wait_until_loaded(x2, y2, pixels=pixels, timeout=timeout)
    time.sleep(1)
    
    print('Match: %s, Attempts: %s' % (match, attempts))
    
    if match is not None:
      return match
    else:
      print('Repeating again')
      self.repeat_until_loaded(x1, y1, x2, y2, pixels=pixels, timeout=timeout, attempts=attempts+1)

  def open_bluestacks(self):
    print('Opening BlueStacks')
    pyautogui.click(328, 1053, button='left')
    self.wait_until_loaded(161, 133, pixels=[(51, 58, 97)])
    print('Opened BlueStacks')
    
  def close_bluestacks(self):
    print('Closing bluestacks')
    pyautogui.click(1781, 29, button='left')
    time.sleep(2)
    self.wait_until_loaded()

  def open_my_apps(self):
    print('Opening My Apps and starting Pocket Evolution')
    pyautogui.click(207, 84, button='left')
    time.sleep(0.2)
    pyautogui.click(368, 190, button='left')
    # Wait until game opened
    self.wait_until_loaded(957, 876, pixels=[(228, 100, 74)])
    time.sleep(0.5)
    
  def start_pocket_evolution(self):
    print('Starting game')
    pyautogui.click(957, 876, button='left')
    self.wait_until_loaded(969, 189, pixels=[(237, 192, 153), (134, 210, 246)])

    # Wait an extra 5 seconds for notification to pop up if it's going to
    print('Waiting for notification if necessary')
    time.sleep(5)
    match = self.wait_until_loaded(969, 189, pixels=[(237, 192, 153), (134, 210, 246)])
    
    if match == 1:
      print('Closing notification')
      pyautogui.click(1523, 172, button='left')
      print('Notification closed, waiting 2 seconds')
      time.sleep(2)
    
  def open_champions_tower(self):
    print('Opening Champions Tower')
    self.repeat_until_loaded(814, 248, 961, 188, pixels=[(246, 102, 32)], timeout=3)
    time.sleep(0.5)

  def challenge_area(self, area, buff=False):
    print('Challenging area %s' % area['id'])
    x, y = area['position']
    
    self.wait_until_loaded(x, y, pixels=[(area['pixel'])], timeout=3)
    
    print('Waiting for challenge')
    self.repeat_until_loaded(x, y, 1436, 517, pixels=[(233, 104, 76)], timeout=3)
    print('Waiting for hero selection for fight')
    self.repeat_until_loaded(1436, 517, 1183, 810, pixels=[(233, 103, 75)], timeout=3)
    print('Waiting until fight completion')
    self.repeat_until_loaded(1183, 810, 1174, 485, pixels=[(3, 224, 17)], timeout=3, max_attempts=15)
    print('Fight completed')
    
    if buff is True:
      print('Getting buff')
      self.repeat_until_loaded(1174, 485, 970, 279, pixels=[(211, 95, 240)], timeout=3)
      print('Waiting on return to tower')
      self.repeat_until_loaded(715, 643, 971, 452, pixels=[(98, 99, 102)], timeout=3)
    else:
      print('Waiting on return to tower')
      self.repeat_until_loaded(1174, 485, 971, 452, pixels=[(98, 99, 102)], timeout=3)
    
    time.sleep(0.5)
    
  def play_champions_tower(self):
    print('Playing Champions Tower')
    print('Check if a reset is needed')
    print('Check if last chest was opened')
    
    last_chest_opened = False
    match = self.wait_until_loaded(715, 303, pixels=[(74, 51, 26)], timeout=3)
    if match == 1:
      last_chest_opened = True
   
    resetable = False
    match = self.wait_until_loaded(1391, 832, pixels=[(229, 100, 74)], timeout=3)
    if match == 1:
      resetable = True
   
    if last_chest_opened and resetable:
      print('Reseting tower')
      self.repeat_until_loaded(1391, 832, 784, 666, pixels=[(233, 104, 76)], timeout=3)
      time.sleep(0.5)
      self.repeat_until_loaded(784, 666, 971, 452, pixels=[(98, 99, 102)], timeout=3)
      time.sleep(0.5)
      
      areas_pre_buff_1 = [{'id': 1, 'position': (1219, 724), 'pixel': (102, 204, 88)},
                          {'id': 2, 'position': (1079, 715), 'pixel': (102, 214, 88)}]
      area_buff_1 = {'id': 3, 'position': (943, 703), 'pixel': (102, 216, 95)}
      area_chest_1 = {'id': 4, 'position': (812, 674), 'pixel': (102, 208, 89)}
      
      for area in areas_pre_buff_1:
        self.challenge_area(area)
      self.challenge_area(area_buff_1, buff=True)
      self.challenge_area(area_chest_1)
      
      print('Getting chest 1')
      self.repeat_until_loaded(699, 571, 941, 243, pixels=[(239, 183, 29)], timeout=5)
      match = self.repeat_until_loaded(699, 571, 971, 452, pixels=[(98, 99, 102), (231, 223, 208)], timeout=3)
      if match == 2:
        print('Equipment max. Reseting dialog')
        self.repeat_until_loaded(800, 641, 971, 452, pixels=[(98, 99, 102)], timeout=3)
      
      area_pre_buff_2 = {'id': 5, 'position': (853, 523), 'pixel': (102, 213, 91)}
      area_buff_2 = {'id': 6, 'position': (1006, 511), 'pixel': (102, 218, 92)}
      area_chest_2 = {'id': 7, 'position': (1169, 494), 'pixel': (102, 206, 95)}
      
      self.challenge_area(area_pre_buff_2)
      self.challenge_area(area_buff_2, buff=True)
      self.challenge_area(area_chest_2)
      
      print('Getting chest 2')
      self.repeat_until_loaded(1358, 417, 941, 243, pixels=[(239, 183, 29)], timeout=5)
      match = self.repeat_until_loaded(1358, 417, 971, 452, pixels=[(98, 99, 102), (231, 223, 208)], timeout=3)
      if match == 2:
        print('Equipment max. Reseting dialog')
        self.repeat_until_loaded(800, 641, 971, 452, pixels=[(98, 99, 102)], timeout=3)
      
      area_pre_buff_3 = {'id': 8, 'position': (1185, 340), 'pixel': (102, 210, 91)}
      area_buff_3 = {'id': 9, 'position': (1041, 334), 'pixel': (106, 219, 91)}
      area_chest_3 = {'id': 10, 'position': (890, 332), 'pixel': (255, 255, 255)}
      #area_chest_3 = {'id': 10, 'position': (889, 306), 'pixel': (84, 163, 201)}
      
      self.challenge_area(area_pre_buff_3)
      self.challenge_area(area_buff_3, buff=True)
      self.challenge_area(area_chest_3)
      
      print('Getting chest 3')
      self.repeat_until_loaded(738, 304, 941, 243, pixels=[(239, 183, 29)], timeout=5)
      match = self.repeat_until_loaded(738, 304, 971, 452, pixels=[(98, 99, 102), (231, 223, 208)], timeout=3)
      if match == 2:
        print('Equipment max. Reseting dialog')
        self.repeat_until_loaded(800, 641, 971, 452, pixels=[(98, 99, 102)], timeout=3)
      
      print('Champions Tower done')
    else:
      print('Last chest opened: %s, Resetable: %s' % (last_chest_opened, resetable))
      sys.exit()   
    
  def go_to_wonderland(self):
    print('Going to Wonderland')
    self.moveTo(228, 500)
    pyautogui.dragRel(self.transform_position(1400,0)[0], 0, 1, button='left')
    self.moveTo(228, 500)
    pyautogui.dragRel(self.transform_position(1000,0)[0], 0, 0.6, button='left')
    self.repeat_until_loaded(396, 367, 396, 367, pixels=[(56, 122, 164)], timeout=3)
    time.sleep(0.5)
    
  def open_exploration(self):
    print('Opening Exploration')
    self.moveTo(228, 500)
    pyautogui.dragRel(self.transform_position(400,0)[0], 0, 0.3, button='left')
    self.moveTo(417, 528)
    time.sleep(0.3)
    self.repeat_until_loaded(417, 528, 967, 127, pixels=[(243, 102, 26)], timeout=3)
    print('Opened Exploration')
    time.sleep(1)

  def check_exploration_slot(self, slot):
    x, y = slot
    self.click(x, y, button='left')
    
    print('Checking for receving exploration goods normally')
    match = self.wait_until_loaded(941, 243, pixels=[(239, 183, 29)], timeout=5)
    time.sleep(0.5)
    
    if match is None:
      print('Not normal performing extra checks')
      
      print('Checking if we are in hero selection')
      match = self.wait_until_loaded(280, 841, pixels=[(229, 99, 74)], timeout=5)
      if match == 1:
        print ('We are in hero selection, skip this hero')
        self.click(1736, 182, button='left')
        self.wait_until_loaded(967, 127, pixels=[(244, 102, 23)])
        time.sleep(0.5)
        return
        
      print('Checking if we are resetting exploration time')
      match = self.wait_until_loaded(1130, 621, pixels=[(233, 104, 76)], timeout=5)
      if match == 1:
        print ('We are resetting this heros time')
        self.click(1130, 621, button='left')
        self.wait_until_loaded(941, 243, pixels=[(239, 183, 29)])
        time.sleep(0.3)
        print('Waiting on return to exploration')
        self.click(1130, 621, button='left')
        self.wait_until_loaded(967, 127, pixels=[(244, 102, 23)])
        time.sleep(0.3)
        return
    else:
      print('Waiting on return to exploration')
      self.click(x, y, button='left')
      self.wait_until_loaded(967, 127, pixels=[(244, 102, 23)])
      time.sleep(0.3)
    
  def send_on_exploration(self, slot):
    x, y = slot

    print('Waiting for hero selection')
    self.repeat_until_loaded(x, y, 280, 841, pixels=[(229, 99, 74)], timeout=3)

    print('Waiting for time selection')
    self.repeat_until_loaded(280, 841, 719, 670, pixels=[(233, 103, 76)], timeout=3)

    print('Waiting on return to exploration')
    self.repeat_until_loaded(719, 670, 967, 127, pixels=[(244, 102, 23)], timeout=3)
    
  def check_and_send_on_exploration(self):
    print('Checking slots')
    slots = [(710, 715), 
             (880, 715), 
             (1060, 715), 
             (1230, 715)]
    for slot in slots:
      self.check_exploration_slot(slot)
      
    print('Sending on exploration')
    number = 1
    for slot in slots:
      print('On Hero %s' % number)
      self.send_on_exploration(slot)
      number += 1
      
  def run(self):
    print('Press Ctrl-C to quit.')
    while True:
      if not self.args.opened:
        self.open_bluestacks()
        self.open_my_apps()
        self.start_pocket_evolution()
      
      if self.args.tower:
        self.open_champions_tower()
        while True:
          self.play_champions_tower()
      
      self.go_to_wonderland()
      self.open_exploration()
      
      if self.args.close:
        self.check_and_send_on_exploration()
        self.close_bluestacks()
        time.sleep(3600)
      else:
        while True:
          self.check_and_send_on_exploration()
          print('Done with exploration, waiting one hour')
          time.sleep(3600)
  
def main():
  desc = 'Pocket Bro! The Happening is now'
  p = ArgumentParser(description=desc)
  p.add_argument('--close', help=('closes BlueStacks on finish'),
                 action='store_true')
  p.add_argument('--tower', help=('Plays Champions Tower'),
                 action='store_true')
  p.add_argument('--opened', help=('Do not try to open BlueStacks'),
                 action='store_true')
  p.add_argument('--start_dims', help=('Starting dimensions, format x=1,y=2,'
                                      'defaults to 125, 53'), type=str)
  p.add_argument('--resolution', help=('Resolution of BlueStacks, format x=1,y=2,'
                                      'defaults to 1687, 951'), type=str)                                          
  args = p.parse_args()
  pocket = Pocket(args)
  pocket.run()
  

if __name__ == "__main__":
    main()