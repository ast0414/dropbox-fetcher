from __future__ import print_function, with_statement

import dropbox
import yaml
from dropbox.files import SharedLink
from tqdm import tqdm

from fetcher.utils import mkdirs
from fetcher.fetcher import Fetcher


def filter_by_mat(str):
    return str.endswith(".mat")

def start(cfg):
    access_token = cfg['dropbox']['access_token']
    input_files = cfg['input']
    output_folder = cfg['output']
    fetcher = Fetcher(access_token, output_folder)

    for input_file in input_files:
        print("input file: %s" % input_file)
        fetcher.load_input_urls(input_file)

    mkdirs(output_folder)
    print("output folder: %s" % output_folder)

    fetcher.add_filter_rule(filter_by_mat)
    print("test filter:")
    if cfg['filter'] and cfg['filter']['test_names']:
        test_names = cfg['filter']['test_names']
        for test_name in test_names:
            print("[ %-5r ]: %s" % (fetcher.test_filter_rule(test_name), test_name))

    fetcher.fetch_all()
    return fetcher


def main():
    try:
        with open('./config.yml') as fp:
            cfg = yaml.load(fp)
            # print("config:", cfg)
            start(cfg)
            pass
    except EnvironmentError as e:
        print("\nWhoops! Start failed, because of:\n\t%s" % e)


if __name__ == "__main__":
    main()
