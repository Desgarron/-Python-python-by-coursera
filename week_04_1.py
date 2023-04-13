import os.path
import tempfile


class File:
    def __init__(self, file_path):
        self._current = 0
        self._file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                pass

    def __str__(self):
        return self._file_path

    def read(self):
        with open(self._file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def write(self, add_new_text):
        with open(self._file_path, 'w', encoding='utf-8') as f:
            f.write(add_new_text)

    def __iter__(self):
        return self

    def __next__(self):
        with open(self._file_path, 'r', encoding='utf-8') as f:
            f.seek(self._current)
            line = f.readline()

            if line:
                self._current = f.tell()
                return line
            else:
                self._current = 0
                raise StopIteration

    def __add__(self, obj):
        new_path = os.path.join(tempfile.gettempdir(), 'temp.txt')
        new_file = File(new_path)
        with open(new_file._file_path, 'w', encoding='utf-8') as f:
            f.write(self.read())
            f.write(obj.read())
        return new_file


if __name__ == '__main__':
    pass