# DOM

## Enable DOM

```python
await session.dom.enable()
```

## Get document

```python
doc = await session.dom.get_document(depth=2)
root_id = doc["root"]["nodeId"]
```

## Query selector

Find the first element matching a selector:

```python
result = await session.dom.query_selector(root_id, "h1")
node_id = result["nodeId"]
```

## Query selector all

Find all matching elements:

```python
result = await session.dom.query_selector_all(root_id, "p")
for node_id in result.get("nodeIds", []):
    html = await session.dom.get_outer_html(node_id)
    print(html["outerHTML"])
```

## Get outer HTML

```python
html = await session.dom.get_outer_html(node_id)
print(html["outerHTML"])
```

## Get inner HTML

```python
html = await session.dom.get_inner_html(node_id)
print(html["innerHTML"])
```

## Remove a node

```python
await session.dom.remove_node(node_id)
```

## Set attribute

```python
await session.dom.set_attribute_value(node_id, "class", "highlight")
```

## Get attribute

```python
result = await session.dom.get_attribute(node_id, "href")
print(result["value"])
```

## Focus an element

```python
await session.dom.focus(node_id)
```

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.page.enable()
        await session.dom.enable()

        doc = await session.dom.get_document(depth=2)
        root_id = doc["root"]["nodeId"]

        h1 = await session.dom.query_selector(root_id, "h1")
        html = await session.dom.get_outer_html(h1["nodeId"])
        print(html["outerHTML"])  # <h1>Example Domain</h1>

        await session.close()

asyncio.run(main())
```
