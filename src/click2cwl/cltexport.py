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

from collections import OrderedDict
from pathlib import Path

import yaml

from .clt import CommandLineTool


def setup_yaml():
    """https://stackoverflow.com/a/8661021"""

    def represent_dict_order(self, data):
        return self.represent_mapping("tag:yaml.org,2002:map", data.items())

    yaml.add_representer(OrderedDict, represent_dict_order)


setup_yaml()


class CLTExport:
    def __init__(self, click2cwl):
        self.click2cwl = click2cwl

        self._clt_doc = CommandLineTool(self.click2cwl).to_dict()

        self._clt_doc["cwlVersion"] = self._get_cwl_version()

    def _get_cwl_version(self):
        if "cwl-version" in self.click2cwl.extra_params:
            return self.click2cwl.extra_params["cwl-version"]
        if "wall-time" in self.click2cwl.extra_params:
            return "v1.1"
        return "v1.0"

    def to_dict(self):
        return self._clt_doc

    def dump(self, stdout=True):
        if stdout:
            print(yaml.dump(self._clt_doc))

        else:
            with Path(f"{self.click2cwl.id}.cwl").open("w") as file:
                yaml.dump(self._clt_doc, file)
