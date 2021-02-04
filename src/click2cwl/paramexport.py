import yaml
from .cwlparam import CWLParam


class ParamExport(object):
    def __init__(self, click2cwl):

        self._params = dict()
        self.click2cwl = click2cwl

        for index, param in enumerate(self.click2cwl.params):

            cwl_param = CWLParam(param)

            self._params[cwl_param.name] = cwl_param.to_param()

    def to_dict(self):

        return self._params

    def dump(self, stdout=True):

        if stdout:

            print(yaml.dump(self._params))

        else:

            with open(f"{self.click2cwl.id}.cwl", "w") as file:

                yaml.dump(self._params, file)
