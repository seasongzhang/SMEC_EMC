# -*-coding:utf-8-*-
import os
import codecs
import re


class DataChecker(object):
    """
        This class if used for 
    """

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.parts = []
        self.actions = []
        self.steps = []
        self.project = []

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

        # 将措施表中的部件名加``，作为修饰。
        for part in [p[1] for p in self.parts if not p[1]=='']:
            for (n, action) in enumerate(self.actions):
                self.actions[n][1] = action[1].replace(part, '[`'+part+'`](#'+part+')')

        # 将步骤测试结果中的超频记录文字转化为可读问题
        for n in range(len(self.steps)):
            x = re.search('(?P<freq>\(.+\))', self.steps[n][5])
            self.steps[n][5] = re.sub('(?P<freq>\(.+\))', u'PK值超限制的频段：\g<freq>MHz', self.steps[n][5])
            # print(self.steps[n][5])

        actions_dict = dict((action[0], action[1]) for action in self.actions)

        with codecs.open(os.path.join(self.dir_path, "report.md"), "w",encoding='utf-8') as f:
            f.write(u"#1.测试日期：\r\n" + self.project[0][0] + "\r\n")
            f.write(u"#2.测试描述：\r\n" + self.project[0][1] + "\r\n")
            f.write(u"#3.测试总结：\r\n" + self.project[0][2] + "\r\n")
            f.write(u"#4.测试步骤：\r\n")
            for step in self.steps:
                f.write("####STEP " + step[0] + "\r\n")
                f.write(u"- **测试条件描述：**")
                for d in step[2].split(","):
                    f.write(actions_dict[d] + '~')
                f.write("\r\n"*2)
                f.write(u'- **步骤依据：**' + step[3] + '\r\n'*2)
                f.write(u'- **测试结果：**' + step[5] + '\r\n'*2)
                f.write(u'- **测试小结：**' + step[6] + '\r\n'*2)
                x = self.dir_path + u'\photos\step_' + step[0] + u'.png'
                print(os.path.exists(x))
                if os.path.exists(x):
                    print("Hello!")
                    f.write(u'![STEP' + step[0] + ur'](..\testdata\MPS1\_P1\_CAN\photos\step_' + step[0] +u'.png)\r\n')

            f.write(u'___\r\n')
            f.write(u"#部件表：\r\n")
            for part in [p for p in self.parts if p[1] != '']:
                f.write(u'- <span id='+part[1]+u'>`'+part[1]+u'`</span>')
                f.write(u'：' + part[2] + u'\r\n'*2)

if __name__ == "__main__":
    chker = DataChecker(ur"E:\SeaGit\SMEC_EMC_FIG\testdata\MPS1_P1_CAN")
    chker.allcheck()
    chker.report()
