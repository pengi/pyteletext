from .page import StaticPage
from threading import Lock, Thread, Event
import traceback

def exception_page(page, e):
	page.clear()
	exception_info = traceback.format_exc()
	print exception_info
	page.putbox(0,0,40,24, exception_info)
	print "Retrying..."

class BufferedPage(StaticPage):
	def __init__(self, **settings):
		StaticPage.__init__(self, **settings)
		self.output_lock = Lock()
		# Populate output buffer
		self.flush()

	def flush(self):
		self.output_lock.acquire()
		# Copy temporary buffer to output buffer
		self.output_buffer = self.content[:]
		self.output_lock.release()

	def get_line(self, y):
		self.output_lock.acquire()
		output_line = self.output_buffer[y]
		self.output_lock.release()
		return output_line

class DynamicPage(BufferedPage):
	def __init__(self, renderer, args, interval=10.0, **settings):
		BufferedPage.__init__(self, **settings)

		self.interval = interval
		self.renderer = renderer
		self.renderer_args = args

		self.stop_event = Event()

		self.thread = Thread(target=self.run)
		self.thread.daemon = True
		self.thread.start()

	def stop(self):
		self.stop_event.set()
		self.thread.join()

	def run(self):
		self.clear()
		try:
			self.renderer(self, *self.renderer_args)
		except Exception as e:
			exception_page(self, e)
		self.flush()
		while not self.stop_event.wait(self.interval):
			self.clear()
			try:
				self.renderer(self, *self.renderer_args)
			except Exception as e:
				exception_page(self, e)
			self.flush()
