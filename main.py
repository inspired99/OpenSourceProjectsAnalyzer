from argparse import ArgumentParser
from GitHubMetrisc import commit_freq
import re




if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-nc', '--n-commits', dest='n_commits', default=10,
                        help='show n last commits (default: 10, max: 100)')
    args = parser.parse_args()
    while True:
        url = input('\nInput github url: \t\t\t\t\t\t\t\t (type "exit" to close the program)\n\n')
        if url == 'exit':
            exit(0)

        matched = re.match('((https:\/\/)|(http:\/\/))?github\.com\/([A-Za-z0-9\S]+)'
                           '\/([A-Za-z0-9\S]+)', url)
        if matched:
            username = matched.group(4)
            repo = matched.group(5)
            print()
            print(commit_freq.run(username, repo))
            print()
        else:
            print('Sorry, it seems like your url is not valid'
                  '\n The valid url should look like that: https://github.com/username/reponame')
