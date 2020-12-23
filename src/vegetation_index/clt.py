import os

import click

from .ctx2cwl import CtxCWL


class CommandLineTool:

    def __init__(self, ctx2cwl, docker=None, requirements=None):
        self._clt_class = dict()
        self.docker = docker
        self.requirements = requirements
        self._clt_class['id'] = 'clt'

        key_list = list(ctx2cwl.params)
        for i in range(len(key_list)):
            self.set_inputs({'inp' + str(i + 1): {
                'inputBinding': {'position': i+1, 'prefix': "--" + str(key_list[i])},
                'type': self.get_type(ctx2cwl.command.params[i].type)}})

        if docker is not None:
            self._clt_class['hints'] = {'DockerRequirement': {'dockerPull': self.docker}}

        self._clt_class['baseCommand'] = ctx2cwl.command_path
        self._clt_class['class'] = 'CommandLineTool'
        self._clt_class['stdout'] = 'std.out'
        self._clt_class['stderr'] = 'std.err'

        self._clt_class['outputs'] = {'results': {'outputBinding': {'glob': '.'},
                                                  'type': 'Directory'}}

        self._clt_class['stdout'] = 'std.out'
        self._clt_class['stderr'] = 'std.err'

        env_vars = {'PATH': self.get_path()}

        if 'PREFIX' in os.environ:
            env_vars['PREFIX'] = os.environ['PREFIX']

        self._clt_class['requirements'] = {'ResourceRequirement': self.requirements if self.requirements else {},
                                           'EnvVarRequirement': {'envDef': env_vars}}

    def type_converter(self, ctx):

        if isinstance(ctx, str):
            return "string"

    def get_type(self, ctx_type):
        if type(ctx_type) == click.Path:
            return 'Directory'

        if type(ctx_type) == click.File:
            return 'File'

        if ctx_type == click.STRING:
            return 'String'

    def set_inputs(self, inputs):
        if 'inputs' in self._clt_class:
            self._clt_class['inputs'].append(inputs)
        else:
            self._clt_class['inputs'] = [inputs]

    def set_outputs(self, outputs):
        self._clt_class['outputs'] = outputs

    def get_path(self):
        path = os.environ['PATH']
        if ';' in path:
            path = os.environ['PATH'].split(';')[1]
        if 'PREFIX' in os.environ:
            path = ':'.join([os.path.join(os.environ['PREFIX'], 'bin'), path])
        return path

    def get_clt(self):
        return self._clt_class
