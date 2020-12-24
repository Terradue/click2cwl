import os

import click
import yaml


class CwlCreator:
    def __init__(self, ctx, docker=None, requirements=None, env=None, scatter=False):
        self._clt_class = dict()
        self._workflow_class = dict()
        self.key_list = [keys for keys in ctx.params.keys() if keys != 'conf_file']
        self.ctx = ctx
        self.create_clt(self.ctx, docker, requirements, env)
        self.create_workflow_class(self.ctx, scatter)

    def create_clt(self, ctx, docker, requirements, env):
        self._clt_class['id'] = 'clt'
        for i in range(len(self.key_list)):
            self.set_clt_inputs({'inp' + str(i + 1): {
                'inputBinding': {'position': i + 1, 'prefix': "--" + str(self.key_list[i])},
                'type': self.get_input_type(ctx.command.params[i])}})
        if docker is not None:
            self._clt_class['hints'] = {'DockerRequirement': {'dockerPull': docker}}

        self._clt_class['baseCommand'] = ctx.command_path
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
            self._clt_class['requirements'] = {'ResourceRequirement': requirements if requirements else {},
                                               'EnvVarRequirement': {'envDef': env_vars}}
        else:
            self._clt_class['requirements'] = {'ResourceRequirement': requirements if requirements else {},
                                               'EnvVarRequirement': {'envDef': [env_vars, env]}}

    def create_workflow_class(self, ctx, scatter=False):
        self._workflow_class['class'] = 'Workflow'
        self._workflow_class['doc'] = ctx.command.help
        self._workflow_class['label'] = ctx.command.get_short_help_str()
        self._workflow_class['id'] = ctx.command_path
        self._workflow_class['inputs'] = {'aoi': {}, 'input_reference': {}}
        self._workflow_class['inputs'][self.key_list[0]] = {'doc': '',
                                                            'label': '',
                                                            'type': self.get_input_type(ctx.command.params[
                                                                                            self.key_list.index(
                                                                                                self.key_list[0])])}

        self._workflow_class['inputs'][self.key_list[1]] = {'doc': '',
                                                            'label': '',
                                                            'type': self.get_input_type(ctx.command.params[
                                                                                            self.key_list.index(
                                                                                                self.key_list[1])])}
        self._workflow_class['outputs'] = {'id': 'wf_outputs', 'outputSource': 'node_1/results', 'type': 'Directory'}
        self._workflow_class['steps'] = {
            'node_1': {'in': {'key1': 'val1', 'key2': 'val2'}, 'out': 'results', 'run': '#clt'}}

        self._workflow_class['cwlVersion'] = 'v1.0'

        if scatter:
            self._workflow_class['requirements'] = {'class': 'ScatterFeatureRequirement'}
            self._workflow_class['steps']['node_1']['scatter'] = 'inp1'
            self._workflow_class['steps']['node_1']['scatterMethod'] = 'dotproduct'

    def dump_file(self, type_of_file):
        if type_of_file == 'cwl':
            with open(self.ctx.command_path + '.cwl', 'w') as file:
                yaml.dump(self._clt_class, file)
                yaml.dump(self._workflow_class, file)
                file.close()
        elif type_of_file == 'params':
            with open(self.ctx.command_path + '.yml', 'w') as file:
                yaml.dump(self.ctx.params, file)
                file.close()

    def get_workflow(self):
        return self._workflow_class

    def get_clt(self):
        return self._clt_class

    def get_input_type(self, ctx):
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

    def set_clt_inputs(self, inputs):
        if 'inputs' in self._clt_class:
            self._clt_class['inputs'].append(inputs)
        else:
            self._clt_class['inputs'] = [inputs]

    def get_path(self):
        path = os.environ['PATH']
        if ';' in path:
            path = os.environ['PATH'].split(';')[1]
        if 'PREFIX' in os.environ:
            path = ':'.join([os.path.join(os.environ['PREFIX'], 'bin'), path])
        return path
