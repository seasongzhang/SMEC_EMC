import os
import codecs


class Chker:
    def __init__(self, prt_path):
        self.txt_path = os.path.join(prt_path, "txt")
        self.txt_list = ['project.txt', 'parts.txt', 'actions.txt', 'steps.txt']
        self.txt_set = set(self.txt_list)
        self.txt_format = {self.txt_list[0]: ['project_date', 'project_description', 'project_summary'],
                           self.txt_list[1]: ['part_number', 'part_name', 'part_description'],
                           self.txt_list[2]: ['action_number', 'action_description'],
                           self.txt_list[3]: ['step_sequence', 'step_ref', 'step_description', 'step_reason',
                                              'step_outputfile', 'step_result', 'step_summary']}

    def txt_exist(self):
        try:
            txt_list = os.listdir(self.txt_path)
            # txt_list = ['project.txt', 'parts.txt', 'actions.txt', 'teps.txt']
        except WindowsError:
            print("Error: directory 'txt' missing.")
            return False

        def print_txt_state(file_set, state_str):
            for x in file_set:
                print("file %s is " % x + state_str)

        if not self.txt_set == set(txt_list):
            print_txt_state(self.txt_set - set(txt_list), "missing.")
            print_txt_state(set(txt_list) - self.txt_set, "useless.")
            return False
        return True

    def has_right_format(self):
        for txt in self.txt_set:
            with codecs.open(os.path.join(self.txt_path, txt), encoding='utf-8') as f:
                lines = [line for line in f.readlines() if ":" in line]
                for (n, line) in enumerate(lines):
                    txt_format = self.txt_format[txt]
                    if not line.startswith(txt_format[n % len(txt_format)]):
                        print("Wrong format! Line: " + line)
                        return False
        return True

    def txt_checked(self):
        return self.txt_exist() and self.has_right_format()

c = Chker(r"E:\Downloads\CS_JT150795B000G99")
if c.txt_checked():
    print('Pass.')
