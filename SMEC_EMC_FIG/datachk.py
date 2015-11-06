# -*- coding: utf-8 -*-
import os
import codecs

class DataChecker(object):
    """
        This class if used for 
    """
    def __init__(self, dir_path):
        self.dir_path = dir_path


    def check(self,file_name,*args):
        """
            Check file format.
        """

        if os.path.exists(os.path.join(self.dir_path,file_name)):
            items = []
            with codecs.open(os.path.join(self.dir_path,file_name),encoding='utf-8') as f:
                lines = [line for line in f.readlines() if not line=="\r\n"]
                index = 0
                for (n,line) in enumerate(lines):
                    try:
                        assert line.startswith(args[n % len(args)])
                    except AssertionError:
                        print("Wrong format of data in " + file_name + ", number " + str((n % len(args))+1))
                    else:
                        items.append(line.split(":")[1].strip())
            items = [items[n:n+len(args)] for n in xrange(0,len(items),len(args))]                              
            return items
        else:
            print(file_name + " does not exist. Creat one.")
            with codecs.open(os.path.join(self.dir_path,file_name),"w",encoding='utf-8') as f:
                for n in range(10):
                    for s in args:
                        f.write(s+":\r\n")
                    f.write("\r\n")
            return []

    def allcheck(self):
        self.parts = self.check("parts.txt","part_number","part_name","part_description","part_photos")
        self.actions = self.check("actions.txt","action_number","action_description","action_photos")
        self.steps = self.check("steps.txt","step_sequence","step_ref","step_description","step_reason","step_outputfile","step_result","step_summary","step_spectrum")
        self.project = self.check("project.txt","project_date","project_description","project_summary")

    def report(self):

        actions_dict = dict((action[0],action[1]) for action in self.actions)

        steps_number = len(self.steps)
        with codecs.open(os.path.join(self.dir_path,"report.txt"),"w",encoding='utf-8') as f:
            f.write(u"#测试日期：\r\n" + self.project[0][0] + "\r\n")
            f.write(u"#测试描述：\r\n" + self.project[0][1] + "\r\n")
            f.write(u"#测试总结：\r\n" + self.project[0][2] + "\r\n" )
            f.write(u"#测试步骤：\r\n")
            for step in self.steps:
                f.write("####STEP " + step[0] + "\r\n")
                f.write(u"测试条件描述：")
                for d in step[2].split(","):
                    f.write(actions_dict[d]+'~')
                f.write("\r\n")

if __name__ == "__main__":
    chker = DataChecker(u"C:\\Users\\zhangx.SMECEIS\\Desktop\\EMC_RECORDS\\MPS1_P1_CAN")
    chker.allcheck()
    chker.report()




