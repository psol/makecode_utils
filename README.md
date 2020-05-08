# MakeCode utils
A script to ease the use of [MakeCode Arcade](https://arcade.makecode.com) with
the [PyBadge](https://www.adafruit.com/product/4200).

## sprite.py
MakeCode Arcade expects its sprite (and all images) in a img`...` format.
The documentation describes the [image type](https://arcade.makecode.com/types/image) and
[how to store them](https://arcade.makecode.com/developer/images).
This script converts a bitmap file into the appropriate format.

It is a quick adaptation from the symbols.py script I wrote for my Lampe project.

Note that the MakeCode Arcade documentation points to
[another script](https://riknoll.github.io/pxt-arcade-asset-tool/) but I found that
it did not worked very well for me... The image was resized and the JavaScript
string was not formatted properly (missing line returns)...