# 發布前檢查（不合併、不推送、不發布）

## 無 JS 與慢載入

- 在 390px 觸控環境停用 JavaScript，以及攔住 navigation-final.js 直到手動釋放；兩種情況均可開啟原生 details 選單，五個單欄項目各高 52px，五個主頁均能換頁。
- JS 接上前，「選單」按鈕使用瀏覽器原生展開／收合；換頁使用原生 a，不依賴腳本。背景捲動鎖定、Esc、焦點管理在 JS 接上後啟用。
- 修復慢載入時未接手已展開選單的狀態：初始化呼叫 sync()，補上背景鎖定、aria-expanded 與焦點；17 頁移除預設 aria-expanded=false，保留原生展開語意。
- 不需新增常駐清單；原生選單已能使用。

## 四項播放器 baseline 差異（本次未修改）

- kuncan：baseline 為封面＋播放按鈕的延遲載入殼，目前為預先載入的 Google Drive iframe，影片 ID 相同。
- suifen：主片與創作分享播放按鈕增加 play-button--icon 樣式類別，影片 ID 相同。
- wenjin：播放按鈕增加 play-button--icon 樣式類別，影片 ID 相同。
- yuan：播放按鈕增加 play-button--icon 樣式類別，影片 ID 相同。

這四項在 main 已存在；沒有修改播放器、documentary.js 或 baseline。

## 五部備援來源與開啟驗證

完整網址、HTTP 狀態、頁面標題與原始來源行號記錄於 2026-10-09-fallback-verification.json。
suifen、kuncan、wenjin 使用各自 content/*.md 第 9 行；ABBY 使用 abby.html 既有主影片播放連結（同 content/abby.md 第 9 行）；yuan 使用 2026-10-08-網站微調驗收.md 第 53 行既有完整網址。
逐一核對 main 原始資料中的完整字串，未拼接、猜測或改寫 URL；五頁均 target="_blank"、rel="noopener"。
五個網址皆回應 HTTP 200，呈現對應影片名稱及播放介面；本次確認開啟，不測完整播放。

## stories 與區網預覽

stories 是舊版課程手記、四次活動與作品彙整入口，不需增加為第六個主導覽；作為仍可索引的舊網址保留既有 sitemap 記錄，本次不改。
唯讀預覽： http://192.168.50.182:8767/works.html ，綁定 0.0.0.0:8767，只接受 GET/HEAD，POST 回應 405，影片 Range 回應 206，未改防火牆。
preview 腳本置於忽略的 tmp/lan-preview.cjs，僅讀取 02_網站；不修改網站檔案、不提供目錄列表。iPhone 同 Wi-Fi 實測由使用者執行。
本機標籤 pre-uiux-polish 指向 main 的 ef8ca87d01fffa809b2bdd774704c027d9c88909；未推送。

## 測試處理

check_final_polish.py 的 summary 檢查改為原生 details 語意（JS 前沒有人工 aria-expanded）；四項播放器差異仍保留失敗。
check_navigation_browser.cjs 的捲動驗證改用 touchscreen.tap，保持原有恢復位置斷言：locator.click 會先自動捲動 sticky header，在修改前與修改後皆將 500px 改成 70px；觸控座標在兩版皆可恢復 500px。
新增 check_prepublication.cjs 與無 JS／慢載入驗證記錄。
