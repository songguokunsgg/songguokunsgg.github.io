<img align="right" width="150" alt="logo" src="https://user-images.githubusercontent.com/5889006/190859553-5b229b4f-c476-4cbd-928f-890f5265ca4c.png">

# Hugo 主题 Stack 起始模板

这是一个快速开始模板，用于[Hugo 主题 Stack](https://github.com/CaiJimmy/hugo-theme-stack)。它使用[Hugo 模块](https://gohugo.io/hugo-modules/)功能来加载主题。

它提供了一个基本的主题结构和配置。GitHub 行动已经设置好，可以自动将主题部署到公共 GitHub 页面。此外，还有一个定时任务，每天自动更新主题。

## 开始使用

1. 点击 *Use this template*，并在 GitHub 上创建一个名为 `<username>.github.io` 的仓库。
![步骤 1](https://user-images.githubusercontent.com/5889006/156916624-20b2a784-f3a9-4718-aa5f-ce2a436b241f.png)

2. 一旦仓库创建完成，就为其创建一个 GitHub codespaces。
![创建 codespaces](https://user-images.githubusercontent.com/5889006/156916672-43b7b6e9-4ffb-4704-b4ba-d5ca40ffcae7.png)

3. 完成！您已经准备好了。codespace 已经配置了最新版本的 Hugo extended，只需在终端运行 `hugo server` 即可看到您的新网站。

4. 检查 `config` 文件夹中的配置文件。您可以编辑它们以满足您的需求。确保更新 `config/_default/config.toml` 中的 `baseurl` 属性为您网站的 URL。

5. 打开设置 -> 页面。将构建分支从 `master` 更改为 `gh-pages`。
![构建](https://github.com/namanh11611/hugo-theme-stack-starter/assets/16586200/12c763cd-bead-4923-b610-8788f388fcb5)

6. 一旦您完成编辑网站，只需提交并推送。GitHub 行动将自动将网站部署到与仓库关联的 GitHub 页面。
![GitHub 行动](https://user-images.githubusercontent.com/5889006/156916881-90b8bb9b-1925-4e60-9d7a-8026cda729bf.png)

---

如果您不想使用 GitHub codespaces，您也可以在本地计算机上运行此模板。**您需要在本地安装 Git、Go 和 Hugo extended。**

## 手动更新主题

运行：

```bash
hugo mod get -u github.com/CaiJimmy/hugo-theme-stack/v3
hugo mod tidy
```

> 此起始模板已配置为使用主题的 `v3` 版本。由于 Go 模块的限制，一旦发布了 `v4` 或更高版本的主题，您需要手动更新主题。（修改 `config/module.toml` 文件）

## 部署到其他静态页面托管

如果您想使用其他静态页面托管来构建此网站，您需要确保它们在机器上安装了 Go。

<details>
  <summary>Vercel</summary>

您需要覆盖构建命令以手动安装 Go：

```bash
amazon-linux-extras install golang1.11 && hugo --gc --minify
```

![](https://user-images.githubusercontent.com/5889006/156917172-01e4d418-3469-4ffb-97e4-a905d28b8424.png)

如果您使用的是 Node.js 20，您需要覆盖安装命令以手动安装 Go：

```bash
dnf install -y golang
```

![image](https://github.com/zhi-yi-huang/hugo-theme-stack-starter/assets/83860323/777c1109-dfc8-4893-9db7-1305ec027cf5)

同时确保在环境变量 `HUGO_VERSION` 中指定 Hugo 版本（使用最新版本的 Hugo extended）：

![环境变量](https://user-images.githubusercontent.com/5889006/156917212-afb7c70d-ab85-480f-8288-b15781a462c0.png)
</details>

---

请注意，Markdown 中的图片链接和代码块需要根据实际情况进行调整，以确保它们在中文环境中能够正确显示。