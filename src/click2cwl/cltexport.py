import yaml
from .clt import CommandLineTool
from collections import OrderedDict


def setup_yaml():
    """https://stackoverflow.com/a/8661021"""
    represent_dict_order = lambda self, data: self.represent_mapping(
        "tag:yaml.org,2002:map", data.items()
    )
    yaml.add_representer(OrderedDict, represent_dict_order)


setup_yaml()


class CLTExport(object):
    def __init__(self, click2cwl):

        self.click2cwl = click2cwl

        self._clt_doc = CommandLineTool(self.click2cwl).to_dict()

        self._clt_doc["cwlVersion"] = self._get_cwl_version()

    def _get_cwl_version(self):

        if "cwl-version" in self.click2cwl.extra_params.keys():
            return self.click2cwl.extra_params["cwl-version"]
        elif "wall-time" in self.click2cwl.extra_params.keys():
            return "v1.1"
        else:
            return "v1.0"

    def to_dict(self):

        return self._clt_doc

    def dump(self, stdout=True):

        if stdout:

            print(yaml.dump(self._clt_doc))

        else:

            with open(f"{self.click2cwl.id}.cwl", "w") as file:

                yaml.dump(self._clt_doc, file)
