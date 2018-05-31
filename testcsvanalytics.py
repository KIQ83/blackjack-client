from analytics import CSVAnalytics, RampAnalytics
import sys


bot = sys.argv[1]
last = 0
if (len(sys.argv) > 2):
    last = sys.argv[2]
CSVAnalytics(bot)
RampAnalytics(bot, last)
