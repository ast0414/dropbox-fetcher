from __future__ import print_function, with_statement

import yaml

from fetcher.utils import mkdirs

class Fetcher(object):
    def __init__(self, app_key, app_secret):
        assert (len(app_key) == 15)
        assert (len(app_secret) == 15)
        super(Fetcher, self).__init__()
        self.app_key = app_key
        self.app_secret = app_secret
        self.urls = []
        self.filter_rule = None
        pass

    def load_input_urls(self, path):
        """ Load data from some text file, extract dropbox using regex
        :param path: input path
        :return: nothing
        """
        pass

    def add_filter_rule(self, filter_rule):
        self.filter_rule = filter_rule

    def test_filter_rule(self, test_str):
        if self.filter_rule:
            return self.filter_rule(test_str)
        else:
            print("always true")
            return True

    def fetch(self, dir):
        pass


def start(cfg):
    app_key = cfg['dropbox']['app_key']
    app_secret = cfg['dropbox']['app_secret']
    input_files = cfg['input']
    output_folder = cfg['output']
    hidden_app_secret = ""
    for _ in app_secret:
        hidden_app_secret += "X"
    print("app_key: %s, app_secret %s" % (app_key, hidden_app_secret))
    fetcher = Fetcher(app_key, app_secret)
    for input_file in input_files:
        print("input file: %s" % input_file)

    mkdirs(output_folder)
    print("output folder: %s" % output_folder)


if __name__ == "__main__":
    try:
        with open('./config.yml') as fp:
            cfg = yaml.load(fp)
            print("config:", cfg)
            start(cfg)
            pass
    except EnvironmentError as e:
        print("\nWhoops! Start failed, because of:\n\t%s" % e)
