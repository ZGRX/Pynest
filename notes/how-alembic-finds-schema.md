# Alembic 是怎么知道要建哪些表的？

在 PyNest 中，我一开始把“从 SQLite 切换到 PostgreSQL”和“Alembic 建表”混在了一起。它们其实是两件连续的事：**数据库地址决定连接谁；Alembic 决定怎样记录和执行表结构变化。**

## 先认清这些文件

| 文件 | 在这件事里的作用 |
| --- | --- |
| `app/db/database.py` | `DATABASE_URL` 指向 PostgreSQL 18；`create_engine()` 准备连接方式 |
| `app/db/models.py` | 定义 `User`、`Product`、`Order`，也就是希望得到的表结构 |
| `alembic.ini` | 告诉 Alembic 迁移脚本在哪里；其中的示例地址会被 `env.py` 覆盖 |
| `alembic/env.py` | 把模型结构和真实数据库连接交给 Alembic |
| `alembic/versions/*.py` | 保存每一次表结构变化的具体操作 |

`alembic/env.py` 是 Alembic 运行的 Python 脚本，**不是**常见的 `.env` 环境变量文件。

## `env.py` 到底做了什么？

我们在这个文件里写了三个关键动作：

1. `from app.db import models`：加载模型。Python 加载 `User`、`Product`、`Order` 类时，它们的表定义会登记到 `Base.metadata`。
2. `target_metadata = Base.metadata`：把这些**期望的表结构**交给 Alembic。
3. `config.set_main_option("sqlalchemy.url", DATABASE_URL)`：让 Alembic 使用 PyNest 的数据库地址。在线运行时，`connectable.connect()` 会真正连接 PostgreSQL，把**现有的表结构**交给 Alembic。

可以把关系画成这样：

```text
models.py → Base.metadata ──期望的表结构──┐
                                          ├→ Alembic 比较差异
DATABASE_URL → PostgreSQL ──现有表结构───┘
```

Alembic 比较的是表、列、索引等**结构**，不会把用户或订单记录逐条拿来比较。它也不会去读取旧的 SQLite 数据文件。

## 两条容易混淆的命令

```bash
uv run alembic revision --autogenerate -m "initial schema"
uv run alembic upgrade head
```

第一条命令中的 `--autogenerate` 让 Alembic 比较模型和数据库，并**生成迁移文件**。生成第一份文件时，PostgreSQL 中还没有这些业务表，因此文件包含 `users`、`products`、`orders` 三次 `op.create_table(...)`。生成后先阅读文件，确认操作符合预期。

第二条命令的 `upgrade head` 会**执行已经生成的迁移文件**。`head` 指最新迁移版本。文件中的 `upgrade()` 写正向操作；`downgrade()` 写反向操作。初始迁移 `e4164fd3b292` 已执行，`alembic current` 显示它是当前 `head`。

## `create_all()` 为什么被移走？

原来的 `Base.metadata.create_all(bind=engine)` 会在应用启动时直接创建缺少的表。它连接的是 `engine` 指向的数据库：以前是 SQLite，后来换成了 PostgreSQL，所以这行代码并不专属于 SQLite。

现在要让 Alembic 记录建表过程，就从 `app/main.py` 移除了这次自动建表调用。模型仍保留在 `models.py`，用于告诉 Alembic 表应该长什么样。

## 当前边界

- 原来的 SQLite 文件还在，但 PyNest 当前连接 PostgreSQL 18（本机端口 `5434`）。
- PostgreSQL 服务和最初空的 `pynest` 数据库由 Docker 容器启动时准备；业务表已由 Alembic 初始迁移创建。
- 这一步是建立 PostgreSQL 的表结构，**没有把 SQLite 的旧数据搬过去**。

延伸阅读：[上一份 PostgreSQL 学习记录](postgresql-alembic-learning.md)、[Alembic 自动生成迁移文档](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)。
