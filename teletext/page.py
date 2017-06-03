import packet
import time

def get_default_clock():
	return time.strftime("%H:%M:%S")

class Page:
	def __init__(self, page_num, headertext="pyteletext", **flags):
		self.magazine = (page_num & 0x700)>>8
		self.page_num = page_num & 0x0ff
		self.subcode = 0
		self.headertext = headertext
		self.flags = flags

	def render(self, out, clocktext=None):
		if clocktext == None:
			clocktext = get_default_clock()
		headertext = (self.headertext + (" "*24))[:24] + clocktext
		out.write(packet.packet_page_header(self.magazine, self.page_num, self.subcode, headertext, **self.flags))
		for i in range(24):
			out.write(packet.packet_direct_display(self.magazine, i+1, self.get_line(i)))

	def get_line(self, y):
		return "." * 40

class StaticPage(Page):
	def __init__(self, *args, **kvargs):
		Page.__init__(self, *args, **kvargs)
		self.content = [" "*40]*24

	def get_line(self, y):
		return self.content[y]
	
	def putstring(self, x, y, data):
		self.content[y] = self.content[y][:x] + data + self.content[y][x+len(data):]
		self.content[y] = self.content[y][:40]
