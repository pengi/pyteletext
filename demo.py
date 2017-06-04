import teletext
import sys
import os
import time

out = os.fdopen(sys.stdout.fileno(), 'w', 42*8)

def color_page(page_num):
	page = teletext.StaticPage(page_num, "teletext man pages", headercolor=teletext.COL_BLUE)

	page.putstring(0, 0, "Color codes", size=teletext.SIZE_DOUBLE)
	page.putstring(0, 2, " "*40, background=teletext.COL_BLUE)

	for x in range(0, 8):
		page.putstring(4+x*3, 4, " %d " % (x,))
	for y in range(0, 8):
		page.putstring(1, y+5, "%1d%c\x1d" % (y, chr(y)))
		page.putstring(4+3*8, y+5, "\x1c")
		for x in range(0, 8):
			page.putstring(4+x*3, y+5, "%cX " % (chr(x),))

	return page

pages = [
	teletext.StaticPage(0x100),
	teletext.StaticPage(0x101),
	teletext.StaticPage(0x102),
	teletext.RotationPage(0x103),
	color_page(0x800)
	]

pages[0].putstring(0,0,"top left")
pages[1].putstring(10, 11, "\x0dHej hej\x01hopp hopp")
pages[2].putstring(40-12, 22, "bottom right")

tmppage = teletext.StaticPage(0)
tmppage.putbox(0, 0, 80, 23, "This is the first page in\na rotation of pages")
pages[3].add_page(tmppage)

tmppage = teletext.StaticPage(0)
tmppage.putbox(0, 0, 80, 23, "This is the second page in\na rotation of pages")
pages[3].add_page(tmppage)

tmppage = teletext.StaticPage(0)
tmppage.putbox(0, 0, 80, 23, "This is the third page in\na rotation of pages")
pages[3].add_page(tmppage)

tmppage = teletext.StaticPage(0)
tmppage.putbox(0, 0, 80, 23, "This is the fourth page in\na rotation of pages")
pages[3].add_page(tmppage)

while True:
	for page in pages:
		page.render(out)
