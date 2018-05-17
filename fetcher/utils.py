import os


def mkdirs(dir_path):
    """
    Create folders with parents
    :param dir_path: path of the expected dir
    :return:
    """
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        return True
    except Exception as e:
        raise e
