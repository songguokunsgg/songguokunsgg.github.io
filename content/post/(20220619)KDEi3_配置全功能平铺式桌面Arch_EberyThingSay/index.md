---
title: KDE+i3 配置全功能平铺式桌面（Arch）
description: 本文介绍了如何在 Arch Linux 上配置 KDE 与 i3 结合的平铺式桌面环境。文章详细说明了安装 i3 所需的软件、将 KDE 的窗口管理器从 KWin 更换为 i3 的步骤，以及如何配置 i3 的快捷键、外观和壁纸管理。适合喜欢平铺式窗口管理器且对效率要求高的用户。
date: 2022-06-19 15:38:08
tags:
- 技术
categories:
- 操作系统杂谈
---

**此方法仅适用于 plasma 5.24 及之前的版本，今天是 2022 年 6 月 17 日，最新的 Plasma 5.25.0 已经无法使用这个方法，请不要再继续！！如何查看 plasma 版本：**

```
pacman -S neofetch
neofetch
```
**输出内容中即可看见 plasma 版本**

5.18 内核滚挂之后，我的 i3wm 也跟着挂了，不过所幸我在 gitee 上有配置备份。但之后的一段时间用了 KDE+KWin 的平铺脚本，最开始的体验还不错，但随着时间的推移，一些 bug 开始暴露出来，不禁让我怀念起 i3wm，但是 i3 也有一些显示上的 bug……没办法，我觉得在 KDE 上使用 i3 也许是个不错的选择。

## 判断你是否需要 KDE+i3  
### 适合 i3 的人  
1. 喜欢平铺式窗口管理器
2. 喜欢极简桌面
3. 对效率要求大于美化
4. 不追求边边角角的功能配置
5. 年轻，有精力折腾

### 适合 KDE 的人  
1. 不爱折腾
2. 不喜欢写配置文件
3. 偶尔用用，保留了 win 的使用习惯
4. 不爱用命令行

以上均为我个人瞎 bb，请勿以此人身攻击

### KDE+i3 你将获得  
1. KDE 的全功能（KWin 除外：废话）
2. 完善的平铺式窗口管理器
3. 一些 bug（难免的）
4. 比纯 i3 大得多的内存占用

如果你觉得可以接受，就可以进行下一步了。这里需要说明一下，今天时间为 2022 年 6 月 7 日，高考的第一天，plasma 版本为 5.24.5，如果看到这里你不知道以下名词的概念和区别，请不要再继续


```
plasma kde WM DE 滚挂 平铺 konsole vim
```
## 安装 i3 所需的软件  
KDE 已经自带了不少的系统软件，但是 KDE 的特效合成器与壁纸管理与 i3 是独立的，所以我们需要针对 i3 进行单独配置。主要为以下三个


```
sudo pacman -S i3 picom feh alacritty
```
其中 picom 为特效管理器，管理 i3 的窗口动画，透明等等，feh 则负责管理 i3 的壁纸

其他的软件，例如 wifi 管理，蓝牙，剪切板，应用启动器都在 KDE 中带有了，无需额外配置。还有一个重要的东西是终端，我不喜欢 KDE 的终端 konsole，所以以 alacritty 为例.（konsole 在 i3 中不一定能用，推荐更换 i3 常用的终端，例如 alacritty、kitty、st 等）

还有，选 i3 仓库的时候选 i3-wm , 别选 i3-gaps 否则屏幕周边会有大边框很难看。


```
:: 在组 i3 中有 5 成员：
:: 软件仓库 community
   1) i3-gaps  2) i3-wm  3) i3blocks  4) i3lock  5) i3status

输入某个选择 ( 默认=全部选定 ):2
```
## 将 KDE 的 WM 从 KWin 更换为 i3  
### 添加自启动脚本（适用某个用户）  
在某个位置创建一个 sh 脚本（以/usr/local/）为例


```
vim /usr/local/kde-i3.sh
```
加入 


```
#!/bin/sh 
export KDEWM=/usr/bin/i3
```
添加执行权限


```
sudo chmod +x /usr/local/kde-i3.sh
```
意为将 KDEWM 这个变量设为 /usr/bin/i3

然后将这个脚本添加到 KDE 的开机启动中：

设置—开机与关机—自动启动

然后添加一个软链接


```
cd $HOME/.config/plasma-workspace/env
sudo ln -s /usr/local/kde-i3.sh ./
```
当然也可以一步到位


```
sudo ln -s /usr/local/kde-i3.sh $HOME/.config/plasma-workspace/env/
```
根据官方的说法，这个软链接是为了让这个脚本在会话启动之前执行，但设置里面不提供这个选项了，所以只能通过软链接的方式进行。

### 添加 XSession 会话（用于所有用户）  

```
cd /usr/share/xsessions
```
在不同的发行版中，XSession 文件位置有所不同，需要根据实际情况确定，Arch 下面是这个路径。复制一份 plasma.desktop 文件为 plasma-i3.desktop


```
cp plasma.desktop plasma-i3.desktop
```
打开 plasma-i3.desktop


```
vim plasma-i3.desktop
```
最顶上有如下内容


```
  1 [Desktop Entry]
  2 Type=XSession
  3 Exec=/usr/bin/startplasma-x11
  4 TryExec=/usr/bin/startplasma-x11
  5 DesktopNames=KDE
  6 Name=Plasma (X11)
  7 Name[ar]=ﺏﻻﺰﻣﺍ (ﺎﻜﺳ  )
  8 Name[ast]=Plasma (X11)
  9 Name[az]=Plasma (X11)
 10 Name[ca]=Plasma (X11)
```
需要注意的是 Exec 和 TryExec 所在的两行，将它们修改为


```
  3 Exec=/usr/share/xsessions/start.sh
  4 TryExec=/usr/share/xsessions/start.sh
```
然后编辑 start.sh，加入如下内容


```
#!/bin/sh
export KDEWM=/usr/bin/i3
/usr/bin/startplasma-x11
```
添加执行权限


```
sudo chmod +x start.sh
```
## 配置 i3  
这一步比较复杂，我很想把我的配置贴出来，但是……

gitee 审核不通过！！！（因为我壁纸也放在配置文件夹，全是二次元美少女）

所以这里的话我手动贴一些配置……

i3 的配置文件位于 ~/.config/i3/config

### 配置 config  

```
# i3 配置文件(sukipai)

####################
#   i3wm  基础设置
####################

# 基础按键设置
set $mod Mod4
set $left j
set $right l
set $up i
set $down k

# 标题字体
font pango: Source Code Pro 12

# Title format
title_align center

# Hide borders
hide_edge_borders none
default_border none
default_floating_border none

# default windows layout
workspace_layout tabbed

# i3 gaps
# gaps inner i3

# reload the configuration file
bindsym $mod+Shift+c reload

# restart i3 inplace (can be used to upgrade i3)
bindsym $mod+Shift+r restart

# exit i3 (logs you out of your X session)
# bindsym Mod4+Shift+e exec "i3-nagbar -t warning -f 'pango: Microsoft YaHei 12' -m 'Do you really want to exit i3?' -b 'Yes, exit i3' 'i3-msg exit'"

# Theme colors
# gruvbox theme
# class                   border  backgr. text    indicator
client.focused          #3c3836 #32302f #fabd2f #fabd2f
client.focused_inactive #3c3836 #504945 #d5c4a1 #504945
client.unfocused        #3c3836 #504945 #d5c4a1 #504945
client.urgent           #7c6f64 #fabd2f #3c3836 #fabd2f
```
这一部分主要为外观，说几点：

1. Mod4 指 win 键
2. exit i3 的配置建议注释掉，有 kde 在，我们不需要这个功能，反而给自己找麻烦。

### 配置按键  
仍然是在 config


```
#############
#   快捷键
#############

## application binding
# start a terminal
bindsym $mod+Return exec --no-startup-id alacritty

## i3wm binding
# Use Mouse+$mod to drag floating windows
floating_modifier $mod

# kill focused window
bindsym $mod+Shift+q kill

# change focus
bindsym $mod+$left focus left
bindsym $mod+$down focus down
bindsym $mod+$up focus up
bindsym $mod+$right focus right

# alternatively, you can use the cursor keys:
bindsym $mod+Left focus left
bindsym $mod+Down focus down
bindsym $mod+Up focus up
bindsym $mod+Right focus right

# move focused window
bindsym $mod+Shift+$left move left
bindsym $mod+Shift+$dowm move down
bindsym $mod+Shift+$up move up
bindsym $mod+Shift+$right move right

# alternatively, you can use the cursor keys: bindsym $mod+Shift+Left move left
bindsym $mod+Shift+Down move down
bindsym $mod+Shift+Up move up
bindsym $mod+Shift+Right move right

# split in horizontal orientation
bindsym $mod+h split h

# split in vertical orientation
bindsym $mod+v split v

# enter fullscreen mode for the focused container
bindsym $mod+f fullscreen toggle

# change container layout (stacked, tabbed, toggle split)
bindsym $mod+s layout stacking
bindsym $mod+w layout tabbed
bindsym $mod+e layout toggle split

# toggle tiling / floating
bindsym $mod+Shift+space floating toggle

# change focus between tiling / floating windows
bindsym $mod+space focus mode_toggle

# focus the parent container
bindsym $mod+a focus parent

####################
# Workspace behavier
####################

# set workspace
set $ws1 "1"
set $ws2 "2"
set $ws3 "3"
set $ws4 "4"
set $ws5 "5"
set $ws6 "6"
set $ws7 "7"
set $ws8 "8"
set $ws9 "9"
set $ws10 "10"

# switch to workspace
bindsym $mod+1 workspace number $ws1
bindsym $mod+2 workspace number $ws2
bindsym $mod+3 workspace number $ws3
bindsym $mod+4 workspace number $ws4
bindsym $mod+5 workspace number $ws5
bindsym $mod+6 workspace number $ws6
bindsym $mod+7 workspace number $ws7
bindsym $mod+8 workspace number $ws8
bindsym $mod+9 workspace number $ws9
bindsym $mod+0 workspace number $ws10

# move focused container to workspace
bindsym $mod+Shift+1 move container to workspace number $ws1
bindsym $mod+Shift+2 move container to workspace number $ws2
bindsym $mod+Shift+3 move container to workspace number $ws3
bindsym $mod+Shift+4 move container to workspace number $ws4
bindsym $mod+Shift+5 move container to workspace number $ws5
bindsym $mod+Shift+6 move container to workspace number $ws6
bindsym $mod+Shift+7 move container to workspace number $ws7
bindsym $mod+Shift+8 move container to workspace number $ws8
bindsym $mod+Shift+9 move container to workspace number $ws9
bindsym $mod+Shift+0 move container to workspace number $ws10
```
这一部分就不多说了，基本都是这样配置的。

### 配置 picom 和 feh  
### picom  
还是 config……


```
exec --no-startup-id picom --config ~/.config/i3/picom/picom.conf -b --experimental-backends
```
意思是自启动 picom 并读取位于 ~/.config/i3/picom/picom.conf 的配置文件。


```
# Backend
# glx mode have more performance, prevent tearing
backend = "glx";

# GLX backend
glx-no-stencil = true;
glx-copy-from-front = false;
glx-no-rebind-pixmap = true;
glx-swap-method = -1;
# prevent flickering after wake up
glx-use-copysubbuffer-mesa = true;

# Shadows
shadow = true;
shadow-radius = 50;
shadow-offset-x = -40;
shadow-offset-y = -40;
shadow-opacity = 0.8;

shadow-exclude = [
    "class_g = 'Dunst'",
    "class_g ?= 'polybar'",
    "class_g ?= 'fcitx'",
    "class_g ?= 'fcitx5'",
    "class_g ?= 'rofi'",
    "class_g = 'i3-frame'",
    "window_type = 'dnd'",
    "window_type = 'tooltip'",
    "_GTK_FRAME_EXTENTS@:c",
    "_NET_WM_STATE@:32a *= '_NET_WM_STATE_HIDDEN'",
];

shadow-ignore-shaped = true;

# Opacity
active-opacity = 0.93;
inactive-opacity = 0.85;
frame-opacity = 1;
inactive-opacity-override = false;

# to show inactive windows
inactive-dim = 0.2;

opacity-rule = [
    "75:class_g = 'Dunst'",
    "75:class_g = 'i3-frame'", # fix: i3 titlebar
    "99:class_g = 'Vmware'",
    "99:class_g = 'Shotwell'",
    "99:class_g = 'Google-chrome'",
];

# Fading
fading = true;
fade-delta = 10;

fade-in-step = 0.09;
fade-out-step = 0.09;

fade-exclude = [
#     "class_g = 'Dunst'",
#     "class_g ?= 'Vlc'",
#     "class_g ?= 'Fcitx'",
#     "class_g ?= 'fcitx'",
#     "class_g ?= 'Fcitx5'",
#     "class_g ?= 'fcitx5'",
#     "class_g ?= 'pycharm'",
#     "window_type = 'dnd'",
#     "window_type = 'tooltip'",
#     "_GTK_FRAME_EXTENTS@:c",
];


# Other
mark-wmwin-focused = true;
mark-ovredir-focused = true;
use-ewmh-active-win = true;

detect-rounded-corners = true;
detect-client-opacity = true;

vsync = true;
dbe = false;

unredir-if-possible = false;

focus-exclude = [ ];

detect-transient = true;
detect-client-leader = true;

# Window type settings
wintypes:
{
  tooltip = { fade = true; shadow = true; opacity = 0.9; focus = true;};
  dock = { shadow = false; }
  dnd = { shadow = false; }
  popup_menu = { opacity = 0.9; }
  dropdown_menu = { opacity = 0.9; }
};

# XSync
xrender-sync-fence = true;
```
复制粘贴就行，你也可以自行更改，这个配置还算易读。

### feh  
feh 一次只能设置一张图片，还是 config


```
feh --bg-fill --no-fehbg --randomize ~/.config/i3/wallpapers/src/1.png
```
~/.config/i3/wallpapers/src/1.png 为你的壁纸路径

但我显然不满足于一张图片，我想要切换，所以可以写个脚本，这里我选择 lua 实现，你也可以选择写 bash 脚本


```
vim ~/.config/i3/wallpapers/autochange.lua
```
内容如下


```
function sleep(n)
   os.execute("sleep " .. n)
end

while (true)
do
  os.execute("feh --bg-fill --no-fehbg --randomize ~/.config/i3/wallpapers/src/*")
  sleep(900)
end
```
前提是你得装了 lua 


```
pacman -S lua
```
然后每过 15 分钟就会在 ~/.config/i3/wallpapers/src/\* 下随机选取一张壁纸。

## 重启  
恭喜你，不出意外的话，已经可以使用了。

