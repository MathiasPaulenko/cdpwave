# JavaScript Evaluation

The Runtime domain lets you execute JavaScript in the page context,
inspect remote objects, and manage execution contexts. This is the
primary way to interact with page content beyond DOM manipulation.

## Prerequisites

Enable the Runtime domain to receive events (console messages,
exceptions, execution context creation):

```python
await session.runtime.enable()
```

You can call `evaluate` without enabling, but you won't receive
`Runtime.consoleAPICalled` or `Runtime.exceptionThrown` events.

## Evaluate an expression

```python
result = await session.runtime.evaluate("document.title")
```

The result dict contains a `result` key with a **remote object**:

```python
{
    "result": {
        "type": "string",
        "value": "Example Domain",
    }
}
```

### Remote objects

Every `evaluate` call returns a remote object descriptor. The `type`
field indicates the JavaScript type:

| `type` | Meaning | Has `value`? |
|---|---|---|
| `"string"` | JS string | Yes |
| `"number"` | JS number | Yes |
| `"boolean"` | JS boolean | Yes |
| `"object"` | JS object | Only with `return_by_value` |
| `"function"` | JS function | No (has `objectId`) |
| `"undefined"` | `undefined` | No |
| `"symbol"` | JS symbol | No (has `description`) |

For objects and functions without `return_by_value`, you get an
`objectId` — a string handle you can pass to other Runtime methods
like `get_properties`, `call_function_on`, or `release_object`.

### Return by value

To get the actual JavaScript value serialized as JSON in the response,
use `return_by_value=True`:

```python
result = await session.runtime.evaluate("1 + 1", return_by_value=True)
print(result["result"]["value"])  # 2
```

Without `return_by_value`, non-primitive values (objects, arrays) are
returned as remote object references with an `objectId` instead of a
serialized `value`. This is more efficient for large objects because
the data stays in the browser's heap.

### Await a promise

When evaluating an expression that returns a Promise, use
`await_promise=True` to wait for it to resolve:

```python
result = await session.runtime.evaluate(
    "fetch('https://api.github.com').then(r => r.status)",
    await_promise=True,
    return_by_value=True,
)
print(result["result"]["value"])  # 200
```

Without `await_promise`, you get a remote object reference to the
pending Promise. You can later await it with `runtime.await_promise`.

### User gesture flag

Some browser APIs require a user gesture (click, key press) to
function — for example, `requestFullscreen()` or opening popups. Pass
`user_gesture=True` to simulate a user gesture:

```python
await session.runtime.evaluate(
    "document.documentElement.requestFullscreen()",
    user_gesture=True,
    await_promise=True,
)
```

## Call function on

`call_function_on` executes a JavaScript function on a specific remote
object or in the global context. It's more flexible than `evaluate`
because you can pass arguments and target specific objects.

### Call with arguments

```python
result = await session.runtime.call_function_on(
    "function(a, b) { return a + b; }",
    arguments=[{"value": 2}, {"value": 3}],
    return_by_value=True,
)
print(result["result"]["value"])  # 5
```

Arguments are remote object descriptors. Use `{"value": ...}` for
primitives. To pass an existing remote object, use
`{"objectId": "..."}`.

### Call on a remote object

Pass an `object_id` to call the function as a method on that object.
Inside the function, `this` refers to the object:

```python
# Get a reference to the document body
body = await session.runtime.evaluate("document.body")
body_id = body["result"]["objectId"]

# Call a function on it
result = await session.runtime.call_function_on(
    "function() { return this.innerHTML; }",
    object_id=body_id,
    return_by_value=True,
)
print(result["result"]["value"])
```

## Remote object inspection

### Get properties

Inspect the properties of a remote object:

```python
obj = await session.runtime.evaluate("({name: 'test', count: 42})")
obj_id = obj["result"]["objectId"]

props = await session.runtime.get_properties(obj_id)
for prop in props["result"]:
    print(f"  {prop['name']}: {prop.get('value', {}).get('value', '?')}")
```

Set `own_properties=False` to include inherited properties from the
prototype chain.

### Query objects by constructor

Find all objects in the heap that were created by a specific
constructor:

```python
# Get a constructor reference
ctor = await session.runtime.evaluate("HTMLDivElement")
ctor_id = ctor["result"]["objectId"]

# Query all instances
result = await session.runtime.query_objects(ctor_id)
print(result["objects"])  # list of objectIds
```

### Release objects

Remote objects persist in the browser's heap until released. Always
clean up to avoid memory leaks:

```python
# Release a single object
await session.runtime.release_object(obj_id)

# Release all objects in a group
await session.runtime.release_object_group("my-group")
```

!!! tip "Object groups"
    Pass `object_group="my-group"` to `evaluate` or `call_function_on`
    to tag all created objects. Then release them all at once with
    `release_object_group("my-group")`.

## Compile and run scripts

For scripts you execute repeatedly, compile once and run many times:

### Compile

```python
compiled = await session.runtime.compile_script(
    source="return 1 + 2;",
    execution_context_id=None,  # use default context
)
script_id = compiled["scriptId"]
```

### Run

```python
result = await session.runtime.run_script(
    script_id=script_id,
    return_by_value=True,
)
print(result["result"]["value"])  # 3
```

This is faster than `evaluate` for hot paths because the browser
caches the compiled script. The script persists until the execution
context is destroyed (page navigation).

## JavaScript bindings

Add a binding so JavaScript code can call back into your Python code:

```python
await session.runtime.add_binding("pyLog")

async def on_binding(params: dict) -> None:
    print(f"JS called pyLog: {params['payload']}")

session.on("Runtime.bindingCalled", on_binding)

await session.runtime.evaluate("pyLog('hello from JS')")
```

**How it works**:

1. `add_binding("pyLog")` creates a global function `window.pyLog` in
   every execution context.
2. When JavaScript calls `pyLog(value)`, the browser sends a
   `Runtime.bindingCalled` event with the `payload`.
3. Your async handler receives the payload as a string. For non-string
   values, `JSON.stringify` them in JS.

Remove a binding when no longer needed:

```python
await session.runtime.remove_binding("pyLog")
```

## Execution contexts

Each frame and worker has its own execution context — an isolated
JavaScript world with its own global object. The top-level frame has
one context; each iframe has another.

### List contexts

```python
names = await session.runtime.global_lexical_scope_names()
print(names)  # ["myVar", "myFunc", ...]
```

### Create an isolated world

Create a separate execution context within a frame. Scripts in an
isolated world don't see the page's JavaScript globals:

```python
result = await session.page.create_isolated_world(
    frame_id="main-frame-id",
    world_name="my-isolated-world",
)
context_id = result["executionContextId"]
```

Pass `context_id` to `evaluate` or `call_function_on` to execute code
in that context. This is useful for running test scripts without
interfering with page code.

## Heap and performance

### Get heap usage

```python
usage = await session.runtime.get_heap_usage()
print(f"Used: {usage['usedSize']} bytes")
print(f"Total: {usage['totalSize']} bytes")
```

### Set async call stack depth

Control how many async frames are captured in stack traces:

```python
await session.runtime.set_async_call_stack_depth(32)
```

Higher values give more context for debugging async code but use more
memory. Default is 0 (no async stacks).

### Terminate execution

Immediately stop JavaScript execution on the page:

```python
await session.runtime.terminate_execution()
```

This is equivalent to DevTools' "Stop" button. Use with caution — it
aborts any running script, including Promise callbacks.

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

`evaluate` runs a single expression. To execute multiple statements,
wrap them in an IIFE or use `JSON.stringify` to return structured data:

```python
result = await session.runtime.evaluate(
    """
    (() => {
        const title = document.title;
        const links = document.querySelectorAll('a').length;
        return JSON.stringify({title, links});
    })()
    """,
    return_by_value=True,
)
import json
data = json.loads(result["result"]["value"])
```

### Read a DOM property

```python
result = await session.runtime.evaluate(
    "document.querySelector('h1').textContent",
    return_by_value=True,
)
heading = result["result"]["value"]
```

### Check if an element exists

```python
result = await session.runtime.evaluate(
    "!!document.querySelector('.my-class')",
    return_by_value=True,
)
exists = result["result"]["value"]  # True or False
```

### Intercept console.log

```python
async def on_console(params: dict) -> None:
    msg_type = params["type"]  # "log", "warn", "error", etc.
    args = [a.get("value", a.get("description", "?")) for a in params["args"]]
    print(f"[console.{msg_type}] {' '.join(str(v) for v in args)}")

session.on("Runtime.consoleAPICalled", on_console)
await session.runtime.evaluate("console.log('hello', 'world')")
```

### Catch JavaScript exceptions

```python
async def on_exception(params: dict) -> None:
    details = params["exceptionDetails"]
    print(f"JS error: {details['text']}")
    if "exception" in details:
        print(f"  {details['exception'].get('description', '')}")

session.on("Runtime.exceptionThrown", on_exception)
await session.runtime.evaluate("undefinedVar.foo")
```

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.runtime.enable()

        # Capture console output
        async def on_console(params: dict) -> None:
            args = [a.get("value", "?") for a in params["args"]]
            print(f"[console.{params['type']}] {' '.join(str(v) for v in args)}")

        session.on("Runtime.consoleAPICalled", on_console)

        # Evaluate
        result = await session.runtime.evaluate(
            "document.title", return_by_value=True
        )
        print(f"Title: {result['result']['value']}")

        # Call function with arguments
        result = await session.runtime.call_function_on(
            "function(a, b) { return a + b; }",
            arguments=[{"value": 10}, {"value": 20}],
            return_by_value=True,
        )
        print(f"10 + 20 = {result['result']['value']}")

        # Await a promise
        result = await session.runtime.evaluate(
            "Promise.resolve('async value')",
            await_promise=True,
            return_by_value=True,
        )
        print(f"Promise: {result['result']['value']}")

        await session.close()

asyncio.run(main())
```
