import teletext
import sys
import os
import time

out = os.fdopen(sys.stdout.fileno(), 'w', 42*8)

pages = [
	teletext.StaticPage(),
	teletext.StaticPage(),
	teletext.StaticPage()
	]

pages[0].putstring(0,0,"top left")
pages[1].putstring(10, 11, "Hej hej hopp hopp")
pages[2].putstring(40-12, 22, "bottom right")

while True:
	for (i, page) in enumerate(pages):
		page.render(out, 1, i)
