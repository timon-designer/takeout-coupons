# Takeout Coupons

English | [简体中文](README.zh-CN.md)

A daily-updated page of takeout coupon codes for Meituan / Taobao–Ele.me / JD.
Open the page → tap the copy button → open the matching app to claim.

**Live page**: https://timon-designer.github.io/takeout-coupons/

## How to use

1. Open the live page above.
2. Tap **复制口令** (copy code) on any coupon — the full code goes to your clipboard.
3. Open Meituan / Taobao / JD — the app detects the code from the clipboard and offers the coupon.

> The page UI is in Chinese. Only two button labels matter: 复制口令 = copy code, 已复制 ✓ = copied.
> Gray notes = restricted entries (new users only / night hours / student) or paid bundles — marked as such, do not treat paid entries as free coupons.

## How it works

- A GitHub Actions workflow runs daily at 07:00 Beijing time, fetches codes from a public aggregator API, rebuilds `index.html`, and auto-commits. GitHub Pages redeploys automatically.
- No accounts, credentials, or secrets are involved — the repo only consumes a public API.

## Credits

- **Coupon data**: [moooai/takeout-coupon](https://github.com/moooai/takeout-coupon). This repo only consumes its public API output and ships no coupon-source code.
- **Page template & auto-update pipeline**: original to this repo (plain template rendering + scheduled GitHub Actions + GitHub Pages).
- **Agent-side skill** (an `SKILL.md` task file for AI assistants): kept in the author's private skills repo, not published here.

## Structure

```
scripts/fetch_and_build.py    fetch codes & rebuild the page
data/latest.json              latest raw data (daily archives kept)
.github/workflows/update.yml  daily cron workflow
index.html                    generated page (do not edit by hand)
```

## Run locally

```bash
python3 scripts/fetch_and_build.py
```

Python 3.9+, zero dependencies.

## Disclaimer

Codes come from a third-party aggregator and may carry referral attribution. An entry is **not** a claimed coupon — eligibility and actual value are subject to each app.
