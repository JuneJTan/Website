# 新网页重构内容结构与后台功能草案

## 1. 重构目标

本次重构目标是将 `legacy_reference/OldVersion/index.htm` 中的个人主页与课题组主页内容整理为结构清晰、便于维护、支持后台更新的新网站。

新网站应保留原网页的主要学术内容，包括程庆沙老师个人介绍、课题组信息、招生信息、教学课程、团队成员、论文成果和学术活动等。同时，新网站应提供后台管理功能，使管理员可以通过网页界面上传图片、添加或修改论文、更新人员信息、发布招生信息，而不需要直接编辑 HTML 文件。

## 2. 原网页主要内容迁移范围

### 2.1 首页基础信息

首页应包含以下内容：

- SUSTech 与电子与电气工程系标识
- em+ Lab 标识
- 程庆沙老师姓名、照片、邮箱、ORCID
- 中英文页面切换入口
- 招生入口，包括英文 `Available Positions` 和中文招生信息
- 简短课题组介绍与研究方向摘要

### 2.2 个人简介

保留并重构原网页中的个人经历介绍：

- 教育经历：重庆大学、McMaster University 等
- 工作经历：北京大学、McMaster University、SUSTech、University of Regina 等
- 学术服务：期刊编委、会议组织、TPC、session chair 等
- 学术影响：Space Mapping 相关贡献、Google Scholar 引用信息

该部分建议拆分为：

- Biography
- Academic Experience
- Professional Service
- Research Impact

### 2.3 研究方向

根据原网页内容，研究方向可整理为：

- Space Mapping
- Surrogate Modeling
- Simulation-based Optimization
- Microwave CAD
- Microwave Circuits and Antennas
- EM-based Modeling and Optimization
- Antenna Design and Optimization
- RF/Microwave Engineering

每个研究方向后台应支持维护标题、简介、代表图片、相关论文链接。

### 2.4 教学课程

迁移原网页课程列表，包括：

- Signals and Systems
- Advanced Nonlinear Optimization
- Antenna Theory and Techniques
- Advanced Microwave Engineering
- Engineering Ethics
- Antenna and Wave Propagation
- Nonlinear Optimization
- Microwave Engineering
- Communication Systems II
- Computer Programming / Java Programming
- Advance Technology Lecture Series
- Engineering Graphics

课程页面建议支持：

- 课程名称
- 开课年份
- 课程链接
- 课程简介
- 课件或资料附件上传

### 2.5 团队成员

迁移原网页中的人员分类：

- Research Assistant Professor
- Postdoctoral Fellows
- Current Ph.D. Students
- Ph.D. Graduates
- Current Master Students
- Master Graduates

每位成员建议包含：

- 姓名
- 中文名
- 身份类别
- 入学或毕业年份
- 合作导师信息
- 当前去向
- 个人主页或邮箱
- 照片

### 2.6 论文成果

已从原网页中提取论文成果到 `legacy_reference/extracted_publications/` 文件夹，分类如下：

- Journal Papers: 110 items
- Books and Book Chapters: 4 items
- Conference Proceedings: 135 items
- Workshop and Invited Seminar Presentations: 35 items

新网站应将论文成果作为独立模块维护，至少包含以下分类：

- Journal Papers
- Books and Book Chapters
- Conference Proceedings
- Workshop and Invited Seminar Presentations

每条论文建议包含：

- 标题
- 作者
- 期刊/会议/书籍/研讨会名称
- 年份
- 卷、期、页码
- DOI 或外部链接
- PDF 文件
- 分类
- 是否代表作
- 是否首页展示

前台功能建议：

- 按年份筛选
- 按分类筛选
- 按关键词搜索
- 默认显示最新若干条
- 支持展开全部
- 自动统计各分类数量

### 2.7 招生与岗位

保留原网页中的招生入口，并扩展为可维护模块：

- 招收硕士生
- 招收博士生
- 招收博士后
- 招收工程师
- 英文 Available Positions

每条岗位信息建议包含：

- 岗位标题
- 岗位类别
- 招聘状态
- 工作地点
- 申请要求
- 联系方式
- 发布时间
- 截止时间

## 3. 新网页建议结构

建议采用以下导航结构：

- Home
- Research
- People
- Publications
- Teaching
- News
- Open Positions
- Contact

中文站点对应：

- 首页
- 研究方向
- 团队成员
- 论文成果
- 教学课程
- 新闻动态
- 招生招聘
- 联系方式

## 4. 页面功能设计

### 4.1 首页

首页应作为课题组核心入口，展示：

- 实验室名称与简介
- 程庆沙老师基本信息
- 研究方向摘要
- 最新论文
- 最新新闻
- 招生入口
- 联系方式

### 4.2 Research 页面

展示研究方向、研究项目和代表性成果。

后台应支持新增、编辑、排序、隐藏研究方向。

### 4.3 People 页面

展示当前成员和毕业成员。

前台建议按人员类型分组，后台支持成员排序和状态切换。

### 4.4 Publications 页面

展示所有论文成果。

前台应支持分类、年份、关键词搜索和 PDF/外链访问。

后台应支持单条录入、批量导入、修改、删除、排序和置顶。

### 4.5 Teaching 页面

展示课程列表和课程资源。

后台应支持上传课程资料，例如 PDF、PPT、作业说明等。

### 4.6 News 页面

用于发布课题组新闻，例如论文发表、获奖、会议报告、学生毕业、招生通知。

后台应支持图文编辑、封面图上传和发布时间设置。

### 4.7 Open Positions 页面

展示招生和招聘信息。

后台应支持设置岗位状态，例如 `Open`、`Closed`、`Archived`。

### 4.8 Contact 页面

展示邮箱、地址、学校链接、学院链接、ORCID、Google Scholar 等信息。

## 5. 后台管理功能

### 5.1 用户与权限

建议至少设置两类后台角色：

- Super Admin：拥有全部权限，包括用户管理、网站设置、内容发布
- Editor：可维护论文、人员、新闻、课程和招生信息

可选扩展：

- Reviewer：只能预览和审核内容，不能直接发布

### 5.2 内容管理

后台应支持以下模块：

- 首页内容管理
- 个人简介管理
- 研究方向管理
- 团队成员管理
- 论文成果管理
- 教学课程管理
- 新闻动态管理
- 招生招聘管理
- 联系信息管理
- 图片与文件资源管理

### 5.3 上传功能

后台应支持上传：

- 人员照片
- 实验室图片
- 新闻封面图
- 论文 PDF
- 课程资料
- 招生附件
- Logo 与页面图片

上传要求：

- 限制文件类型，例如 jpg、png、webp、pdf、docx、pptx
- 限制文件大小
- 自动生成安全文件名
- 支持文件预览
- 支持替换和删除
- 支持未使用文件清理

### 5.4 论文批量导入

由于原网页已有大量论文，后台应支持批量导入。

建议支持格式：

- JSON
- CSV
- BibTeX

当前已提取的数据可作为初始导入来源：

- `legacy_reference/extracted_publications/publications.json`
- `legacy_reference/extracted_publications/journal_papers.md`
- `legacy_reference/extracted_publications/books_and_book_chapters.md`
- `legacy_reference/extracted_publications/conference_proceedings.md`
- `legacy_reference/extracted_publications/workshop_invited_seminars.md`

导入后应支持人工校对字段，例如作者、标题、年份、期刊名和 DOI。

### 5.5 中英文内容管理

网站应支持中英文内容。

后台建议每条内容提供：

- 中文标题
- 英文标题
- 中文正文
- 英文正文
- 是否显示中文版本
- 是否显示英文版本

如果某条内容只有英文或中文，应允许单语言发布。

### 5.6 草稿、预览与发布

后台内容状态建议包括：

- Draft
- Published
- Hidden
- Archived

管理员应可以在发布前预览页面效果。

### 5.7 排序与置顶

后台应支持：

- 首页展示顺序
- 人员排序
- 论文置顶
- 新闻置顶
- 研究方向排序
- 招生信息排序

### 5.8 操作记录

后台建议记录：

- 操作人
- 操作时间
- 操作类型
- 修改前后内容摘要

这有助于后续追踪网页内容变更。

## 6. 数据模型建议

### 6.1 Publication

字段建议：

- id
- title
- authors
- publication_type
- venue
- year
- volume
- issue
- pages
- doi
- external_url
- pdf_file
- abstract
- is_featured
- is_visible
- display_order
- created_at
- updated_at

### 6.2 Person

字段建议：

- id
- name_en
- name_cn
- role
- status
- degree
- photo
- email
- homepage
- bio
- supervisor_note
- graduation_year
- current_position
- display_order
- created_at
- updated_at

### 6.3 News

字段建议：

- id
- title_en
- title_cn
- body_en
- body_cn
- cover_image
- publish_date
- is_pinned
- is_visible
- created_at
- updated_at

### 6.4 Course

字段建议：

- id
- name_en
- name_cn
- years
- description_en
- description_cn
- course_url
- files
- is_visible
- display_order

### 6.5 Position

字段建议：

- id
- title_en
- title_cn
- category
- status
- description_en
- description_cn
- requirements_en
- requirements_cn
- contact_email
- publish_date
- deadline
- is_visible

## 7. 技术实现建议

当前项目已创建 Python 3.10.9 虚拟环境并安装 Django，可使用 Django 实现后台管理。

建议技术栈：

- Backend: Django
- Admin: Django Admin 或自定义后台
- Database: SQLite for development, PostgreSQL for production
- Frontend: Django Templates 或独立前端框架
- Static/Media: Django static files + media uploads

优先实现顺序建议：

1. 建立 Django 项目与基础数据库模型
2. 导入论文成果数据
3. 搭建 Publications 前台页面
4. 搭建 People、Teaching、Positions 页面
5. 配置后台上传与编辑功能
6. 增加中英文切换
7. 完成首页与整体样式重构

## 8. 迁移注意事项

- 原网页存在部分 HTML 标签闭合不规范，需要在迁移时清洗。
- 原网页中部分中文内容可能存在编码问题，应统一转换为 UTF-8。
- 论文条目数量较多，建议先导入文本，再逐步补充 DOI、PDF 和外链。
- 图片资源应统一整理到 `media/` 或 `static/` 下，并避免继续使用散落在根目录的图片路径。
- 新网站不应依赖手写表格布局，应改用响应式布局。
- 移动端适配应通过 CSS 实现，而不是运行时重排 HTML 表格。

## 9. 验收标准

初版重构完成后，应满足：

- 原网页主要内容均已迁移到新网站
- 论文成果可以按分类展示
- 后台可以新增、编辑、删除论文
- 后台可以上传图片和 PDF
- 后台可以维护人员、课程、新闻和招生信息
- 网站支持中英文基础内容展示
- 页面在桌面端和移动端均可正常浏览
- 不再需要直接编辑 `index.htm` 来更新主要内容
