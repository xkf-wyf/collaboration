# R002 · 需求规格：三方协作平台

- 版本：v1.0（已裁决，进入开发）
- 形态：本地网页（localhost），零第三方依赖
- 开发方：WorkBuddy 直接建（人类裁决，不派 CodeBuddy）
- 数据源：协作根目录文件总线（唯一真相，平台只是界面层）

## 目标

把"文件总线协作"装上界面：人类在网页上下需求、做裁决；WorkBuddy 产出的任务单可视化；CodeBuddy 的执行回报实时展示。

## 功能清单

| 编号 | 功能 | 说明 |
|------|------|------|
| F1 | 需求提交 | 文本框提交 → 自动编号写入 00-inbox/，自动 git commit+push |
| F2 | 裁决面板 | 列出 pipeline-state.yaml 的待裁决项/开放问题，点击"确认/驳回/部分确认"→ 记录到 05-platform/decisions.json 并自动提交 |
| F3 | 任务看板 | 解析 03-tasks/*.md 的 T-xxx 任务区块与执行回报，展示状态/分支 |
| F4 | 回报展示 | 每条任务的最新回报摘要（状态、分支、改动摘要） |
| F5 | 门禁与阶段 | G1/G2/G3 状态、stage、kb 快照日期 |
| F6 | 文件查看器 | 六个目录文件列表，点击查看内容（限根目录内，防路径穿越） |
| F7 | 自动刷新 | 前端每 6 秒轮询 /api/state |

## 非目标

1. 不做用户登录（本机使用）
2. 不做在线部署（后续可升级）
3. 不替 CodeBuddy 接收任务——它仍读文件，平台只展示
4. 不改契约：pipeline-state.yaml 的例行维护仍由 WorkBuddy 执行

## 技术方案

- 后端：Python 标准库 http.server（platform/server.py），端口 8765，绑定 127.0.0.1
- 前端：单文件 index.html，原生 JS，无框架
- API：GET /api/state、GET /api/file?path=、POST /api/requirement、POST /api/decision
- 审计：所有写入动作自动 git commit + push

## 验收标准

- [ ] 打开 http://localhost:8765 能看到三栏界面与门禁状态
- [ ] 提交一条需求，00-inbox 出现新文件且 GitHub 有对应提交
- [ ] 点击裁决按钮，decisions.json 出现记录且 GitHub 有对应提交
- [ ] 任务文件新增 T-xxx 区块后，6 秒内看板自动显示
- [ ] 访问根目录外路径被拒绝
