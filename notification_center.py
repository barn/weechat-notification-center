# https://github.com/barn/weechat-notification-center
# Requires `pip install pync`
# Original Author: Sindre Sorhus <sindresorhus@gmail.com>
# Author: Ben Hughes <weechats@mumble.org.uk>
# License: MIT

import weechat as w
from pync import Notifier as N

SCRIPT_NAME = 'notification_center'
SCRIPT_AUTHOR = 'Ben Hughes <weechats@mumble.org.uk>'
SCRIPT_VERSION = '0.4.0'
SCRIPT_LICENSE = 'MIT'
SCRIPT_DESC = 'Pass highlights & private messages to OSXs Notification Center'

w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
           SCRIPT_LICENSE, SCRIPT_DESC, '', '')

DEFAULT_OPTIONS = {
    'show_highlights': 'on',
    'show_private_message': 'on',
    'show_message_text': 'on',
}

for key, val in DEFAULT_OPTIONS.items():
        if not w.config_is_set_plugin(key):
                w.config_set_plugin(key, val)

w.hook_print('', 'irc_privmsg', '', 1, 'notify', '')


def notify(data, buffer, date, tags, displayed, highlight, prefix, message):

        # Skip alerting if you're already looking at it and you're not /away
        if (buffer == w.current_buffer()
           and w.buffer_get_string(buffer, 'localvar_away') == ''):
            return w.WEECHAT_RC_OK

        if w.config_get_plugin('show_highlights') == 'on' and int(highlight):
                channel = w.buffer_get_string(buffer, 'localvar_channel')
                if w.config_get_plugin('show_message_text') == 'on':
                        N.notify(message, title='%s %s' % (prefix, channel))
                else:
                        N.notify('In %s by %s' % (channel, prefix),
                                 title='Highlighted Message')
        elif (w.config_get_plugin('show_private_message') == 'on'
              and 'notify_private' in tags):
                if w.config_get_plugin('show_message_text') == 'on':
                        N.notify(message, title='%s [private]' % prefix)
                else:
                        N.notify('From %s' % prefix, title='Private Message')
        return w.WEECHAT_RC_OK
