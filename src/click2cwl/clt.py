import os
from .cwlparam import CWLParam
from collections import OrderedDict


class CommandLineTool:
    def __init__(self, click2cwl):

        self._clt_class = dict()
        self.click2cwl = click2cwl

        self._clt_class["id"] = "clt"

        if self.click2cwl.get_docker() is not None:

            self._clt_class["hints"] = {
                "DockerRequirement": {"dockerPull": self.click2cwl.get_docker()}
            }

        self._clt_class["class"] = "CommandLineTool"
        self._clt_class["baseCommand"] = self.click2cwl.executable
        self._clt_class["stdout"] = "std.out"
        self._clt_class["stderr"] = "std.err"

        self._clt_class["outputs"] = {
            "results": {"outputBinding": {"glob": "."}, "type": "Directory"}
        }

        self._clt_class["stdout"] = "std.out"
        self._clt_class["stderr"] = "std.err"

        env_vars = self.click2cwl.get_env_vars()

        self._clt_class["requirements"] = {
            "ResourceRequirement": self.click2cwl.get_requirements(),
            "EnvVarRequirement": {"envDef": env_vars},
        }

        if "wall-time" in self.click2cwl.extra_params.keys():
            self._clt_class["requirements"]["ToolTimeLimit"] = {
                "timelimit": self.click2cwl.extra_params["wall-time"]
            }

        self._clt_class["inputs"] = OrderedDict()

        for index, param in enumerate(self.click2cwl.params):

            cwl_param = CWLParam(param)

            self._clt_class["inputs"][cwl_param.name] = cwl_param.to_clt_input(
                position=index + 1
            )

    def to_dict(self):

        return self._clt_class
