import os
import sys
import logging
import click

from .ctx2cwl import CtxCWL

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


#@click.option('--cwl', is_flag=True, default=False, help='Prints CWL')

@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option('--input_reference', '-i', 'input_reference', type=click.Path())
@click.option('--aoi', '-a', 'aoi', default=None)
@click.pass_context
def entry(ctx, **kwargs): #, e_input_reference, e_aoi, cwl):
    
     # vegetation-index --dump cwl --docker a -r a=1 -r b=2
    
    print(ctx.args)
    extra_params = {ctx.args[i][2:]: ctx.args[i+1] for i in range(0, len(ctx.args), 2)}

    # todo
    # check if --dump is in ['--dump', 'cwl', '--docker', 'a'] to generate the CWL or the params file
   
    
    
    
    #print(ctx.get_help())
    #print(ctx.command_path)
    #print(ctx.args)
    #print(dir(ctx))
    #print(dir(ctx.command))
    #print('baseCommand ', ctx.command_path)
    #print(ctx.command.name)
    #for index, param in enumerate(ctx.command.params):
    #    print('its an option: ', isinstance(param, click.Option))
    #    print('its an argument: ', isinstance(param, click.Argument))
    #    print(ctx.command.params[index].opts)
    #    print('type: ', ctx.command.params[index].type)
    #    print('type Path: ', isinstance(ctx.command.params[index].type, click.types.Path))
    #    print('type File: ', isinstance(ctx.command.params[index].type, click.types.File))
    #print(dir(ctx.command.params[0]))
    thing = CtxCWL(ctx)
    
    print(thing.command)

    print(thing.params)
    
    for param in thing.params:
        
        print(thing.is_option(param))
        print(thing.get_opts(param))
    #print('params ', ctx.command.params[0].params)
        
    #print('opts ', ctx.command.params[0].opts)
    print(extra_params)
    sys.exit(0)
    #print(ctx.protected_args)
    
    #print(ctx.params)
    
    print(ctx.params['aoi'])
    
    print(ctx.params['input_reference'])
    
    print(aoi, input_reference, workflow)
    
    sys.exit(0)
            
    do_something(input_reference, aoi)

def do_something(input_reference, aoi):

    return True
    
    
if __name__ == '__main__':
    
    entry()

            

    




