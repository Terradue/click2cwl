# click2cwl

## Rational and context

EO application developers use Click to create command line tools to process EO data.

> [Click](https://click.palletsprojects.com/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary. It’s the “Command Line Interface Creation Kit”. It’s highly configurable but comes with sensible defaults out of the box.
> It aims to make the process of writing command line tools quick and fun while also preventing any frustration caused by the inability to implement an intended CLI API.

To deploy these applications on an Exploitation Plaform on the Cloud, the EO application developers generate a CWL document that becomes an Application Package.

The repo contains a helper Python module that exploits the information contained in a **Click** [context object](https://click.palletsprojects.com/en/7.x/api/?highlight=context#click.Context) to generate the CWL document and eventually the parameters.

This helper Python module can thus be used to add "CWL dump" behaviour to a Python CLI that uses Click by adding an import and call to the `dump(ctx)` function provided in the helper Python module. 