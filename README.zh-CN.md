# 今日外卖券

[English](README.md) | 简体中文

每日自动更新的外卖平台领券口令页面（美团 / 淘宝闪购·饿了么 / 京东）。
打开网页 → 点「复制口令」→ 打开对应 App 领取。

**线上页面**：https://timon-designer.github.io/takeout-coupons/

## 使用方法

1. 打开上面的线上页面。
2. 点任意一张券的「复制口令」按钮，完整口令进入剪贴板。
3. 打开美团 / 淘宝 / 京东 App，会自动识别剪贴板里的口令并弹出领取。

> 灰色小字 = 有限制（新客专享 / 夜宵时段 / 学生）或付费入口，已逐一标注；付费入口不是免费券。
> 按钮只有两个状态：复制口令 → 已复制 ✓。

## 工作原理

- GitHub Actions 每天北京时间 07:00 运行 [`scripts/fetch_and_build.py`](scripts/fetch_and_build.py)：从公共聚合接口拉取当天口令，重建 `index.html` 并自动提交，GitHub Pages 随之自动发布。
- 仓库不含任何账号、登录态或密钥，只消费公开接口。

## 来源与致谢

- **券数据**：[moooai/takeout-coupon](https://github.com/moooai/takeout-coupon)。本仓库只消费其公开接口输出，不含券源代码。
- **页面模板与自动更新流程**：本仓库原创（模板渲染 + 定时 Actions + GitHub Pages，无第三方模板）。
- **Agent 侧技能**（给 AI 助手用的每日任务流程 SKILL.md）：存放在作者本人的私有技能库，不在此公开仓库内。

## 目录结构

```
scripts/fetch_and_build.py    拉取券码 + 重建页面
data/latest.json              最新原始数据（含每日归档）
.github/workflows/update.yml  每日定时任务
index.html                    生成的页面（勿手改）
```

## 本地运行

```bash
python3 scripts/fetch_and_build.py
```

需要 Python 3.9+，无第三方依赖。

## 免责声明

口令来自第三方聚合渠道，可能带推广归因；**入口 ≠ 已领到**，能否领取与实际面额以各 App 内为准。
