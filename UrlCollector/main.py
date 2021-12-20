from dataclasses import dataclass
from datetime import datetime
from github import Github, AuthenticatedUser, NamedUser, Repository
from github.GithubException import UnknownObjectException
import pandas as pd
from typing import List, Union, Optional, Any, Callable
import random

with open('TOKEN.txt') as f:
    ACCESS_TOKEN = f.read().splitlines()[0]
g = Github(ACCESS_TOKEN)


class BaseClass:
    request: Callable
    is_repo: Optional[bool] = None

    def __init__(self, obj: Optional[Any] = None, name: Optional[str] = None) -> None:
        if obj is not None:
            self.obj = obj
            self.name = obj.name
        elif name is not None:
            self.obj = self.request(name)
            self.name = name
        else:
            raise ValueError('No kwargs')
        self.url = self.obj.url
        print(self.name)

    def __eq__(self, other):
        return self.url == other.url


    def neighbours(self):
        raise NotImplementedError('Not implemented')


class User(BaseClass):
    request = g.get_user
    is_repo = False

    def neighbours(self, parent=True):

        if parent:
            return [repo.parent if repo.parent is not None else repo for repo in self.obj.get_repos()]
        return list(self.obj.get_repos())


class Repo(BaseClass):
    request = g.get_repo
    is_repo = True

    def neighbours(self):
        return list(self.obj.get_contributors())

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

    def dfs(self, start_name: str, num: int = 100):
        current_obj = get_user_or_repo(start_name)
        self.dfs_run(current_obj, num=num)

    def dfs_run(self, obj: Union[User, Repo], num: int = 100) -> None:
        print(obj)
        print(obj.neighbours())
        new_obj = [i for i in obj.neighbours() if i not in self.users_and_repos]
        self.users_and_repos.append(obj)
        print([i.name for i in self.users_and_repos])
        if obj.is_repo:
            self.repos.append(obj)
        while new_obj and len(self.repos) < num:
            self.dfs_run(get_user_or_repo(random.choice(new_obj)), num=num)
            new_obj = [i for i in new_obj if i not in self.users_and_repos]
            print(new_obj)

    def write_csv(self):
        repos_info = [repo.get_info() for repo in self.repos]
        pd.DataFrame(repos_info).to_csv('projects.csv')


def get_user_or_repo(obj: Any) -> Union[Repo, User]:
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
