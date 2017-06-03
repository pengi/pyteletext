import teletext
import sys
import os
import time

out = os.fdopen(sys.stdout.fileno(), 'w', 42*8)

pages = [
	teletext.StaticPage(0x100),
	teletext.StaticPage(0x101),
	teletext.StaticPage(0x102)
	]

pages[0].putstring(0,0,"top left")
pages[1].putstring(10, 11, "Hej hej hopp hopp")
pages[2].putstring(40-12, 22, "bottom right")

while True:
	for page in pages:
		page.render(out)
