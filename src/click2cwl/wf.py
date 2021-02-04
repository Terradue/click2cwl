from .cwlparam import CWLParam
from collections import OrderedDict


class Workflow:
    def __init__(self, click2cwl):

        self._wf_class = dict()

        self.click2cwl = click2cwl

        self._wf_class["id"] = self.click2cwl.id
        self._wf_class["label"] = self.click2cwl.label
        self._wf_class["doc"] = self.click2cwl.doc

        self._wf_class["class"] = "Workflow"

        self._wf_class["outputs"] = [
            {
                "id": "wf_outputs",
                "outputSource": ["step_1/results"],
                "type": {"type": "array", "items": "Directory"},
            }
        ]

        self._wf_class["inputs"] = OrderedDict()
        self._step_inputs = OrderedDict()

        for index, param in enumerate(self.click2cwl.params):

            if param.name == self.click2cwl.get_scatter_param():
                cwl_param = CWLParam(param, scatter=True)
            else:
                cwl_param = CWLParam(param)

            self._wf_class["inputs"][cwl_param.name] = cwl_param.to_workflow_param()

            self._step_inputs[cwl_param.name] = cwl_param.name

        if self.click2cwl.get_scatter_param() is not None:

            self._wf_class["outputs"] = [
                {
                    "id": "wf_outputs",
                    "outputSource": ["step_1/results"],
                    "type": {"type": "array", "items": "Directory"},
                }
            ]

            self._wf_class["requirements"] = [{"class": "ScatterFeatureRequirement"}]

            self._wf_class["steps"] = {
                "step_1": {
                    "scatter": self.click2cwl.get_scatter_param(),
                    "scatterMethod": "dotproduct",
                    "in": self._step_inputs,
                    "out": ["results"],
                    "run": "#clt",
                }
            }

        else:

            self._wf_class["outputs"] = [
                {
                    "id": "wf_outputs",
                    "outputSource": ["step_1/results"],
                    "type": "Directory",
                }
            ]

            self._wf_class["steps"] = {
                "step_1": {"in": self._step_inputs, "out": ["results"], "run": "#clt"}
            }

    def to_dict(self):

        return self._wf_class
