import argparse
import os
import re
import datetime


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
        self._dir_date = datetime.date(int(directory_date[0:4]), int(directory_date[4:6]), int(directory_date[6:8]))
        self._future_date = (self._dir_date + datetime.timedelta(days=1))
        self._future_date_patarn = "{}{}{}".format(self._future_date.year, self._future_date.month, self._future_date.day)

        self._abs_date_dir_path = date_directory

    def delete_future_logs(self):
        hour_dir_list = os.listdir(self._abs_date_dir_path)
        for hour_dir in hour_dir_list:
            abs_hour_dir = os.path.join(self._abs_date_dir_path, hour_dir)
            self.delete_future_logs_from_each_hour(abs_hour_dir)

    def delete_future_logs_from_each_hour(self, abs_hour_directory):
        # TODO:  Need to update line below to design file pattern
        future_file_pattern = "*{}*".format(self._future_date_patarn)
        future_file_pattern = re.compile(future_file_pattern)
        log_files = os.listdir(abs_hour_directory)
        for log_file in log_files:
            if re.search(future_file_pattern, log_file):
                log_file_path = os.path.join(abs_hour_directory, log_file)
                try:
                    os.remove(log_file_path)
                except (FileNotFoundError, PermissionError):
                    print("FileNotFound or Permission Error occurred for {} ".format(log_file_path))
                finally:
                    print("Exception occurred other than FileNotFound or PermissionError")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("log_dir_for_a_NE", help="please provide the cache-logs directory path for an NE")
    args = parser.parse_args()
    log_dir_root_path = args.log_dir_for_a_NE
    log_deleter = LogDeleterForNE(log_dir_root_path)
    log_deleter.delete_logs_from_daily_directory()

