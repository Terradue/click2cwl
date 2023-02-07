import click


class CWLParam(object):
    def __init__(self, click_option, scatter=False):

        self._option = click_option

        self.name = self._option.name
        self.opt = self._option.opts[0]
        self.multiple = self._option.multiple
        self.required = self._option.required
        self.help = self._option.help
        self.scatter = scatter
        self.input_type = self.get_type()
        self.default = self._option.default

    def to_clt_input(self, position):

        if self.input_type == "enum":

            if self.required:
                clt_input = {
                    "type": [{
                        "type": self.input_type,
                        "symbols": self._option.type.choices,
                    }],
                    "inputBinding": {"position": position, "prefix": self.opt},
                }

            else:

                clt_input = {
                    "type": [
                        "null",
                        {"type": self.input_type, "symbols": self._option.type.choices},
                    ],
                    "inputBinding": {"position": position, "prefix": self.opt},
                }

        else:

            if self.multiple:

                if self.required:

                    clt_input = {
                        "type": {
                            "type": "array",
                            "items": self.get_type(),
                            "inputBinding": {"position": position, "prefix": self.opt},
                        }
                    }
                else:

                    clt_input = {
                        "type": [
                            "null",
                            {
                                "type": "array",
                                "items": self.get_type(),
                                "inputBinding": {
                                    "position": position,
                                    "prefix": self.opt,
                                },
                            },
                        ]
                    }

            else:

                clt_input = {
                    "type": self.get_type(extended=True),
                    "inputBinding": {"position": position, "prefix": self.opt},
                }

        return clt_input

    def to_workflow_param(self):

        if self.input_type == "enum":

            if self.required:

                workflow_param = {
                    "type": [{
                        "type": self.input_type,
                        "symbols": self._option.type.choices,
                    }],
                    "label": self.help,
                    "doc": self.help,
                }

            else:

                workflow_param = {
                    "type": [
                        "null",
                        {"type": self.input_type, "symbols": self._option.type.choices},
                    ],
                    "label": self.help,
                    "doc": self.help,
                }

        else:

            workflow_param = {
                "type": self.get_type(extended=True),
                "label": self.help,
                "doc": self.help,
            }

        if self.default is not None:
            workflow_param["default"] = self.default

        return workflow_param

    def to_param(self):

        if self.input_type in ["Directory", "File"]:

            param = {
                "class": self.input_type,
                "path": "<value>" if self.default is None else self.default,
            }

        else:

            param = "<value>" if self.default is None else self.default

        if self._option.multiple:

            return [param]

        else:

            return param

    def get_type(self, extended=False):

        cwl_type = None

        cwl_types = {}

        cwl_types[click.types.Path] = "Directory"
        cwl_types[click.types.File] = "File"
        cwl_types[click.types.StringParamType] = "string"
        cwl_types[click.types.Choice] = "enum"
        cwl_types[click.types.BoolParamType] = "boolean"

        cwl_type = cwl_types.get(type(self._option.type))

        if self.scatter:

            return f"{cwl_type}[]"

        if extended:

            if self._option.multiple:

                cwl_type = f"{cwl_type}[]"

            if not self._option.required:

                cwl_type = f"{cwl_type}?"

        return cwl_type
