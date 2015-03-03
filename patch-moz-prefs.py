#
# Python script to patch Mozilla Firefox preferences in bulk.
#
# by ax330d
#
# v 0.0.1     09-11-2014
# v 0.0.2     03-03-2015

import re
import os
import argparse
import ConfigParser

__version__ = '0.0.2'


class AttributeDict(dict):
    '''Implements access to dictionary elements through dot.'''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


class MozPrefsPatcher(object):
    '''Mozilla Firefox preferences patcher.'''
    def __init__(self, path):
        self.path = path
        self.prefs = None

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

        with open(path_to_file) as handle:
            prefs_default = handle.readlines()

        buff = ""
        cache = {}
        for preference in prefs_default:
            matches = re.match(r'user_pref\("(.*?)", (.*?)\);', preference)
            if not matches:
                buff += preference
                continue
            key = matches.group(1)
            val = matches.group(2)
            if key in cache:
                continue
            if key in self.prefs:
                continue
            cache[key] = val

        for key in sorted(cache):
            val = cache[key]
            buff += 'user_pref("{}", {});\n'.format(key, val)

        buff += "\n{}".format(prefsjs_data)

        with open(path_to_file, 'w') as handle:
            handle.write(buff)
        return

    def _get_prefjs_data(self):
        '''Create Firefox-format preference data.'''

        prefs = {}

        # This has been crashing for me too often
        prefs['javascript.options.ion'] = 'false'

        # Disable e10s
        prefs['browser.tabs.remote.autostart'] = 'false'
        prefs['browser.tabs.remote.autostart.1'] = 'false'

        # Disable crash reporting and things
        prefs['datareporting.healthreport.service.firstRun'] = 'false'
        prefs['datareporting.healthreport.service.enabled'] = 'false'
        prefs['datareporting.healthreport.uploadEnabled'] = 'false'
        prefs['dom.ipc.plugins.flash.subprocess.crashreporter.enabled'] = 'false'
        prefs['dom.ipc.plugins.reportCrashURL'] = 'false'

        # Safe fuzzing continuation
        prefs['browser.sessionstore.max_resumed_crashes'] = -1
        prefs['browser.sessionstore.resume_from_crash'] = 'false'
        prefs['toolkit.startup.max_resumed_crashes'] = -1

        # Enable some features
        prefs['webgl.disabled'] = 'false'
        prefs['canvas.filters.enabled'] = 'true'
        prefs['canvas.hitregions.enabled'] = 'true'
        prefs['dom.imagecapture.enabled'] = 'true'
        prefs['dom.indexedDB.experimental'] = 'true'
        prefs['dom.mapped_arraybuffer.enabled'] = 'true'
        prefs['dom.serviceWorkers.enabled'] = 'true'
        prefs['dom.w3c_pointer_events.enabled'] = 'true'
        prefs['dom.webcomponents.enabled'] = 'true'
        prefs['editor.use_css'] = 'true'
        prefs['layout.css.grid.enabled'] = 'true'
        prefs['layout.css.outline-style-auto.enabled'] = 'true'
        prefs['layout.css.overflow-clip-box.enabled'] = 'true'
        prefs['layout.css.text-align-true-value.enabled'] = 'true'
        prefs['layout.css.touch_action.enabled'] = 'true'
        prefs['layout.css.vertical-text.enabled'] = 'true'
        prefs['layout.event-regions.enabled'] = 'true'
        prefs['media.audio_data.enabled'] = 'true'
        prefs['media.mediasource.webm.enabled'] = 'true'
        prefs['media.peerconnection.ice.loopback'] = 'true'
        prefs['media.peerconnection.identity.enabled'] = 'true'
        prefs['media.peerconnection.video.h264_enabled'] = 'true'
        prefs['media.track.enabled'] = 'true'
        prefs['media.webspeech.recognition.enable'] = 'true'
        prefs['media.webspeech.synth.enabled'] = 'true'
        prefs['media.webvtt.regions.enabled'] = 'true'
        prefs['webgl.force-enabled'] = 'true'

        self.prefs = prefs
        data = ''
        for key in sorted(prefs):
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
