# 株式会社Ideal properties — 譲渡型賃貸 公式サイト

> 空室の不安を消し、住まう喜びをカタチにする。

住宅ローンをご利用になれない方へ「譲渡型賃貸」をご紹介するための、静的ウェブサイトです。
ビルドツール・フレームワーク・npm パッケージへの依存はありません。生成された HTML/CSS/JS を
そのままサーバーへアップロードすれば公開できます。

---

## ページ構成

| ファイル | ページ | 内容 |
| --- | --- | --- |
| `index.html` | トップ | キャッチコピー／お悩み／仕組み／5つのメリット／生涯コスト／流れ／事業内容／ニュース／FAQ／お問い合わせ |
| `about.html` | 譲渡型賃貸とは | 仕組みの詳解、5つのメリット、50年間の生涯コスト比較、戦略的比較 |
| `service.html` | 事業内容 | 入居者向けサービス、物件仕入れ・企画開発、オーナー・投資家向け投資支援 |
| `flow.html` | ご利用の流れ | お問い合わせ〜所有権移転までの9ステップ |
| `simulator.html` | コスト比較 | 生涯コスト3プラン比較シミュレーター（既存資産を本サイトに統合） |
| `faq.html` | よくあるご質問 | 審査／費用／暮らし／契約の4カテゴリ・全17問 |
| `news/index.html` | ニュース・トピックス | 一覧（カテゴリ絞り込み付き） |
| `news/*.html` | 記事 | NEWS / TOPICS / COLUMN の記事ページ |
| `company.html` | 会社概要 | 代表メッセージ、私たちが守ること、会社情報、アクセス |
| `contact.html` | お問い合わせ | LINE／電話／フォームの3導線 |
| `privacy.html` | プライバシーポリシー・免責事項 | 個人情報保護方針、掲載内容・シミュレーションに関する免責 |

## ディレクトリ

```
.
├── index.html …… 生成物（直接編集しないでください）
├── about.html / service.html / … 同上
├── news/                      生成物
├── simulator.html             既存シミュレーター（手動管理）
├── assets/
│   ├── css/style.css          デザインシステム（全ページ共通）
│   ├── js/main.js             ナビ・スクロール演出・アコーディオン・フォーム
│   └── img/                   画像（現在は未使用）
└── tools/
    ├── build.py               ビルドスクリプト
    └── pages/*.html           ページ本文のソース ← 編集はこちら
```

## 編集・ビルド方法

ヘッダー・フッター・`<head>` は `tools/build.py` が全ページへ自動で差し込みます。
**ルート直下の HTML は生成物です。編集は `tools/pages/` 側で行ってください。**

```bash
# 本文を編集したあと
python3 tools/build.py

# ローカル確認
python3 -m http.server 8000   # → http://localhost:8000
```

`tools/pages/*.html` の先頭にはフロントマターがあります。

```
---
out: about.html            出力先パス
title: ページタイトル       <title> と og:title
desc: ページ説明            meta description と og:description
active: about.html         ヘッダーで現在地としてハイライトするリンク
ogtype: article            省略時は website
---
```

本文では以下のプレースホルダーが使えます。値は `tools/build.py` の `SITE` にまとまっています。

`{{NAME}}` `{{NAME_EN}}` `{{CATCH}}` `{{TEL}}` `{{TEL_HREF}}` `{{LINE_ID}}` `{{LINE_URL}}`
`{{ADDR}}` `{{HOURS}}` `{{BASE}}`（相対パスの基準）`{{ARROW}}`（矢印アイコン）
`{{LINE_BTN}}` `{{LINE_BTN_LG}}`（LINEボタン）

### ニュース記事を追加する

1. `tools/pages/` に新しいフラグメントを作成（既存の `10-news-loan.html` などをコピーするのが簡単です）
2. `tools/pages/09-news-index.html` の一覧に `<li class="news__i" data-cat="…">` を1行追加
   （`data-cat` は `news` / `topics` / `column`）
3. `python3 tools/build.py` を実行

## デザイン

- **イメージカラー**：ビビッドグリーン `#00E15E`（明るい背景では `#00702E` に切り替わり、可読性を確保）
- **ベース**：ダーク `#050C08` ／ ライト `#F2F6F3`
- **書体**：Zen Kaku Gothic New（見出し）／ Noto Sans JP（本文）／ Archivo・JetBrains Mono（英字・数値）
- 配色・余白・角丸・モーションはすべて `assets/css/style.css` 冒頭の CSS カスタムプロパティで一元管理しています。
  色を変える場合は `:root` の値だけを差し替えてください。

### 品質チェック済みの項目

- 全11ページで文字コントラスト **WCAG 2.1 AA** を達成
- 横スクロール発生なし（375px〜1920px）
- JavaScript エラーなし／リンク切れなし／HTML のタグ構造エラーなし
- `prefers-reduced-motion` に対応（演出を抑制）
- JavaScript 無効環境でも全文が表示される（`<noscript>` フォールバック）
- キーボード操作対応（スキップリンク、`:focus-visible`、アコーディオンの `aria-expanded`）

## 公開前に必要な作業

1. **お問い合わせフォームの送信処理**
   現在はフロントエンドの入力チェックのみで、送信は行われません（`assets/js/main.js` の
   `data-contact-form` 部分）。メール送信 CGI、または外部フォームサービスへの接続が必要です。
2. **会社情報の確定**：所在地・電話番号・設立・代表者・資本金・**宅地建物取引業免許番号**
   （`tools/build.py` の `SITE` と `tools/pages/06-company.html`）
3. **本番ドメインの設定**：`tools/build.py` の `SITE["origin"]`（canonical・og:url に使用）
4. **OGP画像**の用意と `<head>` への追加
5. **Googleマップ**の埋め込み（`tools/pages/06-company.html` のプレースホルダー部分）
6. **アクセス解析**タグの設置
7. 掲載中のシミュレーション数値・免責事項について、**専門家（宅建士・税理士等）による確認**
