from UrlCollector.Container import GithubList
from GitHubMetrisc.elizabet38.contributors_number import ContributorsNumber
from GitHubMetrisc.elizabet38.base.BaseMetrics import BaseMetric
from datetime import date, datetime, timedelta
import pandas as pd
from typing import List, Dict, Union, Any, Type
from loguru import logger
from github import GithubException

METRIC_ID: Dict[str, Type[BaseMetric]] = {
    'contr_num': ContributorsNumber,
}

METRICS_TO_CALCULATE: List[
    Dict[str,
         Union[
             str,
             datetime,
             List[Dict[str, Any]]
         ]
    ]
] = \
    [
        {
            'metric_id': 'contr_num',
            'start_time': datetime.now() - timedelta(days=30),
            'finish_time': datetime.now(),
            'kwargs': [
                {
                    'min_commits': 1,
                },
                {
                    'min_commits': 3,
                },
                {
                    'min_commits': 5,
                },
                {
                    'min_commits': 10,
                },
            ],
        },
    ]

if __name__ == "__main__":
    labeled_projects = pd.read_csv('labeled_projects.csv')
    projects = [i[19:] for i in labeled_projects['project_url']]
    gl = GithubList()
    gl.dfs(projects, num=5)
    logger.info('Calculating metrics:')
    for repo in gl.repos:
        logger.info(f'\tRepository: {repo.name}')
        try:
            repository = repo.obj
            for metric_info in METRICS_TO_CALCULATE:
                metric_type = METRIC_ID[metric_info['metric_id']]
                logger.info(f'\t\tMetric: {metric_type}')
                for kwargs in metric_info['kwargs']:
                    logger.info(f'\t\t\tkwargs: {kwargs}')
                    metric = metric_type(repository, **kwargs)
                    result = metric.run(start_time=metric_info['start_time'], finish_time=metric_info['finish_time'])
                    metric_name = f'{metric_info["metric_id"]}_' \
                                  f'{metric_info["start_time"]}_{metric_info["finish_time"]}_{kwargs}'
                    repo.save_metric_result(metric_name, result)
                    logger.info(f'\t\t\t\t Success!')
        except GithubException as e:
            logger.error(f'An exeption occured:\n\t {e}')
            gl.repos.remove(repo)

    gl.write_csv()
