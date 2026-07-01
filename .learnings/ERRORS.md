# Error Log

## [ERR-20260619-001] local-http-server

**Logged**: 2026-06-19T11:22:05-04:00
**Priority**: low
**Status**: resolved
**Area**: infra

### Summary
Starting the local preview server failed because port 8765 was already occupied by an inaccessible stale Python listener.

### Error
```
OSError: [Errno 48] Address already in use
```

### Context
- Attempted `python3 -m http.server 8765` from the repository root.
- `lsof` showed an existing Python listener on `*:8765`.
- Both `127.0.0.1:8765` and `localhost:8765` were unreachable from the current sandbox.
- Mobile visual QA continued with direct `file://` navigation because the target pages are static and use inline CSS.

### Suggested Fix
Check whether the expected preview port is already usable before starting a new server; use direct local-file navigation for read-only static-page QA when localhost is unavailable.

### Metadata
- Reproducible: unknown
- Related Files: daily_plans/2026-06-19.md

---

## [ERR-20260619-003] steam-news-api-network

**Logged**: 2026-06-19T11:39:00-04:00
**Priority**: low
**Status**: resolved
**Area**: infra

### Summary
Direct shell access to the Steam News API failed because sandbox DNS could not resolve the host.

### Error
```
curl: (6) Could not resolve host: api.steampowered.com
```

### Context
- Attempted to retrieve the historical Lies of P 1.3 patch announcement through Steam's public news API.
- Continued through the in-app Browser and indexed official Steam announcement results.
- The exact Polendina patch wording was independently reproduced by multiple indexed patch-note mirrors.

### Suggested Fix
Use Browser or the normal web retrieval layer for external research when shell DNS is restricted.

### Metadata
- Reproducible: environment-dependent
- Related Files: daily_plans/2026-06-19-task-B-result.md

---

## [ERR-20260619-002] browser-plugin-bootstrap

**Logged**: 2026-06-19T11:24:00-04:00
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
Browser bootstrap failed because the cached plugin version changed and the previously loaded absolute module path no longer existed.

### Error
```
Module not found: .../browser/26.608.12217/scripts/browser-client.mjs
```

### Context
- The installed Browser plugin had moved to version `26.616.32156`.
- Loading `browser-client.mjs` from the current version restored the in-app Browser.
- Real 390px mobile QA then completed successfully through `127.0.0.1:8876`.

### Suggested Fix
Resolve the active Browser plugin version before bootstrap instead of persisting an older versioned absolute path across environment refreshes.

### Metadata
- Reproducible: yes
- Related Files: daily_plans/2026-06-19-task-A-result.md

---

## [ERR-20260619-004] in-app-browser

**Logged**: 2026-06-19T11:24:00-04:00
**Priority**: medium
**Status**: resolved
**Area**: tests

### Summary
The in-app browser disconnected on first navigation and was unavailable after reconnection.

### Error
```
native pipe closed before response
Browser is not available: iab
```

### Context
- Browser runtime initialized successfully and viewport capability documentation was available.
- The first 390x844 navigation attempt closed the browser connection.
- A fresh server on `127.0.0.1:8876` started successfully, but a clean browser reconnection reported that the in-app browser was unavailable.
- Per the Browser skill, no standalone Playwright or Computer Use fallback was used.

### Resolution
The active Browser plugin version was located, the browser backend was restored, and all six pages completed real 390 × 844 visual QA through `127.0.0.1:8876`.

### Suggested Fix
Resolve the currently installed Browser plugin version before reconnecting, then use a free preview port.

### Metadata
- Reproducible: unknown
- Related Files: daily_plans/2026-06-19-task-A-result.md

---
