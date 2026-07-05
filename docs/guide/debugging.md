# Debugging

cdpwave provides full coverage of the `Debugger`, `DOMDebugger`, and
`EventBreakpoints` domains for setting breakpoints, stepping through
code, inspecting variables, and blackboxing scripts.

## How CDP debugging works

When you enable the `Debugger` domain, Chrome's V8 engine enters
debugging mode. This allows you to set breakpoints, pause execution,
inspect call frames, and step through code. The browser fires
`Debugger.paused` events when execution halts, providing the call
frame stack and scope chain for inspection.

!!! warning "Performance impact"
    Enabling the debugger has a performance cost. V8 disables
    certain optimizations when debugging is active. Enable it only
    when needed and disable when done.

## Debugger domain

### Enabling the debugger

```python
await session.debugger.enable()
```

After enabling, V8 will report script parsed events and allow
breakpoint management.

### Breakpoint types

| Type | Method | Use case |
|---|---|---|
| By URL | `set_breakpoint_by_url` | Break at a line in a specific script URL |
| By script ID | `set_breakpoint` | Break at a specific script ID + location |
| On function call | `set_breakpoint_on_function_call` | Break when a function is called |
| Conditional | Any method with `condition` param | Break only when condition is true |

### Set a breakpoint by URL

```python
result = await session.debugger.set_breakpoint_by_url(
    line_number=42,
    url="https://example.com/app.js",
    column_number=0,
    condition="x > 10",
)
breakpoint_id = result["breakpointId"]
```

The `condition` parameter accepts any JavaScript expression. The
breakpoint only fires when the expression evaluates to `true`.

### Set a breakpoint on a function call

```python
# First, get the function's object ID via Runtime.evaluate
func = await session.runtime.evaluate(
    "myFunction",
    return_by_value=False,
)
result = await session.debugger.set_breakpoint_on_function_call(
    object_id=func["result"]["objectId"],
    condition="args[0] > 100",
)
```

### Set a breakpoint by script ID

```python
result = await session.debugger.set_breakpoint(
    location={
        "scriptId": "scr123",
        "lineNumber": 10,
        "columnNumber": 0,
    },
    condition="i === 5",
)
```

### Remove a breakpoint

```python
await session.debugger.remove_breakpoint(breakpoint_id="bp1")
```

### Enable/disable all breakpoints

```python
# Disable all breakpoints (they remain set but inactive)
await session.debugger.set_breakpoints_active(False)

# Re-enable
await session.debugger.set_breakpoints_active(True)
```

### Get possible breakpoints

Find all valid breakpoint locations in a range:

```python
result = await session.debugger.get_possible_breakpoints(
    start={"scriptId": "scr1", "lineNumber": 0, "columnNumber": 0},
    end={"scriptId": "scr1", "lineNumber": 100, "columnNumber": 0},
)
for loc in result["locations"]:
    print(f"Possible BP at line {loc['lineNumber']}")
```

## Pausing and resuming

### Pause on next statement

```python
await session.debugger.pause()
```

The browser will pause at the next JavaScript statement. This fires
a `Debugger.paused` event.

### Resume execution

```python
await session.debugger.resume()
```

### Stepping commands

| Command | Effect |
|---|---|
| `step_over` | Execute current line, stop at next line in same scope |
| `step_into` | Step into function calls |
| `step_out` | Execute until current function returns |

```python
await session.debugger.step_over()
await session.debugger.step_into()
await session.debugger.step_out()
```

### Skip all pauses

Ignore all breakpoints and pause requests — useful for running to
completion without removing breakpoints:

```python
await session.debugger.set_skip_all_pauses(True)
```

## Handling paused events

When the debugger pauses, it sends a `Debugger.paused` event with
the call frame stack. Each call frame contains:

- **`callFrameId`** — unique ID for this frame (used for variable
  inspection).
- **`functionName`** — name of the function.
- **`location`** — `scriptId`, `lineNumber`, `columnNumber`.
- **`scopeChain`** — list of scopes (local, closure, global, etc.).
- **`this`** — the `this` value for this frame.

```python
async def on_paused(event: dict) -> None:
    call_frames = event["callFrames"]
    top_frame = call_frames[0]
    print(f"Paused at {top_frame['url']}:{top_frame['location']['lineNumber']}")

    # Inspect variables in the local scope
    for scope in top_frame["scopeChain"]:
        if scope["type"] == "local":
            props = await session.runtime.get_properties(
                object_id=scope["object"]["objectId"],
                own_properties=True,
            )
            for prop in props["result"]:
                print(f"  {prop['name']} = {prop.get('value', {}).get('value', '...')}")

    # Continue execution
    await session.debugger.resume()

session.on("Debugger.paused", on_paused)
```

### Scope types

| Type | Description |
|---|---|
| `local` | Variables in the current function scope |
| `closure` | Variables from enclosing functions |
| `global` | Global object properties |
| `catch` | Variables in a catch block |
| `block` | Block-scoped variables (let, const) |
| `script` | Script-level declarations |
| `with` | Variables from a `with` statement |
| `module` | Module scope |

## Searching in scripts

### Search for a string in a script

```python
result = await session.debugger.search_in_content(
    script_id="scr1",
    query="TODO",
    case_sensitive=False,
    is_regex=False,
)
for match in result["result"]:
    print(f"Match at line {match['lineNumber']}: {match['lineContent']}")
```

### Get script source

```python
source = await session.debugger.get_script_source(script_id="scr1")
print(source["scriptSource"])
```

## Blackboxing

Blackboxing tells the debugger to skip certain scripts when stepping.
This prevents stepping into library code or frameworks:

```python
await session.debugger.set_blackbox_patterns(
    patterns=["node_modules/.*", "vendor/.*"],
)
```

When stepping and a blackboxed script is encountered, the debugger
runs through it without pausing.

## Variable inspection

### Set a variable value

Modify a variable in a specific scope while paused:

```python
await session.debugger.set_variable_value(
    call_frame_id="cf1",
    scope_number=0,
    variable_name="myVar",
    new_value={"value": 42},
)
```

`scope_number` is the index into the call frame's `scopeChain` array.

### Set return value

Override the return value of a function. Only valid when paused at
a return statement:

```python
await session.debugger.set_return_value(
    new_value={"value": "custom result"},
)
```

## Pause on exceptions

Control when the debugger pauses on exceptions:

```python
# Pause on all exceptions (caught and uncaught)
await session.debugger.set_pause_on_exceptions(state="all")

# Pause only on uncaught exceptions
await session.debugger.set_pause_on_exceptions(state="uncaught")

# Don't pause on exceptions
await session.debugger.set_pause_on_exceptions(state="none")
```

## DOM breakpoints

The `DOMDebugger` domain sets breakpoints on DOM operations. These
fire when the DOM is modified, attributes change, or nodes are
removed.

### DOM breakpoint types

| Type | Fires when |
|---|---|
| `subtree-modified` | Any child of the node is added/removed/modified |
| `attribute-modified` | An attribute on the node is changed |
| `node-removed` | The node is removed from the DOM |

```python
await session.dom_debugger.set_dom_breakpoint(
    node_id=1,
    type="subtree-modified",
)
```

Remove:

```python
await session.dom_debugger.remove_dom_breakpoint(
    node_id=1,
    type="subtree-modified",
)
```

## Event listener breakpoints

Pause when specific DOM events are dispatched. Useful for debugging
event handler registration and execution:

```python
await session.dom_debugger.set_event_listener_breakpoint(
    event_name="click",
    target_name="HTMLInputElement",
)
```

`target_name` is optional — omit it to break on the event for any
target.

Remove:

```python
await session.dom_debugger.remove_event_listener_breakpoint(
    event_name="click",
    target_name="HTMLInputElement",
)
```

## XHR breakpoints

Pause when a matching XHR/fetch is sent:

```python
await session.dom_debugger.set_xhr_breakpoint(url="*api.example.com*")
```

Remove:

```python
await session.dom_debugger.remove_xhr_breakpoint(url="*api.example.com*")
```

## Event breakpoints

The `EventBreakpoints` domain provides instrumentation breakpoints
for native DOM events. These are lower-level than `DOMDebugger` event
listener breakpoints:

```python
await session.event_breakpoints.set_instrumentation_breakpoint(
    event_name="DOMContentLoaded",
)
```

Disable:

```python
await session.event_breakpoints.remove_instrumentation_breakpoint(
    event_name="DOMContentLoaded",
)
```

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.enable()
        await session.debugger.enable()

        # Set a conditional breakpoint
        bp = await session.debugger.set_breakpoint_by_url(
            line_number=5,
            url="https://example.com/app.js",
            condition="counter > 10",
        )
        print(f"Breakpoint: {bp['breakpointId']}")

        # Handle pause events
        async def on_paused(event: dict) -> None:
            top = event["callFrames"][0]
            print(f"Paused at {top['functionName']}:{top['location']['lineNumber']}")

            # Inspect local variables
            for scope in top["scopeChain"]:
                if scope["type"] == "local":
                    props = await session.runtime.get_properties(
                        object_id=scope["object"]["objectId"],
                        own_properties=True,
                    )
                    for prop in props["result"]:
                        val = prop.get("value", {}).get("value", "...")
                        print(f"  {prop['name']} = {val}")

            await session.debugger.resume()

        session.on("Debugger.paused", on_paused)

        # Navigate to trigger the script
        await session.page.navigate("https://example.com")
        await asyncio.sleep(5)

        # Clean up
        await session.debugger.disable()
        await session.close()

asyncio.run(main())
```
