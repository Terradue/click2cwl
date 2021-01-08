import os

import click
import yaml
import errno


class CwlCreator:

    def __init__(self, ctx, docker=None, requirements=None, env=None, scatter=False):
        self._full_cwl_content = dict()
        self._clt_class = dict()
        self._workflow_class = dict()
        self._full_cwl_content['$graph'] = []
        self._full_cwl_content['cwlVersion'] = 'v1.0'
        self.option_command_names = [k for k in ctx.params.keys() if ctx.params[k] is not None]
        self.option_list = ctx.command.params
        self.ctx = ctx
        self.create_clt(self.ctx, docker, requirements, env)
        self.create_workflow_class(self.ctx, scatter)

    def create_clt(self, ctx, docker, requirements, env):
        self._clt_class['id'] = 'clt'

        for i in range(len(self.option_command_names)):
            if "enum" in self.get_input_type(self.option_list[i]):
                self.set_clt_inputs({'inp' + str(i + 1): {
                    'inputBinding': {'position': i + 1, 'prefix': "--" + str(self.option_command_names[i])},
                    'type': self.get_input_type(self.option_list[i]),'symbols':self.option_list[i].type.choices[:]}})
            else:
                self.set_clt_inputs({'inp' + str(i + 1): {
                    'inputBinding': {'position': i + 1, 'prefix': "--" + str(self.option_command_names[i])},
                    'type': self.get_input_type(self.option_list[i])}})
        if docker is not None:
            self._clt_class['hints'] = {'DockerRequirement': {'dockerPull': docker}}

        self._clt_class['baseCommand'] = ctx.command_path
        self._clt_class['class'] = 'CommandLineTool'
        self._clt_class['stderr'] = 'std.err'
        self._clt_class['stdout'] = 'std.out'
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

        self._full_cwl_content['$graph'].append(self._clt_class)

    def create_workflow_class(self, ctx, scatter=None):
        self._workflow_class['class'] = 'Workflow'
        self._workflow_class['doc'] = ctx.command.help
        self._workflow_class['label'] = ctx.command.get_short_help_str()
        self._workflow_class['id'] = ctx.command_path
        self._workflow_class['inputs'] = {}

        for input_idx in range(len(self.option_command_names)):
            if self.option_command_names[input_idx] != 'conf_file':
                self._workflow_class['inputs'][self.option_command_names[input_idx]] = \
                    {'doc': str(self.option_command_names[input_idx]) + " doc",
                     'label': str(self.option_command_names[input_idx]) + " label",
                     'type': str(self.get_input_type(self.option_list[self.option_command_names.index(self.option_command_names[input_idx])]))}

            if self.option_command_names[input_idx] == 'conf_file':
                self._workflow_class['inputs'][self.option_command_names[input_idx]] = \
                    {'type': str(
                        self.get_input_type(self.option_list[self.option_command_names.index(self.option_command_names[input_idx])]))}

        self._workflow_class['outputs'] = {'id': 'wf_outputs', 'outputSource': 'node_1/results', 'type': 'Directory'}

        input_counter = dict()
        for i in range(len(self.option_command_names)):
            input_counter['inp' + str(i + 1)] = str(self.option_command_names[i])
        self._workflow_class['steps'] = {
            'node_1': {'in': input_counter, 'out': 'results', 'run': '#clt'}}

        if scatter is not None:
            resource_requirements = list()
            resource_requirements.append({'class': 'ScatterFeatureRequirement'})
            for key in scatter.keys():
                resource_requirements.append({key: scatter[key]})

            self._workflow_class['requirements'] = resource_requirements

            self._workflow_class['steps']['node_1']['scatter'] = 'inp1'
            self._workflow_class['steps']['node_1']['scatterMethod'] = 'dotproduct'

        self._full_cwl_content['$graph'].append(self._workflow_class)

    def dump_file(self, type_of_file):
        if type_of_file == 'cwl':
            with open(self.ctx.command_path + '.cwl', 'w') as file:
                yaml.dump(self._full_cwl_content, file)
                file.close()

        elif type_of_file == 'params':
            with open(self.ctx.command_path + '.yml', 'w') as file:
                for i in range(len(self.option_command_names)):
                    if "File" in self.get_input_type(self.option_list[i]):
                        yaml.dump({self.option_command_names[i]:{'class':self.get_input_type(self.option_list[i]), 
                        'path':self.ctx.params[self.option_command_names[i]]}})
                    else:
                        yaml.dump({self.option_command_names[i]:self.ctx.params[self.option_command_names[i]]}, 
                        file) 
                file.close()
            
    
    def write_conf(self):
        if self.option_list[list(self.ctx.params).index('conf_file')].multiple:
            return {'class': 'File[]', 'path': str(self.ctx.params['conf_file'].name)}
        else:
            return {'class': 'File', 'path': str(self.ctx.params['conf_file'].name)}
    
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
                return 'string[]'
            elif not ctx.required:
                return 'string?'
            return 'string'

        if type(ctx.type) == click.Choice:
            if ctx.multiple and ctx.required:
                return 'enum[]'
            elif not ctx.required:
                return 'enum?'
            return 'enum'

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

    def get_workflow(self):
        return self._workflow_class

    def get_clt(self):
        return self._clt_class