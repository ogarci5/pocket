im = pyautogui.screenshot(region=(161, 133, 5, 5))
count = 0
while im.getpixel((0, 0)) != (51, 58, 91, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(161, 133, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
  


# Open My Apps
print('Opening My Apps and starting Pocket Evolution')
pyautogui.click(207, 84, button='left')
time.sleep(0.2)
pyautogui.click(368, 190, button='left')

# Wait until game opened
im = pyautogui.screenshot(region=(957, 876, 5, 5))
count = 0
while im.getpixel((0, 0)) != (228, 98, 74, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(957, 876, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()

# Starting Pocket Evolution
print('Starting game')
pyautogui.click(957, 876, button='left')

# Wait until logged in
im = pyautogui.screenshot(region=(969, 189, 5, 5))
count = 0
pixel = im.getpixel((0, 0))
while pixel != (237, 192, 153, 255) or pixel != (142, 216, 248, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(969, 189, 5, 5))
  pixel = im.getpixel((0, 0))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()

# Wait an extra 5 seconds for notification to pop up if it's going to
print('Waiting for notification if necessary')
time.sleep(5)    
im = pyautogui.screenshot(region=(969, 189, 5, 5))
count = 0
pixel = im.getpixel((0, 0))
while pixel != (237, 192, 153, 255) or pixel != (142, 216, 248, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(969, 189, 5, 5))
  pixel = im.getpixel((0, 0))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    
# If the notification is open, close items
if pixel == (237, 192, 153, 255):
  print('Closing notification')
  pyautogui.click(1523, 172, button='left')
  print('Notification closed, waiting 2 seconds')
  time.sleep(2)
  
# Going to wonderland
print('Going to Wonderland')
pyautogui.moveTo(228, 500)
pyautogui.dragRel(1400, 0, 1, button='left')
pyautogui.moveTo(228, 500)
pyautogui.dragRel(1000, 0, 0.6, button='left')
pyautogui.click(396, 367, button='left')

# Opening Exploration
print('Opening Exploration')
pyautogui.moveTo(228, 500)
pyautogui.dragRel(400, 0, 0.3, button='left')
pyautogui.click(417, 528, button='left')

im = pyautogui.screenshot(region=(967, 127, 5, 5))
count = 0
while im.getpixel((0, 0)) != ((244, 102, 23, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(967, 127, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    
print('Opened Exploration')

# Checking slots
print('Checking slots')
710, 715
pyautogui.click(710, 715, button='left')
time.sleep(0.3)
pyautogui.click(710, 715, button='left')
time.sleep(0.3)

pyautogui.click(880, 715, button='left')
time.sleep(0.3)
pyautogui.click(880, 715, button='left')
time.sleep(0.3)

pyautogui.click(1060, 715, button='left')
time.sleep(0.3)
pyautogui.click(1060, 715, button='left')
time.sleep(0.3)

pyautogui.click(1230, 715, button='left')
time.sleep(0.3)
pyautogui.click(1230, 715, button='left')
time.sleep(0.3)

# Sending on exploration
print('Sending on exploration')
print('On Hero 1')
pyautogui.click(710, 715, button='left')
time.sleep(0.3)

print('Waiting for hero selection')
im = pyautogui.screenshot(region=(280, 841, 5, 5))
count = 0
while im.getpixel((0, 0)) != (229, 99, 74, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(280, 841, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    
pyautogui.click(280, 841, button='left')

print('Waiting for time selection')
im = pyautogui.screenshot(region=(719, 670, 5, 5))
count = 0
while im.getpixel((0, 0)) != (233, 103, 76, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(719, 670, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    

pyautogui.click(719, 670, button='left')
time.sleep(1)

print('On Hero 2')
pyautogui.click(880, 715, button='left')
time.sleep(0.3)
print('Waiting for hero selection')
im = pyautogui.screenshot(region=(280, 841, 5, 5))
count = 0
while im.getpixel((0, 0)) != (229, 99, 74, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(280, 841, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    
pyautogui.click(280, 841, button='left')

print('Waiting for time selection')
im = pyautogui.screenshot(region=(719, 670, 5, 5))
count = 0
while im.getpixel((0, 0)) != (233, 103, 76, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(719, 670, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    
pyautogui.click(719, 670, button='left')
time.sleep(1)

print('On Hero 3')
pyautogui.click(1060, 715, button='left')
time.sleep(0.3)
print('Waiting for hero selection')
im = pyautogui.screenshot(region=(280, 841, 5, 5))
count = 0
while im.getpixel((0, 0)) != (229, 99, 74, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(280, 841, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    
pyautogui.click(280, 841, button='left')

print('Waiting for time selection')
im = pyautogui.screenshot(region=(719, 670, 5, 5))
count = 0
while im.getpixel((0, 0)) != (233, 103, 76, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(719, 670, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    
pyautogui.click(719, 670, button='left')
time.sleep(1)

print('On Hero 4')
pyautogui.click(1230, 715, button='left')
time.sleep(0.3)
print('Waiting for hero selection')
im = pyautogui.screenshot(region=(280, 841, 5, 5))
count = 0
while im.getpixel((0, 0)) != (229, 99, 74, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(280, 841, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    
pyautogui.click(280, 841, button='left')

print('Waiting for time selection')
im = pyautogui.screenshot(region=(719, 670, 5, 5))
count = 0
while im.getpixel((0, 0)) != (233, 103, 76, 255):
  time.sleep(0.1)
  im = pyautogui.screenshot(region=(719, 670, 5, 5))
  count = count + 1
  if count > 1200:
    print('Failed after %s attempts' % count)
    sys.exit()
    
pyautogui.click(719, 670, button='left')
time.sleep(1)

print('Appeared to be done closing and restarting in an hour')
pyautogui.click(1781, 29, button='left')
time.sleep(3630)