import teletext
from pybitbucket.bitbucket import Client
from pybitbucket.pullrequest import PullRequest
import itertools

def render_pullrequest(page, header_render, auth, owner, repo):
	row = header_render(page, "pull requests", owner+"/"+repo)

	client = Client(auth)
	prs_open = PullRequest.find_pullrequests_for_repository_by_state(repo, owner=owner, client=client, state='OPEN')
	prs_merged = PullRequest.find_pullrequests_for_repository_by_state(repo, owner=owner, client=client, state='MERGED')

	colormap={'OPEN': teletext.COL_WHITE, 'MERGED': teletext.COL_GREEN}

	for pr in itertools.chain(prs_open, prs_merged):
		if type(pr) == dict:
			continue
		color = colormap.get(pr.state, teletext.COL_WHITE)
		page.putstring(0,  row  , pr.title[:33], color=color)
		page.putstring(32, row  , "#%d" % (pr.id,), color=color)
		page.putstring(0,  row+1, pr.author['display_name'], color=teletext.COL_BLUE)
		page.putstring(32, row+1, pr.state, color=teletext.COL_BLUE)

		row += 2	
		if row > 23:
			return
