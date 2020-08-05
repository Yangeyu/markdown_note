## Linux 服务器配置

### samba服务

1. 安装samba

   ```
   sudo apt install samba samba-common
   ```

2. 建立samba访问目录，并设置目录权限

   ```
   mkdir /home/myshare
   chmode 777 /home/myshare
   ```

3. samba服务添加用户

   ```
   sudo smbpasswd -a test
   ```

4. 配置smb.conf

   ```
   sudo vi /etc/samba/smb.conf
   
   [myshare]
   comment=This is samba dir
   path=/home/myshare
   create mask=0755
   directory mask=0755
   writeable=yes
   valid users=test
   browseable=yes
   ```

5. 重启samba服务

   ```
   sudo /etc/init.d/smbd restart
   ```

6. windows下访问共享目录

   ```
   Win+R 输入\\服务器IP\\myshare
   ```

### NFS服务

1. 安装nfs服务端

   ```
   sudo apt install nfs-kernel-server
   ```

2. 创建目录

   ```
   sudo mkdir -p /mnt/myshare
   ```

3. 使任何客户端可访问

   ```
   sudo chown nobody:nogroup /mnt/myshare
   sudo chmod 755 /mnt/myshare
   ```

4. 配置/etc/exports文件，使任何ip可访问

   ```
   /mnt/myshare *(rw,sync,no_subtree_check)
   
   rw：可读可写
   
   sync：请求或者写入数据时，数据同步写入到NFS server的硬盘中后才会返回
   
   no_root_squash：访问nfs server共享目录的用户如果是root的话，它对该目录具有root权限。
   ```

5. 检查nfs服务目录

   ```
   sudo exportfs -ra (重新加载配置)
   sudo showmount -e (查看共享的目录和允许访问的ip段)
   ```

6. 重启nfs服务

   ```
   sudo /etc/init.d/nfs-kernel-server restart
   ```

7. 安装客户端并测试

   ```
   1. 安装nfs客户端
   	sudo apt install nfs-common
   2. 创建挂载目录
   	sudo mkdir /mnt/share
   3. 查看nfs服务的状态是否为active状态:active(exited)或active(runing)
       systemctl status nfs-kernel-server
   4. 挂载共享目录
   	sudo mount S-nfs-ip:/dir /mnt/share
   ```



### FTP服务

1. 创建用户并设置其家目录

   ```
   adduser ftp
   ```

2. 在/home/ftp下创建共享目录

   ```
   mkdir public
   chmod 777 public
   ```

3. 安装ftp

   ```
   sudo apt install vsftpd
   ```

4. 修改配置文件

   ```
   anonymous_enable=YES
   anon_root=/home/……/ftp
   no_anon_password=YES
   write_enable=YES
   anon_upload_enable=YES
   anon_mkdir_write_enable=YES
   
   //开启ftp用户的访问。指定用户列表
   chroot_local_user=YES
   chroot_list_enable=YES
   chroot_list_file=/etc/vsftpd.chroot_list
   ```

5. 配置登陆用户

   ```
   vim /etc/vsftpd.chroot_list
   输入用户名即可
   
   ```

   

6. 重启服务

   ```
   sudo /etc/init.d/vsftpd restart
   ```

7. ps:[ftp配置](https://www.cnblogs.com/dupengcheng/p/6790143.html)

   

### DNS服务

1. 安装bind9

   ```
   sudo apt install bind9
   //查看版本信息
   dpkg -l bind9
   ```

2. 修改/etc/bind/named.conf.loacl

   ```
   //正向区域
   zone "mytest.com" {
   type master;
   file "db.mytest.com";
   };
   //反向区域
   zone "132.168.192.in-addr.arpa" {
   type master;
   notify no;
   file "reverse/db.132.168.192";
   };
   //132.168.192 指网段
   ```

3. 在/var/cache/bind 下创建db.mytest.com文件

   ```
   sudo cp /etc/bind/db.local db.mytest.com
   ```

   ​		![image-20200701115039721](https://github.com/Yangeyu/markdown_note/blob/master/images/image-20200701115039721.png?raw=true)

4. 在/var/cache/bind/reverse下建立db.132.168.192文件

   ```
   sudo cp /etc/bind/db.127 db.132.168.192
   ```

   ![image-20200701115104709](https://github.com/Yangeyu/markdown_note/blob/master/images/image-20200701115104709.png?raw=true)

5. 重启DNS服务

   ```
   sudo /etc/init.d/bind9 restart
   ```

6. 修改成静态IP地址

   ```
   sudo vi /etc/network/interfaces
   
   # 设置静态IP:
   auto ens37
   iface eth0 inet static
   # 设置本机IP
   address 192.168.132.131
   # 设置子网掩码
   netmask 255.255.255.0
   # 设置网关
   gateway 192.168.132.2
   
   重启网卡
   sudo /etc/init.d/networking  restart
   ```

7. 修改DNS的IP地址

   ```
   sudo vi /etc/resolv.conf
   nameserver ip
   ```

### WEB服务

1. 将Linux版jdk解压到指定目录

   ```
   sudo mkdir /usr/lib/jvm
   tar -zxvf jdk-7u45-linux-x64.tar.gz -C /usr/lib/jvm
   ```

2. 配置环境变量

   ```
   sudo vi /etc/profile
   ---------------------------
   export JAVA_HOME=/usr/lib/jvm/ jdk1.7.0_45
   export JRE_HOME=$JAVA_HOME/jre
   export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH 
   export CLASSPATH=$CLASSPATH:.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
   ---------------------------
   source /etc/profile
   ```

3. 将tomcat解压到指定目录

   ```
   sudo mkdir /usr/local/tomcat7
   sudo -zxvf tomcat... -C /usr/local/tomcat7
   ```

4. 修改apache-tomcat-7.0.47/bin/startup.sh文件

   ```
   JAVA_HOME=/usr/lib/jvm/jdk1.7.0_45
   PATH=$JAVA_HOME/bin:$PATH
   CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
   TOMCAT_HOME=/usr/local/tomcat7/apache-tomcat-7.0.47
   ```

5. 切换到root用户运行

   ```
   su -
   apache-tomcat-7.0.47/bin/startup.sh
   ```

   















 			

