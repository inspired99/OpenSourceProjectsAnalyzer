import os
from datetime import datetime
from github import Github


def prev_month(month):
    return month - 1 if month != 1 else 12


def get_info(username, repo):
    now = datetime.now()
    one_year_ago = now.replace(year=now.year - 1)
    access_token = os.getenv("GITHUB_API_TOKEN")
    g = Github(access_token)
    repo = g.get_repo(f'{username}/{repo}')
    av_commits_count = int(repo.get_commits(since=one_year_ago).totalCount / 12)
    last_month = repo.get_commits(since=now.replace(month=prev_month(now.month))).totalCount

    return f'Average commits count per month in last year: {av_commits_count}\n' \
           f'Commits count in the last month: {last_month}'