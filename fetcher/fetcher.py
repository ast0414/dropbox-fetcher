from __future__ import print_function, with_statement

import dropbox
from dropbox.files import SharedLink
import hashlib
import re
import shelve
from tqdm import tqdm

from .utils import mkdirs


class Fetcher(object):
    def __init__(self, access_token, output):
        """
        Init
        :param access_token: access token from dropbox
        :param output: output folder
        """
        super(Fetcher, self).__init__()
        # assert (len(app_key) == 15)
        # assert (len(app_secret) == 15)
        assert (len(access_token) == 64 or len(access_token) == "")
        assert (len(output) > 0)

        assert (mkdirs(output))

        # self.app_key = app_key
        # self.app_secret = app_secret
        self.access_token = access_token
        self.output = output

        self.meta_rev = shelve.open("%s/meta-rev.shelve" % self.output)

        self.dbx = dropbox.Dropbox(access_token)

        self.urls = []
        self.sha1s = []
        self.filter_rule = None
        # self.link_pattern = 'https?:\\/\\/?[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,6}\\b[-a-zA-Z0-9@:%_\\+.~#?&=\\/]*'
        self.link_pattern = 'https?://www.dropbox.com/sh/[-a-zA-Z0-9@:%_\\+.~#?&=\\/]*'
        pass

    def load_input_urls(self, path):
        """ Load data from some text file, extract dropbox using regex
        :param path: input path
        :return: nothing
        """
        try:
            with open(path) as fp:
                print("[load_input_urls] Processing file: %s" % path)
                for line in fp.readlines():
                    for link in re.findall(self.link_pattern, line):
                        normalized_url = self.normalize_url(link)
                        sha1 = self.sha1(normalized_url)
                        self.urls.append(normalized_url)
                        self.sha1s.append(sha1)
                        print("link:", link, " => ", normalized_url, " folder:", sha1)
                pass
        except EnvironmentError as e:
            print("[load_input_urls] Process file #%s# failed: %s" % (path, e))
        pass

    def add_filter_rule(self, filter_rule):
        self.filter_rule = filter_rule

    def test_filter_rule(self, test_str):
        if self.filter_rule:
            return self.filter_rule(test_str)
        else:
            return True

    def normalize_url(self, url):
        meta = self.dbx.sharing_get_shared_link_metadata(url)
        return meta.url

    def sha1(self, url):
        """
        Extract sha1, and get first 10 characters
        :param url:
        :return:
        """
        return hashlib.sha1(url.encode('utf-8')).hexdigest()[:10]

    def safe_download(self, download_path, url, path):
        def do_download():
            try:
                # return SharedLinkMetadata
                self.dbx.sharing_get_shared_link_file_to_file(download_path,
                                                              url=url,
                                                              path=path)
                return True
            except OSError as e:
                print("Download %s failed :%s" % (url, e))
                return False

        status = False
        while not status:
            status = do_download()

    def fetch_one(self, index):
        num_urls = len(self.urls)
        curr_url = self.urls[index]
        curr_sha1 = self.sha1s[index]

        output_base = "%s/%s" % (self.output, curr_sha1)

        limit = 1000
        shared_link = SharedLink(curr_url)

        def scan_all(base):
            files = self.dbx.files_list_folder(base, limit=limit, shared_link=shared_link)
            while files.entries:
                for entry in tqdm(files.entries,
                                  desc="%d of %d (%s:%s)" % (
                                          index + 1, num_urls, curr_sha1, base)):
                    name = entry.name
                    typename = type(entry).__name__

                    if typename == 'FolderMetadata':
                        print("FolderMetadata: %s" % name)
                        scan_all("%s/%s" % (base, name))
                    elif typename == 'FileMetadata':  #
                        if self.test_filter_rule(name):
                            rev = entry.rev
                            # size = entry.size
                            relative_path = "" 
                            if len(base) > 0:
                                relative_path = base
                            output_file = "%s/%s" % (output_base, relative_path)
                            mkdirs(output_file)
                            output_file = "%s/%s" % (output_file, name)
                            meta_key = "%s/%s" % (relative_path, name)
                            current_rev = self.meta_rev.get(meta_key)
                            if rev != current_rev:
                                self.safe_download(output_file, curr_url, path='/%s/%s' % (
                                    base, name))
                                self.meta_rev[meta_key] = rev
                                self.meta_rev.sync()
                            else:
                                # print("skip... %s" % output_file)
                                pass
                    else:
                        print("## Unexpected Meta: %s" % typename)

                if files.has_more:
                    files = self.dbx.files_list_folder_continue(files.cursor)
                    # print("continue ... ", files.cursor)
                else:
                    break

        scan_all("")

    def fetch_all(self):
        num_urls = len(self.urls)
        print("Fetching... %d urls to %s" % (num_urls, self.output))

        with open("%s/mapping.txt" % self.output, "w") as fmp:
            for i in range(num_urls):
                fmp.write("%s\t%s\n" % (self.sha1s[i], self.urls[i]))
                pass
            fmp.close()

        for i in range(num_urls):
            self.fetch_one(i)

        self.meta_rev.sync()
        self.meta_rev.close()
        pass
