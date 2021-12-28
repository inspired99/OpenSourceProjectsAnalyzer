import datetime
from datetime import date, datetime, timedelta
from typing import Any
from collections import Counter

import pandas as pd
import os

from github import Github
from github.Repository import Repository
from base.BaseMetrics import BaseMetric

"""def run(username, repo):
    now = datetime.now()
    one_year_ago = now.replace(year=now.year - 1)
    try:
        three_month_ago = now.replace(month=now.month - 3)
    except ValueError:
        three_month_ago = now.replace(year=now.year - 1, month=now.month + 9)
    keys_file = open("Resources/access_token.txt")
    lines = keys_file.readlines()
    access_token = lines[0].rstrip()
    g = Github(access_token)
    repo = g.get_repo(f'{username}/{repo}')
    commits = repo.get_commits(since=three_month_ago)
    contributors = set([commit.author for commit in commits])
    return f'Contributors count in the last three month: {len(contributors)}'
"""


class ContributorsNumber(BaseMetric):

    def __init__(self, project: Repository, min_commits: int = 1, **kwargs):
        super().__init__(project, **kwargs)
        self.min_commits = min_commits

    def calculate_metric(self, start_time: date, finish_time: date, **kwargs) -> Any:
        commits = self.project.get_commits(since=start_time, until=finish_time)
        authors = Counter([commit.author for commit in commits])
        return len([author for author in authors if authors[author] >= self.min_commits])


if __name__ == '__main__':
    project_list = pd.read_csv('projects_list.csv')
    project_list = project_list[['project_url', 'average']]
    project_urls = project_list['project_url']
    with open('base\\TOKEN.txt') as f:
        ACCESS_TOKEN = f.read().splitlines()[0]
    g = Github(ACCESS_TOKEN)
    repo = g.get_repo('{}/{}'.format(project_urls[0].split('/')[-2], project_urls[0].split('/')[-1]))
    metric = ContributorsNumber(repo)
    metric.history(history_start=datetime.now() - timedelta(days=360))
    metric.get_picture_graph()

    """labels = []
    labels3 = []
    labels5 = []
    for url in project_urls:
        print(url, type(url))
        repo = g.get_repo('{}/{}'.format(url.split('/')[-2], url.split('/')[-1]))
        metric = ContributorsNumber(repo)
        metric3 = ContributorsNumber(repo, min_commits=3)
        metric5 = ContributorsNumber(repo, min_commits=5)
        label = metric.run(start_time=datetime.datetime.now() - datetime.timedelta(days=30))
        labels.append(label)
        label3 = metric3.run(start_time=datetime.datetime.now() - datetime.timedelta(days=30))
        labels3.append(label3)
        label5 = metric5.run(start_time=datetime.datetime.now() - datetime.timedelta(days=30))
        labels5.append(label5)
        print(label, label3, label5)
    project_list['contr_number'] = labels
    project_list['contr_number3'] = labels3
    project_list['contr_number5'] = labels5
    project_list.to_csv('labeled_projects.csv')"""


