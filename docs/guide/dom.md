# DOM

The DOM domain provides direct access to the browser's document object
model. You can inspect elements, query selectors, read and modify
attributes, manipulate the tree structure, and measure element geometry.

This is lower-level than `Runtime.evaluate("document.querySelector(...)")`
— it uses the browser's internal DOM inspector, which is faster and
doesn't execute JavaScript.

## Prerequisites

Enable the DOM domain:

```python
await session.dom.enable()
```

`DOM.enable` activates document update events. You only need to call it
once per session.

## The document tree

The DOM is a tree of nodes. Each node has a numeric `nodeId` that
identifies it within the current document. The root of the tree is the
`#document` node.

### Get the full document

```python
doc = await session.dom.get_document(depth=-1, pierce=False)
root_id = doc["root"]["nodeId"]
```

Parameters:

- **`depth`** — maximum tree depth to return. `-1` means the entire
  tree. Use `1` for just the root, `2` for root + children, etc.
- **`pierce`** — whether to pierce shadow DOM boundaries. Set to
  `True` to include shadow DOM content in the tree.

The root node contains:

- **`nodeId`** — the ID you pass to other DOM methods.
- **`nodeName`** — e.g. `"#document"`, `"HTML"`, `"BODY"`.
- **`nodeType`** — integer (1=element, 3=text, 8=comment, 9=document).
- **`children`** — list of child nodes (if depth allows).

### Get a child node

Retrieve a specific node's children:

```python
result = await session.dom.get_child_nodes(node_id)
for child in result["nodes"]:
    print(f"  {child['nodeName']}: {child.get('attributes', [])}")
```

## Querying elements

### Query selector

Find the first element matching a CSS selector:

```python
result = await session.dom.query_selector(root_id, "h1")
node_id = result["nodeId"]
```

Returns `{"nodeId": 0}` if no element matches.

### Query selector all

Find all matching elements:

```python
result = await session.dom.query_selector_all(root_id, "p")
for node_id in result.get("nodeIds", []):
    html = await session.dom.get_outer_html(node_id)
    print(html["outerHTML"])
```

### Search in DOM

Search for nodes by query string (supports XPath, CSS selectors, and
plain text):

```python
search = await session.dom.perform_search("h1")
search_id = search["searchId"]
count = search["resultCount"]

results = await session.dom.get_search_results(search_id, 0, count)
for node_id in results["nodeIds"]:
    html = await session.dom.get_outer_html(node_id)
    print(html["outerHTML"])

await session.dom.discard_search_results(search_id)
```

## Reading content

### Get outer HTML

```python
html = await session.dom.get_outer_html(node_id)
print(html["outerHTML"])
```

### Get inner HTML

```python
html = await session.dom.get_inner_html(node_id)
print(html["innerHTML"])
```

### Get attribute

```python
result = await session.dom.get_attribute(node_id, "href")
print(result["value"])
```

### Get all attributes

```python
result = await session.dom.get_attributes(node_id)
# result["attributes"] is a flat list: ["name1", "value1", "name2", "value2", ...]
attrs = dict(zip(result["attributes"][::2], result["attributes"][1::2]))
print(attrs)
```

## Modifying content

### Set attribute

```python
await session.dom.set_attribute_value(node_id, "class", "highlight")
```

### Remove attribute

```python
await session.dom.remove_attribute(node_id, "class")
```

### Set outer HTML

Replace an element entirely:

```python
await session.dom.set_outer_html(node_id, "<h2>Replaced</h2>")
```

### Set inner HTML

Replace an element's children:

```python
await session.dom.set_inner_html(node_id, "<p>New content</p>")
```

### Remove a node

```python
await session.dom.remove_node(node_id)
```

### Request a node

Request the browser to send the node's children (useful for lazy-loaded
content):

```python
result = await session.dom.request_node(node_id)
print(result["nodes"])
```

## Element interaction

### Focus an element

```python
await session.dom.focus(node_id)
```

This is equivalent to calling `element.focus()` in JavaScript. Useful
before dispatching keyboard events via `session.input`.

### Set file input files

Set files on an `<input type="file">` element:

```python
await session.dom.set_file_input_files(
    node_id,
    files=["/path/to/file1.pdf", "/path/to/file2.pdf"],
)
```

!!! note "File chooser interception"
    Alternatively, use `session.page.set_intercept_file_chooser_dialog(True)`
    and listen for `Page.fileChooserOpened` events to intercept file
    dialogs programmatically.

## Box model

Get the element's geometry — useful for clicking at specific coordinates
or verifying layout:

```python
result = await session.dom.get_box_model(node_id)
model = result["model"]
print(f"Content: {model['content']}")
print(f"Padding: {model['padding']}")
print(f"Border:  {model['border']}")
print(f"Margin:  {model['margin']}")
```

The box model contains:

- **`content`** — quad of the content box (x1, y1, x2, y2, x3, y3, x4, y4).
- **`padding`** — quad including padding.
- **`border`** — quad including border.
- **`margin`** — quad including margin.
- **`width`** — content width in pixels.
- **`height`** — content height in pixels.

Each quad is a list of 8 numbers representing 4 (x, y) points,
clockwise from top-left.

### Get content quads

A simpler version that returns just the content quads:

```python
result = await session.dom.get_content_quads(node_id)
print(result["quads"])
```

### Get node coordinates

```python
result = await session.dom.get_node_for_location(
    x=100,
    y=200,
    include_user_agent_shadow_dom=False,
)
print(result["nodeId"])
```

Find which DOM node is at a given pixel coordinate. Useful for
simulating clicks on specific elements.

## Node resolution

### Resolve to a remote object

Get a Runtime remote object reference for a DOM node. This lets you
call JavaScript methods on the element:

```python
result = await session.dom.resolve_node(node_id)
object_id = result["object"]["objectId"]

# Now call JS on it
js_result = await session.runtime.call_function_on(
    "function() { return this.getBoundingClientRect().width; }",
    object_id=object_id,
    return_by_value=True,
)
print(f"Width: {js_result['result']['value']}px")
```

### Describe a node

Get a detailed description of a node:

```python
result = await session.dom.describe_node(node_id, depth=2)
print(result["node"])
```

### Copy to clipboard

Copy an element's HTML to the system clipboard:

```python
await session.dom.copy_to(node_id)
```

## Shadow DOM

Shadow DOM encapsulates a component's internal structure. By default,
`get_document` and `query_selector` don't pierce shadow boundaries.

### Pierce shadow DOM

```python
doc = await session.dom.get_document(depth=-1, pierce=True)
```

With `pierce=True`, shadow hosts include their shadow root children in
the tree. You can then query inside shadow DOM:

```python
# Find a shadow host
host = await session.dom.query_selector(root_id, "my-component")
# Get its shadow root
children = await session.dom.get_child_nodes(host["nodeId"])
shadow_root = children["nodes"][0]  # shadow root is first child
# Query inside shadow DOM
inner = await session.dom.query_selector(shadow_root["nodeId"], ".inner")
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

        # Get the document
        doc = await session.dom.get_document(depth=2)
        root_id = doc["root"]["nodeId"]

        # Find the h1
        h1 = await session.dom.query_selector(root_id, "h1")
        if h1["nodeId"]:
            # Read its HTML
            html = await session.dom.get_outer_html(h1["nodeId"])
            print(f"h1 HTML: {html['outerHTML']}")

            # Get its box model
            box = await session.dom.get_box_model(h1["nodeId"])
            print(f"h1 size: {box['model']['width']}x{box['model']['height']}")

            # Resolve to a remote object and get computed style
            resolved = await session.dom.resolve_node(h1["nodeId"])
            obj_id = resolved["object"]["objectId"]
            style = await session.runtime.call_function_on(
                "function() { return getComputedStyle(this).color; }",
                object_id=obj_id,
                return_by_value=True,
            )
            print(f"h1 color: {style['result']['value']}")

        # Find all links
        links = await session.dom.query_selector_all(root_id, "a")
        for node_id in links.get("nodeIds", []):
            href = await session.dom.get_attribute(node_id, "href")
            print(f"  Link: {href['value']}")

        await session.close()

asyncio.run(main())
```
