from yaml import CLoader as Loader, load

from .stage import Stage
from .status import Status


class Scenario:

    def __init__(self):
        self.status = Status.PENDING
        self.stages = []

    @staticmethod
    def load(file_name):
        s = Scenario()
        s._load_scenario(file_name=file_name)
        return s

    def _load_scenario(self, file_name):
        with open(file_name) as scenario_file:
            stages = load(scenario_file, Loader=Loader)

        for id, stage in enumerate(stages):
            s = Stage(id, stage)
            self.stages.append(s)

    def count_pending_stages(self):
        return len(self.stages)

    def to_dict(self):
        scenario = {'stages': [],
                    'status': {'code': self.status.value,
                               'name': self.status.name}}
        for stage in self.stages:
            scenario['stages'].append(stage.to_dict())
        return scenario
