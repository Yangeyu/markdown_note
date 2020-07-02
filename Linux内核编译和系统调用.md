## Linux内核编译与系统调用

### 内核编译

**内核编译是基于`ubuntu-16.04.1-server-amd64.iso`**

1. 基本环境准备

   ```
   安装工具:
   sudo apt install build-essential kernel-package libncurses5-dev libssl-dev
   ```

2. 查看内核版本

   ```
   uname -r 或者 uname -a
   ```

3. 将源码内核解压到指定目录

   ```
   sudo tar -zxvf ... -C /usr/src
   ```

4. 清除残留文件

   ```
   sudo make mrproper
   该命令的功能在于清除当前目录下残留的.config和.o文件，这些文件一般是以前编译时未清理而残留的。
   ```

5. 配置编译选项

   ```
   sudo make menuconfig
   ```

6. 清除编译中间文件

   ```
   sudo make clean
   ```

7. 编译新内核

   ```
   sudo make bzImage
   sudo make modules
   ```

8. 安装模块

   ```
   sudo make modules_install
   ```

9. 安装内核并重启

   ```
   sudo make install
   sudo reboot
   ```

### 增加系统调用

1. 查看系统调用表，并修改

   ```
   sudo vi /usr/src/linux-4.19.25/arch/x86/entry/syscalls/syscall_64.tbl
   ------------------------------
   335	64	pro_name	sys_pro_name
   ```

   ![image-20200702011552096](D:\Repositories\markdown_note\images\image-20200702011552096.png)

   

2. 声明系统调用服务例程

   ```
   sudo vi /usr/src/linux-4.19.25/include/linux/syscalls.h
   ----------------------------------------
   asmlinkage long sys_pro_name(int number);
   ```

3. 实现自己的系统调用服务例程

   ```
   cd /usr/src/linux-4.19.34(换成自己的版本即可)/kernel
   vim sys.c
   ----------------------------------------
   SYSCALL_DEFINE1(pro_name, int, name){}
   ps:1 --> 一个参数
   ```

4. 开始编译内核 --- end











