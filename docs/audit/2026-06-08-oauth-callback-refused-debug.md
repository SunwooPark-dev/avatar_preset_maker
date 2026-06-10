# Audit: OAuth Callback Connection Refused Debugging

- Date: 2026-06-08
- Agent: Antigravity
- Mode: debug
- Task ID: 31b6948b-490d-430b-8c83-624736ac4d44
- Why: Investigate why the user encountered a "This site can't be reached" (ERR_CONNECTION_REFUSED) error at `http://localhost:1455/auth/callback`.
- Scope: Backend subprocess lifecycle and testing history analysis.
- Evidence / Sources:
  - Screenshot showing callback URL `localhost:1455/auth/callback` refusing connection.
  - Server logs (`task-278.log`) showing sequence: `POST /api/login` at `01:48:24` followed by `POST /api/login/cancel` at `01:48:27`.
- Commands run:
  - `python test_login_devnull.py` to confirm that backgrounding works and doesn't exit prematurely under `DEVNULL` redirection (Exit code: 0, stayed running).
- Results:
  - Isolated the cause: The test `curl` execution for `/api/login/cancel` at `01:48:27` terminated the active `codex login` process.
  - When the OAuth callback was redirected to port 1455, the server was no longer listening, causing the connection refusal.
- Risks: None. Re-running the login flow will spawn a new server instance and resolve the connection.
- Rollback: N/A.
- Remaining TODO: Instruct the user to trigger the login button again to complete the flow.
