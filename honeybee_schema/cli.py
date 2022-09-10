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
import importlib
from inspect import getmembers, isfunction
import pkgutil

from honeybee_schema import updater


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

        # load the model dictionary from the json file and get the version of it
        with open(model_json) as json_file:
            model_dict = json.load(json_file)
        assert 'version' in model_dict, 'No version was found in the input model ' \
            'JSON. Update process cannot be run.'
        print(f'Input model version: {model_dict["version"]}', file=sys.stderr)
        model_version = tuple(int(v) for v in model_dict['version'].split('.'))

        if model_version >= up_version:
            # no point for updating. Normally we should assert here but by writing
            # the same file to a new file we make this command more flexible for cases
            # that we don't know the version for the input model and we want to update
            # it just in case.
            mv = '.'.join(map(str, model_version))
            uv = '.'.join(map(str, up_version))
            print(
                f'The input file has a higher version ({mv}) than the target version'
                f' ({uv}).', file=sys.stderr
            )
            output_file.write(json.dumps(model_dict))
            # let's consider exporting the same file as success
            sys.exit(0)

        # get functions with a higher version than model_version
        updaters = []

        for sub_module in pkgutil.walk_packages(updater.__path__):
            if not sub_module.name.startswith('version_'):
                continue
            module = importlib.import_module(f'honeybee_schema.updater.{sub_module.name}')
            for name, func in getmembers(module, isfunction):
                if not name.startswith('version_'):
                    continue
                func_version = tuple(int(v) for v in name.split('_')[1:])
                if model_version > func_version or func_version > up_version:
                    continue
                updaters.append((func_version, func))

        # sort updaters based on version
        updaters = sorted(updaters, key=lambda x: x[0])

        # update the dictionary
        for func_version, up_func in updaters:
            print(
                f'Updating to version {".".join(map(str, func_version))}',
                file=sys.stderr
            )
            model_dict = up_func(model_dict)

        # update the model dictionary version and write it to log file
        if version:
            model_dict['version'] = version
        elif updaters:
            model_dict['version'] = '.'.join((str(i) for i in updaters[-1][0]))
        output_file.write(json.dumps(model_dict))
    except Exception as e:
        _logger.exception('Failed to update Honeybee Model JSON.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
