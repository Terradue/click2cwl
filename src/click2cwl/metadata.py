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

from types import SimpleNamespace


class WorkflowMetadata(SimpleNamespace):
    def __init__(self, **kwargs):
        self._fields = {**kwargs}

        return super().__init__(**self._fields)

    def to_dict(self):
        metadata = {}
        metadata["$namespaces"] = {"s": "https://schema.org/"}
        metadata["schemas"] = [
            "http://schema.org/version/9.0/schemaorg-current-http.rdf"
        ]

        if "author" in list(self._fields.keys()):
            metadata["s:author"] = [{"class": "s:Person", "s:name": self.author}]

        if "organization" in list(self._fields.keys()):
            metadata["s:organization"] = [
                {"class": "s:Organization", "s:url": self.organization}
            ]

        if "version" in list(self._fields.keys()):
            metadata["s:softwareVersion"] = self.version

        return metadata
