# 部署与使用说明（Bilibili Synced Playback）

## 前置条件
- Python 3.11
- 访问 Bilibili 播放器的网络
- 推荐使用虚拟环境（`python -m venv .venv && source .venv/bin/activate`）

## 安装依赖
```bash
cd /Users/longsiyu/work/videotogether
python -m pip install -r backend/requirements.txt
```

## 必需环境变量
- `APP_SHARED_PASSWORD`：全站共用访问密码（必须设置，示例：`changeme`）

可选：
- `APP_SECRET_KEY`：Flask 会话密钥（默认 `dev-secret-key`，生产环境请自定义）
- `SOCKETIO_MESSAGE_QUEUE`：如需多实例部署，可配置 Redis 队列 URL（本地单实例可不设）

## 本地运行
```bash
cd /Users/longsiyu/work/videotogether
export APP_SHARED_PASSWORD=changeme
# 可选：export APP_SECRET_KEY=your-secret
PYTHONPATH=backend/src python -m flask --app app:create_app run --host 0.0.0.0 --port 5000
```
访问 http://localhost:5000 ，输入共享密码登录。

## 使用步骤
1. 打开登录页，输入 `APP_SHARED_PASSWORD`。
2. 登录后在页面输入 Bilibili 视频链接（例如 `https://www.bilibili.com/video/BV1xx411c7mD`）。
3. 点击“加载视频”后播放页出现嵌入播放器。
4. 多个浏览器/标签页登录后，任一用户的播放/暂停/拖动会实时同步到所有人。

## 测试
### 基础测试
```bash
cd /Users/longsiyu/work/videotogether
PYTHONPATH=backend/src ruff check backend/src backend/tests
PYTHONPATH=backend/src mypy backend/src
PYTHONPATH=backend/src pytest backend/tests --disable-warnings
```

### 浏览器 E2E（可选）
需要安装浏览器内核一次：
```bash
python -m playwright install
```
运行 E2E：
```bash
RUN_E2E=1 APP_URL=http://localhost:5000 APP_SHARED_PASSWORD=changeme \
pytest backend/tests/e2e/test_sync_two_clients.py
```

## 部署提示
- 生产环境请设置唯一的 `APP_SECRET_KEY` 和强密码的 `APP_SHARED_PASSWORD`。
- 如需多实例/容器部署，可通过 `SOCKETIO_MESSAGE_QUEUE` 指向 Redis 以共享 SocketIO 状态。
- 将服务端口暴露给反向代理（如 Nginx），并在 HTTPS 下运行以保证会话与密码安全。
