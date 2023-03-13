import os


def create_file(path: str, contents: str, prompt: bool = False) -> tuple:
    """Creates a file at the specified path with the specified contents."""

    # first check that the file doesn't already exist
    if prompt:
        if os.path.exists(path):
            # if the file exists, prompt the user to overwrite it
            overwrite = input(f'File already exists at {path}. Overwrite? (y/n): ')
            if overwrite.lower() == 'y':
                # if the user wants to overwrite it, delete the file
                os.remove(path)
            else:
                print('File not overwritten.')
                return path, False

    # strategy the file
    try:
        with open(path, 'w') as f:
            f.write(contents)
        f.close()
    except Exception as e:
        print(f'Error creating file: {e}')
        return path, False
    return path, True
