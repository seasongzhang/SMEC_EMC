import os
import codecs


class FileChecker:
    def __init__(self, prt_path):

        self.prt_path = prt_path
        self.txt_dir_name = "txt"
        self.txt_path = ""
        self.txt_format = {'project.txt': ['project_date', 'project_description', 'project_summary'],
                           'parts.txt': ['part_number', 'part_name', 'part_description'],
                           'actions.txt': ['action_number', 'action_description'],
                           'steps.txt': ['step_sequence', 'step_ref', 'step_description', 'step_reason',
                                         'step_outputfile', 'step_result', 'step_summary']}
        self.txt_list = self.txt_format.keys()

    def prt_path_exist(self):
        # Check if project dir exist.
        if os.path.exists(self.prt_path):
            return True
        else:
            print("Error: project directory doesn't exist.")
            return False

    def txt_path_exist(self):
        # Check if txt dir exist.
        if self.prt_path_exist():
            self.txt_path = os.path.join(self.prt_path, self.txt_dir_name)
        if os.path.exists(self.txt_path):
            return True
        else:
            print("Error: txt directory doesn't exist.")
            return False

    def txt_files_exist(self):
        # Check if project dir exist.
        if self.txt_path_exist():
            txt_list = os.listdir(self.txt_path)

            # Check if 4 txt_files exist.
            def print_txt_state(file_set, state_str):
                for x in file_set:
                    print("file %s is " % x + state_str)

            if not self.txt_set == set(txt_list):
                print_txt_state(self.txt_set - set(txt_list), "missing.")
                print_txt_state(set(txt_list) - self.txt_set, "useless.")
                return False

            # If all 3 checks above pass, return True
            return True

    def has_right_format(self):
        # Check the format of each txt file according to self.txt_format
        for txt in self.txt_set:
            with codecs.open(os.path.join(self.txt_path, txt), encoding='utf-8') as f:
                lines = [line for line in f.readlines() if ":" in line]
                for (n, line) in enumerate(lines):
                    txt_format = self.txt_format[txt]
                    if not line.startswith(txt_format[n % len(txt_format)]):
                        print("Wrong format! Line: " + line)
                        return False
        return True

    def pass_checked(self):
        return self.txt_files_exist() and self.has_right_format()


c = FileChecker(r"E:\Downloads\CS_JT150795B000G99")
if c.txt_checked():
    print('Pass.')
