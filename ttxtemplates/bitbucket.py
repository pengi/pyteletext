import teletext
from pybitbucket.pullrequest import PullRequest
import itertools

def render_pullrequest(page, header_render, client, owner, repo):
	header_render(page, "pull requests", owner+"/"+repo)

	prs_open = PullRequest.find_pullrequests_for_repository_by_state(repo, owner=owner, client=client, state='OPEN')
	prs_merged = PullRequest.find_pullrequests_for_repository_by_state(repo, owner=owner, client=client, state='MERGED')

	colormap={'OPEN': teletext.COL_WHITE, 'MERGED': teletext.COL_GREEN}

	i = 0
	for pr in itertools.chain(prs_open, prs_merged):
		row = i*2 + 4
		if row > 20:
			return
		if type(pr) == dict:
			continue
		i+=1
		color = colormap.get(pr.state, teletext.COL_WHITE)
		page.putstring(0,  row  , pr.title[:33], color=color)
		page.putstring(32, row  , "#%d" % (pr.id,), color=color)
		page.putstring(0,  row+1, pr.author['display_name'], color=teletext.COL_BLUE)
		page.putstring(32, row+1, pr.state, color=teletext.COL_BLUE)
	
