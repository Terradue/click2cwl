class Workflow:
    def __init__(self, ctx):
        self.create_workflow_info(ctx)
        self._workflow_class = dict()
        self._workflow_class['class'] = 'Workflow'
        self._workflow_class['doc'] = ctx.command.help
        self._workflow_class['label'] = ctx.command.get_short_help_str()
        self._workflow_class['id'] = ctx.command_path
        self._workflow_class['inputs'] = {'aoi': {}, 'input_reference': {}}
        self._workflow_class['inputs']['aoi'] = self.aoi
        self._workflow_class['inputs']['input_reference'] = self.input_reference
        self._workflow_class['outputs'] = {'id': {'wf_outputs'}, 'outputSource': {}, 'type': {}}
        self._workflow_class['steps'] = {'in': {}, 'out': [], 'run': []}

    def get_workflow(self):
        return self._workflow_class

    def normalize_name(self, name):
        if '-' in name:
            return name.replace('-', ' ')

    def create_workflow_info(self, ctx):
        """
        self.workflow = dict([('id', ctx.command_path),
                              ('label', self.normalize_name(ctx.command_path)),
                              ('doc', self.normalize_name(ctx.command_path) + ' processor')])
        """

        self.aoi = dict([('id', 'aoi'),
                         ('label', 'Area of interest'),
                         ('doc', 'Area of interest in WKT')])

        self.input_reference = dict([('id', 'input_reference'),
                                     ('label', 'EO product for ' + self.normalize_name(ctx.command_path)),
                                     ('doc', 'EO product for ' + self.normalize_name(ctx.command_path))])
