import teletext
import subprocess

from pybitbucket.bitbucket import Client
from pybitbucket.auth import BasicAuthenticator, Anonymous
from ttxtemplates.bitbucket import render_pullrequest

#Render top four rows
def header_render(page, title, subtitle):
	style = {"background": teletext.COL_BLUE, "color":teletext.COL_WHITE}
	page.putstring(0,0," "*37, **style)
	page.putstring(0,1,"%-36s" % (title,), size=teletext.SIZE_DOUBLE_H, **style)
	page.putstring(0,3,"%36s " % (subtitle,), **style)

#bbclient = Client(BasicAuthenticator('username', 'apikey', 'email'))
bbclient = Client(Anonymous())
pages = [
	teletext.DynamicPage(render_pullrequest, [header_render, bbclient, 'atlassian', 'python-bitbucket'], 10.0, page_num=0x100),
	]

teletext_app = "../raspi-teletext/teletext"
proc = subprocess.Popen([teletext_app, "-"], stdin=subprocess.PIPE, close_fds=True)

while True:
	for page in pages:
		page.render(proc.stdin)
