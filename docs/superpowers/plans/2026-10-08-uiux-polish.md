# UI/UX Polish Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 依使用者確認的 UIUX-SPEC.md 分階段微調靜態網站，保留文字順序、學員名單與播放入口。
**Architecture:** 沿用既有 Python 頁面產生器與純 CSS/JS，不增框架或建置工具。共用 HTML 在 shared_components.py，階段樣式保持既有 CSS 的責任；正式 Markdown/JSON 不改意思。
**Tech Stack:** 靜態 HTML/CSS/JavaScript、既有 Python/Pillow；既有 fontTools 可用於一次性字型最佳化。
**Spec:** UIUX-SPEC.md

## Global Constraints
- 分支 uiux-polish，每階段 commit 訊息 phase-N: 簡述。
- 姓名、名單（含張穗芬與 SF Chang）和段落順序不變。
- 引言可見標題不恢復，但 h3 視覺隱藏且整卡連結有名字。
- 播放 URL、影片 ID、嵌入方式不動；16:9 尺寸與 scroll-margin 可調。
- noindex 不加入；［聯絡方式待補］保留；不使用原住民紋樣。
- 新要求與已確認樣式衝突先問；階段外問題只列出。
- 既有 walks.css 外部修改保留，不納入本次提交。

## Review Focus
- 手機 drawer 鎖焦點、背景捲動與返回焦點；窄平板導覽不換行。
- 長中文標題與使用者放大字體不溢出，正文閱讀線長與影像寬度分開。
- 圖片／字體換源與 CLS，所有內容 glyph 含姓名不遺漏。
- 播放入口只有一個且覆蓋層不攔截、影片 URL 與原始內容順序不變。
- 使用者既有未提交變更不得混入 phase commits；不發布新分支。

## Tasks
- [x] Phase 0: 建立分支、正式版確認、CSS 盤點、規格例外同步；commit。
- [ ] Phase 1: :root 色彩／字級／間距／字體統一；字重最小化與下載量比較；對比及 375/1440 實測；phase-1 commit。
- [ ] Phase 2: 五項編號導覽、行動選單鍵盤/焦點、stepper、breadcrumb、頁內目錄、閱讀序列/作品序列/浮動 top；phase-2 commit。
- [ ] Phase 3: 隱藏 h3 的整卡入口、指定 CTA、保留作品順序、頁尾與名單、圖片/卡片節奏；phase-3 commit。
- [ ] Phase 4: 檢核既有 SEO/分享/圖示/sitemap、補所有非互動圖片尺寸/響應式；播放封面只補載入屬性且保持入口方式；phase-4 commit。
- [ ] 最终 QA: 每階段以基線比對正文、名單及播放器 HTML；九種尺寸無溢出、鍵盤操作、對比、font bytes、CLS/Lighthouse 有實測才記分數。留存截圖與逐項未完成。正式發布等待使用者指示。
