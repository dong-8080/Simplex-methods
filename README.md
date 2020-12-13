# Simplex-methods
最优化方法课程作业，设计一个可以运行的平台软件，可以选择单纯形法、运输问题求解。

主要算法为单纯形法和表上作业法，分别解决线性规划求最小值与运输问题求解。单纯形法的实现原理参照课本《最优化理论与算法》第三章中单纯形方法计算步骤，算法由自己实现。表上作业法有点复杂，时间紧迫理解不到位（逃课太多没学会-.-），参考自[BON4](https://github.com/BON4/TransportationProblem)，一位来自俄罗斯的选手，夹杂的俄文属实难以理解。

GUI编程一开始考虑使用熟悉的Vue等前端框架做，想了想也没有必要，并且Python提供的numpy可以简化大量数值运算，于是使用Python提供的gui库进行编写。开始看了easygui（项目名称来源，一直没改），过于简介不能满足需求。本项目使用了Tkinter进行GUI编写，找到的参考资料比较少，所以界面没写的花里胡哨的。

在课程作业里写了个小彩蛋嘻嘻。

## 运行
1. 使用jupyter notebook或者jupyter lab打开easygui.ipynb，自上而下运行即可。推荐使用此种方式查看代码，为了方便我使用jupyter lab编写的代码，后来发现代码量多了之后jupyter不如vscode、pycharm等方便，硬着头皮继续用下去了。
2. 下载easygui.py到本地，python easygui.py运行
3. 打开package/dist/easygui/easygui.exe直接运行。此种方式不依赖于环境，因为将py文件及依赖都打包此文件，故package文件会比较大。

## 运行截图
![image](https://github.com/dong-8080/Simplex-methods/blob/main/image/image1.png)
![image](https://github.com/dong-8080/Simplex-methods/blob/main/image/image2.png)
![image](https://github.com/dong-8080/Simplex-methods/blob/main/image/image3.png)

## 注意
* 单纯形法只能求解最小值问题，交作业表示表示就好了，最大值可以转化成最小值。
* 输入时必须按照给定格式输入，系统健壮性基本为0
* 交作业时请改一下界面，不要和我的一样

## 收获
用了Tkinter编写GUI界面，虽然会的不是很多但也有了一些头绪。实现单纯形法的过程中，调用了很多numpy的函数，用python进行数值操作也越来越熟练了，本次作业的最大收获吧。还有，写了2000多字的项目说明，我tm真是个天才，hh。

回想起大二的时候用MFC写元胞自动机，已经过了代码跑起来就会高兴很久的年纪-.-
