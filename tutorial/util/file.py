import os
import errno


def file_append_if_not(path, text):
    found = False
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if text in line:
                    found = True
    if not found:
        with open(path, 'a+') as f:
            f.write(text + "\n")
    return found


def make_parent_dir(file_path):
    # If parent folders don't exist create them
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def save_data(file_path, data):
    # If parent folders don't exist create them
    make_parent_dir(file_path)

    # Write data to file
    with open(file_path, 'wb') as f:
        f.write(data)


def save_sdata(file_path, data):
    # If parent folders don't exist create them
    make_parent_dir(file_path)

    # Write data to file
    with open(file_path, 'w') as f:
        f.write(data)


def move(src, dist):
    make_parent_dir(dist)
    os.rename(src, dist)


def create_sysln(src, dest):
    if not os.path.exists(dest):
        make_parent_dir(dest)
        os.symlink(src, dest)
