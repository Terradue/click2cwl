import os

import click


class CommandLineTool:

    def __init__(self, ctx2cwl, docker=None, requirements=None, env=None):
        self._clt_class = dict()
        self.docker = docker
        self.requirements = requirements
        self._clt_class['id'] = 'clt'

        key_list = [keys for keys in ctx2cwl.params.keys() if keys != 'conf_file']
        for i in range(len(key_list)):
            self.set_inputs({'inp' + str(i + 1): {
                'inputBinding': {'position': i + 1, 'prefix': "--" + str(key_list[i])},
                'type': self.get_type(ctx2cwl.command.params[i])}})

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

        if env is None:
            self._clt_class['requirements'] = {'ResourceRequirement': self.requirements if self.requirements else {},
                                               'EnvVarRequirement': {'envDef': env_vars}}
        else:
            self._clt_class['requirements'] = {'ResourceRequirement': self.requirements if self.requirements else {},
                                               'EnvVarRequirement': {'envDef': [env_vars, env]}}

    def get_type(self, ctx):
        if type(ctx.type) == click.Path:
            if ctx.multiple and ctx.required:
                return 'Directory[]'
            elif not ctx.required:
                return 'Directory?'
            return 'Directory'

        if type(ctx.type) == click.File:
            if ctx.multiple and ctx.required:
                return 'File[]'
            elif not ctx.required:
                return 'File?'
            return 'File'

        if ctx.type == click.STRING:
            if ctx.multiple and ctx.required:
                return 'String[]'
            elif not ctx.required:
                return 'String?'
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
