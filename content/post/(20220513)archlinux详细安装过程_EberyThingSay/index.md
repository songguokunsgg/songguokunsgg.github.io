---
title: 2022.5 archlinux 详细安装过程
description: 本文详细介绍了 2022 年 5 月版本的 Arch Linux 安装过程，涵盖了从系统安装到图形界面配置的各个步骤，特别强调了 UEFI 启动、网络配置、磁盘分区、包管理、引导安装等关键环节，并提供了常见问题的解决方案。文章适合有一定 Linux 基础的用户，建议新手先了解基本概念再尝试。细安装过程
date: 2022-05-13 16:35:20
tags:
- 技术
categories:
- 操作系统杂谈
---

2022 年 12 月 8 日小更新一波

* 增加了 i3 的一些配置说明

---

2022 年 11 月 17 日小更新一波

* 增加了一些双系统相关说明
* 增加了终端字体推荐
* 修改了一些错误内容



---

其实 arch 的安装不是一件很难的事情，但是随着时间的推移会出现一些坑，所以我记录一下安装过程。

参考文章：

[https://zhuanlan.zhihu.com/p/478075538](https://zhuanlan.zhihu.com/p/478075538)本文分为三个部分进行讲解，第一部分是安装整个系统（不带图形界面），第二部分是安装桌面或者窗口管理器，第三部分是进行一些简单配置，第四部分是一些简单总结。

本文讲解虽然较为详细，但是不建议纯小白尝试（跟着来也没啥问题。。。）建议你能够做对下列名词解释再继续：


```
vim neovim nvim NVME SATA BIOS UEFI kernel Nvidia console bash :q ^X ^C
```
如果上述单词中 80% 以上不知道什么意思，建议左转 ubuntu 或者 deepin，对 linux 稍作了解之后再尝试 Arch。

## 1. 系统安装  
### 1.1 进入 live 系统  
其实这个 live 系统和 ubuntu 或者 manjaro 的 live 系统是完全一致的，只是有没有图形界面，以及系统安装程序的区别，在 arch 的 live 系统中，需要我们手动输入命令进行操作。

1. 制作启动盘的过程就不详细说了，建议使用 ventoy 进行制作（我们以 ventoy 为例），避免重复格式化 U 盘的问题，当然，使用 rufus 也是可以的，**不推荐**使用**UltraISO，容易出问题。**
2. 确认系统的引导方式是 UEFI,，如果不是，请进入 BIOS 开启。
3. 插入 U 盘，重启电脑，根据电脑型号按相应的键盘按键进入启动引导选择，选择刚刚 USB 启动器。进入 ventoy 界面，选取你下载的 ArchLinux 安装镜像（\*.iso），进入 Arch 安装界面。
4. 选择画面中的第一项（Arch Linuxinstallmedium(x86\_64,UEFI)），按回车键，待加载完成后，进入 ArchLinux 的 Live 环境。如果出现“root@archiso~#”，说明启动成功，已经进入终端。
5. 验证是否为 UEFI 启动（如果你确定已经是 UEFI 的话可以略过）  
输入“ls /sys/firmware/efi/efivars”  
输入这一行代码后，如果反馈目录不存在，则说明电脑没有以 UEFI 启动，需要重新执行步骤 3，不要继续，因为没有 UEFI 启动在后面写入引导的时候几乎绝对报错。如果有输出，说明电脑是以 UEFI 启动的。

### 1.2 联网  
### arch 的系统镜像只有 800m，并没有包含所有的系统文件，所以网络是必要的。  
### 1.2.1 电脑有 wifi 的情况，跟参考文章中操作一致  
1. 1. 输入“iwctl”进入 iwd 模式，也就是终端最前方有“[iwd]#”字样。
2. 在 iwd 模式下输入“device list”，按回车（按回车是基本操作，所以下文省略），查询电脑的网卡。记住你的网卡号，一般是 wlan0 或者 wlan1（本文以多数情况 wlan0 为例）
3. 在 iwd 模式下输入“station wlan0 scan”，然后再输入“station wlan0 get-networks”，显示周围的 wifi 的 ssid 扫描结果。（如果你知道自己要连接的 wifi 名称，可以跳过这一步）
4. 在 iwd 模式下输入“station wlan0 connect <ssid>”，如果是加密的 wifi，系统会提示输入 wifi 密码，如无意外，就连上网了。
5. 验证联网。按 ctrl+c 退出 iwd 模式，回到[root@archiso~]模式，输入“ping baidu.com”，如果有返回数据，说明已经连上网了。

### 1.2.2 电脑没有 wifi 的情况  
### 这种情况下，usb 无线网卡一般是用不了的，因为 arch 的 iso 中不带有驱动，而网店里的免驱网卡驱动需要在 AUR 里才能找到，因此，只能考虑 USB 共享手机网络，或者连接网线（这个就不多说了）。  
1. （以 iphone 为例）选一根质量好的线，连上电脑的 usb 口即可。
2. 此时手机上会让你信任该设备，信任即可。
3. 打开热点，输入“ping baidu.com”，如果有返回数据，说明已经连上网了。

iphone 设备，以及 usb 接口的驱动在 live 系统中是存在的，所以非常简单，安卓设备也应该是类似的方法。但是有一点大坑需要注意，**usb 接口驱动需要在后续所安装的系统中单独安装，否则，重启之后是连不上手机的。**


```
pacman -S usbmuxd
```
### 1.2.3 更新时间  

```
timedatectl set-ntp true
```
### 1.3 磁盘分区  
以前的 arch 需要使用 fdisk 命令进行分区，劝退了不少人，现在提供了更人性化的 cfdisk 工具进行分区，操作简单很多了，操作过程与参考文章类似。

1. 输入“fdisk -l”，查看硬盘列表，SATA 硬盘或者机械硬盘是/dev/sdX，nvme 固态硬盘则显示/dev/nvme0nX。
2. 认准你想作为系统盘的硬盘（sda 的例子参考文章已经给出，所以我以/dev/nvme0n1 为例），输入“cfdisk /dev/nvme0n1”进入伪图形界面进行分区。
3. 参考划分大小如下



| 分区 | 挂载点 | 我划分的大小，仅供参考 |
| --- | --- | --- |
| /dev/nvme0n1p1 | / | 100g（软件包都会装在根目录，建议大一点） |
| /dev/nvme0n1p2 | /boot/efi | 500m（不要低于 500m） |
| /dev/nvme0n1p3 | /home | 60g（看个人情况，我的文件多为代码，占用空间较小） |
| /dev/nvme0n1p4 | swap | 24g（交换空间，即虚拟内存） |

  
**注意：**

1. **boot 分区一定是挂载到/boot/efi，后续挂载的时候会再提到。**
2. **home 分区在重装系统的时候是可以复用的，建议单独分区以避免丢失文件。**
3. **swap 视自己内存情况而定，一般 <= 电脑内存（我内存 16g，分了 24g swap 好像也没啥）**

### 1.4 分区格式化  
依次输入下面的命令：（需要确认时输入“y”）


```
mkfs.fat -F32 /dev/nvme0n1p2    (boot分区必须使用fat32格式)
mkfs.ext4 /dev/nvme0n1p1    (/ 和 /home 一般使用ext4分区格式)
mkswap /dev/nvme0n1p4    (swap分区使用swap格式)
swapon /dev/nvme0n1p4    (激活swap分区，不激活不会使用这部分空间)
mkfs.ext4 /dev/nvme0n1p3    (/home分区)
```
格式化结束之后，使用 lsblk 命令查看分区是否划分以及格式化正确


```
nvme0n1     259:0    0 476.9G  0 disk
├─nvme0n1p1 259:1    0  59.3G  0 part 
├─nvme0n1p2 259:2    0    24G  0 part 
├─nvme0n1p3 259:3    0 117.9G  0 part 
├─nvme0n1p4 259:4    0   477M  0 part 
```
我这里跟例子分区顺序不太一样，请根据自己实际情况确定。

### 1.5 分区挂载  
基本和参考文章中一样，但是他犯了一个严重错误，**boot 分区一定是挂载到/boot/efi，，而不是/efi**

依次输入下面的命令：


```
mount /dev/nvme0n1p1 /mnt    (将 / 分区挂载到 live系统中的 /mnt 目录，此时 /mnt 目录就是我们所安装系统的 / 目录)
mkdir -p /mnt/boot/efi    (在新系统的 / 目录中新建 efi 文件夹，-p 参数表示递归创建)
mount /dev/nvme0n1p2 /mnt/boot/efi    (将 boot 分区挂载到efi文件夹)
mkdir /mnt/home    (同理，创建home目录)
mount /dev/nvme0n1p3 /mnt/home    (将home分区挂载到home目录)
```
挂载完成之后会变成这样（根据你的实际分区情况显示）


```
nvme0n1     259:0    0 476.9G  0 disk
├─nvme0n1p1 259:1    0  59.3G  0 part /home
├─nvme0n1p2 259:2    0    24G  0 part [SWAP]
├─nvme0n1p3 259:3    0 117.9G  0 part /
├─nvme0n1p4 259:4    0   477M  0 part /boot/efi
```
### 1.6 安装必要的包，并在系统中写入分区表  
跟参考文章类似，但是，如果你使用 usb 分享网络，要多加一个 usbmuxd 包。

换源：很重要，不然等到天荒地老。方法很多，可以直接修改/etc/pacman.d/mirrorlist 文件，也可以直接


```
reflector --country China --age 72 --sort rate --protocol https --save /etc/pacman.d/mirrorlist
```
解决问题，我一般还是手动换，即替换/etc/pacman.d/mirrorlist 中内容为（任选其一，建议第一个）：


```
Server = https://mirrors.bfsu.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.cqu.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.dgut.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.neusoft.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.nju.edu.cn/archlinux/$repo/os/$arch
Server = https://mirror.redrock.team/archlinux/$repo/os/$arch
Server = https://mirrors.sjtug.sjtu.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.xjtu.edu.cn/archlinux/$repo/os/$arch
```
安装基本系统（包括 linux 内核以及基础软件包），这里相比参考文章多给了几个软件包，因为这些对用户来说还是比较重要的，有几种内核可以安装：

* 普通内核 (linux linux-headers)
* lts 稳定版内核 (linux-lts linux-lts-headers)
* zen 内核 (linux-zen,linux-zen-headers)（高性能）

按自己的需求安装就可以

**这里需要提前说一下，linux-zen 内核不支持 nvidia 显卡，有这个需求的就别装了，如果是原版 linux 内核的话，就要做好随时滚挂的准备，最近的 5.18 内核更新就会导致 nvidia-5.15 版本驱动失效无法开机（需要在启动选项中添加 ibt=off），如果你希望稳定使用，就选择 linux-lts 内核和 linux-lts-headers，并安装相应的 nvidia-lts 驱动（后面会有详细说明），不过不用太担心，即便是系统安装完成，你也可以随时切换自己想要的内核版本。**


```
pacstrap /mnt base linux linux-headers linux-firmware base-devel （usbmuxd）
或者
pacstrap /mnt base linux-lts linux-lts-headers linux-firmware base-devel （usbmuxd）
```
写入分区表：


```
genfstab -U /mnt >> /mnt/etc/fstab
```
开机的时候，系统按照 fstab 文件的分区信息进行挂载，你也可以修改 fstab 以达到自动挂载某个磁盘的功能，例如


```
UUID=86ABB6FEAA91229C   /home/XXX/Documents                 ntfs-3g         defaults        0 0
```
就可以把 UUID 为 86ABB6FEAA91229C 的 ntfs 分区挂载到 /home/XXX/Documents 下面（PS：双系统用这个方式挂载 win 盘很爽

然后使用如下命令进入新系统，进入后会显示[root@archiso /]# 。


```
arch-chroot /mnt
```
### 1.7 新系统的配置  
### 1.7.1 安装必要软件包  
参考文章给出的命令如下：


```
pacman -S vim iwd networkmanager ttf-dejavu sudo bluez
```
我解释一下这都是干嘛的。

1. vim：文本编辑器，可替代有 neovim，nano，其中 nano 对新手比较友好，推荐经验较少或者刚入坑的同志使用。
2. iwd,networkmanager：用 iwd 作为 nm 的 backend 进行使用。（但是我这样使用在 i3 下会出现不少问题，比如网络经常自动断，且短时间无法重连等 (KDE 也会出现，但感觉没有 i3 频繁，我觉得可能是命令行的原因，**安装完成之后卸载**掉 networkmanager 问题解决。另外，如果需要使用网线和 usb 网络共享，networkmanager 必须安装，最好加装一个 dhcpcd）
3. ttf-dejavu：开源字体
4. sudo：用于非 root 用户暂时获取 root 权限
5. bluez：蓝牙模块
6. usbmuxd：参考文章没给这个。现在系统中使用的网络来自于 live 系统，不装这个的话，重启是无法通过 usb 连接手机共享网络的，根据个人情况选择，建议安装。
7. wqy-zenhei：中文字体，避免进入系统后无法显示中
8. dhcpcd：连网线用
9. ntfs-3g：挂载 ntfs 磁盘需要

我最后选择这样安装，所以后续以 vim 为例。


```
pacman -S neovim iwd ttf-dejavu sudo bluez usbmuxd networkmanager dhcpcd wqy-zenhei ntfs-3g
```
neovim 和 vim 的启动命令是不一样的，neovim 为“nvim”，vim 是“vim”我一般会通过软链接


```
ln -s /bin/nvim /bin/vim
ln -s /bin/nvim /bin/vi
```
将他们软链接起来看，这样的话，通过“vim”“vi”命令也可以启动 neovim 了。

nano 的启动命令是“nano”

### 1.7.2 一通设置  
这一部分都是差不多的，也没啥坑。

1. 设置时区和时间

依次输入下面的命令：


```
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime    (设置时区为上海)
hwclock --systohc
```
2. 设置语言

输入“vim /etc/locale.gen”，删除【en\_US.UTF-8】和【zh\_CN.UTF-8】两项前面的“#”，保存。（如果有其他语言需求也可以自行取消注释，比如台湾地区和港澳地区）

（vim 的光标移动、删除和保存退出等命令请另行百度），当然，也可以用 nano

输入“locale-gen”，再输入


```
echo LANG=en_US.UTF-8 >> /etc/locale.conf
```
，意思是将 "en\_US.UTF-8" 追加到 /etc/locale.conf 文件里面，这里不建议使用


```
echo LANG=zh_CN.UTF-8 >> /etc/locale.conf
```
这样会使系统语言成为中文，从而导致 tty 显示中文，但是 tty 本身是不支持中文的，所以会乱码。而中文的问题，一般会通过修改 ~/.xprofile（DE）或者 ~/.xinitrc（WM）进行解决

3. 设置 root 用户的密码

输入“passwd”，再输入密码，密码不会有任何显示，但是是输进去了的。

4. 设置主机名（系统名）

输入“echo {你要设置的主机名，随便一个，不要大括号，不要中文名} >> /etc/hostname”，例如


```
echo sukipai >> /etc/hostname
```
主机名会显示在 bash 中，例如


```
[sukipai@sukipai ~]$
```
意为我用 sukipai(前) 用户登陆了名为 sukipai(后) 的主机。

5. 设置网络

输入“vim /etc/hosts”，把下面的文字打进去，保存（以sukipai为例）。（vim的光标移动、删除和保存退出等命令请另行百度。）


```
127.0.0.1 localhost
::1 localhost
127.0.1.1 sukipai.localdomain sukipai
```
### 1.7.3 安装引导并重启系统  
与参考文章中安装引导有一些差异，输入下面的命令：


```
pacman -S grub efibootmgr   (安装grub)
grub-install /dev/nvme0n1    (超级大坑，注意选择的是整个硬盘，而不是boot分区)
```
一定要注意这个地方，是安装在整个磁盘，而不是 boot 分区。

创建 grub 配置文件


```
grub-mkconfig -o /boot/grub/grub.cfg
```
重启系统（请再次确认你是否需要，且已经安装 usbmuxd）：


```
exit    (退出新系统，回到live系统)
umount -R /mnt    (递归卸载 /mnt 中的磁盘)
reboot    (重启)
```
重启之后登录到 root 账户，密码就是你之前设置的。

### 1.8 打开联网服务和蓝牙  
1. 首先激活服务


```
systemctl start iwd.service
systemctl enable iwd.service
systemctl start systemd-resolved.service
systemctl enable systemd-resolved.service
systemctl enable bluetooth.service
systemctl enable NetworkManager
systemctl enable dhcpcd
```
2. 配置网络连接和 DNS

输入“vim /etc/iwd/main.conf”，把下面的文字打进去，保存。


```
[General]
EnableNetworkConfiguration=true
NameResolvingService=systemd
```
3. 安装了 netwokmanager 的配置

如果安装了 networkmanager，则需要将 backend 服务修改为 iwd，总体上 iwd 比 wpa 好用很多。

输入“vim /etc/NetworkManager/NetworkManager.conf”，把下面的文字打进去，保存。（vim的光标移动、删除和保存退出等命令请另行百度。）


```
[device]
wifi.backend=iwd
```
如果只安装 networkmanager 而不安装 iwd 的话，是不需要这一步的，nm 会使用默认的 wpa。（猜测）

然后重启，并安装先前的联网方法进行联网，并**更换 mirrorlist 中的软件源 (如果前面更换过了，这里就不用更换了)**，这里不再赘述。

### 1.9 安装一些硬件设备  
1. CPU 编码


```
pacman -S intel-ucode    (intel的cpu装这个)
pacman -S amd-ucode    (amd的cpu装这个)
```
注意是 **CPU** 编码，不是显卡

2. 显卡驱动


```
pacman -S xf86-video-intel（Intel核心显卡驱动，用Intel核显就装，否则不用装）
pacman -S mesa nvidia(-lts) nvidia-settings nvidia-dkms nvidia-utils nvidia-prime（nvidia显卡驱动，用nvidia显卡就装，否则不用装）
pacman -S xf86-video-amdgpu (AMD显卡驱动，用amd显卡的就装)
```
这里举两个例子，我的笔记本，i7-11 代，搭配 intel 核显以及 3050 显卡，所以安装前两个。我的台式机，e3-1230 垃圾 CPU，搭配 HD6950 显卡，所以装第三个。nvidia-dkms 与 nvidia-lts 不兼容，如果装 lts 驱动的话无需安装 dkms。

**注意：nvidia 驱动的安装与前面选择的内核有关，如果你安装的是 linux-lts 内核，那么需要将 nvidia 更换为 nvidia-lts，linux-zen 不支持 nvidia 显卡（务必对号入座），如果你选择安装新内核，则需要修改一下 ibt=off，否则无法进入系统**

3. 声卡驱动

在我的设备上，只需这样安装


```
pacman -S pipewire (alsa-utils) pipewire-pulse pipewire-jack pipewire-alsa
```
就可以了，使用参考文章中的 pulseaudio 也是可以的。alsa-utils 用于终端下的音量调节，如果你使用 KDE，Gnome 等桌面环境，可以不装这个。

使用 pulseaudio 的话，需要进行一下配置（我没试过），pipewire 则不用：

输入“vim /etc/modprobe.d/disable\_dmic.conf”，把下面的文字打进去，保存。


```
options snd_hda_intel dmic_detect=0
```
### 1.10 创建一个用户  
仍然以 sukipai 为例


```
useradd -m -G wheel -s /bin/bash sukipai    (添加一个名为sukipai的用户进入wheel用户组，并将bash作为启动命令)
passwd sukipai    (设置密码，和设置root是类似的)
```
然后输入


```
visudo
```
如果报错的话 (应该不会)，就改为


```
vim /etc/sudoers
```
找到如下内容，取消掉“# %wheel ALL=(ALL:ALL) ALL”前面的“# ”


```
## User privilege specification
##
root ALL=(ALL:ALL) ALL

## Uncomment to allow members of group wheel to execute any command
# %wheel ALL=(ALL:ALL) ALL

## Same thing without a password
# %wheel ALL=(ALL:ALL) NOPASSWD: ALL
```
这里说一下，取消“# %wheel ALL=(ALL:ALL) NOPASSWD: ALL”前的“# ”也是可以的，区别就在于，取消这一行后，wheel 组的用户使用 sudo 就不用输密码了，**如果你是新手，不建议这么做**，如果你是老鸟，可以考虑取消 NOPASSWD 所在的这一行。（我取消的是 NOPASWD 这行，图方便）

下面还有个 sudo 组的选项，但是我没有试过加入 sudo 组是什么效果，这里就不多说了。

### 1.11 重启系统  

```
reboot
```
此时的系统已经基本可以使用了，但是还没有配置图形界面，如果你不需要图形界面，就只需登陆 sukipai 用户就可以使用了。

## 2. 图形界面安装  
**！！！注意：从这里开始，如果登陆的是普通用户，则所有的 pacman 和 systemctl 都需要 sudo，如果嫌麻烦，可以先在 ~/.bashrc 中添加“alias pacman='sudo pacman'和 alias systemctl='sudo systemctl'”，我这里就不多写 sudo 了。如果提示需要权限，同样加 sudo 即可。所以这部分安装建议登陆 root 用户。**

### 首先需要选择 X11 或者是 Wayland，现在来看 Wayland 是比较先进的，但为了方便和兼容性还是用 X11 吧。  

```
pacman -S xorg
```
这个是必须安装的，后面的 DE 和 WM 都是基于 x 服务。

### 2.1 KDE  
特点：美观，比较稳定，自定义功能强大，配置方便（最推荐）（括号中为推荐的可替代品）


```
pacman -S plasma sddm konsole dolphin kate ark okular spectacle yay
```
plasma：桌面环境

sddm：登录管理器，KDE 配套的

konsole：kde 下的终端，功能多但是比较慢，也可以使用其他终端

（alacritty,kitty）

kate：文本编辑器，很强大，但是资料比较少，需要自己配置。我感觉比 vscode 好用很多，但是没火起来，很可惜。

（vim,neovim,gvim,nano,gedit,sublime,vscode,atom）（sublime,vscode 需要在 AUR 源或者 Clansty 源中安装）

ark：解压与压缩

okular：PDF 查看器

（wps,edge,chrome,zotero……）

spectacle：截图工具，这三件套配合 KDE 很方便

安装完成之后，需要启用 sddm


```
systemctl enable sddm
```
重启即可

### 2.2 Gnome  
特点：自定义功能丰富（但是被阻隔了），


```
pacman -S gnome
systemctl enable gdm
```
重启即可，部分软件仍然可以用上述软件替代

### 2.3 i3  

```
pacman -S xorg-xinit xorg-server    （窗口管理器一般不会使用登陆管理器(dm)，所以xorg-xinit是必要的）
pacman -S i3    (安装i3，或者i3-gaps)
```
由于窗口管理器配置比较复杂，所以这里只讲最基本的安装。

**在此之前，先补充一下用户登陆的时候发生了什么事。**

1. 用户输入账户 sukipai 以及密码，正确。
2. tty 会解释执行用户目录下的 .bashrc 文件（如果你用的 zsh，则读取.zshrc，以此类推），相当于手动执行 source ~/.bashrc，（~ 表示用户目录，我这里为/home/sukipai/）
3. 此时登陆到了 tty1
4. 你想要进入 i3，则需要执行 startx 命令
5. startx 会执行 ~/.xinitrc 中的内容

所以我们的逻辑就很清楚了，如果你想要自动登陆 i3，就需要修改.bashrc 中的逻辑，而 startx 时要做的事情，就需要写在 ~/.xinitrc 文件中。


```
export LANG=zh_CN.UTF-8  # 将语言环境设置为中文
xrdb -merge ~/.Xresources  # 读取~/.Xresources 文件中的信息，我用来修改dpi
exec i3  # 进入i3wm
```
为什么要把“export LANG=zh\_CN.UTF-8”写在 ~/.xinitrc 里面，是因为，如果你不想进入图形界面，那么你就会停留在 tty，而 tty 本身是不支持中文的。此时，LANG 的值仍然是之前所设置的“en\_US.UTF-8”就不会出现乱码的问题，如果把这句话写在 ~/.bashrc 中，那么每次一登陆就会将语言修改为中文，导致 tty 永远处在乱码状态。

说明一下.Xresources 文件，这个文件可以用来调节 dpi（默认 96），适合高分辨率屏幕，加入以下内容即可


```
Xft.dpi: 192
```
里面的数字填 ( 放大倍数 ) \* 96 就可以了，比如 192 就是放到 200%，给个简单参考

* 15.5 寸笔记本，1920x1080，填 144
* 15.5 寸笔记本，2560x1440，填 192
* 如果觉得太大了，可以调小，建议为 25% 的倍数

那么如何设置自动进入 i3 桌面呢？很简单，将一下代码贴在 ~/.bashrc 中即可


```
if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
    exec startx
fi
```
这样我们就拥有了一个 i3wm 了。

## 3. 后续的配置  
KDE,gnome,i3 等桌面环境的配置，就不在这里赘述了，每个人的需求不一样。

### 3.1 中文输入法  
推荐使用 fcitx5


```
sudo pacman -S fcitx5 fcitx5-chinese-addons fcitx5-gtk fcitx5-qt fcitx5-configtool
```
然后添加环境变量


```
sudo vim /etc/environment

GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
INPUT_METHOD=fcitx
SDL_IM_MODULE=fcitx
GLFW_IM_MODULE=ibus
```
然后设置开机启动即可（桌面环境不同，方法也不同），这里提供一个简单的思路。

tty 下面是不需要中文输入法的（也用不了），所以修改 ~/.xinitrc，添加代码


```
fcitx5 -d &    (后台运行fcitx5，且开机自启)
```
wiki 上的描述


```
注意：
如果您使用的桌面环境是兼容 XDG 的（例如 KDE、GNOME、Xfce、LXDE等），则 无需 此步骤（添加自启）。
如果使用i3、awesome等窗口管理器，需要在其脚本中添加 Fcitx5 以实现自启动。例如，如果您使用 i3 或 sway ,可以在配置文件中添加exec --no-startup-id fcitx5 -d
如果使用dwm，则需要添加 autostart 补丁。在 ~/.dwm/autostart.sh 中添加fcitx5 -d
```
根据需求自取即可。

### 3.2 添加 archlinuxcn 源，并配置 yay  
在装系统时我们已经将 /etc/pacman.d/mirrorlist 换为了国内源（有时候会玄学变回国外源，需要自己查看一下），所以只需要添加 archlinuxcn 即可。

使用方法：在 /etc/pacman.conf 文件末尾添加以下两行：


```
[archlinuxcn]
SigLevel = Optional TrustAll
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```
如果 SigLevel 那一行不加，后面安装 archlinuxcn-keyring 时不会报错的话，可以不加，但是我报错了所以加上了。

这里有一个坑，要取消这两行前面的注释，不然有一部分 32 位包无法安装。


```
 84 # [muiltilib]
 85 # Include = /etc/pacman.d/mirrorlist
```
之后安装 archlinuxcn-keyring 包导入 GPG key。


```
sudo pacman -Syyu
sudo pacman -S archlinuxcn-keyring
```
然后运行


```
sudo pacman -S yay
```
安装 yay 即可，现在 yay 不能换国内源了，所以无需多余配置。电信网使用 yay 容易连不上，建议使用联通。

安装终端字体，推荐 nerd-fonts-hack 需要 anchlinuxcn


```
pacman -S nerd-fonts-hack
```
### 3.3 配置 zsh（可选）  
zsh 是一个非常好用的解释器，配置也不复杂。

[Linux 中国：配置一个简洁高效的 Zsh | Linux 中国](https://zhuanlan.zhihu.com/p/345559097)这里就不多赘述，直接开搞


```
sudo pacman -Sy zsh zsh-autosuggestions zsh-syntax-highlighting zsh-theme-powerlevel10k zsh-completions
（安装zsh以及相应组件）
chsh -s /usr/bin/zsh    （修改为默认解释器）
```
然后**把 ~/.bashrc 中的所有内容迁移到 ~/.zshrc** ，没有就自己创建，并加入


```
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme
```
然后重启就可以使用了，可以删除掉 ~/.bashrc 和 ~/.bash\_history 中的内容，因为已经不用了。

再贴一份好用的配置文件，直接复制所有内容到 ~/.zshrc 最后就行了，然后按需修改，主要修改 alias 部分，以及删去 ibus 输入法相关配置。

[zsh 配置文件\_kuikuitage 的博客-CSDN 博客](https://blog.csdn.net/u013566722/article/details/51231818)链接里面的内容不太好复制，我这里直接贴上来吧 (一般来说，alias 和 function 用的比较多，其他内容不改就行)


```
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme

#color{{{
autoload colors && colors

#命令别名 {{{
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
alias ls='ls -a --color=auto'
alias grep='grep --color=auto'

#终端代理
function proxy_on() {
    export http_proxy=http://127.0.0.1:7890
    export https_proxy=$http_proxy
    echo -e "终端代理已开启。"
}

function proxy_off(){
    unset http_proxy https_proxy
    echo -e "终端代理已关闭。"
}

for color in RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
	eval _$color='%{$terminfo[bold]$fg[${(L)color}]%}'
	eval $color='%{$fg[${(L)color}]%}'
	(( count = $count + 1 ))
done
FINISH="%{$terminfo[sgr0]%}"
#}}}

#命令提示符
RPROMPT=$(echo "$RED%D %T$FINISH")
PROMPT=$(echo "$CYAN%n@$YELLOW%M:$GREEN%/$_YELLOW>$FINISH ")

#PROMPT=$(echo "$BLUE%M$GREEN%/
#$CYAN%n@$BLUE%M:$GREEN%/$_YELLOW>>>$FINISH ")
#标题栏、任务栏样式{{{
case $TERM in (*xterm*|*rxvt*|(dt|k|E)term)
	precmd () { print -Pn "\e]0;%n@%M//%/\a" }
	preexec () { print -Pn "\e]0;%n@%M//%/\ $1\a" }
	;;
esac
#}}}

#编辑器
export EDITOR=vim
#关于历史纪录的配置 {{{
#历史纪录条目数量
export HISTSIZE=10000
#注销后保存的历史纪录条目数量
export SAVEHIST=10000
#历史纪录文件
export HISTFILE=~/.zhistory
#以附加的方式写入历史纪录
setopt INC_APPEND_HISTORY
#如果连续输入的命令相同，历史纪录中只保留一个
setopt HIST_IGNORE_DUPS
#为历史纪录中的命令添加时间戳
setopt EXTENDED_HISTORY      

#启用 cd 命令的历史纪录，cd -[TAB]进入历史路径
setopt AUTO_PUSHD
#相同的历史路径只保留一个
setopt PUSHD_IGNORE_DUPS

#在命令前添加空格，不将此命令添加到纪录文件中
#setopt HIST_IGNORE_SPACE
#}}}

#每个目录使用独立的历史纪录{{{
cd() {
	builtin cd "$@"                             # do actual cd
	fc -W                                       # write current history  file
	local HISTDIR="$HOME/.zsh_history$PWD"      # use nested folders for history
	if  [ ! -d "$HISTDIR" ] ; then          # create folder if needed
		mkdir -p "$HISTDIR"
	fi
	export HISTFILE="$HISTDIR/zhistory"     # set new history file
	touch $HISTFILE
	local ohistsize=$HISTSIZE
	HISTSIZE=0                              # Discard previous dir's history
	HISTSIZE=$ohistsize                     # Prepare for new dir's history
	fc -R                                       #read from current histfile
}
mkdir -p $HOME/.zsh_history$PWD
export HISTFILE="$HOME/.zsh_history$PWD/zhistory"

function allhistory { cat $(find $HOME/.zsh_history -name zhistory) }
function convhistory {
	sort $1 | uniq |
		sed 's/^:[0−9]∗:[0-9]*;.∗/\1::::::\2/' |
		awk -F"::::::" '{ $1=strftime("%Y-%m-%d %T",$1) "|"; print }'
	}
	#使用 histall 命令查看全部历史纪录
	function histall { convhistory =(allhistory) |
		sed '/^.\{20\} *cd/i\\' }
			#使用 hist 查看当前目录历史纪录
			function hist { convhistory $HISTFILE }

#全部历史纪录 top50
function top50 { allhistory | awk -F':[ 0-9]*:[0-9]*;' '{ $1="" ; print }' | sed 's/ /\n/g' | sed '/^$/d' | sort | uniq -c | sort -nr | head -n 50 }

#}}}

#杂项 {{{
#允许在交互模式中使用注释  例如：
#cmd #这是注释
setopt INTERACTIVE_COMMENTS      

#启用自动 cd，输入目录名回车进入目录
#稍微有点混乱，不如 cd 补全实用
setopt AUTO_CD

#扩展路径
#/v/c/p/p => /var/cache/pacman/pkg
setopt complete_in_word

#禁用 core dumps
limit coredumpsize 0

#Emacs风格 键绑定
bindkey -e
#bindkey -v
#设置 [DEL]键 为向后删除
#bindkey "\e[3~" delete-char

#以下字符视为单词的一部分
WORDCHARS='*?_-[]~=&;!#$%^(){}<>'
#}}}

#自动补全功能 {{{
setopt AUTO_LIST
setopt AUTO_MENU
#开启此选项，补全时会直接选中菜单项
#setopt MENU_COMPLETE

autoload -U compinit
compinit

#自动补全缓存
#zstyle ':completion::complete:*' use-cache on
#zstyle ':completion::complete:*' cache-path .zcache
#zstyle ':completion:*:cd:*' ignore-parents parent pwd

#自动补全选项
zstyle ':completion:*' verbose yes
zstyle ':completion:*' menu select
zstyle ':completion:*:*:default' force-list always
zstyle ':completion:*' select-prompt '%SSelect:  lines: %L  matches: %M  [%p]'

zstyle ':completion:*:match:*' original only
zstyle ':completion::prefix-1:*' completer _complete
zstyle ':completion:predict:*' completer _complete
zstyle ':completion:incremental:*' completer _complete _correct
zstyle ':completion:*' completer _complete _prefix _correct _prefix _match _approximate

#路径补全
zstyle ':completion:*' expand 'yes'
zstyle ':completion:*' squeeze-shlashes 'yes'
zstyle ':completion::complete:*' '\\'

#彩色补全菜单
eval $(dircolors -b)
export ZLSCOLORS="${LS_COLORS}"
zmodload zsh/complist
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'

#修正大小写
zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}'
#错误校正
zstyle ':completion:*' completer _complete _match _approximate
zstyle ':completion:*:match:*' original only
zstyle ':completion:*:approximate:*' max-errors 1 numeric

#kill 命令补全
compdef pkill=kill
compdef pkill=killall
zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:*:*:*:processes' force-list always
zstyle ':completion:*:processes' command 'ps -au$USER'

#补全类型提示分组
zstyle ':completion:*:matches' group 'yes'
zstyle ':completion:*' group-name ''
zstyle ':completion:*:options' description 'yes'
zstyle ':completion:*:options' auto-description '%d'
zstyle ':completion:*:descriptions' format $'\e[01;33m -- %d --\e[0m'
zstyle ':completion:*:messages' format $'\e[01;35m -- %d --\e[0m'
zstyle ':completion:*:warnings' format $'\e[01;31m -- No Matches Found --\e[0m'
zstyle ':completion:*:corrections' format $'\e[01;32m -- %d (errors: %e) --\e[0m'

# cd ~ 补全顺序
zstyle ':completion:*:-tilde-:*' group-order 'named-directories' 'path-directories' 'users' 'expand'
#}}}

##行编辑高亮模式 {{{
# Ctrl+@ 设置标记，标记和光标点之间为 region
zle_highlight=(region:bg=magenta #选中区域
	special:bold      #特殊字符
	isearch:underline)#搜索时使用的关键字
	#}}}

##空行(光标在行首)补全 "cd " {{{
user-complete(){
case $BUFFER in
	"" )                       # 空行填入 "cd "
		BUFFER="cd "
		zle end-of-line
		zle expand-or-complete
		;;
	"cd --" )                  # "cd --" 替换为 "cd +"
		BUFFER="cd +"
		zle end-of-line
		zle expand-or-complete
		;;
	"cd +-" )                  # "cd +-" 替换为 "cd -"
		BUFFER="cd -"
		zle end-of-line
		zle expand-or-complete
		;;
	* )
		zle expand-or-complete
		;;
esac
}
zle -N user-complete
bindkey "\t" user-complete
#}}}

##在命令前插入 sudo {{{
#定义功能
sudo-command-line() {
[[ -z $BUFFER ]] && zle up-history
[[ $BUFFER != sudo\ * ]] && BUFFER="sudo $BUFFER"
zle end-of-line                 #光标移动到行末
}
zle -N sudo-command-line
#定义快捷键为： [Esc] [Esc]
bindkey "\e\e" sudo-command-line
#}}}
#[Esc][h] man 当前命令时，显示简短说明
alias run-help >&/dev/null && unalias run-help
autoload run-help

#历史命令 top10
alias top10='print -l  ${(o)history%% *} | uniq -c | sort -nr | head -n 10'
#}}}

#路径别名 {{{
#进入相应的路径时只要 cd ~xxx
hash -d A="/media/ayu/dearest"
hash -d H="/media/data/backup/ayu"
hash -d E="/etc/"
hash -d D="/home/ayumi/Documents"
#}}}

##for Emacs {{{
#在 Emacs终端 中使用 Zsh 的一些设置 不推荐在 Emacs 中使用它
#if [[ "$TERM" == "dumb" ]]; then
#setopt No_zle
#PROMPT='%n@%M %/
#>>'
#alias ls='ls -F'
#fi
#}}}

#{{{自定义补全
#补全 ping
zstyle ':completion:*:ping:*' hosts 192.168.1.{1,50,51,100,101} www.google.com

#补全 ssh scp sftp 等
#zstyle -e ':completion::*:*:*:hosts' hosts 'reply=(${=${${(f)"$(cat {/etc/ssh_,~/.ssh/known_}hosts(|2)(N) /dev/null)"}%%[# ]*}//,/ })'
#}}}

#{{{ F1 计算器
arith-eval-echo() {
LBUFFER="${LBUFFER}echo \$(( "
RBUFFER=" ))$RBUFFER"
}
zle -N arith-eval-echo
bindkey "^[[11~" arith-eval-echo
#}}}

####{{{
function timeconv { date -d @$1 +"%Y-%m-%d %T" }

# }}}

zmodload zsh/mathfunc
autoload -U zsh-mime-setup
zsh-mime-setup
setopt EXTENDED_GLOB
#autoload -U promptinit
#promptinit
#prompt redhat

setopt correctall
autoload compinstall

#漂亮又实用的命令高亮界面
setopt extended_glob
TOKENS_FOLLOWED_BY_COMMANDS=('|' '||' ';' '&' '&&' 'sudo' 'do' 'time' 'strace')

recolor-cmd() {
region_highlight=()
colorize=true
start_pos=0
for arg in ${(z)BUFFER}; do
	((start_pos+=${#BUFFER[$start_pos+1,-1]}-${#${BUFFER[$start_pos+1,-1]## #}}))
	((end_pos=$start_pos+${#arg}))
	if $colorize; then
		colorize=false
		res=$(LC_ALL=C builtin type $arg 2>/dev/null)
		case $res in
			*'reserved word'*)   style="fg=magenta,bold";;
			*'alias for'*)       style="fg=cyan,bold";;
			*'shell builtin'*)   style="fg=yellow,bold";;
			*'shell function'*)  style='fg=green,bold';;
			*"$arg is"*)
				[[ $arg = 'sudo' ]] && style="fg=red,bold" || style="fg=blue,bold";;
			*)                   style='none,bold';;
		esac
		region_highlight+=("$start_pos $end_pos $style")
	fi
	[[ ${${TOKENS_FOLLOWED_BY_COMMANDS[(r)${arg//|/\|}]}:+yes} = 'yes' ]] && colorize=true
	start_pos=$end_pos
done
}
check-cmd-self-insert() { zle .self-insert && recolor-cmd }
check-cmd-backward-delete-char() { zle .backward-delete-char && recolor-cmd }

zle -N self-insert check-cmd-self-insert
zle -N backward-delete-char check-cmd-backward-delete-char
```
### 3.4 安装必要软件  
这个就自己按需安装了，根据评论区建议，可以添加一个 pacman.ltd 源，里面有很多常用的软件，matlab 和 mathmatica 都有，直接 "vim /etc/pacman.conf"，在后面添加：


```
[Clansty]
SigLevel = Never
Server = https://repo.lwqwq.com/archlinux/$arch
Server = https://pacman.ltd/archlinux/$arch
Server = https://repo.clansty.com/archlinux/$arch
```
vscode、matlab、texlive-full 之类的东西都可以直接 pacman 安装了。

## 4 总结  
本来没想要写这么多的，但是写了就。。。。。应该还算比较详细了，罗列了很多教程里面的坑，资料来源几乎都是 wiki，流程主要参考开头的文章，希望可以帮助到大家。我很喜欢 archlinux，能高兴能出一份力。

然后总结一下需要注意的坑点

* pacman 务必先换源
* 如果需要有线网和 usb 共享的话，iwd 和 networkmanager 必须安装，且在第一次重启之前装好。如果只需要无线网，可以卸载 networkmanager，只使用 iwd
* grub-install 是对整个硬盘，不是 boot 分区
* KDE 有些组件比较臃肿，是可以替换的。
* 输入法不要再用旧版的 fcitx4
* boot 分区挂载到 /boot/efi 而不是 /efi
* usb 共享网络安装时，提前安装好 usbmuxd，networkmanager
* 如果需要开启 sshd 服务，请使用 sudo systemctl enble sshd，否则别人连不上你电脑
* dhcpcd 是网线用户需要安装的必备组件
* 不取消注释 /etc/pacman.conf 中的 [multilib] 行，virtualbox 装不上。
