# agnes-monitor
scrapy- and spidermon-based spider which notifies you on Telegram messenger if you have new exam results in you (Humboldt-University-Berlin-)Agnes account.
# How does it work?
This programm is especially designed for agnes.hu-berlin.de .
Basically it simulates a login to your personal student account on Agnes, to check the number of lines in your "Trancript Of Records".
If there are more lines in the Transcript of Records then specified in the spidermon monitors.py file, spidermon will send you a Telegram notification to your specified Telegram user, group or channel.
