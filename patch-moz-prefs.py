#
# Python script to patch Mozilla Firefox preferences in bulk.
#
# by ax330d
#
# v 0.1     09-11-2014

__version__ = '0.1'

import os
import argparse
import ConfigParser


class AttributeDict(dict):
    '''Implements access to dictionary elements through dot.'''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


class MozPrefsPatcher(object):
    def __init__(self, path):
        self.path = path

    def run(self):
        '''Main function - parse config file, patch prefs.js.'''

        config = ConfigParser.ConfigParser()
        config.read(os.path.sep.join([self.path, 'profiles.ini']))
        sections = config.sections()

        for item in sections:
            if item == 'General':
                continue
            path_to_file = os.path.sep.join([self.path,
                                            config.get(item, 'path'),
                                            'prefs.js'])
            self.patch(path_to_file)
        return

    def patch(self, path_to_file):
        '''Patches prefs.js file, adds preferences.'''

        print "Patching {}...".format(path_to_file)

        prefsjs_data = self._get_prefjs_data()
        with open(path_to_file, 'a') as fh:
            fh.write(prefsjs_data)
        return

    @classmethod
    def _get_prefjs_data(cls):
        '''Create Firefox-format preference data.'''

        prefs = {}
        prefs['javascript.options.ion'] = 'false'
        prefs['browser.tabs.remote.autostart'] = 'false'
        prefs['browser.tabs.remote.autostart.1'] = 'false'

        data = ''
        for key in prefs:
            val = prefs[key]
            data += 'user_pref("{}", {});\n'.format(key, val)
        return data


def main():

    print "-" * 80
    print "Mozilla Firefox Preferences Patcher,",
    print "v.{}".format(__version__)
    print

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True,
                        help="Path to profiles.ini file")
    args = parser.parse_args()

    patcher = MozPrefsPatcher(args.path)
    patcher.run()

if __name__ == '__main__':
    main()
