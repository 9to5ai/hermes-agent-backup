import asyncio
import json
import re
import sys
from playwright.async_api import async_playwright

VIDEO_ID = "LF3aUIM57uw"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"

async def get_title(page):
    await page.goto(VIDEO_URL, wait_until="domcontentloaded")
    await asyncio.sleep(2)
    title = await page.title()
    return title

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Get video title first
        print("Getting video title...")
        await page.goto(VIDEO_URL, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        title = await page.title()
        print(f"TITLE: {title}")
        
        # Navigate to Gemini
        print("Opening Gemini...")
        await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Wait for and interact with the textarea
        print("Looking for input field...")
        
        # Try textarea first
        textarea = page.locator("textarea")
        if await textarea.count() > 0:
            print("Found textarea, typing prompt...")
            await textarea.click()
            await textarea.fill(f"Write the most detailed notes about this video: {VIDEO_URL}")
            await asyncio.sleep(1)
            # Press Enter to submit
            await textarea.press("Enter")
            print("Prompt submitted via Enter")
        else:
            # Try contenteditable div
            print("Looking for contenteditable div...")
            div = page.locator("div.ql-editor[contenteditable='true']")
            if await div.count() > 0:
                await div.click()
                await div.fill(f"Write the most detailed notes about this video: {VIDEO_URL}")
                await asyncio.sleep(1)
                # Try to find and click send button
                send_btn = page.locator("button[aria-label='Send message']").first
                if await send_btn.count() > 0:
                    await send_btn.click()
                    print("Prompt submitted via button click")
                else:
                    # Try pressing Enter
                    await div.press("Enter")
                    print("Prompt submitted via Enter")
            else:
                print("No input field found, taking snapshot...")
                await page.screenshot(path="/tmp/gemini_snapshot.png")
                print("Screenshot saved")
                await browser.close()
                sys.exit(1)
        
        # Wait for Gemini response
        print("Waiting for Gemini response (~25 seconds)...")
        await asyncio.sleep(25)
        
        # Check for stop button - wait until gone
        stop_btn = page.locator("button[aria-label='Stop']")
        for i in range(10):
            if await stop_btn.count() == 0:
                print("Response complete (no Stop button)")
                break
            print(f"Still generating... ({i+1})")
            await asyncio.sleep(3)
        
        # Extract response text using TreeWalker
        print("Extracting response...")
        response_text = await page.evaluate("""() => {
            var text = '';
            var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
            while(walker.nextNode()) {
                var t = walker.currentNode.textContent.trim();
                if(t.length > 5 && t.length < 1000) text += t + '\\n';
            }
            return text.substring(0, 15000);
        }""")
        
        print(f"RESPONSE_LENGTH: {len(response_text)}")
        print("---RESPONSE_START---")
        print(response_text)
        print("---RESPONSE_END---")
        
        # Save response to file
        with open("/tmp/gemini_response.txt", "w") as f:
            f.write(response_text)
        print("Response saved to /tmp/gemini_response.txt")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
