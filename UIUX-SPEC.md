# 《消失的原民故事》網站 UI/UX 優化規格

網站：https://aibyabby.github.io/flying-over-ketagalan/
性質：純靜態網站（GitHub Pages），已進入最後階段。
頁面：index / intro / teacher / fieldwork / walks / works / abby / suifen / kuncan / wenjin / yuan

## 全域規則（所有階段都必須遵守）

1. 只做版面、文字呈現、無障礙、SEO、效能的微調。不重構架構、不引入框架或建置工具。
2. 不改動內容的意思與段落順序。
3. **參與學員姓名與名單一律不更動**（包含「張穗芬」與「SF Chang」，保持原樣）。
4. 不要加 noindex。
5. 依使用者最新確認，頁尾不顯示版權與聯絡方式文字。
6. 不使用任何原住民圖騰或刻板的泛原住民紋樣與配色。
7. 在分支 `uiux-polish` 上作業，每個階段完成後 commit，訊息格式：`phase-N: 簡述`。
8. 發現規格以外的問題：只回報，不要自行修改。
9. 每階段結束回報：已完成／未完成／需我確認、改動檔案清單、驗收結果。

---

## 階段 0：盤點與部署確認

- 確認前一輪改動是否已 commit／push 並部署到 GitHub Pages
  （線上版曾觀察到：「回到頁首」仍指向 #main、無上一頁／下一頁、無目前頁面標示）。回報現況。
- 盤點所有 CSS：不重複顏色數量與用途、字體堆疊／字級／字重／行高的不重複數量、
  對比不足 WCAG AA（一般文字 4.5:1、大字與圖示 3:1）的組合清單。

---

## 階段 1：設計系統（字體與配色，最先執行）

目標氣質：安靜、有溫度的田野紀錄。主色維持 `#234f56`。

### 1-1 色彩變數（寫在 :root，全站只能引用變數，禁止散落色碼）

以下為建議起點，請實測對比後微調，並回報最終值與實測對比。

| 變數 | 建議值 | 用途 |
|---|---|---|
| --color-primary | #234f56 | 主要按鈕、連結、目前頁面 |
| --color-primary-hover | #1a3d43 | 主色 hover |
| --color-primary-soft | #e8f0ef | 淺底、目前頁面底色 |
| --color-accent | #a9532c | 點綴（陶土赭紅）：小標、編號、重點線，約 10% |
| --color-bg | #faf8f3 | 頁面底色（暖紙色） |
| --color-surface | #ffffff | 卡片底 |
| --color-surface-alt | #f1f4f2 | 區塊交替底色 |
| --color-text | #1f2a2c | 正文（不用純黑） |
| --color-text-muted | #4a5a5d | 次要文字（對 bg 與 surface 皆須 ≥ 4.5:1） |
| --color-border | #d5dcd8 | 邊框 |
| --color-focus | 與相鄰色對比 ≥ 3:1 | 焦點外框 |

比例：約 60% 背景與留白、30% 主色與深色文字、10% 點綴色。

### 1-2 五區辨識色（只用於卡片左色條、編號圓點、進度列小標記，不大面積鋪色）

- 引言：主色
- 手記（課程手記）：青綠 teal，接近主色
- 空拍（空拍紀錄）：天空藍灰，例如 #3d6a80
- 走讀（現場走讀）：苔綠，例如 #5a6b3a
- 創作（影音創作）：陶土赭紅，接近點綴色

彼此一眼可分，明度相近、飽和度偏低，不像彩虹。**不可是唯一的區別方式**，須搭配文字與編號。

### 1-3 字體

- 標題：`"Noto Serif TC", "Songti TC", "PMingLiU", serif`，字重 600–700
- 內文：`"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", system-ui, sans-serif`，字重 400／500／700，不用 300 以下
- 數字、編號、片長：`font-variant-numeric: tabular-nums`
- 若襯線標題在小字級（手機 < 20px）不易讀，h3 以下退回無襯線並說明理由
- 若使用者之後要求全站單一無襯線字體，以 Noto Sans TC 為唯一字體

載入與效能（不可造成卡頓）：
- 只載入實際用到的字重；使用 display=swap 與 preconnect，或自行 subset 後本地託管 woff2
- 比較兩種方式的載入量與速度，選擇較佳者並回報數據
- 不可造成明顯版面位移；字體 CSS 放 `<head>`，不可阻塞影片 iframe
- 回報字體總載入量（KB）；若 > 400KB 須 subset 或減少字重

### 1-4 字級與排版（用 clamp，避免斷點跳動）

```
--text-xs:   0.8125rem                                       說明、片長、圖說
--text-sm:   0.9375rem                                       次要資訊
--text-base: clamp(1.0625rem, 1.02rem + 0.2vw, 1.1875rem)    正文（手機約 17px、桌機約 19px）
--text-lg:   clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem)         h3、卡片標題
--text-xl:   clamp(1.5rem, 1.3rem + 1vw, 2rem)               h2
--text-2xl:  clamp(1.875rem, 1.5rem + 1.8vw, 2.75rem)        h1
```

- 行高：正文 1.85、標題 1.35、卡片小字 1.6
- 字距：正文 0.02em、標題 0.01em
- 欄寬：正文 36–40 個中文字（max-width: 38em）
- 靠左對齊，不使用兩端對齊
- `text-wrap: balance`（標題）、`text-wrap: pretty`（段落）、`line-break: strict`、`text-autospace: normal`
- 段落間距 1em；h2 上方間距明顯大於下方
- 不用斜體；強調用字重或色塊，底線留給連結

### 1-5 連結、按鈕與焦點

- 內文連結：主色＋底線（`text-underline-offset: 0.2em`）
- 按鈕三種：主要（主色底＋白字）、次要（主色外框＋主色字）、文字連結（底線）
- 高度 ≥ 44px（主要按鈕 ≥ 48px），圓角、字級、內距全站一致
- 狀態齊全：hover、active、:focus-visible（2–3px 外框，與元素保持 2px 間距）、disabled
- 按鈕間距 ≥ 8px；手機版主要按鈕可滿版
- 箭頭「→」「▶」等裝飾符號加 `aria-hidden="true"`；外部連結（YouTube）加視覺與 sr-only「另開新視窗」提示

### 1-6 圖片、卡片、表面

- 圖片圓角 8–12px、1px 邊框、圖說用 --text-xs 與 --color-text-muted
- 卡片：白底、1px 邊框、單層低透明度陰影；hover 只改邊框色與微位移
- 區塊背景在 --color-bg 與 --color-surface-alt 交替
- 全景圖上若有疊字，加漸層遮罩，疊字對比 ≥ 4.5:1

### 1-7 深色模式（選做）

`prefers-color-scheme: dark` 的變數覆寫，不做切換按鈕。若有風險則略過並回報。

### 階段 1 驗收

- 對比檢查表：每組文字／背景／按鈕／連結／焦點外框的色碼與實測對比值
- 字級實測：375px 與 1440px 的 h1／h2／h3／正文實際像素值
- 字體總載入量與位移情形
- grep 檢查全站已無散落色碼與寫死字級，回報殘留處

---

## 階段 2：導覽與「我在哪」（2026-10-09 使用者指令優先）

- 17 頁使用同一份 header、五項單層導覽與簡潔頁尾；保留 skip link、#top、canonical、Open Graph 與 description，不加 noindex。
- 導覽順序為 01 引言、02 課程手記、03 空拍紀錄、04 現場走讀、05 影音創作；現場走讀與影音創作維持主導覽，移除空拍下拉。
- ≤768px header 單行 56px；網站名不換行、過長省略；選單開關至少 44px。
- ≥769px 桌面導覽單行；可用寬度不足則用同一個選單。選單列至少 52px，目前項目有底色、粗體、左色條、「目前頁面」與 aria-current。
- 原生 details 選單配獨立 navigation-final.js：背景鎖捲動、焦點鎖定、Esc／背景／關閉按鈕可關閉，焦點返回開關。不修改 documentary.js，不使用 JS 導航。
- 空拍總覽提供四次活動的本頁導覽；子頁有麵包屑與前後頁／全部空拍入口，從選單至任一活動最多三次點擊。
- 五個主頁底部用至少 64px 的前後頁卡片；桌面左右、手機上下，缺少相鄰頁時改為回到引言。
- 作品切換放最上方麵包屑列，內容區塊之前；順序 suifen → kuncan → wenjin → yuan → abby。
- 作品頁結尾有前後作品卡片；手機另有 56px 底部操作列與 safe-area 留白，端點返回全部作品。作品頁停用浮動頂端按鈕。
- 其他頁保留現有回頂端入口；一律 href="#top"。
- 所有 hover 僅限 (hover: hover) and (pointer: fine)；卡片各一個 h3 標題連結，以 stretched-link 覆蓋全卡，有 active、touch-action: manipulation 與柔和點擊色。
- 影片備援只沿用可核實的既有完整網址；ABBY 用既有 YouTube，其他用既有影片網址，target="_blank"、rel="noopener"。不修改播放器、網址與 documentary.js。
- 驗收 320、360、390、430、768、1024、1440px；卡片四種位置單次點擊、選單焦點與捲動、固定元素留白、17 頁功能核對表。

---

## 階段 3：頁面與元件

### 3-1 引言頁（intro.html）

- 「在這裡，可以讀到什麼」保留剛確認的圓形標籤與介紹文字，四個入口以 01–04 編號及整卡 stretched-link 呈現。每張卡片保留視覺隱藏的 h3（不得 display:none）作為連結名稱；不恢復可見標題。
  整張可點（stretched-link），桌機 2×2 等高、手機 1 欄，卡片間距 ≥ 12px。
  hover 與 :focus-visible 同等樣式。
  原本長段落請保留全文，手機版若過長可截斷至 3 行並提供展開；不適合截斷就只調整層次與間距並回報。
- 前三段引言之後加主按鈕「從課程手記開始閱讀 →」與次要按鈕「直接看影音創作」，
  桌機並排（主按鈕在左）。**按鈕文案維持這兩句，不自行改寫。**
- 全景圖：維持 aspect-ratio，`object-fit: cover` 與 `object-position` 保留重點（碼頭與廟宇），不變形、不造成橫向捲軸。
- 結尾加署名「— Abby 陳翠碧」（置於「希望這個網站能留住…」之後）。

### 3-2 影音創作（works.html）與作品頁

- 作品卡片不要整張一個 `<a>` 包全文。改為 h3 內放連結，用 stretched-link 維持整卡可點；
  作者、片長、簡介放在連結外；裝飾符號 `aria-hidden`。
- 桌機 2–3 欄等高；卡片內順序固定：縮圖／標題／作者與片長／簡介（3 行截斷）。手機 1 欄。
- 影音創作頁不重複顯示「鏡頭裡的故事」；保留視覺隱藏的 h2 供標題階層使用。
- 作品頁：保留現有順序，不搬動任何內容。影片仍套用 16:9 響應式、手機滿版寬，桌機置中且與內容容器對齊；標題以 scroll-margin-top 避免被固定 header 蓋住。


- 創作心得僅套用於 Abby、玉安頁，使用原生 details.reflection-card／summary；原文、作者姓名、標題及段落順序完全保留。
- 收合時保留標題、作者與兩行淡出預覽；Abby 不顯示「創作心得」小標與預估閱讀時間，玉安保留既有小標，移除預估閱讀時間。操作文字「閱讀全文 ＋／收合 －」，整列可點，控制高度至少 48px。
- 心得卡鍵盤驗收為 Enter／Space；文末收合後捲回卡片頂端、避開固定 header，焦點返回 summary。
- #reflection 載入自動展開；列印前展開、列印後恢復，prefers-reduced-motion 取消動畫與平滑捲動。
- 維持原生 details 搜尋展開機制，不採 hidden="until-found"。
- work-reflection.js 維持獨立且只在 Abby／玉安頁載入；同步既有重建來源，documentary.js 不因整併而更動。

### 3-3 頁尾

- 桌機三欄：左「站內導覽」（5 項，含 aria-current）、中「製作資訊」（主辦、指導老師、網站規劃）、右「版權與聯絡」。
- 頁尾保留回到頁首；依使用者最新確認，移除版權與聯絡方式整段文字。
- 參與學員名單維持原文與原順序；桌機多欄、手機單欄。

### 3-4 手機閱讀體驗

- 正文 17px、行高 1.85、段距 1em、左右留白 ≥ 20px，內容不超出螢幕。
- 頁尾的主辦／指導老師／網站規劃／參與學員手機版改單欄，小標與內容分行。

### 3-5 桌機版面節奏

- 主內容容器 max-width 約 1100px，正文欄 36–40 個中文字；圖片、影片、卡片可比正文欄更寬（窄文字、寬影像）。
- 建立統一間距尺度（8／16／24／32／48／64px）並全站套用，取代零散數值。

---

## 階段 4：SEO、分享、圖片

- 每頁獨立的 meta description（60–80 字內，繁體中文，貼合該頁）。
- 每頁加 Open Graph／Twitter Card：og:title、og:description、og:type=website、
  og:url（絕對網址）、og:locale=zh_TW、og:image。
  og:image 以 assets/intro-panorama.jpg 裁成 1200×630 另存為 assets/og-cover.jpg；作品頁若有縮圖則用各自縮圖。
- favicon（主色 #234f56，提供 .ico 與 180px apple-touch-icon）。
- index.html 改為 `<meta http-equiv="refresh" content="0; url=intro.html">`＋canonical＋`<noscript>` 連結，title 改為「消失的原民故事」。
- 新增 404.html（風格一致，附回到引言與主要導覽）。新增 robots.txt 與 sitemap.xml。
- 確認 `<html lang="zh-Hant-TW">`；跳到主要內容連結在鍵盤聚焦時可見。
- 所有 `<img>` 補 width／height；首屏全景圖 `fetchpriority="high"`，其餘 `loading="lazy" decoding="async"`。
- 大圖轉 WebP（保留 jpg 作 `<picture>` fallback），提供 2–3 種寬度的 srcset／sizes。
- 檢查 alt 文字準確且不冗長。

---

## 附錄 A：YouTube 卡頓診斷（只診斷，不修改任何檔案）

問題：作品頁嵌入的 YouTube「不公開」影片，以前順暢，現在網頁版卡頓。
在診斷完成並經我確認前，**不得更動任何影片嵌入方式**。

症狀補充：［瀏覽器／裝置：＿＿＿］［卡頓現象：＿＿＿］［直接在 youtube.com 開會／不會卡］［範圍：所有影片／特定幾支］

請檢查並回報：
1. iframe 完整 src 與屬性（allow、loading、referrerpolicy、autoplay、enablejsapi 等），
   網址是 youtube.com/embed 還是 youtube-nocookie.com/embed。
2. 用 git log／git diff 找出最近與影片嵌入、JS、CSS、圖片、字型、`<head>` 相關的修改，指出哪一次最可能造成變慢。
3. 每頁同時載入幾個 iframe？是否一進頁就全載入？是否有大圖、背景影片、外部字型或第三方 script 搶資源？
4. 影片區塊及祖先是否有 backdrop-filter、filter、大範圍 box-shadow、transform／animation、
   sticky／fixed 搭配模糊、will-change、scroll-behavior 等造成 iframe 反覆重繪。
5. 是否有 scroll／resize 監聽、持續執行的動畫或 observer。
6. 用瀏覽器開發者工具 Performance／Network 實測：iframe 載入時間、主執行緒占用、重複或失敗請求。

回報格式：最可能的 1–3 個原因（依可能性排序，附檔名、行號、數據）＋各自的最小改動修法。不確定處請明說，不要猜。

---

## 附錄 B：最終 QA 清單

- 手機（360／375／390／430）、平板（768）、桌機（1024／1280／1440／1920）截圖，無橫向捲軸、無重疊、無被遮蓋
- 每一頁：頁碼（x／5）、目前導覽項目、下一頁入口 3 秒內可辨識
- 鍵盤完整操作；焦點外框在淺色與深色區塊都清楚
- 全站所有連結無 404；所有圖片有 alt；每頁只有一個 h1、標題階層不跳級
- Lighthouse（手機）：Performance、Accessibility、Best Practices、SEO 分數與主要扣分項
- 字體總載入量與 CLS 數據
## 2026-10-08 使用者確認

採選項 1：保留已確認的引言卡片視覺與作品段落順序，其餘按本規格分階段執行。後續新規格與已確認樣式衝突時，一律先停下來詢問，不自行決定。影片 ID、播放入口、嵌入方式保持不變；11 部影片已由 A 回報驗收通過。現有 walks.css 有其他工作的未提交變更，保留不覆寫。每階段 commit，正式發布另待使用者指示。


### 2026-10-09 現場走讀文字與照片對齊

依使用者確認，現場走讀的主標、小標與內文容器和照片拼貼同寬（最大 1000px），左右邊界對齊；此頁內文取消 38em 寬度限制，字級維持既有設定，手機保留安全邊距。


### 2026-10-09 全站文字與媒體對齊

依使用者指定走讀畫面為基準，各主要內容容器最大寬度統一為 1000px；內文不再另限 38em，與同區塊圖片或卡片內容邊界對齊。正文手機保留既有字級（約 17–18px）、桌面 20px，標題沿用既有分級字級變數。引言與心得卡保留內距，課程手記照片對齊文字卡內側。人物姓名、文章、段落順序與影片嵌入不變。
