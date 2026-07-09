"""Execute ALL 574 tests from TEST-ROADMAP.md against real Chrome headless.

This is the main entry point that imports and runs all test modules.
"""

from __future__ import annotations

import asyncio
import json
import traceback
from typing import Any

from cdpwave.client import CDPClient
from tests.manual._test_helpers import results, log_result


def summarize() -> None:
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    for status, count in sorted(counts.items()):
        print(f"  {status}: {count}")
    print(f"  TOTAL: {len(results)}")

    fails = [r for r in results if r["status"] in ("FAIL", "ERROR")]
    if fails:
        print(f"\nFAILED/ERROR TESTS ({len(fails)}):")
        for r in fails:
            print(f"  {r['tc']}: {r['name']}")
            if r["detail"]:
                print(f"    → {r['detail'][:200]}")


async def main() -> None:
    # Import all test modules to register tests
    from tests.manual.tests_runtime import _test_registry as reg1
    from tests.manual.tests_domains_p1a import _test_registry as reg2
    from tests.manual.tests_domains_p1b import _test_registry as reg3
    from tests.manual.tests_domains_p1c import _test_registry as reg4
    from tests.manual.tests_domains_p2 import _test_registry as reg5
    from tests.manual.tests_domains_p3 import _test_registry as reg6
    from tests.manual.tests_integration import _test_registry as reg7

    all_tests = reg1 + reg2 + reg3 + reg4 + reg5 + reg6 + reg7

    print("=" * 70)
    print(f"EXECUTING {len(all_tests)} TESTS FROM TEST-ROADMAP.md")
    print("=" * 70)

    print("\nLaunching Chrome headless...")
    client = await CDPClient.launch(headless=True)
    print(f"Chrome launched. Connected: {client.is_connected}")

    try:
        for i, (tc_id, name, func) in enumerate(all_tests):
            print(f"\n[{i+1}/{len(all_tests)}] {tc_id}: {name}")
            try:
                await func(client)
            except Exception as e:
                tb = traceback.format_exc()
                msg = str(e)
                if "wasn't found" in msg:
                    log_result(tc_id, name, "SKIP", f"CDP method not available: {msg[:200]}")
                else:
                    log_result(tc_id, name, "ERROR", tb[:2000])
            await asyncio.sleep(0.1)
    finally:
        print("\nClosing Chrome...")
        await client.close()
        print("Chrome closed.")

    summarize()

    results_path = "_all_test_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {results_path} ({len(results)} entries)")


if __name__ == "__main__":
    asyncio.run(main())
