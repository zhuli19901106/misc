大数据分析与内存计算 期末作业

姓名：朱里
专业：2015级计算机系硕士
学号：2015210959
导师：舒继武教授

写在最前面：运行run-me.sh就能看到结果。前提是你装了python、jdk、hadoop。

请先阅读上层的README文件。

运行须知：
1. cleanup.sh 清除输出文件。
2. run-me.sh 运行hadoop示例，所有内容输出log中。
3. README.txt 你正在看。

相关文件如下：
1. add-line-number.py 给每一行加个行号，为什么要加呢，因为mapreduce会对文件进行split和shuffle，之后你就无法得到行号了。
2. cartesian-product.py 两个数据集的笛卡尔积，也就是两两组合。
3. cartesian-product-multithread.py 上面那个的多核版本。
4. env.sh 用到的一些shell脚本变量在此定义，可以修改。
5. generate-random-dataset.py 生成随机的数据集，参数可以指定。
6. run-an-example.sh 示例脚本。
7. JaccardSimilarity/ mapreduce源码。
8. jaccard-similarity.jar 编译打包的jar文件，用于运行mapreduce。

在Hadoop版本耗时共一天。
