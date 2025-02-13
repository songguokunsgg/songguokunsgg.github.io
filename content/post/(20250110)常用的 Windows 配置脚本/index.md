---
title: 常用的 Windows 配置脚本
date: 2025-01-10 14:02:33+0000
tags:
    - 技术
categories:
    - 操作系统杂谈
---

1. 输入法添加小鹤双拼

```powershell
reg add HKCU\Software\Microsoft\InputMethod\Settings\CHS /v UserDefinedDoublePinyinScheme0 /t REG_SZ /d "小鹤双拼*2*^*iuvdjhcwfg^xmlnpbksqszxkrltvyovt" /f
```

2. 右键菜单改为 win10 样式

```powershell
reg add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f
taskkill /F /IM explorer.exe
explorer.exe
```

未完待续……