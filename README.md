# SMEC_EMC_FIG
To extract data from figs saved in EMC report fig. The data could be stored and used to draw more complex figs for research, most of time for comparison of different EMC actions. 
EMC实验室在扫频之后，利用购买的软件生成word报告，只能提供频谱图，不能提供对应频谱图的数据，因此，需要脚本从word中的图片中读取数据，以期在后期数据分析中能有更大的灵活性。

由于从.dat文件中读取数据解码的尝试失败，因此只剩下在word中的png图中通过分析像素的办法读取数据的途径。

目前对本项目的功能要求如下：
1.根据给定的目录，分析目录中的所有png文件，选取数据，保存在txt文件中，最后再生成一个包括所有数据的.txt文件，并添加表头；
2.读取EMC测试的部件表、措施表、以及实验数据记录表，判断表中内容的正确，在分析完文件之后，若有问题，给出error report；
3.根据步骤2中的“对比措施”信息，为每次措施生成一张频谱图，作为实验比对，并在频谱图上标明曲线对应的措施；



如果可以的话，尝试考虑：
1.利用脚本从word文件中提取png图片；
2.将功能3中生成的图以及部件表、措施表以及实验措施记录表整理成符合Markdown格式表格，并编译输出。
