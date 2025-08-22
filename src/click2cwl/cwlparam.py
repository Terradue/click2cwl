import click
from typing import Union

AnyParameter = Union[click.Option, click.Argument, click.Parameter]


class CWLParam(object):
    def __init__(self, click_option: AnyParameter, scatter: bool = False) -> None:

        self._option = click_option

        self.name = self._option.name
        self.opt = self._option.opts[0]
        self.multiple = self._option.multiple
        self.required = self._option.required
        # help only available in 'Option' (https://github.com/pallets/click/issues/587)
        self.help = getattr(self._option, "help", None)
        self.scatter = scatter
        self.input_type = self.get_type()
        self.default = self._option.default

    def to_clt_input(self, position):

        prefix = {"prefix": self.opt} if isinstance(self._option, click.Option) else {}
        binding = {"position": position, **prefix}

        if self.input_type == "enum":

            if self.required:
                clt_input = {
                    "type": [{
                        "type": self.input_type,
                        "symbols": list(self._option.type.choices),
                    }],
                    "inputBinding": binding,
                }

            else:

                clt_input = {
                    "type": [
                        "null",
                        {"type": self.input_type, "symbols": list(self._option.type.choices)},
                    ],
                    "inputBinding": binding,
                }

        else:

            if self.multiple:

                if self.required:

                    clt_input = {
                        "type": {
                            "type": "array",
                            "items": self.get_type(),
                            "inputBinding": binding,
                        }
                    }
                else:

                    clt_input = {
                        "type": [
                            "null",
                            {
                                "type": "array",
                                "items": self.get_type(),
                                "inputBinding": binding,
                            },
                        ]
                    }

            else:

                clt_input = {
                    "type": self.get_type(extended=True),
                    "inputBinding": binding,
                }

        return clt_input

    def to_workflow_param(self):

        help_info = {"label": self.help, "doc": self.help} if self.help else {}

        if self.input_type == "enum":

            if self.required:

                workflow_param = {
                    "type": [{
                        "type": self.input_type,
                        "symbols": list(self._option.type.choices),
                    }],
                    **help_info,
                }

            else:

                workflow_param = {
                    "type": [
                        "null",
                        {"type": self.input_type, "symbols": list(self._option.type.choices)},
                    ],
                    **help_info,
                }

        else:

            workflow_param = {
                "type": self.get_type(extended=True),
                **help_info,
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

        cwl_types = {}

        cwl_types[click.types.Path] = "Directory"
        cwl_types[click.types.File] = "File"
        cwl_types[click.types.StringParamType] = "string"
        cwl_types[click.types.Choice] = "enum"
        cwl_types[click.types.BoolParamType] = "boolean"

        option_type = type(self._option.type)
        cwl_type = cwl_types.get(option_type)

        if option_type is click.types.Path:
            if not self._option.type.dir_okay:
                cwl_type = "File"

        if self.scatter:

            return f"{cwl_type}[]"

        if extended:

            if self._option.multiple:

                cwl_type = f"{cwl_type}[]"

            if not self._option.required:

                cwl_type = f"{cwl_type}?"

        return cwl_type
