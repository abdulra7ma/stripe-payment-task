# Python imports
from os.path import join

# Django imports
from django.conf import settings

from apps.utils.utils.json import get_json_object, read_json


class AirInfo:
    """
    Helper class that facilitates the query process of the Json files
    of air-info
    """

    @property
    def airinfo_json_meta(self):
        return {
            "airline": {
                "json_path": join(settings.PROJECT_ROOT, "json/airlines.json"),
                "lookup_code": "id",
            },
            "airport": {
                "json_path": join(settings.PROJECT_ROOT, "json/airports.json"),
                "lookup_code": "code",
            },
            "aircraft": {
                "json_path": join(
                    settings.PROJECT_ROOT, "json/aircrafts.json"
                ),
                "lookup_code": "code",
            },
        }

    def get_airline_object(self, value):
        json_data = read_json(self.airinfo_json_meta["airline"]["json_path"])
        return get_json_object(
            json_data, self.airinfo_json_meta["airline"]["lookup_code"], value
        )

    def get_airport_object(self, value):
        json_data = read_json(self.airinfo_json_meta["airport"]["json_path"])
        return get_json_object(
            json_data, self.airinfo_json_meta["airport"]["lookup_code"], value
        )

    def get_aircraft_object(self, value):
        json_data = read_json(self.airinfo_json_meta["aircraft"]["json_path"])
        return get_json_object(
            json_data, self.airinfo_json_meta["aircraft"]["lookup_code"], value
        )

    def get_airline_json_data(self):
        return read_json(self.airinfo_json_meta["airline"]["json_path"])

    def get_airport_json_data(self):
        return read_json(self.airinfo_json_meta["airport"]["json_path"])

    def get_aircraft_json_data(self):
        return read_json(self.airinfo_json_meta["aircraft"]["json_path"])
