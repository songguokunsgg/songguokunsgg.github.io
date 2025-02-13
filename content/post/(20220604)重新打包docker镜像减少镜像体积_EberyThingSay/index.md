---
title: 重新打包 docker 镜像，减少镜像体积
description: 重新打包 docker 镜像，减少镜像体积
date: 2022-06-04 12:31:22
tags:
- 技术
categories:
- 编程与容器技术
---

docker 最常用的打包命令是 commit，但是这样的打包方式是增量式的（类似 git），也就是说，这个镜像只会越来越大，不会减小，打包次数多了之后，镜像会变得非常大，所以我们可以采用 tar 命令打包基础镜像的方式进行解决。

这样打包后的镜像会将文字编码更改为 POSIX，导致中文无法显示，因此需要将编码更改为 en\_US.utf8，因此需要在容器中提前进行如下两步（archlinux 为例）。

1. 在/etc/profile 中加入以下语句


```
export LANG=en_US.utf8
```
1. 在 ~/.zshrc 中加入


```
source /etc/profile
```
就可以永久解决该问题

1. 进行清理（根据实际情况）


```
clean
```
1. 进入根目录（"cd /"）打包


```
tar --exclude=./proc --exclude=./sys --exclude=./home/jupyter-file -cvf /home/jupyter-file/base_img.tar .
```
--exclude 为排除某个目录

意思是将除了/proc /sys /home 之外的目录打包为 base\_img.tar，放置在某个目录下 5. 导入包


```
cat base_img.tar | docker import - imagename:latest
```
tar 的大小就是镜像的大小，注意里面的排除目录和镜像存放目录的合理选择。

