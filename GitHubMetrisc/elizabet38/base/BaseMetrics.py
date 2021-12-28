from datetime import date, timedelta, datetime
from typing import Optional, Any, List, Tuple
from github.Repository import Repository
import matplotlib.pyplot as plt
import numpy as np


class BaseMetric(object):

    def __init__(self, project: Repository, **kwargs) -> None:
        self.set_kwargs(**kwargs)
        self.project = project
        self.saved_history = None
        self.metric_name = None

    def set_kwargs(self, **kwargs) -> None:
        for key, value in kwargs:
            self.__setattr__(key, value)

    def run(self, start_time: Optional[datetime] = None, finish_time: Optional[datetime] = None, **kwargs) -> Any:
        if start_time is None:
            start_time = self.project.created_at
        if finish_time is None:
            finish_time = datetime.now()

        result = self.calculate_metric(start_time, finish_time, **kwargs)
        return result

    def calculate_metric(self, start_time: date, finish_time: date, **kwargs) -> Any:
        raise NotImplementedError

    def history(
            self,
            history_start: Optional[datetime] = None,
            run_duration: Optional[Any] = None,
            history_finish: Optional[datetime] = None,
            frequency: Optional[Any] = None,
            **kwargs
    ) -> List[Tuple[date, date, Any]]:
        if history_start is None:
            history_start = self.project.created_at
        if run_duration is None:
            run_duration = timedelta(days=30)
        if history_finish is None:
            history_finish = datetime.now()
        if frequency is None:
            frequency = timedelta(days=30)
        start = history_start
        finish = start + run_duration
        results_history = []

        while finish < history_finish:
            result = self.calculate_metric(start, finish, **kwargs)
            results_history.append((start, finish, result))
            print(start, finish, result)
            start += frequency
            finish += frequency
        self.saved_history = np.array(results_history)
        return results_history

    def get_picture_graph(self) -> None:
        x = self.saved_history[:, 0]
        y = self.saved_history[:, 2]

        fig, ax = plt.subplots()
        plt.xticks(rotation=45)

        ax.bar(x, y, width=30, edgecolor='white')
        ax.set_title(self.metric_name)

        plt.savefig('plot.png', bbox_inches='tight')
