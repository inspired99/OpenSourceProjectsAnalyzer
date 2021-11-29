from argparse import ArgumentParser
from GitHubMetrisc import commit_freq
import re


if __name__ == '__main__':
    url = input()
    matched = re.match('((https:\/\/)|(http:\/\/))?github\.com\/([A-Za-z0-9\S]+)'
                       '\/([A-Za-z0-9\S]+)', url)
    if matched:
        username = matched.group(4)
        repo = matched.group(5)
        print(commit_freq.run(username, repo))
        print(issues_activity.run(username, repo))
    else:
        print('Sorry, it seems like your url is not valid'
              '\n The valid url should look like that: https://github.com/username/reponame')
