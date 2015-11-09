# -*-coding:utf-8-*-
import os
import codecs
import re
import numpy
import matplotlib.pyplot as pl
import pickle

import SMEC_EMC_FIG

class ReportMaker(object):
    """
        This class if used for 
    """

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.parts = []
        self.actions = []
        self.steps = []
        self.project = []

    def read_info(self, file_name, *args):
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

    def gather_infos(self):
        self.parts = self.read_info("parts.txt", "part_number", "part_name", "part_description", "part_photos")
        self.actions = self.read_info("actions.txt", "action_number", "action_description", "action_photos")
        self.steps = self.read_info("steps.txt", "step_sequence", "step_ref", "step_description", "step_reason",
                                "step_outputfile", "step_result", "step_summary", "step_spectrum")
        self.project = self.read_info("project.txt", "project_date", "project_description", "project_summary")

    def compare_plot(self):

        with open(ur'E:\SeaGit\SMEC_EMC_FIG\testdata\MPS1_P1_CAN\data' + ur'\decimal_specs.pkl', 'rb') as f:
            specs = pickle.load(f)

        if not len(specs) == len(self.steps):
            print("Steps number is different from spectrum data number!!!")

        for (n, step) in enumerate(self.steps):
            compare_list = step[1].split(',')
            pl.figure()
            plot_name = self.dir_path + ur'\photos\STEP_' + str(n+1) + ur'.png'
            plot_data = list(numpy.transpose(specs[n]))
            pl.semilogx(plot_data[0], plot_data[1], label=u'STEP'+str(n+1), basex=10)
            if not compare_list == [u'']:
                for c in compare_list:
                    plot_data = list(numpy.transpose(specs[int(c)-1]))
                    pl.semilogx(plot_data[0], plot_data[1], label=u'STEP'+str(int(c)), basex=10)
            pl.title("STEP"+str(n+1))
            pl.xlim(plot_data[0][0], plot_data[0][-1])
            pl.ylim(-20,100)
            pl.axhline(y=46, xmin=0, xmax=0.8846, color='r')
            pl.axhline(y=53, xmin=0.8846, xmax=1, color='r')
            pl.axvline(x=230, ymin=0.55, ymax=0.6083, color='r')
            pl.xlabel("Frequency")
            pl.ylabel("Level")
            pl.grid(b=True, which='both')
            pl.legend()
            pl.savefig(plot_name)

    def make_markdown(self):

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
            f.write(u"##1.测试日期：\r\n" + self.project[0][0] + "\r\n")
            f.write(u"##2.测试描述：\r\n" + self.project[0][1] + "\r\n")
            f.write(u"##3.测试总结：\r\n" + self.project[0][2] + "\r\n")
            f.write(u"##4.测试步骤：\r\n")
            for step in self.steps:
                f.write("####STEP " + step[0] + "\r\n")
                f.write(u"- **测试条件描述：**")
                for d in step[2].split(","):
                    f.write(actions_dict[d] + '~')
                f.write("\r\n"*2)
                f.write(u'- **步骤依据：**' + step[3] + '\r\n'*2)
                f.write(u'- **测试结果：**' + step[5] + '\r\n'*2)
                f.write(u'- **测试小结：**' + step[6] + '\r\n'*2)
                x = self.dir_path + u'\photos\STEP_' + step[0] + u'.png'
                print(os.path.exists(x))
                if os.path.exists(x):
                    print("Hello!")
                    f.write(u'![STEP' + step[0] + ur'](.\photos\STEP_' + step[0] +u'.png)\r\n')

            f.write(u'___\r\n')
            f.write(u"#部件表：\r\n")
            for part in [p for p in self.parts if p[1] != '']:
                f.write(u'- <span id='+part[1]+u'>`'+part[1]+u'`</span>')
                f.write(u'：' + part[2] + u'\r\n'*2)


if __name__ == "__main__":
    chker = ReportMaker(ur"E:\SeaGit\SMEC_EMC_FIG\testdata\MPS1_P1_CAN")
    chker.gather_infos()
    chker.compare_plot()
    chker.make_markdown()

