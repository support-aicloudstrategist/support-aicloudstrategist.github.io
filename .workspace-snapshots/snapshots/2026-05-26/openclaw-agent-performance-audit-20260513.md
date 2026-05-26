# OpenClaw Agent Performance Audit — 2026-05-13

## Scope
Diagnose why recent AICloudStrategist subagents failed, lost active execution context, or timed out. Reviewed:
- `/home/OpenClaw/.openclaw/subagents/runs.json`
- `/home/OpenClaw/.openclaw/openclaw.json` with secrets redacted in inspection
- `/home/OpenClaw/.openclaw/logs/config-audit.jsonl`
- `journalctl --user` for `openclaw-gateway.service`
- `/tmp/openclaw/openclaw-2026-05-13.log`
- systemd unit metadata for `openclaw-gateway.service`

No risky config changes were made.

## Executive finding
The failures were not caused by a single bad subagent prompt. They came from a cascade:

1. Several long-running/high-complexity subagents were launched concurrently.
2. The model/provider (`openai-codex/gpt-5.5`) showed idle-timeout/stall behavior under load.
3. Gateway restarts were triggered while subagents were still active.
4. The gateway tried to drain for 300s, but the systemd user unit only allowed 30s stop time, so systemd SIGKILLed the gateway.
5. Active subagent sessions became orphaned or lost their active execution context. Recovery later resumed some tasks, but several runs had already been marked failed/timeout.

## Evidence timeline, IST

### Successful initial research burst
At ~14:30–14:35 IST, several research subagents completed successfully:
- `aics-million-dollar-market-whitespace` — ok, ~194s
- `aics-scalable-business-model-research` — ok, ~121s
- `aics-customer-communication-differentiation` — ok, ~156s
- `aics-brand-architecture-two-sites-retry` — ok, ~95s

There were already liveness warnings during this phase:
- Event loop delay p99 ~134ms, max ~1059ms
- Active model calls: main + multiple subagents
- Queue present on main session

### Primary lost-context failures
At ~14:40–14:44 IST, four complex implementation/sync tasks failed with `subagent run lost active execution context`:
- `aics-website-two-lanes-live-redesign`
- `aics-enterprise-docs-drive-notion`
- `aics-messaging-whatsapp-email-refresh`
- `aics-github-ops-docs-sync`

These tasks were broad and tool-heavy: website production deploy, Drive/Notion sync, GitHub docs sync, config/messaging review. They were likely too large to run concurrently through model-driven subagents during a gateway disturbance.

### Restart/draining failure
At ~14:42:29 IST, journal shows:
- Gateway received SIGTERM/restart.
- Gateway started draining `8 active task(s)` and `3 active embedded run(s)` with internal drain timeout `300000ms`.
- Restart was blocked by active background task runs.

At ~14:42:59 IST:
- systemd `TimeoutStopSec=30` expired.
- systemd killed gateway and children with SIGKILL.
- Unit restarted.
- Memory peak reported ~1.0GB.

This is a key mismatch: OpenClaw attempted a 300s graceful drain, but systemd allowed only 30s before hard-killing it.

### Second restart during active recovery
At ~14:48:53 IST, another restart occurred while active recovery tasks were running:
- Gateway again tried to drain `8 active task(s)` and `3 active embedded run(s)`.
- A new task failed immediately with `GatewayDrainingError: Gateway is draining for restart; new tasks are not accepted`.

At ~14:49:23 IST:
- systemd again killed the gateway after 30s.
- Memory peak reported ~900MB.

### Model idle timeout/stalls
Logs show repeated model issues:
- `embedded run failover decision ... reason=timeout ... fallbackConfigured=false`
- `The model did not produce a response before the model idle timeout`
- `[llm-idle-timeout] openai-codex/gpt-5.5 produced no reply before the idle watchdog; retrying same model`
- Diagnostic stalled sessions with `activeWorkKind=model_call`, no progress for 129s–268s+

This indicates provider/model latency or overload was a real contributor. Because no fallback is configured, timeout surfaces directly or retries the same model.

## Current configuration observations

### OpenClaw version/runtime
- OpenClaw package version: `2026.5.7`
- Gateway process active after restart: `/usr/bin/node ... openclaw/dist/index.js gateway --port 18789`
- Runtime line indicated Node `v24.15.0`.

### Model configuration
Current `openclaw.json` has:
- Default primary model: `openai-codex/gpt-5.5`
- Agent model entries only for `openai-codex/gpt-5.5`
- No visible fallback provider/model configuration in inspected keys.
- No visible explicit provider timeout setting in inspected config.

### Agent count/concurrency
- 18 agents are configured.
- Many subagent jobs were active concurrently during the incident.
- `subagents` config section was not present in inspected config, so no explicit active-task/concurrency cap was observed.

### Gateway/systemd mismatch
Systemd user unit has:
- `TimeoutStopSec=30`
- `Restart=always`
- `KillMode=control-group`

Gateway drain log says:
- drain timeout `300000ms` (300s)

This mismatch made graceful draining impossible under active task load.

### Security/config side notes
Not directly related to the subagent failures, but observed:
- Gateway binds to LAN (`bind: lan`), not loopback.
- Gateway logs warn `gateway.controlUi.allowInsecureAuth=true`.
- `plugins.allow` is empty, and non-bundled WhatsApp plugin auto-loads.

These should be reviewed separately for security posture, but they were not the immediate cause of lost subagent context.

## Root-cause assessment

### Primary root cause
Gateway restarts occurred while multiple long-running subagents and embedded model calls were active. The gateway attempted graceful drain, but systemd killed it after 30 seconds, causing active execution context loss.

### Contributing factors
1. **Model/provider idle timeouts**: `openai-codex/gpt-5.5` had repeated no-reply/idle timeout warnings.
2. **No configured fallback**: logs say `fallbackConfigured=false`.
3. **High concurrent task load**: active=4+ model calls and queued sessions before the incident; later 8 active tasks/3 embedded runs during restarts.
4. **Large monolithic tasks**: production deploy + Drive + Notion + GitHub + config edits are high variance and should not all run as broad autonomous subagents at once.
5. **Announcement path timeouts**: subagent completion announcement calls themselves hit `gateway timeout after 120000ms`, delaying/duplicating recovery status.

## Recommended configuration/process changes

### Highest priority — safe operational standards
1. **Do not restart gateway during active subagents.**
   - Before restart, confirm no active subagent/background tasks.
   - If restart is required, pause spawning and let active tasks finish or intentionally cancel/retry them.

2. **Cap concurrent heavy subagents.**
   - Recommended operating limit: 1–2 heavy subagents at a time.
   - Use more only for short research tasks with no external writes.

3. **Split implementation tasks into deterministic units.**
   - Good: “edit index.html section X, run grep, commit.”
   - Risky: “redesign site, deploy, sync Drive/Notion/GitHub, update config, verify all.”

4. **Use direct tools for deterministic generation.**
   - For docs/templates: use direct file generation/editing, then upload/sync.
   - For website patches: inspect repo, targeted edit, local diff/build, commit/push.
   - Avoid asking a model subagent to hold a long plan in active context while doing many independent side effects.

### Configuration recommendations to evaluate
1. **Align systemd stop timeout with gateway drain.**
   - Current: systemd `TimeoutStopSec=30`; gateway drain `300s`.
   - Recommended: increase systemd `TimeoutStopSec` to at least 330–360s, or configure gateway drain lower than systemd timeout.
   - This is reversible but service-level; should be changed via proper OpenClaw/gateway config or unit management with approval.

2. **Configure provider timeout/fallback if supported.**
   - Logs explicitly recommend increasing `models.providers.<id>.timeoutSeconds` for slow providers.
   - Add a fallback model/provider if available, because logs currently show `fallbackConfigured=false`.
   - For long synthesis tasks, consider a more stable/fast model profile; reserve `gpt-5.5` for high-value reasoning, not every subagent.

3. **Add or use concurrency controls if available.**
   - No explicit `subagents` concurrency config was visible in `openclaw.json`.
   - If OpenClaw supports max active subagents / per-agent queue limits, set conservative defaults.

4. **Pin trusted plugins.**
   - Set `plugins.allow` explicitly for trusted plugin IDs, especially WhatsApp, to remove auto-load warnings.
   - This is security hygiene, not performance-critical.

5. **Review LAN/insecure auth posture.**
   - Because gateway binds to LAN and `allowInsecureAuth=true`, run a separate security audit before broader exposure.

## Proposed agent execution standards for AICloudStrategist

### Task sizing
- Research-only: max 3 parallel subagents, 15–30 min timeout.
- Tool-heavy local writes: max 1–2 parallel subagents, explicit file targets and output paths.
- External writes/deploys/config: one task at a time; no gateway restart while active.

### Prompt structure
Every subagent task should include:
- Exact deliverable path(s)
- Maximum scope and exclusions
- Verification command/check
- “Do not restart gateway unless explicitly instructed”
- “If blocked, write report instead of looping”

### Output discipline
- Ask for concise structured outputs, not giant unbounded narratives.
- Require a local report artifact for every long task.
- For implementation, require “files changed, commands run, verification result, blockers.”

### Timeout guidance
- Short deterministic edits: 600–1200s
- Medium docs/build tasks: 1800–2400s
- Large deploy/sync tasks: 3600s only if split into clear phases with checkpoints
- If a model call stalls repeatedly, stop retrying the same subagent and switch to deterministic/direct tool work.

### Recovery playbook
If context-loss happens again:
1. Stop spawning new subagents.
2. Check gateway state and active tasks.
3. Avoid restart unless gateway is truly stuck.
4. Recover from artifacts: inspect workspace, git status, generated reports.
5. Relaunch smaller deterministic tasks, not the same broad prompt.

## Current status at audit time
- Gateway service is active/running again.
- Gateway process uptime from `ps` was ~41 minutes at inspection.
- New audit subagent was running successfully while logs still showed occasional event-loop delay warnings.
- No config changes were made by this audit.

## Bottom line
The biggest fix is operational: stop restarting while active subagents are running, and stop launching multiple broad external-write tasks concurrently. The biggest configuration fix is to align systemd `TimeoutStopSec` with OpenClaw’s 300s drain behavior and add model timeout/fallback settings if supported.