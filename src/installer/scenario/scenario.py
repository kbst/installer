from yaml import CLoader as Loader, load

from .stage import Stage


class Scenario:

    def __init__(self):
        self.stages = []

    @staticmethod
    def load(file_name):
        s = Scenario()
        s._load_scenario(file_name=file_name)
        return s

    def _load_scenario(self, file_name):
        with open(file_name) as scenario_file:
            stages = load(scenario_file, Loader=Loader)

        for stage in stages:
            s = Stage(stage)
            self.stages.append(s)
