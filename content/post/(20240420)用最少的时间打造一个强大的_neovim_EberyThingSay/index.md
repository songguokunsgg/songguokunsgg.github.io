---
title: 用最少的时间打造一个强大的 neovim
description: 用最少的时间打造一个强大的 neovim
date: 2024-04-20 11:38:02
tags:
- 技术
categories:
- 终端与编辑器
---

vim 的作者去世一段时间了，所以我将这篇文章从新组织了一次。2024 年，vim 还是存在一些小问题，在 windows 和 macos 上的体验不太好，所以我现在换用 neovim 了，这套配置还是依然适用，vim 和 neovim。

### 为什么不用 lua 写配置  
以前写过一套 lua 的配置，但是，就这点配置，这点插件，性能差距不大，用 vimscript 写的话，适用性更好，用 vim 和 neovim 的人都能用。

### 适用人群  
简单的代码或者文本编辑，无需将 neovim 配置成 IDE。

### 插件  
配了几个轻量插件，实用性更强，需要安装[https://github.com/junegunn/vim-plug](https://github.com/junegunn/vim-plug)，兼顾了外观和功能。

注意：如果你使用的是 windows 下 git 自带的 vim，则会被认为处在 linux 环境下，安装 vimplug 的目录需要选择 linux 的目录。

把下面的代码放在 ~/.config/nvim/init.vim 里面

vim 的话是 ~/.vimrc


```
let g:iswindows = 0
let g:islinux = 0
if(has("win32") || has("win64") || has("win95") || has("win16"))
        set shell=powershell
        set shellcmdflag=-command
        " 设置默认终端，不然会使用cmd
        let g:iswindows = 1
else
        set encoding=utf-8
        " 编码设置
        let g:islinux = 1
endif
" 首先进行平台判断

if has("gui_running")
        set guifont=Source\ Code\ Pro:h16
endif
" gui判断

" Configuration file for vim
set modelines=0" CVE-2007-2438

" let &t_SI.="\e[5 q" "SI = INSERT mode
" let &t_SR.="\e[4 q" "SR = REPLACE mode
" let &t_EI.="\e[1 q" "EI = NORMAL mode (ELSE)
" 正确设置光标，使用 vim 的话取消注释这三行

syntax on
" 语法高亮

autocmd InsertLeave * se nocul
autocmd InsertEnter * se cul
" 用浅色高亮当前行

set smartindent
" 智能对齐

set autoindent
" 自动对齐

set confirm
" 在处理未保存或只读文件的时候，弹出确认

set tabstop=2
" Tab键的宽度

set softtabstop=4
set shiftwidth=4
"  统一缩进为 4

set noexpandtab
" 不要用空格代替制表符

set number
" 显示行号

set history=50
" 历史纪录数

set hlsearch
set incsearch
" 搜索逐字符高亮

set gdefault
" 行内替换

set langmenu=zn_CN.UTF-8
set helplang=cn
" 语言设置

set cmdheight=2
" 命令行（在状态行）的高度，默认为1,这里是2

set ruler
" 在编辑过程中，在右下角显示光标位置的状态行

set laststatus=2
" 总是显示状态行

set showcmd
" 在状态行显示目前所执行的命令，未完成的指令片段亦会显示出来

set scrolloff=3
" 光标移动到buffer的顶部和底部时保持3行距离

set showmatch
" 高亮显示对应的括号

set matchtime=5
" 对应括号高亮的时间（单位是十分之一秒）

set autowrite
" 在切换buffer时自动保存当前文件

set wildmenu
" 增强模式中的命令行自动完成操作

set linespace=2
" 字符间插入的像素行数目

set whichwrap=b,s,<,>,[,]
" 开启Normal或Visual模式下Backspace键，空格键，左方向键，右方向键，Insert或replace模式下左方向键，右方向键跳行的功能。

filetype plugin indent on
" 分为三部分命令：file on, file plugin on, file indent on.分别表示自动识别文件类型，用文件类型脚本，使用缩进定义文件。

if executable('clipboard-provider')
  let g:clipboard = {
          \ 'name': 'myClipboard',
          \     'copy': {
          \         '+': 'clipboard-provider copy',
          \         '*': 'clipboard-provider copy',
          \     },
          \     'paste': {
          \         '+': 'clipboard-provider paste',
          \         '*': 'clipboard-provider paste',
          \     },
          \ }
endif
" 使用系统剪切板 "+y "+p

" vim-plug 安装
" sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
"   https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
call plug#begin('~/.vim/plugged/')
Plug 'skywind3000/vim-auto-popmenu'
Plug 'skywind3000/vim-dict'
Plug 'preservim/nerdtree'
Plug 'jiangmiao/auto-pairs'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'morhetz/gruvbox'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'skywind3000/asynctasks.vim'
Plug 'skywind3000/asyncrun.vim'
call plug#end()

" 代码补全配置
" 设定需要生效的文件类型，如果是 "*" 的话，代表所有类型
let g:apc_enable_ft = {'*':1}
" 设定从字典文件以及当前打开的文件里收集补全单词，详情看 ':help cpt'
set cpt=.,k,w,b

" 不要自动选中第一个选项。
set completeopt=menu,menuone,noselect

" 禁止在下方显示一些啰嗦的提示
set shortmess+=c

" nerdtree 按F1 打开关闭
map <F1> :NERDTreeToggle<CR>

" 状态栏设置
set laststatus=2  "永远显示状态栏
let g:airline_powerline_fonts = 1  " 支持 powerline 字体
let g:airline#extensions#tabline#enabled = 1 " 显示窗口tab和buffer
let g:airline_theme='molokai'  " murmur配色不错

if !exists('g:airline_symbols')
let g:airline_symbols = {}
endif
let g:airline_left_sep = '▶'
let g:airline_left_alt_sep = '❯'
let g:airline_right_sep = '◀'
let g:airline_right_alt_sep = '❮'
let g:airline_symbols.linenr = '¶'
let g:airline_symbols.branch = '⎇'

" colorscheme pablo
" colorscheme torte
" colorscheme koehler
colorscheme gruvbox
set background=dark
" 设置颜色主题

" 映射两个代码运行的快捷键
let g:asyncrun_open = 10
noremap <silent><C-g> :AsyncTask file-run<cr>
noremap <silent><C-b> :AsyncTask file-build<cr>
```
去掉了快捷键基本上使用默认配置，F1 打开 nerdtree，Ctrl+g 运行当前文件，Ctrl+b 构建当前项目（但针对这一点我不做过多讲解，否则偏离了文章的主题）。使用 gruvbox 主题

更新一版，加入了 gui 和平台特性，因为我要在 win 下用 gvim

再一键安装 Coc 插件，这是我常用的，你可以装自己需要的插件


```
CocInstall coc-html coc-tsserver coc-sumneko-lua coc-sh coc-pyright coc-json coc-clangd
```
然后简单的配置一下 asyncrun, vim ~/.vim/tasks.ini，我常用的语言配置如下：


```
[file-run]
command="$(VIM_FILEPATH)"
command:python=python "$(VIM_FILENAME)"
command:javascript=node "$(VIM_FILENAME)"
command:sh=bash "$(VIM_FILENAME)"
command:lua=lua "$(VIM_FILENAME)"
command:rust=rust "$(VIM_FILENAME)"
output=terminal
cwd=$(VIM_FILEDIR)
save=2
```
这个插件功能十分强大，详情可见[https://github.com/skywind3000/asynctasks.vim](https://github.com/skywind3000/asynctasks.vim)

这样的话，进行一些简易的代码编写和文本编辑都没问题了

### 后话  
我并不建议将 neovim 作为大型项目的编辑器，因为它在项目管理，构建上的配置难度比单文件高得多，插件装得太多也会影响 neovim 本身的性能，所以还是专注于简单文本编辑比较好。如果需要管理大型工程，使用 vs、xcode 等 IDE 是更为明智的选择。

