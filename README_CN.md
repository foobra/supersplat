# SuperSplat 本地开发与上传服务（中文说明）

本文档说明如何在本项目中启动 SuperSplat 前端与 Python 上传服务，并通过 URL 一键加载 `.ply` 文件，以及将修改后的 `.ply` 上传保存到本地目录。

## 前置条件

- Node.js 18+（用于 SuperSplat 前端）
- uv（用于 Python 依赖管理与启动）

## 目录约定

- `build/`：放置本地要加载的 `.ply` 文件（例如 `build/1.ply`）
- `tools/`：Python 上传服务代码
- `tools/uploads/`：上传保存目录（已被 `.gitignore` 忽略）

## 一、启动 SuperSplat（前端）

```sh
cd /Users/jtang/work/supersplat
npm install
npm run develop
```

启动后访问：

```
http://localhost:3000
```

## 二、启动 Python 上传服务（FastAPI + uv）

使用 `uv` 一键启动（无需手动创建虚拟环境）：

```sh
cd /Users/jtang/work/supersplat/tools
uv run uvicorn upload_server:app --host 0.0.0.0 --port 8000
```

上传服务启动后可用：

- 访问根地址：`http://127.0.0.1:8000/`
- 访问本地 `build` 目录文件：`http://127.0.0.1:8000/build/1.ply`
- 上传接口（POST）：`http://127.0.0.1:8000/upload`

## 三、通过 URL 一键载入本地 `.ply`

SuperSplat 支持通过 URL 参数 `load` 自动加载资源。请使用 `127.0.0.1`：

```
http://localhost:3000/?load=http%3A%2F%2F127.0.0.1%3A8000%2Fbuild%2F1.ply
```

说明：
- `load` 参数需要 URL 编码
- 资源由 Python 服务提供（`/build/1.ply`）

## 四、保存修改后的 `.ply` 到本地目录

SuperSplat 的“保存到服务器”功能会向以下地址提交文件：

```
http://127.0.0.1:8000/upload
```

上传后的文件会保存到：

```
tools/uploads/
```

接口返回示例（JSON）：

```json
{
  "ok": true,
  "filename": "upload.ply",
  "path": ".../tools/uploads/upload.ply"
}
```

## 五、完整流程示例

1. 把 `1.ply` 放到 `build/`（本仓库已经放好）
2. 启动 Python 上传服务（端口 8000）
3. 启动 SuperSplat 前端（端口 3000）
4. 打开一键加载 URL：
   ```
   http://localhost:3000/?load=http%3A%2F%2F127.0.0.1%3A8000%2Fbuild%2F1.ply
   ```
5. 在 SuperSplat 中编辑后选择“保存到服务器”
6. 在 `tools/uploads/` 找到保存后的 `.ply`
