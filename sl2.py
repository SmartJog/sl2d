#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import signal
import subprocess
import ConfigParser

import sjutils

OPTIONS = {
    # Unclassified settings
    'format':       'f',
    'flags':        'flags',
    'flags2':       'flags2',
    'partitions':   'partitions',
    'coder':        'coder',
    'refs':         'refs',
    'threads':      'threads',

    # Audio settings known by ffserver
    'audio_codec':       'acodec',
    'audio_bit_rate':    'ab',
    'audio_channels':    'ac',
    'audio_sample_rate': 'ar',

    # Video settings known by ffserver
    'video_codec':      'vcodec',
    'video_bit_rate':   'b',
    'video_size':       's',
    'video_gop_size':   'g',
    'video_q_min':      'qmin',
    'video_q_max':      'qmax',
    'video_frame_rate': 'r',

    # Other video settings
    'video_macroblock_decision': 'mbd',
    'video_macroblock_l_max':    'mblmax',
    'video_l_max':               'lmax',
    'video_q_comp':              'qcomp',
    'video_q_diff':              'qdiff',
    'video_b_frames':            'bf',
    'video_b_strategy':          'b_strategy',
    'video_i_q_factor':          'i_qfactor',
    'video_sc_threshold':        'sc_threshold',
    'video_direct_pred':         'directpred',
    'video_me_method':           'me_method',
    'video_me_range':            'me_range',
    'video_cmp':                 'cmp',
    'video_sub_q':               'subq',
    'video_keyint_min':          'keyint_min',
    'video_sync_method':         'vsync',
    'video_trellis':             'trellis',

    'audio_sync_method':         'async',
    'audio_sync_method': 'async',
}

OPTIONS_SINGLE = {
    'video_copy_timestamps': 'copyts',
}

def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]

    Taken from http://kogs-www.informatik.uni-hamburg.de/~meine/python_tricks"""

    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def build_commands():
    """ Build ffmpeg command line. """

    commands = []
    config = ConfigParser.ConfigParser()
    config.read('/etc/sl2d.conf')

    for section in config.sections():
        options = dict(config.items(section))
        command = [ [ "ffmpeg", '-v', '0'] ]

        # Threads must go in first position to do any difference
        if 'threads' in options:
            command += [ "-threads %s" % options['threads'] ]
            del options['threads']

        url_in = options['url-in']
        url_out = options['url-out']
        del options['url-in']
        del options['url-out']
        command += [ ["-i", url_in ] ]

        # Generate the rest of the command
        command += [ ['-' + OPTIONS[setting], value]
            for (setting, value) in options.iteritems() if setting in OPTIONS]

        # Single valued parameter
        command += [ '-%s' % OPTIONS_SINGLE[setting]
            for (setting, value) in options.iteritems()
            if setting in OPTIONS_SINGLE and value in ('true', 'yes', 'on')]

        command += [ url_out ]
        commands += [ flatten(command) ]

    return commands

class Monitor:

    def __init__(self):
        """ Init method. """

        self.schedule = {}
        self.process_list = {}
        self.log = sjutils.Logger2("/var/log/sl2d/sl2d.log")
        self.log.redirect_stdout_stderr()

        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def shutdown(self, signum, frame):
        """ Handling of sl2d shutdown. """

        if frame:
            del frame

        while len(self.process_list.keys()) > 0:
            self.log.write('%d process alive' % len(self.process_list.keys()))

            for pid in self.process_list.keys():
                # shutdown ffmpeg instances
                process = self.process_list[pid]['process']
                ret = process.poll()
                if ret is None:
                    process.stdin.write('q')
                else:
                    process.stdin.close()
                    process.stdout.close()
                    process.stderr.close()
                    del self.process_list[pid]

            time.sleep(2)

        self.log.write("sl2d terminated by signal", signum)
        self.log.close()
        sys.exit(os.EX_OK)

    def start_command(self, command):
        """ Start command and store it in process_list for reference. """

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.process_list[process.pid] = {'process': process, 'command': command}
        self.log.write('Starting "%s" as pid %d' % (" ".join(command), process.pid))

    def run(self):
        """ Main function. """

        # Bookkeeping our instanciations
        for command in build_commands():
            self.start_command(command)

        while True:
            time.sleep(2)

            # Restart a command in error after a number of iteration of the loop
            for sched_item in self.schedule.keys():
                if self.schedule[sched_item]['iter'] > 0:
                    self.schedule[sched_item]['iter'] -= 1
                else:
                    self.log.write('Respawning "%s"' % " ".join(self.schedule[sched_item]['command']))
                    self.start_command(self.schedule[sched_item]['command'])
                    del self.schedule[sched_item]


            # Monitor status of running process
            for pid in self.process_list.keys():
                process = self.process_list[pid]['process']
                command = self.process_list[pid]['command']

                if process.poll() is None:
                    #self.log.write('%d is alive' % pid)
                    continue
                else:
                    self.log.write('%d died unexpectedly, error code is %d' % (pid, process.poll()))
                    self.log.write('%d said: %s' % (pid, process.stderr.read()))
                    process.stdin.close()
                    process.stdout.close()
                    process.stderr.close()
                    del self.process_list[pid]
                    self.schedule[pid] = {'iter': 2, 'command': command }

        self.shutdown()

if __name__ == '__main__':
    Monitor().run()
