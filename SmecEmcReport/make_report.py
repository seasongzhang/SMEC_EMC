# -*-coding:utf-8-*-
import codecs
import os
import re

import matplotlib.pyplot as pl
import numpy

import gather_data


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
        print("Reading information from " + file_name)
        if os.path.exists(os.path.join(self.dir_path, file_name)):
            items = []
            with codecs.open(os.path.join(self.dir_path, file_name), encoding='utf-8') as f:
                lines = [line for line in f.readlines() if (not line == "\r\n") and (not line == "\n")]
                for (n, line) in enumerate(lines):
                    try:
                        assert line.startswith(args[n % len(args)])
                    except AssertionError:
                        print(n, len(args), line)
                        print("Wrong format of data in " + file_name + ", number " + str((n % len(args)) + 1))
                    else:
                        items.append(line.split(":")[1].strip())
            items = [items[n:n + len(args)] for n in xrange(0, len(items), len(args))]
            return items
        else:
            print(file_name + " does not exist. Create one.")
            with codecs.open(os.path.join(self.dir_path, file_name), "w", encoding='utf-8') as f:
                for n in range(10):
                    for s in args:
                        f.write(s + ":\r\n")
                    f.write("\r\n")
            return []

    def gather_infos(self):
        self.parts = self.read_info("parts.txt", "part_number", "part_name", "part_description")
        self.actions = self.read_info("actions.txt", "action_number", "action_description")
        self.steps = self.read_info("steps.txt", "step_sequence", "step_ref", "step_description", "step_reason", "step_outputfile", "step_result", "step_summary")
        self.project = self.read_info("project.txt", "project_date", "project_description", "project_summary")

    def compare_plot(self):

        sr = gather_data.SpecReader()
        specs = sr.gather_specs(self.dir_path + '\data', re_str='.png')

        if not len(specs) == len(self.steps):
            print("Step number in step.txt must be same as number of .png files!!!")

        for (n, step) in enumerate(self.steps):
            compare_list = step[1].split(',')
            pl.figure()
            plot_name = self.dir_path + ur'\images\STEP_' + str(n+1) + ur'.png'
            plot_data = list(numpy.transpose(specs[n]))
            pl.semilogx(plot_data[0], plot_data[1], label=u'STEP'+str(n+1), basex=10)
            if not compare_list == [u'']:
                for c in compare_list:
                    plot_data = list(numpy.transpose(specs[int(c)-1]))
                    pl.semilogx(plot_data[0], plot_data[1], label=u'STEP'+str(int(c)), basex=10)
            pl.title("STEP"+str(n+1))
            pl.xlim(plot_data[0][0], plot_data[0][-1])
            pl.ylim(-20,100)
            pl.xticks([30,40,50,80,100,200,300],['30','40','50','80','100','200','300'])
            pl.yticks([-20,0,20,40,46,53,60,80,100],['-20','0','20','40','46','53','60','80','100'])
            pl.axhline(y=46, xmin=0, xmax=0.8846, color='r')
            pl.axhline(y=53, xmin=0.8846, xmax=1, color='r')
            pl.axvline(x=230, ymin=0.55, ymax=0.6083, color='r')
            pl.xlabel(u"Frequency(MHz)")
            pl.ylabel(u"Level[dB(uV/m)]")
            pl.grid(b=True, which='both')
            pl.legend()
            pl.savefig(plot_name)
            pl.close('all')

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
            # 测试项目描述
            f.write(u"##1.测试日期：\r\n" + self.project[0][0] + "\r\n")
            f.write(u"##2.测试描述：\r\n" + self.project[0][1] + "\r\n")
            f.write(u"##3.测试总结：\r\n" + self.project[0][2] + "\r\n")
            # 测试项目步骤及对比曲线
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
                x = self.dir_path + u'\images\STEP_' + step[0] + u'.png'
                if os.path.exists(x):
                    f.write(u'![STEP' + step[0] + ur'](.\images\STEP_' + step[0] +u'.png)\r\n')

            # 部件表
            f.write(u'___\r\n')
            f.write(u"#部件表：\r\n")
            for part in [p for p in self.parts if p[1] != '']:
                f.write(u'- <span id='+part[1]+u'>`'+part[1]+u'`</span>')
                f.write(u'：' + part[2] + u'\r\n'*2)
                part_photos = [ff for ff in os.listdir(self.dir_path+u'\images') if re.match('part_'+part[0], ff)]
                for (n, pp) in enumerate(part_photos):
                    f.write(u'![part_'+part[0]+'_'+str(n+1)+u'](.\\images\\' + pp + u')\r\n')
                f.write('\r\n'*2)


            # 措施表
            f.write(u'___\r\n')
            f.write(u'#措施表：\r\n')
            for action in [a for a in self.actions if a[1] != '']:
                f.write(u'- ' + action[1] + u'\r\n'*2)
                action_photos = [ff for ff in os.listdir(self.dir_path+u'\images') if re.match('action_'+action[0], ff)]
                for (n, ap) in enumerate(action_photos):
                    f.write(u'![action_'+action[0]+'_'+str(n+1)+u'](.\\images\\' + ap + u')')
                f.write('\r\n'*2)

if __name__ == "__main__":
    chker = ReportMaker(u"C:\\Users\\zhangx.SMECEIS\\Desktop\\EMC_RECORDS\\LEHY-H-SEP")
    chker.gather_infos()
    chker.compare_plot()
    chker.make_markdown()

