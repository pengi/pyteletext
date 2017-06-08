from teletext.constants import *

class RenderException(Exception):
	def __init__(self, message=""):
		Exception.__init__(self, message)

def active_sprint(client, boardid):
	boards = client.sprints(boardid, state='active')
	if len(boards) == 1:
		return boards[0]
	raise Error("stuff error")

def sprint_issues(client, sprint):
	return client.search_issues('sprint = %d' % (sprint.id,))

def issue_status(issue):
	return str(issue.fields.status.name)

def issue_type(issue):
	return str(issue.fields.issuetype)

def render_jira_board(page, header_render, client, board_id, status_order, status_color, color_by_type={}):
	try:
		sprint = active_sprint(client, board_id)
		issues = sprint_issues(client, sprint)

		row = header_render(page, sprint.name, "")

		issues_by_status = {}
		color_by_status = {}
		for status, color in zip(status_order, status_color):
			issues_by_status[status] = []
			color_by_status[status] = color

		for issue in issues:
			if issues_by_status.has_key(issue.fields.status.name):
				issues_by_status[issue_status(issue)].append(issue)

		issues_ordered = []
		for status in status_order:
			issues_ordered.extend(issues_by_status[status])

		for issue in issues_ordered:
			key_proj, key_num = issue.key.split('-')
			shortkey = key_proj[0]+"-"+key_num
			
			type_color = color_by_type.get(issue_type(issue), COL_WHITE)
			status_color = color_by_status[issue_status(issue)]

			page.putstring(0, row, (type_color + "%-6s" + status_color + "%-32s") % (shortkey, issue.fields.summary.strip()[:32]))

			row += 1
			if row > 23:
				return
	except RenderException:
		header_render(page, "no sprint", "")
