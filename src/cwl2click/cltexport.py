import yaml
from .clt import CommandLineTool
from collections import OrderedDict


def setup_yaml():
    """ https://stackoverflow.com/a/8661021 """
    represent_dict_order = lambda self, data:  self.represent_mapping('tag:yaml.org,2002:map', data.items())
    yaml.add_representer(OrderedDict, represent_dict_order)    

setup_yaml()

class CLTExport(object):

    def __init__(self, click2cwl):

        self.click2cwl = click2cwl

        self._clt_doc = CommandLineTool(self.click2cwl).to_dict()
        
        self._clt_doc['cwlVersion'] = 'v1.0'

        
    def to_dict(self):
        
        return self._clt_doc

    def dump(self):

        with open(f'clt_{self.click2cwl.id}.cwl', 'w') as file:

            yaml.dump(self._clt_doc, file)
