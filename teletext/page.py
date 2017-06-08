import packet
import time
from .constants import *
from .settings import *

def get_default_clock():
	return time.strftime("%H:%M:%S")

class Page:
	def __init__(self, headercolor=None, **settings):
		self.settings = defaults(settings,
			headertext = "",
			page_num = 0,
			sub_code = 0
		)

		if headercolor != None:
			self.settings['headertext'] = headercolor + self.settings['headertext'] + COL_WHITE

	def render(self, out, clocktext = None, **settings):
		settings = apply(self.settings, **settings)

		if clocktext == None:
			clocktext = get_default_clock()

		headertext = (settings['headertext'] + (" "*24))[:24] + clocktext

		out.write(packet.packet_page_header(headertext, **settings))
		for i in range(24):
			out.write(packet.packet_direct_display(i+1, self.get_line(i), **settings))

	def get_line(self, y):
		return "." * 40

class RotationPage(Page):
	def __init__(self, **settings):
		Page.__init__(self, **settings)
		self.pages=[]
		self.lastpage=0

	def add_page(self, page):
		self.pages.append(page)

	def render(self, out, clocktext=None, **settings):
		settings = apply(self.settings, **settings)

		self.lastpage = (self.lastpage+1) % len(self.pages)
		num = self.lastpage + 1

		page = self.pages[self.lastpage]
		sub_code = ((num/10) << 4) | (num%10)

		page.render(out, clocktext, **apply(settings, sub_code=sub_code))

class StaticPage(Page):
	def __init__(self, **settings):
		Page.__init__(self, **settings)
		self.clear()

	def get_line(self, y):
		return self.content[y]

	def clear(self):
		self.content = [" "*40]*24
	
	def putstring(self, x, y, data, color=None, background=None, size=None):
		if y < 0 or y >= len(self.content):
			return
		if size != None:
			if size == SIZE_DOUBLE_W or size == SIZE_DOUBLE:
				data = " ".join(data) + " "
			data = size + data + SIZE_NORMAL
		if color != None:
			data = color + data + COL_WHITE
		if background != None:
			data = background + BKG_NEW + data + BKG_BLACK
		self.content[y] = self.content[y][:x] + data + self.content[y][x+len(data):]
		self.content[y] = self.content[y][:40]

	def putbox(self, x, y, w, h, data, **style):
		lines = data.splitlines() + [""]*h
		for yi in range(h):
			line = lines[yi] + " "*w
			line = line[:w]
			self.putstring(x, y+yi, line, **style)
