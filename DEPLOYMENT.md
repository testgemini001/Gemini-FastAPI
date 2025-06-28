# Gemini-FastAPI 部署指南

## 动态扩展 Gemini 客户端

本项目支持**自动扩展**Gemini客户端数量，无需修改配置文件。

### 工作原理

系统会自动扫描所有以 `CONFIG_GEMINI__CLIENTS__` 开头的环境变量，动态构建客户端配置。

### 环境变量命名规则

```bash
CONFIG_GEMINI__CLIENTS__[索引]__[字段名]
```

每个客户端需要3个环境变量：
- `CONFIG_GEMINI__CLIENTS__[索引]__ID` - 客户端标识符
- `CONFIG_GEMINI__CLIENTS__[索引]__SECURE_1PSID` - Google账号的 __Secure-1PSID cookie
- `CONFIG_GEMINI__CLIENTS__[索引]__SECURE_1PSIDTS` - Google账号的 __Secure-1PSIDTS cookie

### 在 Render 中添加客户端

#### 1. 访问环境变量页面
- 登录 [Render Dashboard](https://dashboard.render.com/)
- 选择您的 `gemini-fastapi` 服务
- 点击 "Environment" 标签页

#### 2. 添加第一个客户端（索引0）
```bash
CONFIG_GEMINI__CLIENTS__0__ID=account-main
CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID=your-first-account-1psid-here
CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS=your-first-account-1psidts-here
```

#### 3. 添加第二个客户端（索引1）
```bash
CONFIG_GEMINI__CLIENTS__1__ID=account-backup
CONFIG_GEMINI__CLIENTS__1__SECURE_1PSID=your-second-account-1psid-here
CONFIG_GEMINI__CLIENTS__1__SECURE_1PSIDTS=your-second-account-1psidts-here
```

#### 4. 继续添加更多客户端
```bash
# 第三个客户端
CONFIG_GEMINI__CLIENTS__2__ID=account-extra1
CONFIG_GEMINI__CLIENTS__2__SECURE_1PSID=your-third-account-1psid-here
CONFIG_GEMINI__CLIENTS__2__SECURE_1PSIDTS=your-third-account-1psidts-here

# 第四个客户端
CONFIG_GEMINI__CLIENTS__3__ID=account-extra2
CONFIG_GEMINI__CLIENTS__3__SECURE_1PSID=your-fourth-account-1psid-here
CONFIG_GEMINI__CLIENTS__3__SECURE_1PSIDTS=your-fourth-account-1psidts-here

# ... 可以继续添加任意数量的客户端
```

### 重要说明

#### ✅ 优势
- **无限扩展**: 可以添加任意数量的Google账号
- **即时生效**: 添加环境变量后服务会自动重启并加载新配置
- **负载均衡**: 系统自动在所有客户端间分配请求
- **容错性**: 单个客户端失效不影响整体服务

#### ⚠️ 注意事项
1. **索引必须连续**: 从0开始，不能跳跃（0,1,2... 不能是0,2,4）
2. **三个字段都必须设置**: ID、SECURE_1PSID、SECURE_1PSIDTS 缺一不可
3. **ID必须唯一**: 每个客户端的ID不能重复
4. **cookies有效性**: 确保从Google账号获取的cookies是有效的

### 获取 Google Cookies

为每个要添加的Google账号：

1. **打开无痕窗口**
2. **访问** [Gemini](https://gemini.google.com/)
3. **登录** 对应的Google账号
4. **打开开发者工具** (F12)
5. **导航到** Application → Storage → Cookies → `https://gemini.google.com`
6. **复制值**:
   - 查找 `__Secure-1PSID` 并复制其值
   - 查找 `__Secure-1PSIDTS` 并复制其值

### 验证配置

添加环境变量后，可以通过以下方式验证：

1. **健康检查**:
   ```bash
   curl https://your-app.onrender.com/health
   ```

2. **查看日志**: 在Render控制台查看部署日志，确认客户端初始化成功

3. **测试API**:
   ```bash
   curl -X POST https://your-app.onrender.com/v1/chat/completions \
     -H "Authorization: Bearer your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"model": "gemini-pro", "messages": [{"role": "user", "content": "Hello"}]}'
   ```

### 客户端管理最佳实践

#### 推荐配置
- **生产环境**: 至少3-5个客户端，确保高可用性
- **开发环境**: 1-2个客户端即可
- **高并发**: 5-10个客户端，根据请求量调整

#### 命名约定
```bash
# 建议使用有意义的ID
CONFIG_GEMINI__CLIENTS__0__ID=main-account
CONFIG_GEMINI__CLIENTS__1__ID=backup-account
CONFIG_GEMINI__CLIENTS__2__ID=high-volume-account
CONFIG_GEMINI__CLIENTS__3__ID=dev-account
```

#### 监控和维护
- **定期检查**: cookies可能会过期，需要定期更新
- **负载监控**: 观察各客户端的使用情况
- **错误处理**: 单个客户端失效时，其他客户端会自动接管

---

## 其他平台部署

### Railway
```bash
railway variables set CONFIG_GEMINI__CLIENTS__0__ID="main-account"
railway variables set CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID="your-1psid"
railway variables set CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS="your-1psidts"
```

### Fly.io
```bash
flyctl secrets set CONFIG_GEMINI__CLIENTS__0__ID="main-account"
flyctl secrets set CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID="your-1psid"
flyctl secrets set CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS="your-1psidts"
```

### Heroku
```bash
heroku config:set CONFIG_GEMINI__CLIENTS__0__ID="main-account"
heroku config:set CONFIG_GEMINI__CLIENTS__0__SECURE_1PSID="your-1psid"
heroku config:set CONFIG_GEMINI__CLIENTS__0__SECURE_1PSIDTS="your-1psidts"
```

这样，您就可以在任何平台上动态扩展Gemini客户端数量了！ 