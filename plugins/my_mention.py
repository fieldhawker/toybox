from slackbot.bot import respond_to

import datetime

@respond_to('勤怠ファイル名')
def cheer(message):
    d = datetime.datetime.today()
    month = d.month

    if d.day > 20:
        month = month + 1

    message.reply('xxxx勤務表(SEP用)_ｘｘｘｘ%04d%02d' % (d.year, month))
