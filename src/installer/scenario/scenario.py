from yaml import CLoader as Loader, load

from .event import Event


class Scenario:
    events = []

    @staticmethod
    def load(file_name):
        s = Scenario()
        s._load_scenario(file_name=file_name)
        return s

    def _load_scenario(self, file_name):
        with open(file_name) as scenario_file:
            events = load(scenario_file, Loader=Loader)

        for event in events:
            e = Event(event)
            self.events.append(e)
