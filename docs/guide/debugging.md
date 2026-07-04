# Debugging

cdpwave provides full coverage of the `Debugger`, `DOMDebugger`, and
`EventBreakpoints` domains for setting breakpoints, stepping through code,
inspecting variables, and blackboxing scripts.

## Enabling the debugger

```python
await session.debugger.enable()
```

## Breakpoints

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
# Disable all breakpoints
await session.debugger.set_breakpoints_active(False)

# Re-enable
await session.debugger.set_breakpoints_active(True)
```

### Get possible breakpoints

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

### Resume execution

```python
await session.debugger.resume()
```

### Step over

```python
await session.debugger.step_over()
```

### Step into

```python
await session.debugger.step_into()
```

### Step out

```python
await session.debugger.step_out()
```

### Skip all pauses

```python
await session.debugger.set_skip_all_pauses(True)
```

## Handling paused events

```python
async def on_paused(event: dict) -> None:
    call_frames = event["callFrames"]
    top_frame = call_frames[0]
    print(f"Paused at {top_frame['url']}:{top_frame['location']['lineNumber']}")

    # Inspect variables
    for scope in top_frame["scopeChain"]:
        if scope["type"] == "local":
            props = await session.runtime.get_properties(
                object_id=scope["object"]["objectId"],
                own_properties=True,
            )
            for prop in props["result"]:
                print(f"  {prop['name']} = {prop.get('value', {}).get('value', '...')}")

    # Continue
    await session.debugger.resume()

session.on("Debugger.paused", on_paused)
```

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

Skip stepping into matched scripts:

```python
await session.debugger.set_blackbox_patterns(
    patterns=["node_modules/.*", "vendor/.*"],
)
```

## Variable inspection

### Set a variable value

```python
await session.debugger.set_variable_value(
    call_frame_id="cf1",
    scope_number=0,
    variable_name="myVar",
    new_value={"value": 42},
)
```

### Set return value

Only valid when paused at a return statement:

```python
await session.debugger.set_return_value(
    new_value={"value": "custom result"},
)
```

## Pause on exceptions

```python
# Pause on all exceptions
await session.debugger.set_pause_on_exceptions(state="all")

# Pause only on uncaught exceptions
await session.debugger.set_pause_on_exceptions(state="uncaught")

# Don't pause on exceptions
await session.debugger.set_pause_on_exceptions(state="none")
```

---

## DOM breakpoints

The `DOMDebugger` domain allows setting breakpoints on DOM operations.

### Set a subtree breakpoint

```python
await session.dom_debugger.set_dom_breakpoint(
    node_id=1,
    type="subtree-modified",
)
```

### Set an attribute breakpoint

```python
await session.dom_debugger.set_dom_breakpoint(
    node_id=1,
    type="attribute-modified",
)
```

### Set a node removal breakpoint

```python
await session.dom_debugger.set_dom_breakpoint(
    node_id=1,
    type="node-removed",
)
```

### Remove a DOM breakpoint

```python
await session.dom_debugger.remove_dom_breakpoint(
    node_id=1,
    type="subtree-modified",
)
```

## Event listener breakpoints

Pause when specific events are dispatched:

```python
await session.dom_debugger.set_event_listener_breakpoint(
    event_name="click",
    target_name="HTMLInputElement",
)
```

Remove:

```python
await session.dom_debugger.remove_event_listener_breakpoint(
    event_name="click",
    target_name="HTMLInputElement",
)
```

## XHR breakpoints

Pause when a matching XHR is sent:

```python
await session.dom_debugger.set_xhr_breakpoint(url="*api.example.com*")
```

Remove:

```python
await session.dom_debugger.remove_xhr_breakpoint(url="*api.example.com*")
```

---

## Event breakpoints

The `EventBreakpoints` domain provides instrumentation breakpoints for
native DOM events:

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
