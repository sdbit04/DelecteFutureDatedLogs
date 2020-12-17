import argparse
import os
import re
import datetime
import time


class LogDeleterForNE(object):

    def __init__(self, log_dir_for_an_ne):
        self.logs_dir = log_dir_for_an_ne

    def _get_dates_dir(self):
        abs_date_dirs = {}
        for _dir in os.listdir(self.logs_dir):
            abs_dir = os.path.join(self.logs_dir, _dir)
            # print(abs_dir)
            abs_date_dirs[_dir] = abs_dir
        return abs_date_dirs

    def delete_logs_from_daily_directory(self):
        abs_dir_path_list = self._get_dates_dir()
        for dir_date, abs_dir_path in abs_dir_path_list.items():
            # Composite of DailyLogDeleter
            daily_log_deleter = _DailyLogDeleter(dir_date, abs_dir_path)
            daily_log_deleter.delete_future_logs()


class _DailyLogDeleter(object):

    def __init__(self, directory_date, date_directory):
        with open("delete-incorrect-date-pchr.log", 'a') as delete_log:
            print("Directory date is = {}".format(directory_date), file=delete_log)
        self._dir_date = datetime.date(int(directory_date[0:4]), int(directory_date[4:6]), int(directory_date[6:8]))

        # self._future_date = (self._dir_date + datetime.timedelta(days=1))
        # self._year = str(self._future_date.year)
        # if len(self._year) < 4:
        #     self._year = "{}{}".format(0, self._year)
        # self._month= str(self._future_date.month)
        # if len(self._month) < 2:
        #     self._month = "{}{}".format(0, self._month)
        # self._day= str(self._future_date.day)
        # if len(self._day) < 2:
        #     self._day = "{}{}".format(0, self._day)
        # self._future_date_patarn = "{}{}{}".format(self._year, self._month, self._day)
        self.current_date_pattern = directory_date
        self._abs_date_dir_path = date_directory

    def delete_future_logs(self):
        hour_dir_list = os.listdir(self._abs_date_dir_path)
        for hour_dir in hour_dir_list:
            abs_hour_dir = os.path.join(self._abs_date_dir_path, hour_dir)
            self.delete_future_logs_from_each_hour(abs_hour_dir)

    def delete_future_logs_from_each_hour(self, abs_hour_directory):
        # TODO:  Need to update line below to design file pattern
        # future_file_pattern = ".*{}{}+".format("Log",self._future_date_patarn)
        current_file_pattern = ".*{}{}+".format("Log", self.current_date_pattern)
        # print("Future file pattern is {}".format(current_file_pattern))
        current_file_pattern = re.compile(current_file_pattern)
        log_files = os.listdir(abs_hour_directory)
        for log_file in log_files:
            with open("delete-incorrect-date-pchr.log", 'a') as delete_log:
                print("Log files name {}".format(log_file), file=delete_log)
            if current_file_pattern.search(log_file) is None:
                log_file_path = os.path.join(abs_hour_directory, log_file)
                try:
                    os.remove(log_file_path)
                except (FileNotFoundError, PermissionError):
                    with open("delete-incorrect-date-pchr.log", 'a') as delete_log:
                        print("FileNotFound or Permission Error occurred for {} ".format(log_file_path), file=delete_log)
                else:
                    with open("delete-incorrect-date-pchr.log", 'a') as delete_log:
                        print("{} is deleted ".format(log_file_path), file=delete_log)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("log_dir_for_a_NE", help="please provide the cache-logs directory path for an NE")
    args = parser.parse_args()
    log_dir_root_path = args.log_dir_for_a_NE
    start_time = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    with open("delete-incorrect-date-pchr.log", 'w') as delete_log:
        print("Started Deletion of future dated logs at {}".format(start_time), file=delete_log)
    log_deleter = LogDeleterForNE(log_dir_root_path)
    log_deleter.delete_logs_from_daily_directory()

