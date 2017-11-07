import chardet
import glob
from joblib import Parallel, delayed
from ModelBuilder import *
from FileModel.FragmentType import *
from Condition import *
from FileModel.ConditionAccessor import ConditionAccessor


class SharpCleaner:
    def __init__(self, keys):
        self.keys = keys

    def clean_file(self, file, apply_changes=True):
        encoding = self._read_encoding(file)
        with open(file, 'r', encoding=encoding) as fr:
            data = fr.read()
        model = ModelBuilder.build(data)
        result = self._clean(model)
        if result is not None:
            result['file'] = file
        if apply_changes and (result is not None and result['success']):
            with open(file, 'w', encoding=encoding) as fw:
                fw.write(result['text'])
        return result

    def clean_folder(self, folder, apply_changes=True):
        files = list(glob.iglob(folder + '//**//*.cs', recursive=True))
        return Parallel(n_jobs=-1)(delayed(self.clean_file)(file, apply_changes) for file in files)

    def _clean(self, fragments):  # TODO: refactor
        text = ''
        cond_stack = [[True]]
        body_lines_counter = 0
        total_lines_counter = 0
        modified = False
        error = False
        try:
            for f in fragments:
                if f.type == FragmentType.Body:
                    remove = SharpCleaner._should_remove(cond_stack, f.type)
                    modified |= remove
                    text = SharpCleaner._change_text(text, f.text, remove)
                    if remove:
                        lines_count = len(f.text.split('\n'))
                        body_lines_counter += lines_count
                        total_lines_counter += lines_count
                else:
                    if f.type == FragmentType.IfStatement:
                        cond_stack.append([self._patch_cond(f)])
                    if f.type == FragmentType.ElIfStatement:
                        orig_cond = ConditionAccessor.get(f)
                        elif_cond = self._patch_cond(f)
                        if type(cond_stack[-1][-1]) is bool:
                            f.type = FragmentType.IfStatement
                            ConditionAccessor.set(f, elif_cond)
                        elif type(elif_cond) is bool:
                            elif_cond = str.format("!({0}) && {1}", cond_stack[-1][-1], orig_cond)
                            remove = SharpCleaner._should_remove(cond_stack, FragmentType.EndIfStatement)
                            modified = True
                            text = SharpCleaner._change_text(text, "#endif\n", remove)
                            total_lines_counter += 1
                            cond_stack.pop()
                            f.type = FragmentType.IfStatement
                            ConditionAccessor.set(f, elif_cond)
                            cond_stack.append([])
                        cond_stack[-1].append(self._patch_cond(f))
                    if f.type == FragmentType.ElseStatement:
                        prev_cond = cond_stack[-1][-1]
                        cond_stack[-1].append(not prev_cond if type(prev_cond) is bool else str.format("!({{0}})", prev_cond))
                    remove = SharpCleaner._should_remove(cond_stack, f.type)
                    modified |= remove
                    text = SharpCleaner._change_text(text, f.text, remove)
                    if remove:
                        total_lines_counter += len(f.text.split('\n'))
                    if f.type == FragmentType.EndIfStatement:
                        cond_stack.pop()
        except:
            error = True
        return {
            'success': not error,
            'text': text,
            'body_lines': body_lines_counter,
            'total_lines': total_lines_counter
        } if modified else None

    def _patch_cond(self, f):
        cond = Condition.simplify(ConditionAccessor.get(f), self.keys)
        ConditionAccessor.set(f, cond)
        return cond

    @staticmethod
    def _read_encoding(file):
        with open(file, 'rb') as f:
            data = b''.join([f.read()])
        return chardet.detect(data)['encoding']

    @staticmethod
    def _should_remove(cond_stack, frag_type):  # TODO: refactor
        hasCurrentLevelRealCond = False
        for cond in cond_stack[-1]:
            if type(cond) is not bool:
                hasCurrentLevelRealCond = True
        hasFalseCondOnNonLastLevel = False
        for cond in cond_stack[:-1]:
            if cond[-1] is False:
                hasFalseCondOnNonLastLevel = True
        isKeyWord = frag_type is not FragmentType.Body
        if hasFalseCondOnNonLastLevel:
            return True
        elif not isKeyWord and cond_stack[-1][-1] is False:
            return True
        elif frag_type == FragmentType.EndIfStatement and not hasCurrentLevelRealCond:
            return True
        if frag_type == FragmentType.EndIfStatement and hasCurrentLevelRealCond:
            return False
        if isKeyWord and frag_type != FragmentType.EndIfStatement and type(cond_stack[-1][-1]) is bool:
            return True
        return False

    @staticmethod
    def _change_text(text, addon, ignoreAddon):
        return text if ignoreAddon else text + addon
