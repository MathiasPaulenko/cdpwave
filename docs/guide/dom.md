# DOM

## Enable DOM

```python
await page.dom.enable()
```

## Get document

```python
doc = await page.dom.get_document(depth=2)
root_id = doc["root"]["nodeId"]
```

## Query selector

Find the first element matching a selector:

```python
result = await page.dom.query_selector(root_id, "h1")
node_id = result["nodeId"]
```

## Query selector all

Find all matching elements:

```python
result = await page.dom.query_selector_all(root_id, "p")
for node_id in result.get("nodeIds", []):
    html = await page.dom.get_outer_html(node_id)
    print(html["outerHTML"])
```

## Get outer HTML

```python
html = await page.dom.get_outer_html(node_id)
print(html["outerHTML"])
```

## Get inner HTML

```python
html = await page.dom.get_inner_html(node_id)
print(html["innerHTML"])
```

## Remove a node

```python
await page.dom.remove_node(node_id)
```

## Set attribute

```python
await page.dom.set_attribute_value(node_id, "class", "highlight")
```

## Get attribute

```python
result = await page.dom.get_attribute(node_id, "href")
print(result["value"])
```

## Focus an element

```python
await page.dom.focus(node_id)
```

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        page = await client.new_page("https://example.com")
        await page.page.enable()
        await page.dom.enable()

        doc = await page.dom.get_document(depth=2)
        root_id = doc["root"]["nodeId"]

        h1 = await page.dom.query_selector(root_id, "h1")
        html = await page.dom.get_outer_html(h1["nodeId"])
        print(html["outerHTML"])  # <h1>Example Domain</h1>

        await page.close()

asyncio.run(main())
```
