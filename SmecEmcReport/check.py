import os

class Chker:
    def __init__(self, prt_path):
        self.prt_path = prt_path

    def does_txt_exsit(self):
        try:
            txt_list = os.listdir(os.path.join(self.prt_path, "txt"))
        except WindowsError:
            print("Error: directory 'txt' missing.")
            return False
        assert 'project.txt' in txt_list, "project.txt missing."
        assert 'parts.txt' in txt_list, "parts.txt missing."
        assert 'actions.txt' in txt_list, "actions.txt missing."
        assert 'steps.txt' in txt_list, "steps.txt missing."



