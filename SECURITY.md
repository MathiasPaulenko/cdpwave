# Security Policy

## Supported Versions

cdpwave is under active development. Security fixes are applied to the latest
release only.

| Version | Supported |
|---------|-----------|
| 2.0.x   | Yes       |
| < 2.0   | No        |

## Reporting a Vulnerability

If you discover a security vulnerability in cdpwave, please report it
responsibly:

1. **Do not** open a public GitHub issue
2. Email **mathias.paulenko@outlook.com** with:
   - A description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
3. You will receive a response within 48 hours

## Security Considerations

cdpwave launches and controls Chromium-based browsers via the Chrome DevTools
Protocol. Keep the following in mind:

- **Remote debugging port**: cdpwave uses `--remote-debugging-port` which
  exposes a WebSocket endpoint. In production, ensure this port is not
  accessible to untrusted networks.
- **Arbitrary JavaScript execution**: `Runtime.evaluate()` executes arbitrary
  JavaScript in the browser context. Only run trusted code.
- **Browser subprocess**: The browser process inherits the permissions of the
  user running the Python script. Run with least privilege.
- **URL navigation**: `Page.navigate()` can open any URL. Validate user input
  if accepting URLs from untrusted sources.

## Disclosure Policy

- Vulnerabilities are disclosed after a fix is released
- Credit is given to the reporter (unless they prefer to remain anonymous)
