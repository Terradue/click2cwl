import os

import click
import yaml
import errno


class CwlCreator:
    def __init__(self, ctx, docker=None, requirements=None, env=None, scatter=False, conf_file=None):
        self._full_cwl_content = dict()
        self._full_cwl_content['$graph'] = []
        self._full_cwl_content['cwlVersion'] = 'v1.0'
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

        self._full_cwl_content['$graph'].append(self._clt_class)

    def create_workflow_class(self, ctx, scatter=None):
        self._workflow_class['class'] = 'Workflow'
        self._workflow_class['doc'] = ctx.command.help
        self._workflow_class['label'] = ctx.command.get_short_help_str()
        self._workflow_class['id'] = ctx.command_path
        self._workflow_class['inputs'] = {'aoi': {}, 'input_reference': {}}

        for input_idx in range(len(self.key_list)):
            self._workflow_class['inputs'][self.key_list[input_idx]] = {'doc': self.key_list[input_idx] + " doc",
                                                                        'label': self.key_list[input_idx] + " label",
                                                                        'type': self.get_input_type(ctx.command.params[
                                                                                                        self.key_list.index(
                                                                                                            self.key_list[
                                                                                                                input_idx])])}

        self._workflow_class['outputs'] = {'id': 'wf_outputs', 'outputSource': 'node_1/results', 'type': 'Directory'}

        input_counter = dict()
        for i in range(len(self.key_list)):
            input_counter['inp' + str(i + 1)] = str(self.key_list[i])
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
            self.write_conf()
            with open(self.ctx.command_path + '.yml', 'w') as file:

                yaml.dump(self.ctx.params, file)
                # yaml.dump(self.write_conf(), file)
                file.close()

    def write_conf(self):

        if self.ctx.params['conf_file'] is not None:
            full_path = self.ctx.params['conf_file'].name
            """
            dir_name = full_path.rsplit('/', 1)[0]
            filename = full_path.split("/")[-1]
            """

            """
            if not os.path.exists(os.path.dirname(dir_name)):
                try:
                    os.makedirs(os.path.dirname(dir_name))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            """

            # with open(full_path, 'w') as ff:
            #   yaml.dump(self.ctx.params, ff)
            #  ff.close()

            f = open("demofile2.txt", "w")
            f.write("Now the file has more content!")
            f.close()

            """
            if self.ctx.command.params[list(self.ctx.params).index('conf_file')].multiple:
                return {'class': 'File[]', 'path': str(filename)}
            else:
                return {'class': 'File', 'path': str(filename)}
        else:
            return
            """

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
