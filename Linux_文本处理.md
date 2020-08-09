# Linux_文本处理

## awk

| 条件    | 说明                                                         |
| ------- | :----------------------------------------------------------- |
| BEGIN   | 在 awk 程序一开始，尚未读取任何数据之前执行。BEGIN 后的动作只在程序开始时执行一次 |
| EBD     | 在 awk 程序处理完所有数据，即将结束时执行END 后的动作只在程序结束时执行一次 |
| `> >= ` | 大于 和 大于等于                                             |
| `< <=`  | 小于 和 小于等于                                             |
| `= !=`  | 等于 和 不等于                                               |
| `~ !~`  | 匹配正则表达式和不匹配正则表达式                             |
| /正则/  | 如果在“//”中可以写入字符，则也可以支持正则表达式             |
| -F fs   | 指定输入文件折分隔符，fs是一个字符串或者是一个正则表达式，如-F: |
| -v      | 赋值一个用户定义变量                                         |

#### 基本用法

```shell
log.txt
	2 this is a test
    3 Are you like awk
    This's a test
    10 There are orange,apple,mongo	

```

`awk '{[pattern] action}' {filenames}  # 行匹配语句 awk '' 只能用单引号`

```shell
 $ awk '{print $1,$4}' log.txt
 ---------------------------------------------
 2 a
 3 like
 This's
 10 orange,apple,mongo
 # 格式化输出
 $ awk '{printf "%-8s %-10s\n",$1,$4}' log.txt
 ---------------------------------------------
 2        a
 3        like
 This's
 10       orange,apple,mongo
```

`awk -F  #-F相当于内置变量FS, 指定分割字符`

```shell
# 使用","分割
 $  awk -F, '{print $1,$2}'   log.txt
 ---------------------------------------------
 2 this is a test
 3 Are you like awk
 This's a test
 10 There are orange apple
 # 或者使用内建变量
 $ awk 'BEGIN{FS=","} {print $1,$2}'     log.txt
 ---------------------------------------------
 2 this is a test
 3 Are you like awk
 This's a test
 10 There are orange apple
 # 使用多个分隔符.先使用空格分割，然后对分割结果再使用","分割
 $ awk -F '[ ,]'  '{print $1,$2,$5}'   log.txt
 ---------------------------------------------
 2 this test
 3 Are awk
 This's a
 10 There apple
```

`awk -v  # 设置变量`

```shell
 $ awk -va=1 '{print $1,$1+a}' log.txt
 ---------------------------------------------
 2 3
 3 4
 This's 1
 10 11
 $ awk -va=1 -vb=s '{print $1,$1+a,$1b}' log.txt
 ---------------------------------------------
 2 3 2s
 3 4 3s
 This's 1 This'ss
 10 11 10s
```

###### 过滤

```shell
# 过滤第一列大于2并且第二列等于'Are'的行
$ awk '$1>2 && $2=="Are" {print $1,$2,$3}' log.txt    #命令
#输出
3 Are you
```

###### 正则

```shell
# 输出第二列包含 "th"，并打印第二列与第四列
# ~ 表示模式开始。// 中是模式
$ awk '$2 ~ /th/ {print $2,$4}' log.txt
---------------------------------------------
this a
```

```shell
# 输出包含 "re" 的行
$ awk '/re/ ' log.txt
---------------------------------------------
3 Are you like awk
10 There are orange,apple,mongo
```

```shell
# 模式取反
$ awk '$2 !~ /th/ {print $2,$4}' log.txt
---------------------------------------------
Are like
a
There orange,apple,mongo
$ awk '!/th/ {print $2,$4}' log.txt
---------------------------------------------
Are like
a
There orange,apple,mongo
```

###### 脚本案例

```shell
$ cat score.txt
Marry   2143 78 84 77
Jack    2321 66 78 45
Tom     2122 48 77 71
Mike    2537 87 97 95
Bob     2415 40 57 62
-----------------------------
$ cat cal.awk
#!/bin/awk -f
#运行前
BEGIN {
    math = 0
    english = 0
    computer = 0
 
    printf "NAME    NO.   MATH  ENGLISH  COMPUTER   TOTAL\n"
    printf "---------------------------------------------\n"
}
#运行中
{
    math+=$3
    english+=$4
    computer+=$5
    printf "%-6s %-6s %4d %8d %8d %8d\n", $1, $2, $3,$4,$5, $3+$4+$5
}
#运行后
END {
    printf "---------------------------------------------\n"
    printf "  TOTAL:%10d %8d %8d \n", math, english, computer
    printf "AVERAGE:%10.2f %8.2f %8.2f\n", math/NR, english/NR, computer/NR
}
我们来看一下执行结果：

$ awk -f cal.awk score.txt
NAME    NO.   MATH  ENGLISH  COMPUTER   TOTAL
---------------------------------------------
Marry  2143     78       84       77      239
Jack   2321     66       78       45      189
Tom    2122     48       77       71      196
Mike   2537     87       97       95      279
Bob    2415     40       57       62      159
---------------------------------------------
  TOTAL:       319      393      350
AVERAGE:     63.80    78.60    70.00
```

## sed

| 参数 | 说明                                           |
| ---- | ---------------------------------------------- |
| -e   | 以选项中指定的script来处理输入的文本文件。     |
| -f   | 以选项中指定的script文件来处理输入的文本文件。 |
| -n   | 仅显示script处理后的结果。                     |
| -V   | 显示版本信息。                                 |
|      |                                                |

| 动作      | 说明                                                         |
| --------- | ------------------------------------------------------------ |
| a : 新增  | a 的后面可以接字串，而这些字串会在新的一行出现(目前的下一行)～ |
| c : 取代  | c 的后面可以接字串，这些字串可以取代 n1,n2 之间的行！        |
| d : 删除  | d 后面通常不接任何咚咚                                       |
| i : 插入  | i 的后面可以接字串，而这些字串会在新的一行出现(目前的上一行)； |
| p : 打印  | 将某个选择的数据印出。通常 p 会与参数 sed -n 一起运行        |
| s  : 取代 | 可以直接进行取代的工作, 通常这个 s 的动作可以搭配正规表示法  |
|           |                                                              |

```shell
$ cat testfile #查看testfile 中的内容  
HELLO LINUX!  
Linux is a free unix-type opterating system.  
This is a linux testfile!  
Linux test 
```

#### a动作

```shell
# 在testfile文件的第四行后添加一行，并将结果输出到标准输出
$ sed -e 4a\newline testfile #使用sed 在第四行后添加新字符串  
HELLO LINUX! #testfile文件原有的内容  
Linux is a free unix-type opterating system.  
This is a linux testfile!  
Linux test  
newline 
```

#### d动作

```shell
# 删除第 3 到最后一行 用单引号包含''
nl /etc/passwd | sed '3,$d' 
# 使用正则匹配
nl /etc/passwd | sed  '/root/d'
2  daemon:x:1:1:daemon:/usr/sbin:/bin/sh
3  bin:x:2:2:bin:/bin:/bin/sh
....下面忽略
#第一行的匹配root已经删除了
```

#### c动作

```shell
[root@www ~]# nl /etc/passwd | sed '2,5c No 2-5 number'
1 root:x:0:0:root:/root:/bin/bash
No 2-5 number
6 sync:x:5:0:sync:/sbin:/bin/sync
.....(后面省略).....
```

#### p动作

```shell
[root@www ~]# nl /etc/passwd | sed -n '5,7p'
5 lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
6 sync:x:5:0:sync:/sbin:/bin/sync
7 shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
# 使用正则匹配
nl /etc/passwd | sed '/root/p'
1  root:x:0:0:root:/root:/bin/bash
1  root:x:0:0:root:/root:/bin/bash
2  daemon:x:1:1:daemon:/usr/sbin:/bin/sh
3  bin:x:2:2:bin:/bin:/bin/sh
4  sys:x:3:3:sys:/dev:/bin/sh
5  sync:x:4:65534:sync:/bin:/bin/sync
....下面忽略 
# 如果root找到，除了输出所有行，还会输出匹配行。
# 使用-n的时候将只打印包含模板的行。
nl /etc/passwd | sed -n '/root/p'
1  root:x:0:0:root:/root:/bin/bash
```

#### s动作

```shell
# 搜索/etc/passwd,找到root对应的行，执行后面花括号中的一组命令，
# 每个命令之间用分号分隔，这里把bash替换为blueshell，再输出这行
nl /etc/passwd | sed -n '/root/{s/bash/blueshell/;p;q}'    
1  root:x:0:0:root:/root:/bin/blueshell
```

#### -i 命令

```shell
利用 sed 将 regular_express.txt 内每一行结尾若为 . 则换成 !
[root@www ~]# sed -i 's/\.$/\!/g' regular_express.txt
[root@www ~]# cat regular_express.txt 
runoob!
google!
taobao!
facebook!
zhihu-
weibo-
----------------------------------------------------------
# 利用 sed 直接在 regular_express.txt 最后一行加入 # This is a test:
# 由於 $ 代表的是最后一行，而 a 的动作是新增，因此该文件最后新增 # This is a test！
[root@www ~]# sed -i '$a # This is a test' regular_express.txt
[root@www ~]# cat regular_express.txt 
runoob!
google!
taobao!
facebook!
zhihu-
weibo-
# This is a test
```



#### 多点编辑

```shell
nl /etc/passwd | sed -e '3,$d' -e 's/bash/blueshell/'
1  root:x:0:0:root:/root:/bin/blueshell
2  daemon:x:1:1:daemon:/usr/sbin:/bin/sh

# -e表示多点编辑，第一个编辑命令删除/etc/passwd第三行到末尾的数据
# 第二条命令搜索bash替换为blueshell
```

## grep

| 参数 | 说明                                                   |
| ---- | ------------------------------------------------------ |
| -A   | 除了显示符合范本样式的那一列之外，并显示该行之后的内容 |
| -i   | 忽略字符大小写的差别                                   |
| -v   | 显示不包含匹配文本的所有行                             |
| -w   | 只显示全字符合的列                                     |
| -n   | 在显示符合样式的那一行之前，标示出该行的列数编号       |
| -r   | 递归查询文件                                           |

```shell
# 查找指定目录/etc/acpi 及其子目录（如果存在子目录的话）下所有文件中包含字符串"update"的文件，并打印出该字符串所在行的内容
grep -r update /etc/acpi 
```

## cut

| 参数 | 说明                       |
| ---- | -------------------------- |
| -c   | 以字符为单位进行分割       |
| -d   | 自定义分隔符，默认为制表符 |
| -f   | 显示列数                   |
| 示例 | cut -d: -f1,2 log.txt      |
|      |                            |

