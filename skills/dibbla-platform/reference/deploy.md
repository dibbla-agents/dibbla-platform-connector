<!-- DIBBLA-GENERATED
This file is generated from the Dibbla connector skill source. Do not edit it by
hand: edit the source and regenerate, or your change is gone at the next release.
source: app-hosting-service/mcp-server/skillset/dibbla-platform
source-version: 1.0.0
source-digest: sha256:b712061da97e82b2f5ea7725ed593241665aa788144b87d3895b881f12f78fa9
generator: app-hosting-service/mcp-server/connectorpkg
-->

# Publishing and changing an application

## What the platform needs in order to build at all

Whatever you send must be buildable by the platform. That means one of:

- a **`Dockerfile` at the root** of what you send, or
- a **`dibbla.yaml`** at the root naming services that each have one.

Nothing is auto-detected. A tree without either fails **at build**, not at
validation — you will see it in the operation's logs, not in the answer to the
call that started it. If you are writing an application from scratch, write the
Dockerfile too; it is part of the source, not part of the platform.

`platform_catalog kind=templates` lists the project templates the platform
scaffolds from. They all ship a working Dockerfile, so they are the fastest
answer to "what should this look like".

Exclude build output and dependencies from what you send — `node_modules`, a
`dist` or `target` directory, `.git`. They are rebuilt inside the image, they
count against the bounds below, and sending them is the most common reason a
first publish is refused for size.

## The three sources, and which one you have

`platform_deployment_start` takes exactly one of `files`, `archive` or `source`.

**`files` — the tree in the call itself.** `[{file, data, encoding}]`. This is
the path that works with no shell, no filesystem and no git: you wrote the code
in your head, and it goes straight into the call. Bounded at **200 files and
2 MB of decoded content**. Above that the answer tells you to use `archive` or
the Dibbla CLI — that is a real bound, not a suggestion to try again in pieces.

**`archive` — a gzipped tar you can read from a filesystem.** You give its exact
byte size and sha256; the answer carries a structured `upload` field, and a
client process PUTs the bytes there with the platform access token it already
holds, resuming from `Upload-Offset`. The deploy starts by itself when the last
chunk lands. Bytes never pass through the conversation. If you cannot run a
process that does an HTTP PUT, this is not your path.

**`source` — a ref in the repository the application is linked to.** A branch,
tag or commit that you have already pushed. The platform fetches it with its own
credential; nothing is uploaded, and the answer names the exact `commit_sha`
being deployed. This is the normal answer in a cloud sandbox that can reach
GitHub but cannot reach an upload URL.

Never put an archive's bytes or base64 into `files`. An archive moves on the
byte plane; `files` carries source text. They are different things and mixing
them fails in a confusing way.

## `mode=replace` versus `mode=patch`

`mode=replace` means *this is the application now* — the tree you send is the
whole source. Use it for a first publish, or when you genuinely rewrote
everything.

`mode=patch` means *change these files, leave the rest alone*. Send only the
files that change, **each as its whole new content**, plus `delete` for paths to
remove. Everything you do not mention stays exactly as it is, and the deploy
lands as one commit on top of the app's current revision.

Two rules that matter more than they look:

- **Never send a diff, a patch hunk, or line numbers.** The field is the file's
  new content. A unified diff sent as content deploys a file containing a
  unified diff.
- **Pass `base_sha`.** Set it to the revision `platform_files` reported when you
  read the code. If a deploy landed while you were working, the platform refuses
  your patch instead of quietly overwriting that person's change. Omitting it
  applies your patch to whatever is current, which is the behaviour you want
  roughly never.

To change an app you did not create, you do not need its source in your hands.
`platform_files` reads the deployed revision, and `mode=patch` writes back to
it.

## Dry-running a manifest

`platform_deployment_preflight` resolves a `dibbla.yaml` exactly as a deploy
would — parsing, env-aware resolution, profiles, public routing, resource shapes
and the organization's quota limits — and applies nothing. `depth=validate` (the
default) answers with findings: a stable code, the path in the manifest, and a
sentence. `depth=preview` additionally lists what a deploy would apply: the
active services with their image, port, replicas and resources, the services
skipped for this env and profile combination and why, the public service, and
any warnings.

**A manifest that fails preflight fails at deploy.** For anything with a
`dibbla.yaml`, running preflight first is cheaper than reading a build log.

## Following the deploy

`platform_deployment_start` never waits. It returns an `operation_id`.

- `platform_operation view=status` — the phase, until it is terminal
- `platform_operation view=logs` — the build output while it runs
- `platform_operation view=output` — **the deployed application's URL lives
  here**, and nowhere else

Repeating the call with the same `idempotency_key` returns the same operation,
so an interrupted upload resumes and a retried deploy is still one deploy.

Report the outcome. Not the upload link, not the operation id on its own.

## When the organization requires review

Some organizations require a deploy to be reviewed. There, the operation does
not go live — it records a **pending** deploy that a different authorized person
approves in the Dibbla console. Nothing is running until they do, and you can
never approve your own. When you see this, say so plainly: the change is
staged and waiting for a named human, not deployed.

`platform_deployment_proposals` is the tool for that queue, and also the way to
propose a deploy from a branch you pushed to the application's Dibbla git
remote:

- `action=create` pins the branch's head as the source revision and the platform
  builds and checks it. It carries **no environment variables and no secret
  values** — secrets stay referenced by name in the app's manifest.
- `action=events` is what you poll to follow a proposal you created: created,
  checks passed or failed, approved or denied, deployed.
- `action=approve` / `deny` / `retry` decide one, or rebuild one whose checks
  failed. Under four-eyes the decider must be somebody other than the author, so
  you can never decide your own, and an agent-authored proposal always needs an
  owner or admin other than its author. A refusal names the reason.

## After it is live

- `platform_deployments` — the history, newest first; each deployment is an
  immutable revision and one is marked current. `view=logs` reads the current
  deployment's logs.
- `platform_app_logs` — a bounded window of the running application's logs.
- `platform_app_checks` and `platform_app_run kind=checks` — the application's
  own checks. A failing check is a **result**, not an error.
- `platform_app_config_update` — non-secret environment variables by name, and
  `replicas`, `cpu`, `memory` within the plan. The app restarts to pick the
  change up. Secret values, ports, login policy and OAuth scopes are not
  changeable here, and a variable whose name or value looks like a credential is
  refused; those belong in `platform_secret_write`.
- `platform_app_restart` — a rolling restart, everything or one service. Nothing
  is deleted and no configuration changes.
