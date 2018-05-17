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

    # # dbx = dropbox.Dropbox(fetcher.access_token)
    # dbx = dropbox.Dropbox(fetcher.access_token)
    # # print(dbx.users_get_current_account())
    #
    # link = 'https://www.dropbox.com/sh/u6cn2yj1w89jnoq/AAA30wnEcfNq-3UkX4Kn7L04a?dl=0&lst='
    # # link = 'https://www.dropbox.com/sh/vbl5m3f2ujkg2ot/AAAREJfPbcAdtOEhleIyU11sa/Input?dl=0'
    #
    # # hashlib.sha1('https://www.dropbox.com/sh/u6cn2yj1w89jnoq/AAA30wnEcfNq-3UkX4Kn7L04a?dl=0&lst='.encode('utf-8')).hexdigest()[:10]
    #
    # # link = 'https://www.dropbox.com/sh/748f94925f0gesq/AAACxOBrrlgYrMtZ804XECFQa/Pusheen.jpg?dl=0'
    #
    # # meta = dbx.sharing_get_shared_link_file(link, '/')
    # # meta = dbx.sharing_get_shared_link_metadata(link)
    # # sharing_get_shared_link_file_to_file
    # meta = dbx.sharing_get_shared_link_metadata(link)
    # # print(meta)
    #
    # print("url:", meta.url)
    # limit = 1000
    # shared_link = SharedLink(meta.url)
    #
    # def scan_all(base):
    #     files = dbx.files_list_folder(base, limit=limit, shared_link=shared_link)
    #     while files.entries:
    #         for entry in tqdm(files.entries,
    #                           desc="scan: %s ## %s" % (shared_link.url, base)):  # type of entry: FileMetadata
    #             id = entry.id
    #             name = entry.name
    #             typename = type(entry).__name__
    #
    #             if typename == 'FolderMetadata':
    #                 print("FolderMetadata: %s" % name)
    #                 scan_all("%s/%s" % (base, name))
    #             elif typename == 'FileMetadata':  #
    #                 rev = entry.rev
    #                 size = entry.size
    #                 if filter_by_mat(name):
    #                     # print("@", base, "$$$ > ", id, "##", name, "$", size, "$", rev)
    #
    #                     # if base == "":
    #                     #     cmeta = dbx.sharing_get_shared_link_file_to_file(output_folder + '/' + entry.name,
    #                     #                                                      url=link,
    #                     #                                                      path='/' + entry.name)  # SharedLinkMetadata
    #                     #     print("cmeta:", cmeta)
    #                     import time
    #                     time.sleep(1)
    #                     pass
    #             else:
    #                 print("## Unexpected Meta: %s" % typename)
    #
    #         if files.cursor:
    #             files = dbx.files_list_folder_continue(files.cursor)
    #             # print("continue ... ", files.cursor)
    #         else:
    #             break
    #
    # scan_all("")

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
