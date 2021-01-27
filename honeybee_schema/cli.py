"""Command Line Interface (CLI) entry point for honeybee schema."""

try:
    import click
except ImportError:
    raise ImportError(
        'click module is not installed. Try `pip install honeybee-schema[cli]` command.'
    )

import sys
import logging
import json
import os
import importlib

import honeybee_schema.updater


@click.group()
@click.version_option()
def main():
    pass


_logger = logging.getLogger(__name__)


@main.command('update-model')
@click.argument('model-json', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option('--version', '-v', help='Text to indicate the version to which the model '
              'JSON will be updated (eg. 1.41.2). Versions must always consist of '
              'three integers separated b periods. If None, the Model JSON will '
              'be updated to the last release that included a breaking change.',
              type=str, default=None)
@click.option('--output-file', help='Optional file to output the JSON string of '
              'the config object. By default, it will be printed out to stdout',
              type=click.File('w'), default='-', show_default=True)
def update_model(model_json, version, output_file):
    """Update a Honeybee Model JSON to a newer version of honeybee-schema.

    \b
    Args:
        model_json: Full path to a Model JSON file.
    """
    try:
        # get the version to which the model will be updated
        up_version = (999, 999, 999) if version is None else \
            tuple(int(v) for v in version.split('.'))

        # build an array of all versions to date with breaking changes
        root_dir = os.path.join(os.path.dirname(__file__), 'updater')
        modules = os.listdir(root_dir)
        modules = [os.path.join(root_dir, mod) for mod in modules]
        updaters = ['.{}'.format(os.path.basename(f)[:-3]) for f in modules
                    if os.path.isfile(f) and f.endswith('.py')
                    and not f.endswith('__init__.py')
                    and not f.endswith('base.py')]
        versions = [tuple(int(v) for v in mod.split('_')[-3:]) for mod in updaters]

        # load the model dictionary from the json file and get the version of it
        with open(model_json) as json_file:
            model_dict = json.load(json_file)
        assert 'version' in model_dict, 'No version was found in the input model ' \
            'JSON. Update process cannot be run.'
        model_version = tuple(int(v) for v in model_dict['version'].split('.'))

        # figure out which update modules need to run and import them
        update_functions, update_vers = [], []
        for mod, ver in zip(updaters, versions):
            if ver < up_version and model_version < ver:
                importlib.import_module(mod, 'honeybee_schema.updater')
                update_vers.append(ver)
                update_functions.append('version_{}_{}_{}'.format(*ver))
        func_mapper = {}
        base_state = 'getattr(subpackage.{0}, "{0}")'
        for func in update_functions:
            statement = base_state.format(func)
            namespace = {'subpackage': honeybee_schema.updater}
            func_mapper[func] = eval(statement, namespace)

        # execute the update modules on the Model dictionary to update it
        update_vers, update_functions = zip(*sorted(zip(update_vers, update_functions)))
        statement = 'update_funct(model_dict)'
        for up_func in update_functions:
            namespace = {'update_funct': func_mapper[up_func], 'model_dict': model_dict}
            model_dict = eval(statement, namespace)

        # update the model dictionary version and write it to log file
        final_ver = up_version if version is not None else update_vers[-1]
        model_dict['version'] = '.'.join((str(i) for i in final_ver))
        output_file.write(json.dumps(model_dict))
    except Exception as e:
        _logger.exception('Failed to update Honeybee Model JSON.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
