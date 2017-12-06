'''Methode for access json files.'''
import json

class JsonHandler(object):
    '''Imports and exports from and to json files.'''

    @staticmethod
    def importer(filename):
        '''Imports dictionary from a json file.'''
        with open('data/' + filename + '.json', 'r') as jsonfile:
            return json.load(jsonfile)

    @staticmethod
    def exporter(filename, json_object):
        '''Exports dictionary to a json file.'''
        with open('data/' + filename + '.json', 'w') as jsonfile:
            json.dump(json_object, jsonfile)
