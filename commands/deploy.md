---
description: Deploy a change to a Dibbla application and follow it until it is live
argument-hint: "[app alias] [what to change]"
---

<!-- DIBBLA-GENERATED
This file is generated from the Dibbla connector skill source. Do not edit it by
hand: edit the source and regenerate, or your change is gone at the next release.
source: app-hosting-service/mcp-server/skillset/dibbla-platform
source-version: 1.0.0
source-digest: sha256:b712061da97e82b2f5ea7725ed593241665aa788144b87d3895b881f12f78fa9
generator: app-hosting-service/mcp-server/connectorpkg
-->
Deploy to Dibbla: $ARGUMENTS

Work over the connector only. There is no shell here, nothing is downloaded, and
no local copy is involved.

1. **Find the app.** `platform_apps` with no alias lists them; with an alias it
   answers status, URL, resources and each service. If the person did not name
   one and there is more than one, ask which.
2. **Read what is actually running.** `platform_files` — `action=glob` for paths,
   `action=grep` to find the place, `action=read` for a numbered window of one
   file. These answer the deployed revision, not a branch and not a local copy.
   Note the revision the answer reports.
3. **Change only what changes.** `platform_deployment_start` with `mode=patch` and
   `files` holding only the files you touched, each as its **whole new content** —
   never a diff, never line numbers — plus `delete` for paths to remove. Pass
   `base_sha` set to the revision step 2 reported, so a deploy that landed while
   you worked refuses your patch instead of silently overwriting it. A first
   publish is the same call with `mode=replace` and the whole tree, which needs a
   Dockerfile at the root of what you send, or a `dibbla.yaml` naming services
   that each have one.
4. **Show it immediately.** `platform_app_card` with the alias and the
   `operation_id` the deploy just answered — before you start polling, and without
   being asked. The card keeps itself up to date until the app is live on the
   surfaces that draw it, and arrives as ordinary text on the ones that do not.
   Call it either way; you cannot see which kind of surface you are on.
5. **Follow it.** `platform_operation` `view=status` until the phase is terminal,
   `view=logs` while it builds, `view=output` for the result. **The live URL is in
   `view=output`**, not in the answer that started the deploy.
6. **Say what happened.** The app is live at its URL, or the build failed at this
   line of the build log. Never report an operation id or an upload link as if it
   were a result.

If the organization requires review, the deploy is recorded as pending and
nothing is live until a different authorized person approves it in the Dibbla
console. Say that plainly instead of waiting; you cannot approve your own.
