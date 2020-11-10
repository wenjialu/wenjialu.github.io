## Psychological-counseling-system
数据库大作业(SSM框架 数据库为mysql）<br>
一个简易的心理咨询预约系统<br>
前端采用html(bootstrap)+ajax<br>
后端为java的ssm框架<br>
<b>部分呢js和css的引入偷懒了,从之前外包做的网站上直接导入,如果失效了请自行百度下载

#### 启动方式:
- 1.导入到IDEA

- 2.创建你自己的数据库，然后把文件中的sql文件执行即可

- 3.修改jdbc.properties中的配置属性即可

- 4.下载tomcat8.5 直接在IDEA配置运行或者将导出war包丢tomcat运行（IntelliJ IDEA导出war包及Tomcat部署）都可以
- ps。bug：
	- 不支持发行版本，需要改Java版本 [https://blog.csdn.net/weixin\_42301797/article/details/105854002?utm\_medium=distribute.pc\_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.pc\_relevant\_is\_cache&depth\_1-utm\_source=distribute.pc\_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.pc\_relevant\_is\_cache][1]
	- 然后更新整个marven项目 [https://blog.csdn.net/qq\_39751320/article/details/104671112?utm\_medium=distribute.pc\_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-8.pc\_relevant\_is\_cache&depth\_1-utm\_source=distribute.pc\_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-8.pc\_relevant\_is\_cache][2]
		   

  - 环境变量： open \~/.bash\_profile
  - java 安装路径 ：java -verbose

  tomcat教程：https://juejin.im/post/5d6e22dee51d453c12504e59

- 5.启动后访问http://localhost:端口号/index.html

![Image text][image-1]

![Image text][image-2]

![Image text][image-3]



[1]:	https://blog.csdn.net/weixin_42301797/article/details/105854002?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.pc_relevant_is_cache&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.pc_relevant_is_cache
[2]:	https://blog.csdn.net/qq_39751320/article/details/104671112?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-8.pc_relevant_is_cache&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-8.pc_relevant_is_cache

[image-1]:	https://github.com/jsphLim/Psychological-counseling-system/blob/master/docs/1.png?raw=true
[image-2]:	https://github.com/jsphLim/Psychological-counseling-system/blob/master/docs/2.png?raw=true
[image-3]:	https://github.com/jsphLim/Psychological-counseling-system/blob/master/docs/3.png?raw=true