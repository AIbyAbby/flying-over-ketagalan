# 靜態網站最後微調 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 完成使用者階段二的版面、無障礙、SEO 與非影片圖片微調。

**Architecture:** 沿用現有 Python 靜態輸出與共用元件；產物仍是 HTML、CSS、JS 與圖片。影片診斷與修正分開，播放器區塊與影片 JS 不變。

**Tech Stack:** 現有 Python/Pillow、原生 HTML/CSS/JS，無新框架或建置工具。

**Spec:** 本次使用者訊息的階段一、階段二 A–F 與完成回報要求。

## Global Constraints

- 不改內容意思、段落順序、任何學員姓名與名單。
- 階段一僅診斷；影片相關修改須使用者確認。
- 保留本次開始時既有未提交改動；不提交、不推送、不發布。
- 聯絡方式保留「［聯絡方式待補］」，不加 noindex。

## Review Focus

- 窄螢幕導覽能換行，展開選單可用鍵盤與觸控。
- 卡片標題連結有清楚焦點，作者與簡介不被讀成連結文字。
- 圖片尺寸與 picture 包裝不能改變拼貼裁切或播放器封面。
- 每页分享網址使用正式絕對網址，圖片 fallback 存在。
- 原文與參與名單逐段比對，影片 HTML/JS 與基線逐字比對。

## Tasks

- [x] 保存基線；先跑缺項檢查。
- [x] 修改 shared_components.py、build_first_version.py、editorial_home.py：作品卡片、署名、head、頁尾與前後頁。
- [x] reading-layout.css 補閱讀字體、焦點、觸控尺寸與手機導覽；保留影片樣式。
- [x] 建立 WebP 衍生圖片、og-cover、favicon；建立 404、robots、sitemap。
- [x] 全頁結構、內容保存、連結與圖片檢查；實測 375/390/768/1280。
- [x] 寫出影片診斷與逐項完成報告；列出無法量測或需要確認項目。

## 驗收紀錄

階段二非影片範圍完成；17 頁靜態驗證與 64 次響應式檢查通過。影片 Performance/Network 完整量測及 11 個播放器封面屬性待確認；保留在報告中，不宣稱完成。沒有提交／發布。獨立複核後修補 404 路徑、敘述字體与 srcset 寬度，dry-run 0 差異。
