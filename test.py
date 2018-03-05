import pyautogui


def test_pixel():
  pos = pyautogui.position()
  x, y = pos
  im = pyautogui.screenshot(region=(x, y, 5, 5))
  pixel = im.getpixel((0,0))
  r, g, b = pixel
  print('Current Position: (%s, %s)' % (x, y))
  print('Current Pixel: (%s, %s, %s)' % (r, g, b))

  
