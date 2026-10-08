# 創作心得可展開卡片：交接審查與驗收

日期：2026-10-08。範圍為 A 交接的 Abby、玉安心得卡；整個 UI/UX 計畫尚未完成，本次未推送或發布。

## 改動範圍審查

- 已檢查 git status、git diff。工作區除 A 的四個交接檔案，還有 Codex 先前進行中的全站字型／樣式與成品引用調整；不能把整份 dirty status 歸因於 A。
- 可辨認的心得元件落在 uiux-polish.css、work-reflection.js、abby.html、yuan.html。以交接前 tmp/uiux-baseline 比較，suifen、kuncan、wenjin 的 main 正文完全一致，這三頁只有先前的 stylesheet 引用變更。
- 沒有 A 修改前的獨立 commit，無法僅靠 git 精確證明每一行的作者歸屬；本報告以實際差異與保留的 baseline 為依據。
- documentary.js 與 baseline 位元組完全相同；SHA-256 已保存在 tests/reflection-baseline.json。

## 審查後的最小補修

1. 心得 CSS 使用既有顏色、字級、間距變數；新增集中式邊框、圓角、48px 控制高度、焦點、陰影與動態時間變數。元件內移除散落的色碼及寫死的 px；media query 用 48rem，CSS 變數不放入不支援變數的 media 條件。
2. summary 採原生控制，移除其內的 div；標題直接位於 summary，不包在僅允許 phrasing content 的 span。補齊 active，使用 reflection-* 前綴避免與其他 toggle 元件混淆。
3. JS 捲動尊重 prefers-reduced-motion，實際量測固定／sticky header 高度，收合後 focus 返回 summary。列印後恢復列印前的展開狀態；無 JS 時隱藏無法作用的文末按鈕，仍可用 summary 收合。
4. 同步既有 build_first_version.py 的心得 renderer 與兩頁條件式 script 引用，防止日後重建抹掉交接成果；未新增建置工具或更動 documentary.js。

## 逐項驗收

| 項目 | 狀態與證據 |
|---|---|
| 原生 details／summary、无 JS 可展開 | 已完成。兩頁各建立暫時的零 script 副本，以瀏覽器 Enter／Space 實測切換；副本已刪除，不列入網站或 sitemap。 |
| aria-labelledby 與階層 | 已完成。指向唯一 creator-note-title h2，正文 h3 保留；瀏覽器無障礙樹顯示原生 expanded／collapsed。 |
| 小標、作者、閱讀時間、兩行預覽 | 已完成。Abby 約 3 分鐘、玉安約 4 分鐘沿用交接值；兩行 clamp 及 mask fade 實測。 |
| 閱讀全文 ＋／收合 －、整列可點、48px | 已完成。summary 原生整列控制，標籤按 open 切換；控制列實測約 47.998px，CSS min-height 為 48px。 |
| 文末收合、焦點、header 避讓 | 已完成。實際點擊後 open=false、焦點回 summary；375px 玉安卡頂約 268px，header 底約 156px，未遮住。 |
| #reflection 載入自動展開 | 已完成。兩頁以完整 URL 載入，確認 open=true；舊 creator-note-title／creator-note 錨點亦保留。 |
| hover／active／focus-visible | 已完成樣式及焦點實測。summary focus-visible 為實線 outline；原生 Enter／Space 與實際點擊均可切換。hover／active 規則已核對，未聲稱逐平台觸控狀態測試。 |
| 減少動態效果 | 已完成 CSS／JS 補修與事件邏輯測試。CSS 取消 animation／transition；JS 選 instant 捲動。未修改使用者 OS 設定，沒有冒充真實 OS 減少動態效果的端到端驗收。 |
| 列印時自動展開 | beforeprint／afterprint 事件邏輯測試已通過，包含重複 beforeprint 與狀態恢復。內建瀏覽器 Ctrl+P 沒有開啟列印 UI，實際列印預覽／PDF 分頁仍未驗收。 |
| hidden=until-found／搜尋 | 不疊加 hidden 狀態。原生 details 已有標準搜尋祖先展開機制；既有 [hidden]{display:none!important} 不適用 until-found 所需的 content-visibility 行為。瀏覽器原生搜尋 UI 與跨引擎結果仍未實測，不能宣稱所有瀏覽器皆通過。 |
| 正文、標題、段落順序 | 已完成精確比對。Abby 30 個 h2/h3/p 區塊、玉安 26 個區塊，含作者段，一字未改、順序相同。 |
| JS 載入範圍／影片保護 | 已完成。17 頁只有 Abby／玉安引用 work-reflection.js。所有原影片連結、控制、ID 與 documentary.js 通過 baseline 檢查；本次未重新實測各第三方影片串流。 |

搜尋實作依據：[HTML Standard：find-in-page 與 details 的祖先展開](https://html.spec.whatwg.org/multipage/interaction.html#find-in-page)。標準依據不等同各瀏覽器實測。

## 實際尺寸結果

| CSS viewport | 兩頁水平溢出 | 預覽兩行高度／每行高度 | 操作列 |
|---|---|---|---|
| 375px | 無 | 約 63.15／31.58px | 約 48px |
| 390px | 無 | 約 63.29／31.64px | 約 48px |
| 768px | 無 | 約 66.06／33.03px | 約 48px |
| 1440px | 無 | 約 70.30／35.15px | 約 48px |

使用 Codex 內建 Chromium 預覽，尺寸經 innerWidth 校準；不是實體手機或 Safari 測試。暫時 viewport 已重置。

## 本次補修檔案

- 02_網站/uiux-polish.css
- 02_網站/work-reflection.js
- 02_網站/abby.html
- 02_網站/yuan.html
- build_first_version.py：同步既有來源，避免重建回退
- UIUX-SPEC.md：新增交接約束，不改已確認的引言卡片或作品頁順序
- tests/check_reflection.py、tests/check_reflection_events.cjs、tests/reflection-baseline.json
- 本報告、uiux-phase-1-progress.md，以及 reflection-abby-375.png、reflection-yuan-375.png、reflection-desktop.png

## 驗證命令

- python build_first_version.py --pages abby.html yuan.html：成功重建兩頁。
- python tests/check_reflection.py：56 個原始區塊、原生標記、載入範圍、播放器鎖定通過。
- node tests/check_reflection_events.cjs：減少動態、錨點、收合焦點、header 高度、列印展開／恢復通過。
- python tests/check_uiux.py：17 頁原文段落、影片 ID／控制／連結、語系、聯絡佔位與檔案路徑通過。
- node --check 02_網站/work-reflection.js、git diff --check：通過。

## 未完成／需另驗

實際列印預覽、原生搜尋 UI、Safari／Firefox 與實體手機尚未驗收。整站 UI/UX 的後續導覽、頁尾、所有尺寸及效能檢核仍未完成，不因本次心得卡審查而視為全站收尾。


## 定案與補充驗收（2026-10-08）

- 心得卡不新增 Esc 收合，不採 hidden="until-found"，使用者已定案。
- 3-2 的作品順序規則在第 210 行；第 213–218 行補入心得卡的原文保留、兩行預覽、48px 操作、Enter／Space、焦點返回、錨點／列印／減少動態、搜尋決定與獨立 JS／來源同步；該節無 Esc 收合驗收條款。導覽選單的 Esc 規則保持原樣。
- 8 張截圖存於本報告同目錄：reflection-{abby|yuan}-{375|1440}-{closed|open}.jpg，不直接貼入文字審查回報。
- 頁面高度（CSS px）：375 Abby 4973→9118（+4145）、玉安 4052→8262（+4210）；1440 Abby 4893→7481（+2588）、玉安 3826→6429（+2603）。完整數據為 reflection-height-metrics.json。
- 減少動態效果：work-reflection.js 依 prefers-reduced-motion 使用即時捲動，uiux-polish.css 取消心得動畫／transition。
- 焦點返回：work-reflection.js 文末收合後將焦點交回 summary 並避開 header。
- 重建來源同步：build_first_version.py 的原有 renderer 改輸出相同 details 卡片，僅兩頁載入独立腳本，避免重建覆蓋。
- 心得卡提交與階段 1 尚未完成的工作區修改分開；本報告截圖量測來自目前工作區，包含既有階段 1 字型／設計調整，不代表該階段全部已提交或驗收通過。
