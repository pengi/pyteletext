import teletext
import subprocess

from pybitbucket.auth import BasicAuthenticator, Anonymous
from ttxtemplates.bitbucket import render_pullrequest

#Render top rows, return number of rows occupied
def header_render(page, title, subtitle):
	style = {"background": teletext.COL_BLUE, "color":teletext.COL_WHITE}
	page.putstring(0,0," "*37, **style)
	page.putstring(0,1,"%-36s" % (title,), size=teletext.SIZE_DOUBLE_H, **style)
	page.putstring(0,3,"%36s " % (subtitle,), **style)
	return 4

#bbauth = BasicAuthenticator('username', 'apikey', 'email')
bbauth = Anonymous()
pages = [
	teletext.DynamicPage(render_pullrequest, [header_render, bbauth, 'atlassian', 'python-bitbucket'], 10.0, page_num=0x100),
	]

teletext_app = "../raspi-teletext/teletext"
proc = subprocess.Popen([teletext_app, "-"], stdin=subprocess.PIPE, close_fds=True)

while True:
	for page in pages:
		page.render(proc.stdin)
