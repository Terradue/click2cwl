import yaml
from .clt import CommandLineTool
from .wf import Workflow
from .metadata import WorkflowMetadata
from collections import OrderedDict

# yaml_same_ids_deep_copy.py
from copy import deepcopy

def setup_yaml():
    """https://stackoverflow.com/a/8661021"""
    represent_dict_order = lambda self, data: self.represent_mapping(
        "tag:yaml.org,2002:map", data.items()
    )
    yaml.add_representer(OrderedDict, represent_dict_order)


setup_yaml()

    
class CWLExport(object):
    def __init__(self, click2cwl):

        self._cwl_doc = dict()
        self.click2cwl = click2cwl

        self.metadata = WorkflowMetadata(**click2cwl.extra_params["metadata"])

        self._cwl_doc = self.metadata.to_dict()

        self._cwl_doc["cwlVersion"] = self._get_cwl_version()

        self._cwl_doc["$graph"] = [
            deepcopy(CommandLineTool(self.click2cwl).to_dict()),
            deepcopy(Workflow(self.click2cwl).to_dict()),
        ]

    def _get_cwl_version(self):

        if "cwl-version" in self.click2cwl.extra_params.keys():
            return self.click2cwl.extra_params["cwl-version"]
        elif "wall-time" in self.click2cwl.extra_params.keys():
            return "v1.1"
        else:
            return "v1.0"

    def to_dict(self):

        return self._cwl_doc

    def dump(self, stdout=True):

        if stdout:

            print(yaml.dump(self._cwl_doc))

        else:

            with open(f"{self.click2cwl.id}.cwl", "w") as file:

                yaml.dump(self._cwl_doc, file)
