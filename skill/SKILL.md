---
name: takeout-coupons-daily
description: "跑外卖优惠券任务时用：查券→生成券页→发布→微信发 1 条链接。"
version: 1.0.0
author: 刘涛 (timon-designer), Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [takeout, coupons, weixin, github-actions, daily]
    related_skills: [weixin-ilink-gateway, headless-chrome-verify, static-site-deploy]
---

# 外卖券每日任务（takeout-coupons）

涛哥说「跑今天的优惠券 / 外卖券」，或发来本技能，即执行。简单查券用 flash，不建机器人、不装额外依赖。
代码与页面真身在仓库 `~/WorkBuddy/软件制作/takeout-coupons`（GitHub: timon-designer/takeout-coupons，公开仓），
线上页 `https://timon-designer.github.io/takeout-coupons/`，GitHub Actions 每天 07:00（北京时间）自动更新，无需人工。

## When to Use

- 「跑今天的优惠券」「外卖券」「领券口令」——完整走一遍：抓取→发布→微信 1 条链接。
- 「券页怎么打不开了」——诊断 Actions / Pages / 接口三层。
- 不要用于：代领券、登录账号、自动下单；只给入口，不保证到账。

## Procedure（每日执行）

1. 仓库内 `python3 scripts/fetch_and_build.py`——拉公共接口、重建 `index.html`、归档 `data/`。
   完成标志：stdout 出现 `OK MM-DD 共 N 条：美团x 淘宝闪购x 京东外卖x`。
   接口连续 3 次失败会非零退出并保留昨天页面——此时直接报告，不重试第四次（熔断）。
2. `git add -A && git commit && git push`。推送即触发 Pages 部署（约 1 分钟）；Actions 的每日跑批只是兜底，手动跑过就不用等它。
3. 轮询 `https://timon-designer.github.io/takeout-coupons/` 到 200。
4. 验收（skill: headless-chrome-verify 第八节要点）：390px 视口渲染 + `Input.dispatchMouseEvent` 真实点击第一个复制按钮 +
   `navigator.clipboard.readText()` 回读与口令逐字符一致 + 零 JS 报错。grantPermissions 的源必须是页面自己的 origin。
5. 微信发 **1 条**（WEIXIN_HOME_CHANNEL，`hermes send --to weixin:<target>`）：日期 + 「点开链接→每张券点复制口令→打开对应App」+ 线上链接 + 「灰字=有限制」。
   桌面侧只报投递状态。链接是固定的，换仓库才变。
6. 归档：会话里报「N 条已发 + 链接」，不再粘贴口令全文。

## 微信发起时

微信里说「跑优惠券」→ 同样执行，结果回微信会话（链接 1 条），不额外 send 一份。

## 回退：逐条消息模式（仅当发布链路不可用）

脚本 `~/.hermes/tasks/takeout-coupons/coupons_multisend.py`：图例 1 条 + 每券 1 条，间隔 1.2s。
**iLink 连发约 8 条必撞配额**（session not ready）——熔断停止，请涛哥回任意消息刷新会话，按已发条数续发，绝不从头重发。

## Pitfalls

- 券接口 `agskills.moontai.top` **无 CORS 头**：页面数据必须构建时烤进 HTML，不能前端现拉。
- 口令原样保留，不补写不修复；重复码/付费入口（神券包年卡）标灰字，不作为免费券推荐。
- Pages 更新偶发延迟 1-3 分钟，轮询间隔 15s，最多 12 次；超时先查 Actions 运行记录。
- GitHub release/克隆加速用 `https://ghfast.top/` 前缀（国内网络）。
- 页面与技能只许住本仓库；**portfolio-site 仓库已清理过一次，禁止再把 qu/ 或本任务产物放回个人站白名单**。
- 微信正文口令一旦要贴原文，必须整段独立成一条消息（长按复制），绝不夹在长文里。

## Verification

- 页面 200 + 验收 4 项全过（见 Procedure 第 4 步）。
- `data/latest.json` 日期字段是今天；`git log` 顶部提交是今天的「券码更新」。
- 微信回执 JSON `"success": true` 且 `context_token_used: true`。
- 每日跑批是否健康：`gh run list -R timon-designer/takeout-coupons --limit 3`。
