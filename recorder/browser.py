import asyncio
import time
import json
from playwright.async_api import async_playwright, Page
from typing import Callable, Awaitable

class BrowserRecorder:
    def __init__(self, event_callback: Callable[[dict], Awaitable[None]]):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.event_callback = event_callback
        self.is_recording = False

    @property
    def is_open(self):
        return self.page and not self.page.is_closed()

    async def start(self):
        """Launches the browser and starts monitoring events."""
        self.playwright = await async_playwright().start()
        # Launch non-headless so user can interact
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context(
            record_video_dir=None, # We'll handle screenshots manually for better control/resolution
            viewport={'width': 1280, 'height': 720}
        )
        self.page = await self.context.new_page()
        
        # Inject scripts to monitor events
        await self._inject_monitoring_scripts()
        
        # Go to a blank page or default
        await self.page.goto('about:blank')
        self.is_recording = True
        print("Browser recorder started.")

    async def stop(self):
        """Stops the browser and cleanup."""
        self.is_recording = False
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser recorder stopped.")

    async def _inject_monitoring_scripts(self):
        """Injects JS to detect clicks and inputs."""
        await self.context.expose_binding("on_action", self._handle_event)
        
        script = """
        document.addEventListener('click', (event) => {
            const target = event.target;
            const selector = target.id ? '#' + target.id : target.tagName;
            const text = target.innerText || target.value || '';
            window.on_action({
                type: 'click',
                selector: selector,
                text: text.substring(0, 50),
                timestamp: Date.now() / 1000
            });
        }, true);
        
        document.addEventListener('input', (event) => {
            const target = event.target;
            const selector = target.id ? '#' + target.id : target.tagName;
             window.on_action({
                type: 'input',
                selector: selector,
                value: target.value,
                timestamp: Date.now() / 1000
            });
        }, true);
        """
        await self.context.add_init_script(script)
        
        # Monitor navigations via Playwright API
        self.page.on("framenavigated", self._handle_navigation)

    async def _handle_event(self, source, event_data):
        """Callback from JS."""
        if not self.is_recording:
            return
        
        # Capture screenshot for clicks
        screenshot_path = None
        if event_data['type'] == 'click':
             # Generate unique filename
            timestamp = int(time.time() * 1000)
            screenshot_path = f"screenshot_{timestamp}.png"
            # We capture the page state
            await self.page.screenshot(path=screenshot_path)
            event_data['screenshot'] = screenshot_path
            
        await self.event_callback(event_data)

    async def _handle_navigation(self, frame):
        """Callback for navigation events."""
        if not self.is_recording or not frame.page:
            return
            
        try:
            url = frame.url
            if url == "about:blank":
                return

            timestamp = int(time.time() * 1000)
            screenshot_path = f"screenshot_nav_{timestamp}.png"
            await self.page.screenshot(path=screenshot_path)

            event_data = {
                "type": "navigation",
                "url": url,
                "timestamp": time.time(),
                "screenshot": screenshot_path
            }
            await self.event_callback(event_data)
        except Exception as e:
            print(f"Error handling navigation: {e}")

# Example usage (for testing)
async def test_main():
    async def print_event(event):
        print(f"Event: {event}")

    recorder = BrowserRecorder(print_event)
    await recorder.start()
    
    # Keep alive for testing
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await recorder.stop()

if __name__ == "__main__":
    asyncio.run(test_main())
