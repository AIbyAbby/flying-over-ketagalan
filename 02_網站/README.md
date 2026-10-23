# 網站第一版

以本機 HTTP 伺服器開啟 index.html。網站為純 HTML/CSS/JavaScript，無需安裝套件或建置。

2026-10-03 雜誌閱讀版：首頁、故事目錄、土地的記憶（老師全文）、四篇田野紀實、四篇影像作品，另保留 fieldwork.html 總覽入口，共12個HTML。PDF 位於 materials；照片及影片截圖位於 assets；正式整理文字位於 content。

影片由 Google Drive 載入。若嵌入無法播放，使用「在雲端觀看」按鈕。

2026-10-23 作品增補：侯淑敏四部影片及一份圖像簡報加入「05 影音創作」。新增文案以 `content/hou-shumin.md` 為來源，素材對應保存在 `content/hou-shumin-media.json`。使用 `python build_hou_shumin.py` 從目前正式版頁面更新這五件作品與作品導覽；程式可重跑，不會重複插入卡片。它不取代舊版產生器，且會檢查正式版導覽結構，避免誤套舊版頁面。

目前樣式為 magazine.css，互動程式為 documentary.js。執行專案根目錄 build_site.py 可重新產生頁面。老師正文依原文與照片順序完整整理；四份掃描通告文字人工轉寫於 content/notice-*.md。

GitHub Pages 可發布本資料夾根目錄；使用網站需要的HTML、magazine.css、documentary.js、assets、content及 .nojekyll。不要上傳專案根目錄 MP4、tmp 或原始影片。未正式發布。
