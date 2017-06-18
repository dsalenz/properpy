import os
import re
import subprocess


# VARIABLES to set

triumph_working_dir_path = '/Users/salenz/git/triumph/demandware-frontend/cartridges/triumph_storefront/cartridge/templates/resources'
sloggi_working_dir_path = '/Users/salenz/git/triumph/demandware-frontend/cartridges/sloggi_storefront/cartridge/templates/resources'

country_codes = ['de', 'de_CH', 'de_AT', 'fr', 'fr_CH', 'fr_BE', 'sv', 'pl_PL', 'nl', 'nl_BE', 'it_IT', 'it_CH', 'da', 'fi', 'en', 'en_GB']

logfile = open('/Users/salenz/git/triumph/demandware-frontend/properpy_log/log.txt', 'w')



# FUNCTIONS

def is_default_property_file(property_file):
    regex = re.compile('_..\.properties$')
    return not regex.search(property_file)


def is_real_property (property_file_line):
    if property_file_line.startswith('#') or property_file_line.startswith('\n') or '=' not in property_file_line:
        return False
    else:
        return True


def find_property_keys(default_property_paths):
    property_keys = []
    for x in default_property_paths:
        full_property_file_path = triumph_working_dir_path + '/' + x
        with open(full_property_file_path) as f:
            print(f)
            try:
                property_file_lines = f.readlines()
            except UnicodeDecodeError:
                print(f, file=logfile)
            property_file_lines = [line for line in property_file_lines if is_real_property(line)]

            for line in property_file_lines:
                separator = '='
                separator_index = line.index(separator)
                property_key = line[:separator_index]
                property_keys.append(property_key)
    print(len(property_keys))
    return property_keys


def find_unreferenced_keys(property_keys):
    unreferenced_keys = []
    for property_key in property_keys:
        if not is_key_referenced(property_key):
            unreferenced_keys.append(property_key)
            print('UNREFERENCED: ' + property_key)
            print(property_key, file=logfile)
    return unreferenced_keys


def is_key_referenced(property_key):
    # search for a specific property_key in all files in all cartridges
    search_path = '/Users/salenz/git/triumph/demandware-frontend/cartridges/'
    excluded_cartridge_paths = ['sloggi_storefront', '.DS_Store', 'bc_serviceframework']
    working_cartridge_paths = os.listdir(search_path)
    for excluded_cartridge_path in excluded_cartridge_paths:
        working_cartridge_paths = [cartridge_path for cartridge_path in working_cartridge_paths if excluded_cartridge_path not in cartridge_path]
    for working_cartridge_path in working_cartridge_paths:
        if is_key_referenced_in_path(working_cartridge_path, property_key):
            return True
    return False


def is_key_referenced_in_path(path, key):
    path_to_search = '/Users/salenz/git/triumph/demandware-frontend/cartridges/' + path + '/cartridge/'
    output = subprocess.call(['grep', '-r', '--exclude=*.properties', key, path_to_search])
    return output == 0

# imperative Code

# default language
all_properties_file_paths = os.listdir(triumph_working_dir_path)

default_property_paths = [path for path in all_properties_file_paths if is_default_property_file(path)]
default_property_paths = [path for path in default_property_paths if path.endswith('.properties')]


print(find_unreferenced_keys(find_property_keys(default_property_paths)))

# multilanguage
for locale in country_codes:
    print('##### ##### ##### ##### #####', file=logfile)
    print(locale, file=logfile)
    print('##### ##### ##### ##### #####', file=logfile)

    reg = re.compile('_' + locale + '\.properties$')
    local_property_paths = [path for path in all_properties_file_paths if reg.search(path)]
    find_unreferenced_keys(find_property_keys(local_property_paths))
