"""Run all sample-genrating modules."""
import os
import importlib


# gather all of the modules the contain sample files
root_dir = os.path.dirname(os.path.abspath(__file__))
module_names = os.listdir(root_dir)
module_files = [os.path.join(root_dir, mod) for mod in module_names]
sample_modules = []
for mod, mod_file in zip(module_names, module_files):
    if os.path.isfile(mod_file) and mod_file.endswith('.py') \
            and mod.startswith('sample'):
        sample_modules.append(mod[:-3])

# execute each of the sample file modules
for mod in sample_modules:
    print('Generating samples for {}'.format(mod))
    importlib.import_module(mod)
