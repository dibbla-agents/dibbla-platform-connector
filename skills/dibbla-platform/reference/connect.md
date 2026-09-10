<!-- DIBBLA-GENERATED
This file is generated from the Dibbla connector skill source. Do not edit it by
hand: edit the source and regenerate, or your change is gone at the next release.
source: app-hosting-service/mcp-server/skillset/dibbla-platform
source-version: 1.0.0
source-digest: sha256:b712061da97e82b2f5ea7725ed593241665aa788144b87d3895b881f12f78fa9
generator: app-hosting-service/mcp-server/connectorpkg
-->

# Connecting, consent, and what a refusal means

## The endpoint

The Dibbla connector is one URL: `https://mcp.dibbla.com/platform`. It is
OAuth-protected, so nothing is configured with a token — the surface you are
running in performs the authorization itself, the person approves in their
browser, and the grant is stored by that surface.

Four surfaces reach it, and they differ only in where the browser step happens:

- **claude.ai and Claude Cowork** — added as a connector in the account's
  connector settings. The redirect is `https`, so nothing about the local
  machine matters.
- **Claude Code** — added as a remote MCP server pointing at that URL. The
  browser consent runs on first use, with a loopback callback.
- **Codex CLI** — the same, also over a loopback callback.
- **ChatGPT** — added as a connector.

A loopback callback may use `127.0.0.1`, `[::1]` **or** `localhost`; all three
are accepted over plain `http`. Nothing else is: a hostname that merely contains
"localhost", and any LAN address, is refused at registration and again at
authorization.

Reconnecting the same surface does not create a new client. Identity is derived
from what the client is — its metadata document URL, or the exact registration
it presented — so an agent that reconnects lands on the client it already had.

## Which surfaces draw a card, and which read it as text

The four surfaces above differ in one more way that matters to the person
watching: whether they render an MCP App. claude.ai, the Claude apps and Cowork
draw the card `platform_app_card` returns, and so does ChatGPT on web and
mobile. A terminal client — Claude Code, Codex CLI — does not, and neither does
any client that has not implemented the extension.

This never changes what you call. The card tool answers the same content either
way: drawn where it can be drawn, ordinary text where it cannot. What differs is
that the drawn card keeps itself up to date while a deploy runs and the text
does not, so keep following the operation and keep saying what happened in
words: you cannot see which kind of client you are on, and the sentence has to
be true on both.

## Consent is a page the person reads, not a flag you set

The authorization page says who is asking, which organization it will act in,
and what it wants to do — in plain language, with the exact scope names one
click away. It ends in **two buttons: "Allow read-only" and "Allow full
access".** Read-only grants the reads and nothing else, however much was asked
for; full access adds the writes that were asked for. That is deliberate: a
connection approved without anybody thinking about it is a read-only
connection.

The practical consequence for you: a grant can come back holding fewer scopes
than were requested, and everything will look fine until the first write answers
`INSUFFICIENT_SCOPE`. That is not a bug in the platform and not something to
work around — it is somebody who chose read-only. Say that plainly and ask them
to reconnect and choose full access; do not retry. `platform_whoami` lists the
scopes you actually hold; check there before you conclude anything else.

The person also picks **one organization** on that page. The grant is bound to
it. There is no tool, parameter or header that reaches another one.

## Scope by scope

| Scope | Class | Tools it unlocks |
|---|---|---|
| `platform:identity:read` | read, on by default | `platform_catalog`, `platform_whoami` |
| `platform:apps:read` | read, on by default | `platform_apps` |
| `platform:apps:write` | write, off by default | `platform_app_config_update`, `platform_app_run` |
| `platform:apps:restart` | narrow-write, off by default | `platform_app_restart` |
| `platform:apps:delete` | destructive, off by default | `platform_destructive_execute` |
| `platform:deployments:read` | read, on by default | `platform_deployment_proposals`, `platform_deployments` |
| `platform:deployment-proposals:write` | write, off by default | `platform_deployment_proposals` |
| `platform:deployments:execute` | narrow-write, off by default | `platform_deployment_start` |
| `platform:deployments:preflight` | read, on by default | `platform_deployment_preflight` |
| `platform:logs:read` | read, on by default | `platform_app_logs` |
| `platform:checks:read` | read, on by default | `platform_app_checks` |
| `platform:checks:write` | write, off by default | `platform_app_checks_set_enabled` |
| `platform:checks:execute` | narrow-write, off by default | `platform_app_run` |
| `platform:secrets:metadata:read` | read, on by default | `platform_secrets` |
| `platform:secrets:write` | write, off by default | `platform_secret_write` |
| `platform:databases:read` | read, on by default | `platform_databases` |
| `platform:databases:rows:read` | read, off by default | `platform_database_rows_query` |
| `platform:databases:write` | write, off by default | `platform_database_provision` |
| `platform:databases:restore` | destructive, off by default | `platform_destructive_execute` |
| `platform:databases:delete` | destructive, off by default | `platform_destructive_execute` |
| `platform:storage:read` | read, on by default | `platform_storage_buckets` |
| `platform:storage:write` | write, off by default | `platform_storage_bucket_write` |
| `platform:storage:rotate` | narrow-write, off by default | `platform_storage_bucket_write` |
| `platform:storage:delete` | destructive, off by default | `platform_destructive_execute` |
| `platform:workflows:read` | read, on by default | `platform_catalog`, `platform_workflows` |
| `platform:workflows:write` | write, off by default | `platform_workflow_apply` |
| `platform:workflows:execute` | narrow-write, off by default | `platform_workflow_execute` |
| `platform:files:read` | read, on by default | `platform_files` |
| `platform:files:write` | write, off by default | `platform_files` |
| `platform:files:delete` | destructive, off by default | `platform_destructive_execute` |
| `platform:operations:read` | read, on by default | `platform_operation` |
| `platform:operations:cancel` | narrow-write, off by default | `platform_operation_cancel` |
| `platform:workflows:delete` | destructive, off by default | `platform_destructive_execute` |
| `platform:feedback:write` | write, off by default | `platform_feedback` |
| `platform:tools:execute` | narrow-write, off by default | every tool on the `/platform/tools` mount — the functions the organization has exposed, listed with `platform:workflows:read` |

`platform_workflow_validate` and `platform_destructive_plan` come with the read
side of their family: validating a draft saves nothing, and planning a deletion
destroys nothing.

Two rules about this table are worth knowing because they explain refusals that
otherwise look arbitrary:

- **No scope implies another.** Holding `platform:apps:write` does not let you
  restart an app; that is `platform:apps:restart`. Holding
  `platform:workflows:write` does not let you run a workflow; that is
  `platform:workflows:execute`. The irreversible and the expensive always have
  their own scope, so a person can grant the everyday one without granting them.
- **Some scopes do not exist, on purpose.** There is no scope that returns a
  secret's value, no scope that runs arbitrary SQL, and no admin scope. If a
  task needs one of those, the answer is that the surface does not do it — not
  that a wider grant would help.

## Reading a refusal

| Answer | What it means | What to do |
|---|---|---|
| The tool is **not in your tool list** | The grant does not hold its scope | Name the scope; ask for a connection that includes it |
| `INSUFFICIENT_SCOPE` | The grant does not hold the scope this call needs; the answer names it | The same — this is not a retry |
| `FORBIDDEN` | The scope is held, but the user's role in this organization is too low | Tell them which role the action needs |
| `NOT_FOUND` for something that exists | Almost always the wrong organization | `platform_whoami` lists the others; ask them to connect the right one |
| `CONFLICT` | Something changed under you — a stale `base_sha`, an operation already finished, an idempotency key reused with different arguments | Re-read the current state and decide again; do not force it |

When you ask for a wider connection, ask **once**, name the exact scope strings,
and say what they let you do. "I need `platform:deployments:execute` to deploy
this change" is a request somebody can act on; "I got a permission error" is not.
