from datetime import datetime
from github import Github


def run(username, repo):
    now = datetime.now()
    one_year_ago = now.replace(year=now.year - 1)
    access_token = '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'
    g = Github(access_token)
    repo = g.get_repo(f'{username}/{repo}')
    av_commits_count = int(repo.get_commits(since=one_year_ago).totalCount / 12)
    last_month = repo.get_commits(since=now.replace(month=now.month - 1)).totalCount
    return f'Average commits count per month in last year: {av_commits_count}\n' \
           f'Commits count in the last month: {last_month}'
