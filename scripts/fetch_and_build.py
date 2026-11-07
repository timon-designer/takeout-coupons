#!/usr/bin/env python3
"""每日券码机器人核心：拉公共接口 → 归档 JSON → 重建 index.html。
接口连续失败或三平台全缺时非零退出，保留昨天的页面不覆盖。"""
import json, re, sys, time, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

API = "https://agskills.moontai.top/coupon/takeout"
SOURCE_REPO = "https://github.com/moooai/takeout-coupon"
ROOT = Path(__file__).resolve().parent.parent
TZ_BJ = timezone(timedelta(hours=8))
REQUIRED = ["美团隐藏外卖券列表", "饿了么/淘宝闪购隐藏外卖券列表", "京东隐藏外卖券列表"]

TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<title>今日外卖券 · __DATE__</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;color:#111;font:15px/1.5 -apple-system,BlinkMacSystemFont,"PingFang SC","Helvetica Neue",sans-serif;padding:24px 16px 48px;max-width:480px;margin:0 auto;-webkit-tap-highlight-color:transparent}
h1{font-size:20px;font-weight:600;letter-spacing:.5px}
.date{color:#888;font-size:13px;margin-top:4px}
.tip{color:#888;font-size:13px;margin-top:12px;line-height:1.6}
.group{margin-top:28px}
.group h2{font-size:13px;font-weight:500;color:#888;letter-spacing:2px;padding-bottom:8px;border-bottom:1px solid #e5e5e5}
.item{padding:16px 0;border-bottom:1px solid #e5e5e5}
.item .t{font-size:15px;font-weight:500}
.item .tag{font-size:12px;color:#888;margin-left:8px;font-weight:400}
.item button{display:block;width:100%;height:48px;margin-top:12px;background:#fff;border:1px solid #111;border-radius:4px;font-size:16px;color:#111;font-family:inherit;cursor:pointer}
.item button.ok{background:#111;color:#fff}
.item .g{display:none;font-size:13px;color:#888;margin-top:8px}
footer{margin-top:32px;font-size:12px;color:#aaa;line-height:1.6}
</style>
</head>
<body>
<h1>今日外卖券</h1>
<div class="date" id="date"></div>
<p class="tip">点「复制口令」→ 打开对应 App，会自动识别领取。<br>数量共 __TOTAL__ 条，标灰字的有限制，点开前看一眼。__MISSING__</p>
<div id="list"></div>
<footer>入口来自第三方聚合渠道（<a href="__SOURCE__" style="color:#aaa">moooai/takeout-coupon</a>），可能带推广归因；入口≠已领到，实际面额与资格以 App 内为准。</footer>
<script id="data" type="application/json">__DATA__</script>
<script>
var DATA = JSON.parse(document.getElementById('data').textContent);
document.getElementById('date').textContent = DATA.date + '（北京时间）';
var list = document.getElementById('list');
DATA.groups.forEach(function (g) {
  var sec = document.createElement('section');
  sec.className = 'group';
  var h = document.createElement('h2');
  h.textContent = g.name;
  sec.appendChild(h);
  g.items.forEach(function (it) {
    var d = document.createElement('div');
    d.className = 'item';
    var t = document.createElement('div');
    t.className = 't';
    t.textContent = it.t;
    if (it.tag) {
      var s = document.createElement('span');
      s.className = 'tag';
      s.textContent = it.tag;
      t.appendChild(s);
    }
    var b = document.createElement('button');
    b.textContent = '复制口令';
    var tip = document.createElement('div');
    tip.className = 'g';
    tip.textContent = it.g;
    b.addEventListener('click', function () { copyCode(it.code, b, tip); });
    d.appendChild(t); d.appendChild(b); d.appendChild(tip);
    sec.appendChild(d);
  });
  list.appendChild(sec);
});
function copyCode(text, btn, tip) {
  function done() {
    btn.textContent = '已复制 ✓ 打开App';
    btn.classList.add('ok');
    tip.style.display = 'block';
  }
  function fallback() {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    done();
  }
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(done, fallback);
  } else { fallback(); }
}
</script>
</body>
</html>
"""


def fetch(retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(API, headers={"User-Agent": "takeout-coupons-bot/1.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status != 200:
                    raise RuntimeError(f"HTTP {r.status}")
                return json.loads(r.read().decode())
        except Exception as e:
            last = e
            print(f"拉取失败({i + 1}/{retries}): {e}", flush=True)
            if i < retries - 1:
                time.sleep(5)
    raise SystemExit(f"接口连续 {retries} 次失败: {last}")


def build_groups(raw):
    platforms = [
        ("美团外卖", raw.get("美团隐藏外卖券列表") or []),
        ("淘宝闪购", raw.get("饿了么/淘宝闪购隐藏外卖券列表") or []),
        ("京东外卖", raw.get("京东隐藏外卖券列表") or []),
    ]
    groups, missing = [], []
    for name, items in platforms:
        if not items:
            missing.append(name)
            continue
        out, seen = [], set()
        for it in items:
            title = re.sub(r"[🔥✨]+$", "", it.get("title", "")).strip()
            code = it.get("coupon_code", "")
            tag = ""
            if "神券包" in title or "年卡" in title:
                tag = "付费入口·勿当免费券"
            elif any(k in title for k in ("新客", "夜宵", "学生", "宵夜")):
                tag = "资格/时段受限"
            elif code in seen:
                tag = "与上一条同码"
            seen.add(code)
            guide = it.get("guideline", "")
            if "搜索" in guide:
                tag = (tag + " " if tag else "") + "首页搜索框输入"
            out.append({"t": title, "tag": tag, "code": code, "g": guide})
        groups.append({"name": name, "items": out})
    return groups, missing


def main():
    now = datetime.now(TZ_BJ)
    date_label = f"{now:%m-%d}"
    raw = fetch()
    empty = [k for k in REQUIRED if not raw.get(k)]
    if len(empty) == len(REQUIRED):
        raise SystemExit(f"接口三平台全部缺失，疑似结构变更：{list(raw)}")
    data_dir = ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "latest.json").write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n")
    (data_dir / f"{now:%Y-%m-%d}.json").write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n")

    groups, missing = build_groups(raw)
    total = sum(len(g["items"]) for g in groups)
    data_json = json.dumps({"date": date_label, "groups": groups},
                           ensure_ascii=False, separators=(",", ":"))
    assert "</" not in data_json, "数据含 </ 序列"
    note = f"<br>今日接口未返回：{'、'.join(missing)}。" if missing else ""
    html = (TEMPLATE.replace("__DATE__", date_label)
                    .replace("__TOTAL__", str(total))
                    .replace("__MISSING__", note)
                    .replace("__SOURCE__", SOURCE_REPO)
                    .replace("__DATA__", data_json))
    (ROOT / "index.html").write_text(html)
    print(f"OK {now:%Y-%m-%d} 共 {total} 条：" +
          " ".join(f"{g['name']}{len(g['items'])}" for g in groups) +
          (f"（未返回：{'、'.join(missing)}）" if missing else ""))


if __name__ == "__main__":
    main()
