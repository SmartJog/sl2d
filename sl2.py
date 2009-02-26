#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ConfigParser

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

def main():
    """ Main function. """

    commands = []
    config = ConfigParser.ConfigParser()
    config.read('/etc/sl2d.conf')

    for section in config.sections():
        options = dict(config.items(section))
        command = []

        # Threads must go in first position to do any difference
        if 'threads' in options:
            command += [ "-threads %s" % options['threads'] ]
            del options['threads']

        url_in = options['url-in']
        url_out = options['url-out']
        del options['url-in']
        del options['url-out']

        # Generate the rest of the command
        command += [ '-%s %s' % (OPTIONS[setting], value)
            for (setting, value) in options.iteritems() if setting in OPTIONS]

        # Single valued parameter
        command += [ '-%s' % OPTIONS_SINGLE[setting]
            for (setting, value) in options.iteritems()
            if setting in OPTIONS_SINGLE and value in ('true', 'yes', 'on')]

        commands += [ "ffmpeg -i " + url_in + " " + " ".join(command) + " " + url_out ]
        print commands[-1]


if __name__ == '__main__':
    main()

