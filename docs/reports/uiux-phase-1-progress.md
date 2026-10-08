# UI/UX 階段 1：進度與交接審查

## 已完成（尚未完成整個階段／尚未 commit）

- :root 設計變數與既有別名已建立，主色保留 #234f56；正文暖紙色 #faf8f3 與文字 #1f2a2c。
- 正文 clamp 實測：375px 為 17.0711px，1440px 為 19px；兩個寬度均無橫向溢出。
- Google Fonts 官方來源及 OFL 授權已下載，本地 WOFF2 子集以網站實際文字製作；不提交原始 TTF。
- 3 個字型檔總容量 **391,796 bytes（391.8 KB／382.6 KiB）**，小於規格 400 KB。
- 比較過本地製作方式：可變字體子集 496,320 bytes；全字集靜態字重 548,028 bytes；依正文／標題用途分配字形的靜態版本 391,796 bytes，選用最後者。
- 這是字型檔容量比較，不冒充 Google Fonts 與正式 GitHub Pages 在同一網路條件下的載入速度比較。新版本尚未發布，正式站速度未實測。
- 17 頁保護檢查通過：原文段落順序、影片控制與 ID、播放連結、語系、聯絡佔位與成品路徑保留。

## 未完成／待驗收

- 標題字體覆蓋與 stylesheet 快取版本已修正，心得 h2 實測使用 Serif；全站 h1/h3 還需逐頁驗收。
- h3、所有實際文字／背景／焦點狀態對比與九種尺寸尚未全部驗收。不存在「全站已完成」的結論。
- 原 walks.css 的變更保留；其散落字級／色碼尚未納入轉換。其他歷史 CSS 的 :root 舊值需再整理，不能宣稱全站已無殘留。
- 完整 Google Fonts 外部載入比較、CLS、Lighthouse、影片 Performance trace 尚未取得。瀏覽器工具的唯讀頁面範圍不提供 performance 物件，沒有捏造數字。
- 深色模式為選做，尚未執行。

## 同時寫入觀察

作業時工作區出現非本回合製作的創作心得 reflection-card 樣式，直接加入同一份 uiux-polish.css，並有相關內容／renderer 變化。分支基線前另有 c53ea81（走讀手機修正）與 9b3d500（空拍按鈕）提交；因此階段零所寫 d3a3c9b 是已確認發布的那一版，並非分支實際父提交。uiux-polish 的 phase-0 提交為 27a02d4，父提交 c53ea81。

使用者已確認由 Codex 接手，A 暫停所有寫入。Abby／玉安心得卡已獨立審查並完成最小補修，詳見 reflection-review.md；本報告不代表整個 UI/UX 階段已完成或已發布。

## 檔案清單

- 設計與字體：02_網站/uiux-polish.css、uiux-fonts.css、assets/fonts 的 3 個 WOFF2 與 2 份 OFL 授權。
- 9 份 CSS 的色碼／字級引用整理：aviation、documentary、editorial-home、editorial、magazine、reading-layout、stories-trial、styles、video-layout。walks.css 未由本回合修改。
- 17 份成品 HTML 的字型／設計 stylesheet 引用。
- 來源：build_first_version.py、editorial_home.py。
- 保護檢查：tests/check_uiux.py、tests/uiux-content-baseline.json。
- 數據：uiux-phase-1-fonts.json（第一次方案）、uiux-phase-1-font-final.json（目前方案）；本報告。

## 最終字型值

- NotoSansTC 400: 212,520 bytes
- NotoSansTC 700: 107,796 bytes
- NotoSerifTC 700: 71,480 bytes
