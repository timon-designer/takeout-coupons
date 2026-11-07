# 今日外卖券 · Takeout Coupons

每日自动更新的外卖平台领券口令页面。打开网页 → 点「复制口令」→ 打开对应 App 领取。
A daily-updated page of takeout coupon codes. Open the page → tap "复制口令" (Copy code) → open the matching app to claim.

**线上页面 Live page**：https://timon-designer.github.io/takeout-coupons/

## 使用 How to use

1. 打开上面的页面。Open the page above.
2. 点任意一张券的「复制口令」按钮，口令进入剪贴板。Tap any coupon's copy button — the code goes to your clipboard.
3. 打开美团 / 淘宝 / 京东 App，会自动识别剪贴板里的口令并弹出领取。Open Meituan / Taobao / JD — the app detects the full code from your clipboard and offers the coupon.

> English: codes must be copied in full and pasted-detected inside the Chinese apps (Meituan, Taobao, JD). The page is in Chinese; button labels mean: 复制口令 = copy code, 已复制 = copied, 灰色小字 = restrictions (new users only / time-limited / paid entry — marked, do not treat paid ones as free coupons).

## 它是怎么工作的 How it works

- GitHub Actions 每天北京时间 07:00 运行 [`scripts/fetch_and_build.py`](scripts/fetch_and_build.py)，从公共聚合接口拉取当天口令，重建 `index.html` 并自动提交。本仓库不含任何账号、登录态或密钥。
- GitHub Actions runs daily at 07:00 Beijing time, fetches codes from a public aggregator API ([moooai/takeout-coupon](https://github.com/moooai/takeout-coupon)), rebuilds `index.html` and auto-commits. No accounts, credentials or secrets involved.
- 口令来自第三方聚合渠道，可能带推广归因；**入口 ≠ 已领到**，能否领取与实际面额以 App 内为准。
- Codes come from a third-party aggregator and may carry referral attribution. **An entry is not a claimed coupon** — eligibility and value are subject to each app.

## 目录 Structure

```
scripts/fetch_and_build.py   拉取 + 重建页面 fetch & rebuild
data/latest.json             最新原始数据 latest raw data（含每日归档 daily archives）
.github/workflows/update.yml 每日定时任务 daily cron workflow
index.html                   生成的页面 generated page（勿手改 do not edit by hand）
```

## 本地运行 Run locally

```bash
python3 scripts/fetch_and_build.py
```

需要 Python 3.9+，无第三方依赖。Python 3.9+ only, zero dependencies.
