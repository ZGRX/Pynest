# 从 SQLite 走向 PostgreSQL：PyNest 数据库学习记录

这次我们给 PyNest 准备了 PostgreSQL，并开始接入 Alembic。我的目标不是背下一串命令，而是弄清楚：每个工具负责什么，项目目前走到了哪一步。

## 为什么要换数据库？

PyNest 原来使用 SQLite。它把数据保存在一个文件里，适合刚开始开发和练习。PostgreSQL 则是一个独立运行的数据库服务，项目需要通过地址、端口、用户名和密码连接它。MySQL 也属于这一类；它和 PostgreSQL 是不同的选择，并不是 PostgreSQL 的组成部分。

PyNest 的项目目标包含 PostgreSQL，所以我们现在练习把应用连接过去。Alembic 解决的是另一个问题：当表结构以后发生变化时，怎样记录并应用这些变化。

## Docker：镜像和容器

先运行了 `docker pull postgres:17`。`pull` 下载的是**镜像**，可以把它理解成创建 PostgreSQL 容器的模板；下载完成并不代表数据库已经运行。

接着使用 `docker run` 创建并启动了名为 `pynest-postgres` 的容器。启动选项各有用途：

| 选项 | 作用 |
| --- | --- |
| `--name pynest-postgres` | 给容器取名，方便以后操作 |
| `-e POSTGRES_PASSWORD=...` | 首次启动时设置数据库密码 |
| `-e POSTGRES_DB=pynest` | 创建名为 `pynest` 的数据库 |
| `-p 127.0.0.1:5433:5432` | 把本机的 5433 端口连接到容器里的 5432 端口 |
| `-v pynest-pgdata:/var/lib/postgresql/data` | 用 Docker 数据卷保存数据库文件 |
| `-d` | 让容器在后台运行 |

这里的 `-e` 是 Docker 的命令选项，用来给容器传启动配置。它和 Python 代码中的 `getenv()` 不是同一个操作。我们还用 `docker exec ... pg_isready` 检查了数据库是否准备好接受连接。

## Python 怎样连接 PostgreSQL？

PyNest 已经使用 SQLAlchemy，但还需要 PostgreSQL 驱动。我们运行了：

```bash
uv add "psycopg[binary]"
```

`psycopg` 负责让 Python 与 PostgreSQL 通信；`binary` 版本方便在本地安装。`uv add` 会安装依赖，并自动把依赖名称记入 `pyproject.toml`。因此，`pyproject.toml` 可以看作项目需要哪些 Python 库的清单。

SQLAlchemy 使用的 PostgreSQL 地址长这样：

```text
postgresql+psycopg://用户名:密码@主机:端口/数据库名
```

其中 `postgresql` 是数据库类型，`psycopg` 是驱动。最初的 PostgreSQL 17 练习容器使用本机 `5433`；现在 PyNest 指向 PostgreSQL 18 容器的 `127.0.0.1:5434` 和其中的 `pynest` 数据库。SQLite 专用的 `check_same_thread` 参数已经删掉。

一个让我印象深刻的区别是：`create_engine(...)` 准备好连接方式，`engine.connect()` 才会实际尝试连接。我们在 Python 交互环境中调用了 `engine.connect()`，看到了“连接成功”，随后用 `conn.close()` 关闭连接。这次检查没有创建任何表。

交互环境中的 `>>>` 表示可以输入新语句；如果出现 `...`，Python 还在等当前语句写完。遇到这种情况，可以按 `Ctrl+C` 回到 `>>>`，再逐行输入。

## Alembic 目前做到哪里？

我们运行了：

```bash
uv add alembic
uv run alembic init alembic
```

第一条命令安装 Alembic，并把它加入 `pyproject.toml`。第二条命令运行 Alembic 的初始化操作，生成了 `alembic.ini` 和 `alembic/` 目录；它**没有修改 PostgreSQL 中的表**。

Alembic 已经通过 `alembic/env.py` 中的 `target_metadata = Base.metadata` 读到 PyNest 的模型，并使用项目的数据库地址覆盖 `alembic.ini` 中的占位内容。`app/main.py` 已移除自动调用 `create_all()` 的建表代码。第一份迁移文件已经生成并检查，下一步是执行 `uv run alembic upgrade head`。这个过程另见[《Alembic 是怎么知道要建哪些表的？》](how-alembic-finds-schema.md)。

## 我现在能说清楚的流程

```text
Docker 镜像 → 运行 PostgreSQL 容器 → 安装 psycopg → SQLAlchemy 连接成功
                                              ↓
                              配置 Alembic → 生成迁移 → 应用迁移
```

目前已经完成数据库连接、Alembic 配置和迁移文件生成；迁移文件尚未执行。

## 参考资料

- [PostgreSQL 官方 Docker 镜像](https://hub.docker.com/_/postgres)
- [Psycopg 安装说明](https://www.psycopg.org/psycopg3/docs/basic/install.html)
- [SQLAlchemy PostgreSQL 方言](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Alembic 官方教程](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [uv 项目依赖说明](https://docs.astral.sh/uv/concepts/projects/dependencies/)
