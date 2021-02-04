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
