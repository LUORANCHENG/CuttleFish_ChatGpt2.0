# CuttleFish_ChatGpt2.0
> **说在前面**
> 
> 在文库更新规则前，一天最多可以上传100篇文章，最多可以5个账号同时跑，一个月就可以搞到5000多元，部分统计数据如下图(是不是很诱人)
> # <img src="docx/1.jpeg" width="500" >
> 
> 但是，后面百度文库更新了规则(如下图)，现在每天上传文章数量的限制和通过率挂钩了，但是gpt写的文章通过率大约在30%~40%，香饽饽瞬间就变得不香了（f**k，百度你是不是玩不起）
> # <img src="docx/2.jpeg" width="500" >
<div align="center">
  <img src="docx/3.png" width="500" >
  <img src="docx/4.png" width="500" >
  <img src="docx/5.png" width="500" >
  <img src="docx/6.png" width="500" >
  <img src="docx/7.png" width="500" >
</div>

## 如果你可以看到这里，说明你对这个项目还有兴趣(反正我是没啥兴趣了，搞不到大钱哪有兴趣哦)。既然你有兴趣，那我就教你怎么去部署这个项目
前提：1.本项目只适用于windows系统，linux系统用户自己把代码中有关win32的库自己注释掉(不过我想不会有人那么蛋疼用linux系统吧，当然我不是在说我自己)；2.本项目不适合python小白，至少你要会安装python吧(python你都装不明白还是先去把基础搞好)

### 1.安装依赖
```
pip install -r requirements.txt
```

### 2.安装chrome浏览器和chromedriver
安装chrome浏览器就不用我多说了吧(小学生都会)

安装好后查看自己chrome浏览器的版本(如下图)
# <img src="docx/8.png" width="500" >

然后到这个网址下载相应版本的驱动：[chrome驱动](http://chromedriver.storage.googleapis.com/index.html)。到这里就可能有的小伙伴会问了：Oh,shit！这里面怎么只有win32版本的驱动，老子的电脑可是高贵的X64架构的；我的回答是：你就下32位版本的，在64位的电脑上也能用。

然后把chromedriver.exe的地址添加到环境变量path里面

一定要注意的是， 加入环境变量 Path 的，

不是浏览器驱动全路径，比如 d:\tools\chromedriver.exe

而是 浏览器驱动所在目录，比如 d:\tools

而且设置完环境变量后，别忘了重启IDE（比如 PyCharm） 新的环境变量才会生效。

（这一步不再详细讲述，不懂的看这篇教程:[windowns系统chromedriver安装与环境变量配置](https://ceshiren.com/t/topic/21687)

### 3.修改setting.json文件
此文件在conf/目录下





