<!-- DIBBLA-GENERATED
This file is generated from the Dibbla connector skill source. Do not edit it by
hand: edit the source and regenerate, or your change is gone at the next release.
source: app-hosting-service/mcp-server/skillset/dibbla-platform
source-version: 1.0.0
source-digest: sha256:dc705685f321e53738323892c3a10d340dc741bcdd2fd01644e57ba2c4cee2a1
generator: app-hosting-service/mcp-server/connectorpkg
-->

# Irreversible changes

Seven things on Dibbla cannot be undone, and all seven go through the same two
tools. There is no delete parameter hidden on a normal tool, and there is no
tool that approves — on purpose.

| `resource` | What is destroyed |
|---|---|
| `app` | An application by alias, with its services, routes, deployment-scoped secrets, version-control history and persistent volumes |
| `database` | A managed database by name, with every table, its PostgreSQL role, its ownership record and its injected `DATABASE_URL` secret |
| `database_restore` | Loads a dump into a database, replacing every object the dump defines; the data there today cannot be brought back |
| `file` | A file record by its opaque `source_file_id`, so every capability naming it stops working; the shared blob stays |
| `storage_bucket` | A bucket by name with every object in it, its service account, its ownership record and four injected secrets |
| `workflow` | A workflow by name, with every revision of its definition and every run it recorded |
| `workflow_runs` | The run history of a workflow older than `before`; the workflow keeps working, its audit trail of those runs does not |

## The two steps

**1. `platform_destructive_plan`.** Changes nothing. It answers with exactly
what would be destroyed, an expiring `request_id`, and a Dibbla console URL. A
human must open that URL, read the bound organization, actor, target and
effects, and approve there. The `request_id` on its own authorizes nothing.

Give the person the console link and the list of effects, in their own terms.
"This deletes the app `checkout`, its database and its two persistent volumes,
and none of it can be restored" is what they need to decide.

**2. `platform_destructive_execute`.** Performs exactly the change stored in the
approved plan. Supply only the `resource` and the `request_id` — what is
destroyed was fixed when the human approved, and cannot be changed here. The
server redeems the `request_id` once and durably replays its terminal result.

It refuses: a target that changed after planning, an expired approval, a denied
approval, and any mismatch in user, organization, client, grant, role or scope.
Each of those is the guard working. Do not plan a second time to get around a
refusal without telling the person why the first one was refused.

Execute returns an operation, like the other long work. Follow it with
`platform_operation`.

## Before you plan anything

Deletion is almost never what somebody meant. If the request is "clean this up",
"get rid of the old one" or "reset it", find out which of these seven it maps to
and say so out loud before planning. Restarting an app, disabling its checks,
rolling a workflow back to an earlier revision, or deploying a fix are all
reversible, and one of them is usually the actual request.
