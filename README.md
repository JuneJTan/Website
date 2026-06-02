# SUSTech Academic Website

基于 Django 重构的课题组学术网站，用于替代旧版静态 HTML 页面。项目支持中英文首页、论文成果检索、团队成员展示、Join Us 招聘信息、后台内容维护、图片/附件上传和 BibTeX 论文导入。

## 功能概览

- 中英文双语首页：`/` 和 `/zh/`
- Django 后台管理：`/admin/`
- 教师简介、研究方向、课程、新闻、招聘信息可后台维护
- 团队成员按角色分组展示，支持展开/折叠
- 论文成果支持分类、关键词搜索、年份筛选、分页和每页数量切换
- 支持上传或粘贴 BibTeX 并解析导入论文
- 支持 Windows Server + IIS + Waitress 部署

## 技术栈

- Python 3.10
- Django 5.2
- SQLite
- Waitress
- IIS / URL Rewrite / ARR，生产部署可选

## 项目结构

```text
cms/                 Django 内容管理应用
labsite/             Django 项目配置
assets/              前台静态资源
legacy_reference/    旧网页和提取资料，仅供参考
home.html            前台首页模板
manage.py            Django 管理入口
requirements.txt     Python 依赖
db.sqlite3           本地数据库，通常不建议提交到远程仓库
```

## 本地运行

创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

安装依赖：

```powershell
pip install -r requirements.txt
```

执行数据库迁移：

```powershell
python manage.py migrate
```

收集静态文件：

```powershell
python manage.py collectstatic --noinput
```

启动开发服务器：

```powershell
python manage.py runserver
```

访问：

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/zh/
http://127.0.0.1:8000/admin/
```

## 后台管理

创建超级管理员：

```powershell
python manage.py createsuperuser
```

后台可维护内容包括：

- 站点资料
- 研究方向
- 团队成员
- 论文成果
- 课程
- 新闻动态
- 招聘信息

## Windows Server 部署

使用 Waitress 启动 Django：

```powershell
.\.venv\Scripts\waitress-serve.exe --listen=127.0.0.1:8000 labsite.wsgi:application
```

如果通过 IIS 对外提供访问，推荐结构：

```text
用户 -> IIS:8080 -> Waitress:127.0.0.1:8000
```

IIS 需要安装：

- Static Content
- URL Rewrite
- Application Request Routing

`web.config` 中应将 `/static/` 指向 `staticfiles/`，将其他请求反向代理到 Waitress。

部署后常用命令：

```powershell
python manage.py migrate
python manage.py collectstatic --noinput
```

如果后台登录出现 CSRF 错误，需要在 `labsite/settings.py` 中配置：

```python
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "服务器IP",
]

CSRF_TRUSTED_ORIGINS = [
    "http://服务器IP:8080",
]
```

## Git 建议

建议不要提交以下内容：

```text
.venv/
__pycache__/
staticfiles/
db.sqlite3
media/
*.log
```

日常更新流程：

```powershell
git status
git add .
git commit -m "Update website"
git push
```

服务器同步后执行：

```powershell
git pull
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

然后重启 Waitress 或对应的 Windows 服务。
