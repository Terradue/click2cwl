import sys
import click
from .click2cwl import Click2CWL
from .cwlexport import CWLExport
from .paramexport import ParamExport

#test1 -i a --dump cwl --requirement ramMax=1 --requirement ramMin=2 --docker aaa  --env a=1 --env b=2
@click.command(short_help='hello Im the label of Workflow class',
               help='hello Im the doc of Workflow class',
               context_settings=dict(
                   ignore_unknown_options=True,
                   allow_extra_args=True, ))
@click.option('--input_reference', '-i', 'input_reference', type=click.Path(), help='this input reference', multiple=True, required=True)
@click.option('--aoi', '-a', 'aoi', help='help for the area of interest', default='POLYGON()', required=False)
@click.option('--file', '-f', 'conf_file', help='help for the conf file', type=click.File(mode='w'))
@click.option('--mode', '-m', 'mode', type=click.Choice(['local', 'ftp']), required=False)
@click.pass_context
def test1(ctx, **kwargs):

    click2cwl = Click2CWL(ctx)

    if click2cwl.extra_params:   
        
        if click2cwl.extra_params['dump'] == 'cwl':

            CWLExport(click2cwl).dump()
        
        else:

            ParamExport(click2cwl).dump()

    print('business as usual')
    print(kwargs)        

    sys.exit(0)
    

@click.command(context_settings=dict(
   ignore_unknown_options=True,
   allow_extra_args=True,
))
@click.option('--input_reference',
              '-i',
              'input_reference',
              help='help for input reference', 
              type=click.Path())
@click.option('--aoi', 
              '-a', 
              'aoi', 
              help='help for the area of interest',
              multiple=True,
              default=None)
@click.pass_context
def test2(ctx, input_reference, aoi):

    click2cwl = Click2CWL(ctx)

    if click2cwl.extra_params:   
        
        if click2cwl.extra_params['dump'] == 'cwl':

            CWLExport(click2cwl).dump()
        
        else:

            ParamExport(click2cwl).dump()

    print('business as usual')
    print(input_reference, aoi)        

    sys.exit(0)