from datetime import datetime
from github import Github, AuthenticatedUser, NamedUser, Repository
import pandas as pd
from typing import List, Union, Optional, Any, Callable, Dict
import random

with open('TOKEN.txt') as f:
    ACCESS_TOKEN = f.read().splitlines()[0]
g = Github(ACCESS_TOKEN)


class BaseClass:
    request: Callable
    is_repo: Optional[bool] = None

    def __init__(self, obj: Optional[Any] = None, name: Optional[str] = None) -> None:
        if obj is not None:
            print(f'Obj is known: {obj}. \t\t\t\t Do not request to {obj.name}')
            self.obj = obj
            self.name = obj.name
        elif name is not None:
            print(f'Only name is known. \t\t\t\tRequesting to {name}')
            self.obj = self.request(name)
            self.name = name
        else:
            raise ValueError('No kwargs')
        self.url = self.obj.url
        print(self.name)

    def __eq__(self, other):
        return self.url == other.url

    def get_neighbours(self):
        raise NotImplementedError('Not implemented')


class User(BaseClass):
    request = g.get_user
    is_repo = False
    neighbours = None

    def get_neighbours(self, parent=True):

        if parent:
            self.neighbours = [repo.parent if repo.parent is not None else repo for repo in self.obj.get_repos()]
        else:
            self.neighbours = list(self.obj.get_repos())
        return self.neighbours

    def get_info(self):
        return {
            'url': self.obj.html_url,
            'repos count': len(list(self.neighbours)) if self.neighbours is not None else "null"
        }


class Repo(BaseClass):
    request = g.get_repo
    is_repo = True
    neighbours = None

    def get_neighbours(self):
        self.neighbours = list(self.obj.get_contributors())
        return self.neighbours

    def get_info(self):
        return {
            'url': self.obj.html_url,
            'forks count': self.obj.forks_count,
            'contributors count': len(list(self.obj.get_contributors())),
            'stargazers_count': self.obj.stargazers_count,
        }


class GithubList:

    def __init__(self):
        self.users_and_repos: List[Union[User, Repo]] = []
        self.users: List[User] = []
        self.repos: List[Repo] = []
        self.big_users: Optional[List[User]] = None
        self.big_repos: Optional[List[Repo]] = None
        self.neighbours: Dict[str, Union[List[User], List[Repo]]] = {}

    def dfs(self, start_name: str, num: int = 100):
        current_obj = get_user_or_repo(start_name)
        self.dfs_run(current_obj, num=num)

    def dfs_run(self, obj: Union[User, Repo], num: int = 100) -> None:
        if obj.neighbours is None:
            new_obj = [i for i in obj.get_neighbours() if i not in self.users_and_repos]
        else:
            new_obj = [i for i in self.neighbours[obj.name] if i not in self.users_and_repos]
        self.neighbours[obj.name] = new_obj
        self.users_and_repos.append(obj)
        if obj.is_repo:
            self.repos.append(obj)
        else:
            self.users.append(obj)
        while new_obj and len(self.repos) < num:
            self.dfs_run(get_user_or_repo(random.choice(new_obj)), num=num)
            new_obj = [i for i in new_obj if i not in self.users_and_repos]

    def get_big_lists(self):
        self.big_users = self.users
        self.big_repos = self.repos
        for key, value in self.neighbours.items():
            if value:
                if isinstance(value[0], Repository.Repository):
                    for repo in value:
                        self.big_repos.append(Repo(repo))
                else:
                    for user in value:
                        self.big_users.append(User(user))

    def write_csv(self):
        repos_name = 'repos_list.csv'
        big_repos_name = 'big_repos_list.csv'
        users_name = 'users_list.csv'
        big_users_name = 'big_users_list.csv'

        repos_info = [repo.get_info() for repo in self.repos]
        pd.DataFrame(repos_info).to_csv(repos_name)
        users_info = [user.get_info() for user in self.users]
        pd.DataFrame(users_info).to_csv(users_name)

        self.get_big_lists()
        repos_info = [repo.get_info() for repo in self.big_repos]
        pd.DataFrame(repos_info).to_csv(big_repos_name)
        users_info = [user.get_info() for user in self.big_users]
        pd.DataFrame(users_info).to_csv(big_users_name)


def get_user_or_repo(obj: Any) -> Union[Repo, User]:
    print(f'Got obj: {obj}')
    if isinstance(obj, (Repo, User)):
        return obj
    elif isinstance(obj, str):
        if '/' in obj:
            return Repo(name=obj)
        else:
            return User(name=obj)
    elif isinstance(obj, Repository.Repository):
        return Repo(obj=obj)
    elif isinstance(obj, (AuthenticatedUser.AuthenticatedUser, NamedUser.NamedUser)):
        return User(obj=obj)


qwer = GithubList()
qwer.dfs('elizabet38', num=10)
qwer.write_csv()
