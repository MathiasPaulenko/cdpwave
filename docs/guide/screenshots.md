# Screenshots & PDF

## PNG screenshot

```python
import base64

result = await page.page.capture_screenshot(format="png")
with open("screenshot.png", "wb") as f:
    f.write(base64.b64decode(result["data"]))
```

## JPEG screenshot

```python
result = await page.page.capture_screenshot(format="jpeg", quality=90)
with open("screenshot.jpg", "wb") as f:
    f.write(base64.b64decode(result["data"]))
```

## Clip region

Capture a specific area:

```python
clip = {
    "x": 0,
    "y": 0,
    "width": 100,
    "height": 100,
    "scale": 1,
}
result = await page.page.capture_screenshot(format="png", clip=clip)
```

## Full page screenshot

```python
result = await page.page.capture_screenshot(
    format="png",
    capture_beyond_viewport=True,
)
```

## PDF generation

```python
import base64

result = await page.page.print_to_pdf(
    print_background=True,
    paper_width=8.5,
    paper_height=11.0,
    margin_top=0.4,
    margin_bottom=0.4,
    margin_left=0.4,
    margin_right=0.4,
)
with open("output.pdf", "wb") as f:
    f.write(base64.b64decode(result["data"]))
```

## Landscape PDF

```python
result = await page.page.print_to_pdf(
    landscape=True,
    print_background=True,
)
```

## Full example

```python
import asyncio
import base64
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        page = await client.new_page("https://example.com")
        await page.page.enable()
        await page.page.navigate("https://example.com")

        # Wait for load
        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        page.on("Page.loadEventFired", on_load)
        await asyncio.wait_for(loaded.wait(), timeout=10.0)

        # Screenshot
        shot = await page.page.capture_screenshot(format="png")
        with open("screenshot.png", "wb") as f:
            f.write(base64.b64decode(shot["data"]))

        # PDF
        pdf = await page.page.print_to_pdf(print_background=True)
        with open("output.pdf", "wb") as f:
            f.write(base64.b64decode(pdf["data"]))

        await page.close()

asyncio.run(main())
```
