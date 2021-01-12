import os
from .cwlexport import CWLExport
from .cltexport import CLTExport
from .paramexport import ParamExport

def dump(ctx):

    click2cwl = Click2CWL(ctx)

    options = dict()

    options['cwl'] = CWLExport
    options['params'] = ParamExport
    options['clt'] = CLTExport
 
    if click2cwl.extra_params:   

        options[click2cwl.extra_params['dump']](click2cwl).dump()

    else:

        return None
        #if click2cwl.extra_params['dump'] == 'cwl':

        #    CWLExport(click2cwl).dump()
        
        #else:

        #    ParamExport(click2cwl).dump()


valid_requirements = ['coresMin', 'coresMax', 'ramMin', 'ramMax']

class Click2CWL(object):

    def __init__(self, ctx):

        self.ctx = ctx
        self.extra_params = self._get_extra_params()
        self.executable = self.ctx.command_path
        self.params = self.ctx.command.params

        self.id = self.ctx.command_path
        self.label = self.ctx.command.short_help
        self.doc = self.ctx.command.help

        if not self.extra_params:
    
            return None

        self.extra_params['env']['PATH'] = self.get_path()

    def _get_extra_params(self):

        extra_params = {}

        extra_params['requirements'] = {}
        
        extra_params['env'] = {}

        for i in range(0, len(self.ctx.args), 2):

            key = self.ctx.args[i][2:]

            if key == 'requirement':
    
                if self.ctx.args[i + 1].split('=')[0] in valid_requirements: 
                
                    extra_params['requirements'][self.ctx.args[i + 1].split('=')[0]] = int(self.ctx.args[i + 1].split('=')[1])
        
                else:

                    raise ValueError('Requirement {} is not valid'.format(self.ctx.args[i + 1].split('=')[0]))

            elif key == 'env':

                extra_params['env'][self.ctx.args[i + 1].split('=')[0]] = self.ctx.args[i + 1].split('=')[1]

            else: 

                extra_params[key] = self.ctx.args[i + 1]

        return extra_params


    def get_env_vars(self):

        return self.extra_params.get('env')

    def get_requirements(self):
    
        return {} if self.extra_params.get('requirements') is None else self.extra_params.get('requirements')


    def get_docker(self):

        return self.extra_params.get('docker')

    def get_path(self):
        
        path = os.environ['PATH']

        if ';' in path:

            path = os.environ['PATH'].split(';')[1]

        if 'PREFIX' in os.environ:

            path = ':'.join([os.path.join(os.environ['PREFIX'], 'bin'), path])

        return path
    
    def get_scatter_param(self):

        return self.extra_params.get('scatter')