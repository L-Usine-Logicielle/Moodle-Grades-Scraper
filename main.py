__author__ = "Andréa Joly"
__date__ = "31-01-2023"

from apscheduler.schedulers.blocking import BlockingScheduler
from lib.check import do_check

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone='Europe/Paris')
    scheduler.add_job(do_check, "interval", seconds=300)
    scheduler.start()
