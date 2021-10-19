from argparse import ArgumentParser
import requests
import re


def run(matched, count):
    request_url = f'https://api.github.com/repos/{matched.group(4)}/{matched.group(5)}' \
                  f'/commits?per_page={count}'
    response = requests.get(request_url).json()
    if type(response) is type(dict()):
        print('\n', response)
    else:
        for i in range(len(response)):
            print('\n', i + 1, ':', f'\n"{response[i].get("commit").get("message")}"')
        print(f'\nTotal {len(response)} commits\n')


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
            run(matched, min(args.n_commits, 100))
        else:
            print('Sorry, it seems like your url is not valid'
                  '\n The valid url should look like that: https://github.com/username/reponame')
