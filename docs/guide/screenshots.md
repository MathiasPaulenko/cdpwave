# Screenshots & PDF

The Page domain provides methods for capturing visual output: PNG/JPEG
screenshots, PDF generation, and MHTML snapshots. This guide covers all
capture modes and their trade-offs.

## Screenshots

### PNG screenshot

```python
import base64

result = await session.page.capture_screenshot(format="png")
with open("screenshot.png", "wb") as f:
    f.write(base64.b64decode(result["data"]))
```

The response contains a `data` field with a base64-encoded image. PNG
is lossless and supports transparency, but produces larger files.

### JPEG screenshot

```python
result = await session.page.capture_screenshot(format="jpeg", quality=90)
with open("screenshot.jpg", "wb") as f:
    f.write(base64.b64decode(result["data"]))
```

JPEG produces smaller files but doesn't support transparency. The
`quality` parameter (0-100) controls compression — 80 is a good
balance, 90+ is near-lossless.

### WebP screenshot

```python
result = await session.page.capture_screenshot(format="webp", quality=85)
```

WebP offers better compression than JPEG with similar quality. Not all
browsers support it for screenshots — Chrome does.

### Format comparison

| Format | Transparency | Lossless | Size | Use case |
|---|---|---|---|---|
| PNG | Yes | Yes | Large | Pixel-perfect captures |
| JPEG | No | No | Small | Photos, quick previews |
| WebP | Yes | Optional | Smallest | Web deployment |

## Capture regions

### Viewport only (default)

By default, the screenshot captures only the visible viewport — the
area you can see in the browser window:

```python
result = await session.page.capture_screenshot(format="png")
```

### Clip region

Capture a specific rectangular area of the page:

```python
clip = {
    "x": 0,
    "y": 0,
    "width": 100,
    "height": 100,
    "scale": 1,
}
result = await session.page.capture_screenshot(format="png", clip=clip)
```

The `clip` dict defines:

- **`x`**, **`y`** — top-left corner in CSS pixels.
- **`width`**, **`height`** — dimensions in CSS pixels.
- **`scale`** — device scale factor. Use `1` for 1:1, `2` for retina.

### Full page screenshot

Capture the entire scrollable page, not just the viewport:

```python
result = await session.page.capture_screenshot(
    format="png",
    capture_beyond_viewport=True,
)
```

Without `capture_beyond_viewport=True`, the screenshot is limited to
the viewport even if the page is taller. With it, the browser scrolls
internally to capture the full content.

!!! note "Memory usage"
    Full-page screenshots of very long pages can produce large images.
    For pages taller than 16384px, the browser may truncate the output.

### From surface

By default, screenshots are taken from the compositor surface. Set
`from_surface=False` to capture from the view instead:

```python
result = await session.page.capture_screenshot(
    format="png",
    from_surface=False,
)
```

This is rarely needed. `from_surface=True` (default) is faster and
captures the actual rendered content including GPU-accelerated layers.

## PDF generation

### Basic PDF

```python
import base64

result = await session.page.print_to_pdf(
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

### PDF parameters

| Parameter | Default | Description |
|---|---|---|
| `landscape` | `False` | Orientation |
| `display_header_footer` | `False` | Show header/footer |
| `print_background` | `False` | Include background colors/images |
| `scale` | `1.0` | Scale factor (0.1-2.0) |
| `paper_width` | `8.5` | Width in inches |
| `paper_height` | `11.0` | Height in inches |
| `margin_top` | `0.4` | Top margin in inches |
| `margin_bottom` | `0.4` | Bottom margin in inches |
| `margin_left` | `0.4` | Left margin in inches |
| `margin_right` | `0.4` | Right margin in inches |
| `page_ranges` | `None` | e.g. `"1-3,5,8-11"` |
| `prefer_css_page_size` | `False` | Use CSS @page size |
| `return_as_stream` | `False` | Return as stream handle |

### Landscape PDF

```python
result = await session.page.print_to_pdf(
    landscape=True,
    print_background=True,
)
```

### A4 format

```python
result = await session.page.print_to_pdf(
    paper_width=8.27,   # A4 width in inches
    paper_height=11.69, # A4 height in inches
    print_background=True,
)
```

### With header and footer

```python
result = await session.page.print_to_pdf(
    display_header_footer=True,
    header_template="<div class='header'>My Report</div>",
    footer_template="<div class='footer'>Page <span class='pageNumber'></span> of <span class='totalPages'></span></div>",
)
```

The header/footer templates support special CSS classes:

- **`.pageNumber`** — current page number.
- **`.totalPages`** — total page count.
- **`.date`** — formatted date.
- **`.title`** — document title.
- **`.url`** — page URL.

### PDF as stream

For large PDFs, return a stream handle instead of base64 to avoid
loading the entire file into memory:

```python
result = await session.page.print_to_pdf(return_as_stream=True)
stream_handle = result["stream"]

# Read the stream in chunks
data = await session.io.read(stream_handle, offset=0, size=65536)
# ... read more chunks until empty
await session.io.close(stream_handle)
```

!!! note "IO domain required"
    Stream reading uses the `session.io` domain. See the
    [IO API reference](../api/domains.md) for details.

## MHTML snapshots

Capture the entire page as a single MHTML file — a self-contained
archive with HTML, CSS, images, and other resources encoded inline:

```python
result = await session.page.capture_snapshot()
with open("page.mhtml", "w", encoding="utf-8") as f:
    f.write(result["data"])
```

MHTML is useful for:

- **Archiving** — save a complete page state for later analysis.
- **Sharing** — single file contains everything, no external dependencies.
- **Testing** — replay page state in other tools.

!!! note "MHTML vs PDF"
    MHTML preserves the interactive HTML/CSS/JS, while PDF is a static
    visual snapshot. Use MHTML for archiving, PDF for printing.

## Layout metrics

Get page dimensions before capturing to calculate clip regions:

```python
metrics = await session.page.get_layout_metrics()
layout = metrics["cssLayoutViewport"]
content = metrics["cssContentSize"]

print(f"Viewport: {layout['width']}x{layout['height']}")
print(f"Content:  {content['width']}x{content['height']}")
```

The response contains:

- **`cssLayoutViewport`** — the CSS viewport dimensions (what the user
  sees).
- **`cssContentSize`** — the full page content dimensions (including
  scrolled-out areas).
- **`cssVisualViewport`** — the visual viewport (may differ with pinch
  zoom).

## Full example

```python
import asyncio
import base64
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.page.enable()

        # Wait for load
        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        session.on("Page.loadEventFired", on_load)
        await session.page.navigate("https://example.com")
        await asyncio.wait_for(loaded.wait(), timeout=10.0)

        # Get layout metrics
        metrics = await session.page.get_layout_metrics()
        content = metrics["cssContentSize"]
        print(f"Page size: {content['width']}x{content['height']}")

        # Viewport screenshot
        shot = await session.page.capture_screenshot(format="png")
        with open("viewport.png", "wb") as f:
            f.write(base64.b64decode(shot["data"]))

        # Full page screenshot
        shot = await session.page.capture_screenshot(
            format="png",
            capture_beyond_viewport=True,
        )
        with open("fullpage.png", "wb") as f:
            f.write(base64.b64decode(shot["data"]))

        # PDF
        pdf = await session.page.print_to_pdf(print_background=True)
        with open("output.pdf", "wb") as f:
            f.write(base64.b64decode(pdf["data"]))

        # MHTML snapshot
        mhtml = await session.page.capture_snapshot()
        with open("page.mhtml", "w", encoding="utf-8") as f:
            f.write(mhtml["data"])

        await session.close()

asyncio.run(main())
```
