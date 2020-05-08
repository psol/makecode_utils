"""
 compile a sprite/image in the format that MakeCode Arcade expects
"""

import os
import sys
import math
try:  # import as appropriate for 2.x vs. 3.x
  import tkinter
except:
  import Tkinter as tkinter

def rgb(colour):
  red = (colour & 0xff0000) >> 16
  green = (colour & 0x00ff00) >> 8
  blue = colour & 0x0000ff
  return (red, green, blue)

def cname(fname):
  name, ext = os.path.splitext(os.path.basename(fname))
  return name

def args():
  overwrite = False
  help = False
  js_fname = 'sprite.js'

  try:
    last_input = sys.argv.index('-o')
    if len(sys.argv) < last_input + 2:
      help = True
    else:
      js_fname = sys.argv[last_input + 1]
  except ValueError:
    try:
      last_input = sys.argv.index('-O')
      overwrite = True
      if len(sys.argv) >= last_input + 2:
        js_fname = sys.argv[last_input + 1]
    except ValueError:
      last_input = len(sys.argv)
  path, ext = os.path.splitext(js_fname)
  if ext != '.js':
    help = True

  if help or last_input == 1:
    print('usage: python symbols.py <image>... [-o|-O [<javascript>]]')
    print('  <image> list of bitmap files in a format known to Tkinter')
    print('  options:')
    print('    -o <javascript>   specify .js file name')
    print('    -O [<javascript>] overwrites existing .js file')
    sys.exit(2)

  if not overwrite and os.path.exists(js_fname):
    print('error: "{}" already exists, use -O option to overwrite'.format(js_fname))
    sys.exit(3)

  input = []
  for i in range(1, last_input):
    if not os.path.exists(sys.argv[i]) or not os.path.isfile(sys.argv[i]):
      print('error: "{}"" not found or not a file'.format(sys.argv[i]))
      sys.exit(4)
    input.append(sys.argv[i])

  return ( input, js_fname )

def image(fname):
  try:
    return tkinter.PhotoImage(file=fname)
  except tkinter.TclError as error:
    print('error: {}'.format(error))
    path, ext = os.path.splitext(fname)
    if ext.lower() == '.png':
      print('PNG files may not be supported by this version of TK')
    sys.exit(5)

def distance(c1, c2):
  r1, g1, b1 = c1
  r2, g2, b2 = c2
  # https://en.wikipedia.org/wiki/Color_difference
  return math.sqrt(math.pow(r1 - r2, 2) + math.pow(g1 - g2, 2) + math.pow(b1 - b2, 2))

def letter(pixel, palette):
  result = 0xf
  lowest = float('inf')
  if distance(pixel, (0, 0, 0)) < 10:
    return '0'
  else:
    for current in enumerate(palette[1:]):
      idx, colour = current
      d = distance(pixel, colour)
      if d < lowest:
        result = idx
        lowest = d
    return '{:x}'.format(result + 1)
  
def pixel(image, x, y):
  result = image.get(x, y)
  if type(result) ==  type(0):
    result = [value, value, value]
  elif type(result) == type((0,0,0)):
    result = list(pixel)
  else:
    result = list(map(int, result.split()))
  return result

def resize(fname, image, dim):
  dim = float(dim)
  if image.width() > dim or image.height() > dim:
    scale_w = int(math.ceil(image.width() / dim))
    scale_h = int(math.ceil(image.height() / dim))
    print('warning: downsampling {} (size: {}, {})'.format(fname, image.width(), image.height()))
    return image.subsample(max(scale_w, scale_h))
  else:
    return image

def compileImage(file, cname, image, palette):
  file.write('const {} = img`\n'.format(cname))
  for y in range(image.height()):
    line = []
    for x in range(image.width()):
      line.append(pixel(image, x, y))
      file.write(' {}'.format(letter(pixel(image, x, y), palette)))
    file.write('\n')
  file.write('`\n')

def compileSprite(js_fname, images, palette):
  with open(js_fname, 'w') as file:
    file.write('// {}\n'.format(os.path.basename(js_fname)))
    file.write('// generated file, do not edit\n')
    file.write('// run sprite.py to re-generate\n\n')
    for cname, image in images:
      compileImage(file, cname, image, palette)

tk = tkinter.Tk()

DefaultPalette = [
  0x000000,
  0xffffff,
  0xff2121,
  0xff93c4,
  0xff8135,
  0xfff609,
  0x249ca3,
  0x78dc52,
  0x003fad,
  0x87f2ff,
  0x8e2ec4,
  0xa4839f,
  0x5c406c,
  0xe5cdc4,
  0x91463d,
  0x000000
]

palette = []
for colour in DefaultPalette:
  palette.append(rgb(colour))

input, js_fname = args()
images = map(lambda fname: (cname(fname), resize(fname, image(fname), 50)), input)
ffname, fimage = images[0]
for cfname, cimage in images:
  if cimage.height() != fimage.height():
    print('error: "{}" height is different from "{}" height'.format(cfname, ffname))
    sys.exit(7)
compileSprite(js_fname, images, palette)
