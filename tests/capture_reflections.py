"""
使用 Chrome DevTools Protocol (CDP) 驗證創作心得卡片，測量高度差並擷取視埠截圖。
"""
import asyncio
import base64
import json
import subprocess
import time
import urllib.request
from pathlib import Path
import websockets

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = Path(r"C:\Users\abby8\.gemini\antigravity\brain\4c40653b-eca3-4fc4-a7aa-3681aafbee8b")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9222


async def send_cmd(ws, method, params=None, msg_id=1):
    req = {"id": msg_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(req))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get("id") == msg_id:
            return resp.get("result", {})


async def test_page(page_name, width, height, results):
    url = f"http://127.0.0.1:8081/{page_name}.html"
    
    # 建立新分頁
    create_url = f"http://127.0.0.1:{PORT}/json/new"
    req = urllib.request.Request(create_url, method="PUT")
    with urllib.request.urlopen(req) as r:
        tab_info = json.loads(r.read())
    
    ws_url = tab_info["webSocketDebuggerUrl"]
    
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        msg_id = 1
        await send_cmd(ws, "Page.enable", {}, msg_id); msg_id += 1
        await send_cmd(ws, "DOM.enable", {}, msg_id); msg_id += 1
        
        # 設定視埠
        await send_cmd(ws, "Emulation.setDeviceMetricsOverride", {
            "width": width,
            "height": height,
            "deviceScaleFactor": 1,
            "mobile": width <= 768
        }, msg_id); msg_id += 1
        
        # 導覽到目標頁面
        await send_cmd(ws, "Page.navigate", {"url": url}, msg_id); msg_id += 1
        
        # 等候頁面載入
        await asyncio.sleep(1.5)
        
        # 1. 測量收合狀態的高度與卡片屬性
        eval_collapsed = await send_cmd(ws, "Runtime.evaluate", {
            "expression": """
            (() => {
                const card = document.querySelector('details.reflection-card');
                const cardRect = card ? card.getBoundingClientRect() : null;
                const scrollHeight = document.documentElement.scrollHeight;
                const isOpen = card ? card.open : false;
                return {
                    scrollHeight,
                    isOpen,
                    cardWidth: cardRect ? cardRect.width : 0,
                    cardHeight: cardRect ? cardRect.height : 0
                };
            })()
            """,
            "returnByValue": True
        }, msg_id); msg_id += 1
        
        collapsed_data = eval_collapsed.get("result", {}).get("value", {})
        
        # 截圖：收合狀態
        # 捲動到卡片位置
        await send_cmd(ws, "Runtime.evaluate", {
            "expression": "document.querySelector('details.reflection-card').scrollIntoView({block: 'center', behavior: 'instant'});"
        }, msg_id); msg_id += 1
        await asyncio.sleep(0.3)
        
        shot_collapsed = await send_cmd(ws, "Page.captureScreenshot", {"format": "png"}, msg_id); msg_id += 1
        collapsed_img_path = ARTIFACT_DIR / f"{page_name}-collapsed-{width}.png"
        collapsed_img_path.write_bytes(base64.b64decode(shot_collapsed["data"]))
        
        # 2. 展開卡片
        await send_cmd(ws, "Runtime.evaluate", {
            "expression": """
            (() => {
                const card = document.querySelector('details.reflection-card');
                if (card) {
                    card.open = true;
                }
            })()
            """
        }, msg_id); msg_id += 1
        await asyncio.sleep(0.4)
        
        eval_expanded = await send_cmd(ws, "Runtime.evaluate", {
            "expression": """
            (() => {
                const card = document.querySelector('details.reflection-card');
                const cardRect = card ? card.getBoundingClientRect() : null;
                const scrollHeight = document.documentElement.scrollHeight;
                const isOpen = card ? card.open : false;
                return {
                    scrollHeight,
                    isOpen,
                    cardWidth: cardRect ? cardRect.width : 0,
                    cardHeight: cardRect ? cardRect.height : 0
                };
            })()
            """,
            "returnByValue": True
        }, msg_id); msg_id += 1
        
        expanded_data = eval_expanded.get("result", {}).get("value", {})
        
        # 截圖：展開狀態
        shot_expanded = await send_cmd(ws, "Page.captureScreenshot", {"format": "png"}, msg_id); msg_id += 1
        expanded_img_path = ARTIFACT_DIR / f"{page_name}-expanded-{width}.png"
        expanded_img_path.write_bytes(base64.b64decode(shot_expanded["data"]))
        
        # 3. 測試文末收合按鈕
        close_test = await send_cmd(ws, "Runtime.evaluate", {
            "expression": """
            (() => {
                const closeBtn = document.querySelector('.reflection-close-btn');
                if (closeBtn) {
                    closeBtn.click();
                    return { clicked: true, isOpen: document.querySelector('details.reflection-card').open };
                }
                return { clicked: false, isOpen: null };
            })()
            """,
            "returnByValue": True
        }, msg_id); msg_id += 1
        
        close_val = close_test.get("result", {}).get("value", {})
        
        results.append({
            "page": page_name,
            "width": width,
            "collapsed_page_height": collapsed_data.get("scrollHeight", 0),
            "expanded_page_height": expanded_data.get("scrollHeight", 0),
            "height_difference": expanded_data.get("scrollHeight", 0) - collapsed_data.get("scrollHeight", 0),
            "card_collapsed_height": round(collapsed_data.get("cardHeight", 0), 1),
            "card_expanded_height": round(expanded_data.get("cardHeight", 0), 1),
            "card_width": round(collapsed_data.get("cardWidth", 0), 1),
            "close_btn_works": close_val.get("isOpen") is False,
            "screenshots": [collapsed_img_path.name, expanded_img_path.name]
        })

    # 關閉分頁
    close_url = f"http://127.0.0.1:{PORT}/json/close/{tab_info['id']}"
    with urllib.request.urlopen(close_url) as r:
        pass


async def main():
    chrome_proc = subprocess.Popen([
        CHROME,
        "--headless=new",
        f"--remote-debugging-port={PORT}",
        "--disable-gpu",
        "--hide-scrollbars",
        "about:blank"
    ])
    time.sleep(1.5)
    
    results = []
    try:
        for page in ["abby", "yuan"]:
            for width in [375, 1440]:
                height = 812 if width == 375 else 900
                await test_page(page, width, height, results)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    finally:
        chrome_proc.terminate()


if __name__ == "__main__":
    asyncio.run(main())
