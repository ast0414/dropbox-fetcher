import os


def mkdirs(dir_path):
    """
    Create folders with parents
    :param dir_path: path of the expected dir
    :return:
    """
    try:
        clean_path = os.path.abspath(dir_path)
        if not os.path.exists(clean_path):
            os.makedirs(clean_path)
        return True
    except Exception as e:
        raise e
