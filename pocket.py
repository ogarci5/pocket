import sys
import time
import subprocess
import pyautogui
from argparse import ArgumentParser
from sys import exit


def wait_until_loaded(x, y, pixels=[], timeout=None):
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
      
 
def repeat_until_loaded(x1, y1, x2, y2, pixels=[], timeout=None, max_attempts=2, attempts=0):
  pyautogui.moveTo(x1, y1)
  time.sleep(0.3)
  
  pyautogui.click(x1, y1, button='left')
  time.sleep(0.5)
  
  if attempts >= max_attempts:
    match = wait_until_loaded(x2, y2, pixels=pixels)
  else:  
    match = wait_until_loaded(x2, y2, pixels=pixels, timeout=timeout)
  time.sleep(1)
  
  print('Match: %s, Attempts: %s' % (match, attempts))
  
  if match is not None:
    return match
  else:
    print('Repeating again')
    repeat_until_loaded(x1, y1, x2, y2, pixels=pixels, timeout=timeout, attempts=attempts+1)
  

def open_bluestacks():
  print('Opening BlueStacks')
  pyautogui.click(328, 1053, button='left')
  wait_until_loaded(161, 133, pixels=[(51, 58, 97)])
  print('Opened BlueStacks')
  
  
def close_bluestacks():
  print('Closing bluestacks')
  pyautogui.click(1781, 29, button='left')
  time.sleep(2)
  wait_until_loaded()
  

def open_my_apps():
  print('Opening My Apps and starting Pocket Evolution')
  pyautogui.click(207, 84, button='left')
  time.sleep(0.2)
  pyautogui.click(368, 190, button='left')
  # Wait until game opened
  wait_until_loaded(957, 876, pixels=[(228, 100, 74)])
  time.sleep(0.5)
  
  
def start_pocket_evolution():
  print('Starting game')
  pyautogui.click(957, 876, button='left')
  wait_until_loaded(969, 189, pixels=[(237, 192, 153), (134, 210, 246)])

  # Wait an extra 5 seconds for notification to pop up if it's going to
  print('Waiting for notification if necessary')
  time.sleep(5)
  match = wait_until_loaded(969, 189, pixels=[(237, 192, 153), (134, 210, 246)])
  
  if match == 1:
    print('Closing notification')
    pyautogui.click(1523, 172, button='left')
    print('Notification closed, waiting 2 seconds')
    time.sleep(2)
  
  
def open_champions_tower():
  print('Opening Champions Tower')
  repeat_until_loaded(814, 248, 961, 188, pixels=[(246, 102, 32)], timeout=3)
  time.sleep(0.5)
  

def challenge_area(area, buff=False):
  print('Challenging area %s' % area['id'])
  x, y = area['position']
  
  wait_until_loaded(x, y, pixels=[(area['pixel'])], timeout=3)
  
  print('Waiting for challenge')
  repeat_until_loaded(x, y, 1436, 517, pixels=[(233, 104, 76)], timeout=3)
  print('Waiting for hero selection for fight')
  repeat_until_loaded(1436, 517, 1183, 810, pixels=[(233, 103, 75)], timeout=3)
  print('Waiting until fight completion')
  repeat_until_loaded(1183, 810, 1174, 485, pixels=[(3, 224, 17)], timeout=3, max_attempts=15)
  print('Fight completed')
  
  if buff is True:
    print('Getting buff')
    repeat_until_loaded(1174, 485, 970, 279, pixels=[(211, 95, 240)], timeout=3)
    print('Waiting on return to tower')
    repeat_until_loaded(715, 643, 971, 452, pixels=[(98, 99, 102)], timeout=3)
  else:
    print('Waiting on return to tower')
    repeat_until_loaded(1174, 485, 971, 452, pixels=[(98, 99, 102)], timeout=3)
  
  time.sleep(0.5)

  
def play_champions_tower():
  print('Playing Champions Tower')
  print('Check if a reset is needed')
  print('Check if last chest was opened')
  
  last_chest_opened = False
  match = wait_until_loaded(715, 303, pixels=[(74, 51, 26)], timeout=3)
  if match == 1:
    last_chest_opened = True
 
  resetable = False
  match = wait_until_loaded(1391, 832, pixels=[(229, 100, 74)], timeout=3)
  if match == 1:
    resetable = True
 
  if last_chest_opened and resetable:
    print('Reseting tower')
    repeat_until_loaded(1391, 832, 784, 666, pixels=[(233, 104, 76)], timeout=3)
    time.sleep(0.5)
    repeat_until_loaded(784, 666, 971, 452, pixels=[(98, 99, 102)], timeout=3)
    time.sleep(0.5)
    
    areas_pre_buff_1 = [{'id': 1, 'position': (1219, 724), 'pixel': (102, 204, 88)},
                        {'id': 2, 'position': (1079, 715), 'pixel': (102, 214, 88)}]
    area_buff_1 = {'id': 3, 'position': (943, 703), 'pixel': (102, 216, 95)}
    area_chest_1 = {'id': 4, 'position': (812, 674), 'pixel': (102, 208, 89)}
    
    for area in areas_pre_buff_1:
      challenge_area(area)
    challenge_area(area_buff_1, buff=True)
    challenge_area(area_chest_1)
    
    print('Getting chest 1')
    repeat_until_loaded(699, 571, 941, 243, pixels=[(239, 183, 29)], timeout=5)
    repeat_until_loaded(699, 571, 971, 452, pixels=[(98, 99, 102)], timeout=3)
    
    area_pre_buff_2 = {'id': 5, 'position': (853, 523), 'pixel': (102, 213, 91)}
    area_buff_2 = {'id': 6, 'position': (1006, 511), 'pixel': (102, 218, 92)}
    area_chest_2 = {'id': 7, 'position': (1169, 494), 'pixel': (102, 206, 95)}
    
    challenge_area(area_pre_buff_2)
    challenge_area(area_buff_2, buff=True)
    challenge_area(area_chest_2)
    
    print('Getting chest 2')
    repeat_until_loaded(1358, 417, 941, 243, pixels=[(239, 183, 29)], timeout=5)
    repeat_until_loaded(1358, 417, 971, 452, pixels=[(98, 99, 102)], timeout=3)
    
    area_pre_buff_3 = {'id': 8, 'position': (1185, 340), 'pixel': (102, 210, 91)}
    area_buff_3 = {'id': 9, 'position': (1041, 334), 'pixel': (106, 219, 91)}
    area_chest_3 = {'id': 10, 'position': (890, 332), 'pixel': (255, 255, 255)}
    #area_chest_3 = {'id': 10, 'position': (889, 306), 'pixel': (84, 163, 201)}
    
    challenge_area(area_pre_buff_3)
    challenge_area(area_buff_3, buff=True)
    challenge_area(area_chest_3)
    
    print('Getting chest 3')
    repeat_until_loaded(738, 304, 941, 243, pixels=[(239, 183, 29)], timeout=5)
    repeat_until_loaded(738, 304, 971, 452, pixels=[(98, 99, 102)], timeout=3)
    
    print('Champions Tower done')
  else:
    print('Last chest opened: %s, Resetable: %s' % (last_chest_opened, resetable))
    sys.exit()
    
  
def go_to_wonderland():
  print('Going to Wonderland')
  pyautogui.moveTo(228, 500)
  pyautogui.dragRel(1400, 0, 1, button='left')
  pyautogui.moveTo(228, 500)
  pyautogui.dragRel(1000, 0, 0.6, button='left')
  repeat_until_loaded(396, 367, 396, 367, pixels=[(56, 122, 164)], timeout=3)
  time.sleep(0.5)
  
  
def open_exploration():
  print('Opening Exploration')
  pyautogui.moveTo(228, 500)
  pyautogui.dragRel(400, 0, 0.3, button='left')
  pyautogui.moveTo(417, 528)
  time.sleep(0.3)
  repeat_until_loaded(417, 528, 967, 127, pixels=[(243, 102, 26)], timeout=3)
  print('Opened Exploration')
  time.sleep(1)
  

def check_exploration_slot(slot):
  x, y = slot
  pyautogui.click(x, y, button='left')
  
  print('Checking for receving exploration goods normally')
  match = wait_until_loaded(941, 243, pixels=[(239, 183, 29)], timeout=5)
  time.sleep(0.5)
  
  if match is None:
    print('Not normal performing extra checks')
    
    print('Checking if we are in hero selection')
    match = wait_until_loaded(280, 841, pixels=[(229, 99, 74)], timeout=5)
    if match == 1:
      print ('We are in hero selection, skip this hero')
      pyautogui.click(1736, 182, button='left')
      wait_until_loaded(967, 127, pixels=[(244, 102, 23)])
      time.sleep(0.5)
      return
      
    print('Checking if we are resetting exploration time')
    match = wait_until_loaded(1130, 621, pixels=[(233, 104, 76)], timeout=5)
    if match == 1:
      print ('We are resetting this heros time')
      pyautogui.click(1130, 621, button='left')
      wait_until_loaded(941, 243, pixels=[(239, 183, 29)])
      time.sleep(0.3)
      print('Waiting on return to exploration')
      pyautogui.click(1130, 621, button='left')
      wait_until_loaded(967, 127, pixels=[(244, 102, 23)])
      time.sleep(0.3)
      return
  else:
    print('Waiting on return to exploration')
    pyautogui.click(x, y, button='left')
    wait_until_loaded(967, 127, pixels=[(244, 102, 23)])
    time.sleep(0.3)
  
  
def send_on_exploration(slot):
  x, y = slot

  print('Waiting for hero selection')
  repeat_until_loaded(x, y, 280, 841, pixels=[(229, 99, 74)], timeout=3)

  print('Waiting for time selection')
  repeat_until_loaded(280, 841, 719, 670, pixels=[(233, 103, 76)], timeout=3)

  print('Waiting on return to exploration')
  repeat_until_loaded(719, 670, 967, 127, pixels=[(244, 102, 23)], timeout=3)

  
def check_and_send_on_exploration():
  print('Checking slots')
  slots = [(710, 715), 
           (880, 715), 
           (1060, 715), 
           (1230, 715)]
  for slot in slots:
    check_exploration_slot(slot)
    
  print('Sending on exploration')
  number = 1
  for slot in slots:
    print('On Hero %s' % number)
    send_on_exploration(slot)
    number += 1
    
    
def run(args):
  print('Press Ctrl-C to quit.')
  while True:
    if not args.opened:
      open_bluestacks()
      open_my_apps()
      start_pocket_evolution()
    
    if args.tower:
      open_champions_tower()
      while True:
        play_champions_tower()
    
    go_to_wonderland()
    open_exploration()
    
    if args.close:
      check_and_send_on_exploration()
      close_bluestacks()
      time.sleep(3600)
    else:
      while True:
        check_and_send_on_exploration()
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
  args = p.parse_args()

  run(args)
  

if __name__ == "__main__":
    main()