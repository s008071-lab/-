#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ideal properties — 静的サイトビルダー

tools/pages/*.html （本文フラグメント）に共通のヘッダー/フッターを合成して、
リポジトリ直下に配信用の HTML を出力します。

  $ python3 tools/build.py

依存ライブラリはありません（Python 3.8+ の標準ライブラリのみ）。
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = Path(__file__).resolve().parent / "pages"

# ---------------------------------------------------------------- site config
SITE = {
    "name": "株式会社Ideal properties",
    "name_en": "Ideal properties Inc.",
    "catch": "空室の不安を消し、住まう喜びをカタチにする。",
    "tel": "03-△△△△-△△△△",
    "tel_href": "03-0000-0000",
    "line_id": "@441smfiq",
    "line_url": "https://line.me/R/ti/p/@441smfiq",
    "addr": "東京都○○区■■",
    "hours": "平日 10:00 – 19:00（土日祝を除く）",
    "origin": "https://www.ideal-properties.example.jp",
}

NAV = [
    ("about.html",       "譲渡型賃貸とは", "ABOUT"),
    ("service.html",     "事業内容",       "SERVICE"),
    ("flow.html",        "ご利用の流れ",   "FLOW"),
    ("simulator.html",   "コスト比較",     "SIMULATOR"),
    ("faq.html",         "よくあるご質問", "FAQ"),
    ("news/index.html",  "ニュース",       "NEWS"),
    ("company.html",     "会社概要",       "COMPANY"),
]

ICON_ARROW = ('<svg class="btn__arrow" width="15" height="11" viewBox="0 0 15 11" fill="none" aria-hidden="true">'
              '<path d="M9.2 1l4.3 4.5L9.2 10M13.2 5.5H1" stroke="currentColor" stroke-width="1.6" '
              'stroke-linecap="round" stroke-linejoin="round"/></svg>')

LOGO_MARK = (
    '<svg class="logo__mark" viewBox="0 0 40 40" fill="none" aria-hidden="true">'
    '<path d="M20 2.5 36.5 13v14L20 37.5 3.5 27V13L20 2.5Z" stroke="#00E15E" stroke-width="2.2" '
    'stroke-linejoin="round"/>'
    '<path d="M13 25.5V17l7-4.4 7 4.4v8.5" stroke="#00E15E" stroke-width="2.2" stroke-linecap="round" '
    'stroke-linejoin="round"/>'
    '<path d="M17.2 25.5v-4.8h5.6v4.8" stroke="#EAF3ED" stroke-width="1.8" stroke-linecap="round"/>'
    '</svg>'
)


def line_btn(cls: str = "btn btn--line", label: str = "LINEで無料相談") -> str:
    return (f'<a class="{cls}" href="{SITE["line_url"]}" target="_blank" rel="noopener">'
            f'<svg width="19" height="18" viewBox="0 0 20 19" fill="currentColor" aria-hidden="true">'
            f'<path d="M10 0C4.48 0 0 3.64 0 8.12c0 4.02 3.55 7.38 8.35 8.02.33.07.77.21.88.49.1.25.07.65.03.9l-.14.85c-.04.25-.2.99.87.54 1.07-.45 5.75-3.39 7.85-5.8 1.44-1.58 2.16-3.19 2.16-5C20 3.64 15.52 0 10 0Z"/>'
            f'</svg>{label}</a>')


def header(base: str, active: str) -> str:
    links = "".join(
        f'<a class="nav__link" href="{base}{href}"'
        + (' aria-current="page"' if href == active else "")
        + f">{jp}</a>"
        for href, jp, _ in NAV
    )
    drawer_items = "".join(
        f'<li class="drawer__item"><a class="drawer__a" href="{base}{href}">'
        f'<span class="n">{i+1:02d}</span><span class="jp">{jp}</span><span class="en">{en}</span></a></li>'
        for i, (href, jp, en) in enumerate(NAV)
    )
    return f"""<header class="hdr">
  <div class="hdr__in">
    <a class="logo" href="{base}index.html" aria-label="{SITE['name']} ホームへ">
      {LOGO_MARK}
      <span class="logo__txt">
        <span class="logo__en">Ideal properties</span>
        <span class="logo__jp">JYOTO-GATA CHINTAI</span>
      </span>
    </a>
    <nav class="nav" aria-label="メインメニュー">{links}</nav>
    <div class="hdr__cta">
      <a class="btn btn--ghost btn--sm" href="{base}contact.html">お問い合わせ</a>
      {line_btn("btn btn--line btn--sm", "LINE相談")}
      <button class="burger" type="button" aria-label="メニューを開く" aria-expanded="false" aria-controls="drawer">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer">
  <ul class="drawer__list">{drawer_items}
    <li class="drawer__item"><a class="drawer__a" href="{base}contact.html">
      <span class="n">08</span><span class="jp">お問い合わせ</span><span class="en">CONTACT</span></a></li>
  </ul>
  <div class="drawer__foot">
    {line_btn()}
    <a class="btn btn--ghost" href="tel:{SITE['tel_href']}">お電話でのご相談</a>
  </div>
</div>"""


def footer(base: str) -> str:
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="ftr__top">
      <div class="ftr__brand">
        <a class="logo" href="{base}index.html">
          {LOGO_MARK}
          <span class="logo__txt">
            <span class="logo__en">Ideal properties</span>
            <span class="logo__jp">JYOTO-GATA CHINTAI</span>
          </span>
        </a>
        <p class="ftr__copy">{SITE['catch']}<br>住宅ローンに頼らない「譲渡型賃貸」で、マイホームという選択肢をすべての方へ。</p>
        <address class="ftr__addr">
          {SITE['name']}<br>
          {SITE['addr']}<br>
          TEL: <a href="tel:{SITE['tel_href']}">{SITE['tel']}</a>（{SITE['hours']}）<br>
          LINE ID: <a href="{SITE['line_url']}" target="_blank" rel="noopener">{SITE['line_id']}</a>
        </address>
      </div>
      <nav class="ftr__nav" aria-label="フッターメニュー">
        <div>
          <p class="ftr__h">ABOUT</p>
          <ul class="ftr__l">
            <li><a href="{base}about.html">譲渡型賃貸とは</a></li>
            <li><a href="{base}about.html#merit">5つのメリット</a></li>
            <li><a href="{base}about.html#cost">生涯コスト比較</a></li>
            <li><a href="{base}simulator.html">コストシミュレーター</a></li>
          </ul>
        </div>
        <div>
          <p class="ftr__h">SERVICE</p>
          <ul class="ftr__l">
            <li><a href="{base}service.html">事業内容</a></li>
            <li><a href="{base}service.html#owner">オーナー・投資家の方へ</a></li>
            <li><a href="{base}flow.html">ご利用の流れ</a></li>
            <li><a href="{base}faq.html">よくあるご質問</a></li>
          </ul>
        </div>
        <div>
          <p class="ftr__h">COMPANY</p>
          <ul class="ftr__l">
            <li><a href="{base}company.html">会社概要</a></li>
            <li><a href="{base}news/index.html">ニュース・トピックス</a></li>
            <li><a href="{base}contact.html">お問い合わせ</a></li>
            <li><a href="{base}privacy.html">プライバシーポリシー</a></li>
          </ul>
        </div>
      </nav>
    </div>
    <div class="ftr__bot">
      <p class="ftr__sm">&copy; <span data-year>2026</span> {SITE['name_en']} All rights reserved.</p>
      <div class="ftr__links">
        <a href="{base}privacy.html">プライバシーポリシー</a>
        <a href="{base}privacy.html#disclaimer">免責事項</a>
        <a href="{base}contact.html">お問い合わせ</a>
      </div>
    </div>
  </div>
</footer>

<div class="fab">
  {line_btn("btn btn--line", "LINEで相談")}
  <a class="btn" href="{base}contact.html">無料相談</a>
</div>"""


HEAD = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="format-detection" content="telephone=no">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#050C08">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='9' fill='%23050C08'/%3E%3Cpath d='M20 7.5 33 16v12L20 34.5 7 28V16L20 7.5Z' stroke='%2300E15E' stroke-width='2.4' fill='none' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;500;600;700;900&family=Shippori+Mincho:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/style.css">
<noscript><style>[data-reveal]{{opacity:1!important;transform:none!important}}.bar__fill{{width:var(--w)!important}}</style></noscript>
{jsonld}
</head>
<body>
<a class="visually-hidden" href="#main">本文へスキップ</a>
"""


def org_jsonld(base: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "RealEstateAgent",
        "name": SITE["name"],
        "alternateName": SITE["name_en"],
        "url": SITE["origin"] + "/",
        "slogan": SITE["catch"],
        "telephone": SITE["tel"],
        "address": {"@type": "PostalAddress", "addressCountry": "JP",
                    "addressRegion": "東京都", "streetAddress": SITE["addr"]},
        "areaServed": "JP",
        "description": "住宅ローンをご利用になれない方へ、賃貸借契約と売買予約契約を同時に結ぶ「譲渡型賃貸」でマイホーム取得をご支援します。",
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def build_page(src: Path) -> None:
    raw = src.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if not m:
        raise SystemExit(f"front matter がありません: {src}")
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    body = raw[m.end():]

    out_rel = meta["out"]
    base = "../" * (out_rel.count("/"))
    canonical = SITE["origin"] + "/" + out_rel.replace("index.html", "")

    head = HEAD.format(
        title=meta["title"],
        desc=meta["desc"],
        robots=meta.get("robots", "index,follow"),
        canonical=canonical,
        ogtype=meta.get("ogtype", "website"),
        site_name=SITE["name"],
        base=base,
        jsonld=org_jsonld(base) if out_rel == "index.html" else "",
    )

    for key, val in SITE.items():
        body = body.replace("{{" + key.upper() + "}}", val)
    body = body.replace("{{BASE}}", base)
    body = body.replace("{{ARROW}}", ICON_ARROW)
    body = body.replace("{{LINE_BTN}}", line_btn())
    body = body.replace("{{LINE_BTN_LG}}", line_btn("btn btn--line btn--lg"))

    html = head + header(base, meta.get("active", "")) + "\n<main id=\"main\">\n" + body.strip() \
        + "\n</main>\n" + footer(base) + f'\n<script src="{base}assets/js/main.js" defer></script>\n</body>\n</html>\n'

    dest = ROOT / out_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print(f"  ✓ {out_rel}  ({len(html):,} bytes)")


def main() -> None:
    srcs = sorted(PAGES.glob("*.html"))
    if not srcs:
        raise SystemExit("tools/pages/ にページがありません")
    print(f"building {len(srcs)} pages …")
    for s in srcs:
        build_page(s)
    print("done.")


if __name__ == "__main__":
    main()
