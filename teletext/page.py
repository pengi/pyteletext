import packet
import time
from .constants import *

def get_default_clock():
	return time.strftime("%H:%M:%S")

class Page:
	def __init__(self, page_num, headertext="", headercolor=None, **flags):
		self.magazine = (page_num & 0x700)>>8
		self.page_num = page_num & 0x0ff
		self.headertext = headertext
		self.flags = flags

		if headercolor != None:
			self.headertext = headercolor + self.headertext + COL_WHITE

	def render(self, out, clocktext=None, subcode=0, magazine=None, page_num=None):
		if magazine == None:
			magazine = self.magazine
		if page_num == None:
			page_num = self.page_num
		if clocktext == None:
			clocktext = get_default_clock()
		headertext = (self.headertext + (" "*24))[:24] + clocktext
		out.write(packet.packet_page_header(magazine, page_num, subcode, headertext, **self.flags))
		for i in range(24):
			out.write(packet.packet_direct_display(magazine, i+1, self.get_line(i)))

	def get_line(self, y):
		return "." * 40

class RotationPage(Page):
	def __init__(self, *args, **kvargs):
		Page.__init__(self, *args, **kvargs)
		self.pages=[]
		self.lastpage=0

	def add_page(self, page):
		self.pages.append(page)

	def render(self, out, clocktext=None):
		self.lastpage = (self.lastpage+1) % len(self.pages)
		num = self.lastpage + 1
		subcode = ((num/10) << 4) | (num%10)
		self.pages[self.lastpage].render(out, clocktext, subcode = subcode, magazine = self.magazine, page_num = self.page_num)

class StaticPage(Page):
	def __init__(self, *args, **kvargs):
		Page.__init__(self, *args, **kvargs)
		self.content = [" "*40]*24

	def get_line(self, y):
		return self.content[y]
	
	def putstring(self, x, y, data, color=None, background=None, size=None):
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

	def putbox(self, x, y, w, h, data, **kvargs):
		lines = data.splitlines() + [""]*h
		for yi in range(h):
			line = lines[yi] + " "*w
			line = line[:w]
			self.putstring(x, y+yi, line, **kvargs)
