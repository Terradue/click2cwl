import yaml
from .clt import CommandLineTool
from .wf import Workflow
from collections import OrderedDict


def setup_yaml():
    """ https://stackoverflow.com/a/8661021 """
    represent_dict_order = lambda self, data:  self.represent_mapping('tag:yaml.org,2002:map', data.items())
    yaml.add_representer(OrderedDict, represent_dict_order)    

setup_yaml()

class CWLExport(object):

    def __init__(self, click2cwl):
            
        self._cwl_doc = dict()
        self.click2cwl = click2cwl

        self._cwl_doc['cwlVersion'] = 'v1.0'

        self._cwl_doc['$graph'] = [CommandLineTool(self.click2cwl).to_dict(),
                                   Workflow(self.click2cwl).to_dict()]

    def to_dict(self):
        
        return self._cwl_doc

    def dump(self):

        with open(f'{self.click2cwl.id}.cwl', 'w') as file:

            yaml.dump(self._cwl_doc, file)
