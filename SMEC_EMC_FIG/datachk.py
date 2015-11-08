# -*-coding:utf-8-*-
import os
import codecs


class DataChecker(object):
    """
        This class if used for 
    """

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def check(self, file_name, *args):
        """
            Check file format.
            :param args: a list, in which sequence the raw data txt is listed.
            :param file_name: the raw data txt file name.
        """

        if os.path.exists(os.path.join(self.dir_path, file_name)):
            items = []
            with codecs.open(os.path.join(self.dir_path, file_name), encoding='utf-8') as f:
                lines = [line for line in f.readlines() if not line == "\r\n"]
                for (n, line) in enumerate(lines):
                    try:
                        assert line.startswith(args[n % len(args)])
                    except AssertionError:
                        print("Wrong format of data in " + file_name + ", number " + str((n % len(args)) + 1))
                    else:
                        items.append(line.split(":")[1].strip())
            items = [items[n:n + len(args)] for n in xrange(0, len(items), len(args))]
            return items
        else:
            print(file_name + " does not exist. Creat one.")
            with codecs.open(os.path.join(self.dir_path, file_name), "w", encoding='utf-8') as f:
                for n in range(10):
                    for s in args:
                        f.write(s + ":\r\n")
                    f.write("\r\n")
            return []

    def allcheck(self):
        self.parts = self.check("parts.txt", "part_number", "part_name", "part_description", "part_photos")
        self.actions = self.check("actions.txt", "action_number", "action_description", "action_photos")
        self.steps = self.check("steps.txt", "step_sequence", "step_ref", "step_description", "step_reason",
                                "step_outputfile", "step_result", "step_summary", "step_spectrum")
        self.project = self.check("project.txt", "project_date", "project_description", "project_summary")

    def report(self):

        for part in [p[1] for p in self.parts if not p[1]=='']:
            for (n, action) in enumerate(self.actions):
                self.actions[n][1] = action[1].replace(part, '`'+part+'`')

        actions_dict = dict((action[0], action[1]) for action in self.actions)

        with codecs.open(os.path.join(self.dir_path,"report.txt"),"w",encoding='utf-8') as f:
            f.write(u"#测试日期：\r\n" + self.project[0][0] + "\r\n")
            f.write(u"#测试描述：\r\n" + self.project[0][1] + "\r\n")
            f.write(u"#测试总结：\r\n" + self.project[0][2] + "\r\n")
            f.write(u"#测试步骤：\r\n")
            for step in self.steps:
                f.write("####STEP " + step[0] + "\r\n")
                f.write(u"测试条件描述：")
                for d in step[2].split(","):
                    f.write(actions_dict[d] + '~')
                f.write("\r\n")

        with codecs.open(os.path.join(self.dir_path, "report.txt"), "r", encoding='utf-8') as f:
            context = f.read()
            parts_list = [p[0] for p in self.parts]
            for p in parts_list:
                context.replace(p, '`'+p+'`')




if __name__ == "__main__":
    chker = DataChecker(ur"E:\SeaGit\SMEC_EMC_FIG\testdata\MPS1_P1_CAN")
    chker.allcheck()
    chker.report()
