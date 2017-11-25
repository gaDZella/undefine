import chardet
import glob
from joblib import Parallel, delayed
import FlatModelBuilder
import BlockModelBuilder
import Processor
from CleanResult import CleanResult


class SharpCleaner:
    def __init__(self, keys):
        self.keys = keys

    def clean_file(self, file, apply_changes=True):
        encoding = self._read_encoding(file)
        with open(file, 'r', encoding=encoding) as fr:
            data = fr.read()
        model = FlatModelBuilder.build(data)
        result = self._clean(model)
        if result is not None:
            result.file = file
        if apply_changes and (result is not None and result.error is None):
            with open(file, 'w', encoding=encoding) as fw:
                fw.write(result.text)
        return result

    def clean_folder(self, folder, apply_changes=True):
        files = list(glob.iglob(folder + '//**//*.cs', recursive=True))
        return Parallel(n_jobs=-1)(delayed(self.clean_file)(file, apply_changes) for file in files)

    def _clean(self, fragments):
        try:
            model = BlockModelBuilder.build(fragments)
        except BlockModelBuilder.SyntaxException:
            return CleanResult(None, "Syntax Error", 0, 0)
        try:
            return Processor.process(model, self.keys)
        except:
            return CleanResult(None, "Undefined Error", 0, 0)


    @staticmethod
    def _read_encoding(file):
        with open(file, 'rb') as f:
            data = b''.join([f.read()])
        return chardet.detect(data)['encoding']
