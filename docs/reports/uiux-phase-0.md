# UI/UX 階段 0：盤點與部署確認

## 已完成

- 作業分支 `uiux-polish`，基線為已發布的 `d3a3c9b`。正式引言已實際開啟核對：回頂端為 `#top`、有「下一頁 課程手記」、目前導覽有 `aria-current="page"`。規格中先前觀察到的三項缺漏已在上一輪修好。
- 最新老師致謝與引言卡片可見標題移除已正式上線。
- 已保存 `tmp/uiux-baseline`，內容、名單、影片區塊可逐階段比對；不提交本機備份。
- `UIUX-SPEC.md` 已同步使用者確認：引言保留既定外觀、h3 視覺隱藏；作品頁段落順序保留。新規格與既定樣式衝突先詢問。
- 全部 10 份 CSS 已盤點；詳細數值及逐檔用途見 `uiux-phase-0-inventory.json`。

## 數量與用途

|類型|不重複宣告值數量|
|---|---:|
|colors|139|
|font-family|13|
|font-size|109|
|font-weight|6|
|line-height|22|

另有 64 種 font shorthand。以上為宣告值詞彙數，不將縮寫 hex、rgba 與實際合成色誤稱為不同感知色；包括未被目前頁面載入的歷史 CSS。正文、按鈕、卡片與導覽存在多層覆寫，階段一將統一為設計變數。

既有主要用途：paper／paper-soft 為紙色底；ink／muted 為正文與次要字；river-dark／river 為標題連結；brick 為點綴；moss／gold 多屬裝飾；rgba 多屬遮罩、邊框、陰影。

## 對比初步清單（既有基線）

上一輪實際頁面色組：主色 #234f56 對 #f5efe4 約 7.89，正文 #25352f 約 11.26，次要字 #59675f 約 5.20，河水色 #2e737c 約 4.75，磚紅 #9b5b43 約 4.62。已修正的目前導覽色組約 7.20。以上不是全 10 份 CSS 的所有可能色組認證。

歷史 moss #6f7d55 與 gold #c79b55 對紙色可能不足一般文字 4.5:1，不應套在小字；透明字、圖片疊字、hover／focus 的合成背景須於階段一再實測，不能僅靠 CSS 詞彙盤點判定。

## 未完成／需確認

- 全站實際狀態對比與字體載入量、CLS 在階段一量測。完整 Lighthouse 及影片 Performance trace 需工具支援，沒有數據時明記未量測。
- 字體目前 Google Fonts 要求兩家族共 10 字重，尚未測得實際下載 bytes。
- 作業開始即存在 walks.css 未提交變更，與本次無關；階段零 commit 不包含它。
- 不更改影片 ID／嵌入方式。A 已回報 11 部影片正常，附錄 A 歷史存取問題不再猜測成卡頓原因。

## 改動檔案

UIUX-SPEC.md、docs/reports/uiux-phase-0-inventory.json、本報告，以及 docs/superpowers/plans/2026-10-08-uiux-polish.md。
