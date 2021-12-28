from datetime import datetime
from loguru import logger
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

    def __init__(self,
                 obj: Optional[Union[Repository.Repository,
                                     NamedUser.NamedUser,
                                     AuthenticatedUser.AuthenticatedUser]] = None,
                 name: Optional[str] = None) -> None:
        if obj is not None:
            if isinstance(obj, Repository.Repository):
                if obj.parent is not None:
                    logger.info(f'Found parent repo switching to it')
                    self.obj = obj.parent
                else:
                    self.obj = obj
                obj_name = self.obj.full_name
            else:
                obj_name = obj.login
                self.obj = obj

            logger.info(f'Initialization of {obj_name}. Object is known. Request is not needed')
            self.name = obj_name
        elif name is not None:
            logger.info(f'Initialization of {name}. Only name is known. Requesting...')
            self.obj = self.request(name)
            self.name = name
        else:
            raise ValueError('No kwargs')
        self.url = self.obj.html_url
        self.html_url = self.obj.html_url
        self.metric_results = {'url': self.url}

    def __eq__(self, other):
        return self.url == other.url

    def get_neighbours(self):
        raise NotImplementedError('Not implemented')

    def save_metric_result(self, name: str, result: Any):
        self.metric_results[name] = result


class User(BaseClass):
    request = g.get_user
    is_repo = False
    neighbours = None

    def get_neighbours(self):
        logger.info(f'Getting neighbours for user {self.name}')
        self.neighbours = list(self.obj.get_repos())
        logger.info(f'Got {len(self.neighbours)} neighbours')
        return self.neighbours

    def get_info(self):
        self.metric_results.update({
            'url': self.obj.html_url,
            'repos count': len(list(self.neighbours)) if self.neighbours is not None else "null"
        })
        return self.metric_results


class Repo(BaseClass):
    request = g.get_repo
    is_repo = True
    neighbours = None

    def get_neighbours(self):
        logger.info(f'Getting neighbours for repo {self.name}')
        self.neighbours = list(self.obj.get_contributors())
        logger.info(f'Got {len(self.neighbours)} neighbours')
        return self.neighbours

    def get_info(self):
        self.metric_results.update({
            'url': self.obj.html_url,
            'forks count': self.obj.forks_count,
            'subscribers count': self.obj.subscribers_count,
            'stargazers_count': self.obj.stargazers_count,
        })
        return self.metric_results


class GithubList:

    def __init__(self):
        self.users_and_repos: List[str] = []
        self.users: List[User] = []
        self.repos: List[Repo] = []
        self.big_users: Optional[List[User]] = None
        self.big_repos: Optional[List[Repo]] = None
        self.neighbours: Dict[str, Union[List[User], List[Repo]]] = {}

    def dfs(self, start_name: Union[str, List[str]], num: int = 100):
        if isinstance(start_name, str):
            logger.info(f'Starting dfs for {start_name}')
            current_obj = get_user_or_repo(start_name)
            self.dfs_run(current_obj, num=num)
        else:
            for name in start_name:
                logger.info(f'Starting dfs for {name}')
                self.dfs_run(get_user_or_repo(name), num=len(self.repos) + num)

    def dfs_run(self, obj: Union[User, Repo], num: int = 100) -> None:
        logger.debug(f'Current state:\t users: {len(self.users)};\t repos: {len(self.repos)}')
        self.users_and_repos.append(obj.html_url)

        if obj.neighbours is None:
            new_obj = [i for i in obj.get_neighbours() if i.html_url not in self.users_and_repos]
        else:
            new_obj = [i for i in self.neighbours[obj.name] if i.html_url not in self.users_and_repos]

        self.neighbours[obj.name] = new_obj

        if obj.is_repo:
            self.repos.append(obj)
        else:
            self.users.append(obj)

        while new_obj and len(self.repos) < num:
            self.dfs_run(get_user_or_repo(random.choice(new_obj)), num=num)
            new_obj = [i for i in new_obj if i.html_url not in self.users_and_repos]
            self.neighbours[obj.name] = new_obj

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

    def write_csv(self, do_users=False, do_big_lists=False):
        date = datetime.now()
        str_date = f'_{date.day}_{date.month}_{date.year}_{date.hour}_{date.minute}.csv'
        repos_name = 'repos_list' + str_date
        big_repos_name = 'big_repos_list' + str_date
        users_name = 'users_list' + str_date
        big_users_name = 'big_users_list' + str_date

        logger.info('Writing repos csv')
        repos_info = [repo.get_info() for repo in self.repos]
        pd.DataFrame(repos_info).to_csv(repos_name)
        if do_users:
            logger.info('Writing users csv')
            users_info = [user.get_info() for user in self.users]
            pd.DataFrame(users_info).to_csv(users_name)

        if do_big_lists:
            logger.info('Getting big lists')
            self.get_big_lists()

            logger.info('Writing big repos csv')
            repos_info = [repo.get_info() for repo in self.big_repos]
            pd.DataFrame(repos_info).to_csv(big_repos_name)
            if do_users:
                logger.info('Writing big users csv')
                users_info = [user.get_info() for user in self.big_users]
                pd.DataFrame(users_info).to_csv(big_users_name)


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


user = g.get_user('gitter-badger')
user.get_repos()