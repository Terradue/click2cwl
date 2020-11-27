import click

class CtxCWL:
    
    def __init__(self, ctx):
        
        self.command = ctx.command_path
        self.params = ctx.command.params
        
    def is_path(self, param): 
    
        return isinstance(param.type, click.types.Path)
    
    def is_file(self, param):
    
        return isinstance(param.type, click.types.File)
    
    def is_option(self, param):
    
        return isinstance(param, click.Option)
    
    def is_argument(self, param):
    
        return isinstance(param, click.Argument)
    
    def get_opts(self, param):
        
        return param.opts
    
    def get_cwl(self):
        
        
    