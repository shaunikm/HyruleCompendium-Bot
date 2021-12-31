from pyrule_compendium import compendium
from difflib import get_close_matches

comp = compendium()
list_of_keys = ['creatures', 'equipment', 'materials', 'monsters', 'treasure']
all_data = comp.get_all()
list_of_all_entries = []


def get_key_from_value(dict_, value):
    dict_keys = list(dict_.keys())
    dict_values = list(dict_.values())
    key_ = dict_keys[dict_values.index(value)]
    return key_


def cap_all(in_str: str):
    term_list = [i for i in in_str.split()]
    for i in term_list:
        term_list[term_list.index(i)] = term_list[term_list.index(i)].capitalize()
    return ' '.join(i for i in term_list)


def parse_double_L(data):
    list_ = []
    for first_layer in data.keys():
        for first_layer_data in data[first_layer]:
            list_.append(first_layer_data['name'])
    return list_


def parse_uni_L(data):
    list_ = []
    for layer in data:
        list_.append(layer['name'])
    return list_


def make_into_uniL_list(item_):
    global list_of_all_entries
    for data in item_:
        list_of_all_entries.append(data)


def format_closest_match(entry, dict_):
    matches = []
    for i in range(len(entry)-2, len(entry)+3):
        try:
            matches += get_close_matches(entry, dict_[str(i)])
        except KeyError:
            pass
    return ', '.join(match for match in matches)


make_into_uniL_list(parse_double_L(all_data['creatures']))

for key in list_of_keys[1:]:
    make_into_uniL_list(parse_uni_L(all_data[key]))

indexed_dict = {}
for entry in list_of_all_entries:
    try:
        indexed_dict[str(len(entry))] += [entry]
    except KeyError:
        indexed_dict[str(len(entry))] = [entry]
