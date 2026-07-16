# Copyright 2020 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
