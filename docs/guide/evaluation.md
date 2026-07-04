# JavaScript Evaluation

## Evaluate an expression

```python
result = await session.runtime.evaluate("document.title")
```

The result dict contains a `result` key with the remote object:

```python
{
    "result": {
        "type": "string",
        "value": "Example Domain",
    }
}
```

## Return by value

To get the actual JavaScript value in the response, use `return_by_value=True`:

```python
result = await session.runtime.evaluate("1 + 1", return_by_value=True)
print(result["result"]["value"])  # 2
```

Without `return_by_value`, non-primitive values are returned as remote object references.

## Await a promise

```python
result = await session.runtime.evaluate(
    "fetch('https://api.github.com').then(r => r.status)",
    await_promise=True,
    return_by_value=True,
)
print(result["result"]["value"])  # 200
```

## Call function on

Execute a function with arguments:

```python
result = await session.runtime.call_function_on(
    "function(a, b) { return a + b; }",
    arguments=[{"value": 2}, {"value": 3}],
    return_by_value=True,
)
print(result["result"]["value"])  # 5
```

## Enable Runtime

Some events require `Runtime.enable` to be called first:

```python
await session.runtime.enable()
```

## Common patterns

### Get page title

```python
result = await session.runtime.evaluate(
    "document.title", return_by_value=True
)
title = result["result"]["value"]
```

### Get all links

```python
result = await session.runtime.evaluate(
    "Array.from(document.querySelectorAll('a')).map(a => a.href)",
    return_by_value=True,
)
links = result["result"]["value"]
```

### Execute multiple statements

```python
result = await session.runtime.evaluate(
    """
    const title = document.title;
    const links = document.querySelectorAll('a').length;
    JSON.stringify({title, links});
    """,
    return_by_value=True,
)
import json
data = json.loads(result["result"]["value"])
```
