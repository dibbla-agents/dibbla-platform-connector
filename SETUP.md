<!-- DIBBLA-GENERATED
This file is generated from the Dibbla connector skill source. Do not edit it by
hand: edit the source and regenerate, or your change is gone at the next release.
source: app-hosting-service/mcp-server/skillset/dibbla-platform
source-version: 1.0.0
source-digest: sha256:b712061da97e82b2f5ea7725ed593241665aa788144b87d3895b881f12f78fa9
generator: app-hosting-service/mcp-server/connectorpkg
-->

# Setting up the Dibbla connector

Dibbla hosts applications: their source, deployments, logs, secrets, databases,
storage buckets, workflows and scheduled checks. This package connects an agent
to a Dibbla organization over one URL:

    https://mcp.dibbla.com/platform

That is the whole configuration. There is no token to paste, no header to set
and no API key anywhere in this repository. The endpoint is OAuth-protected: the
surface you are running in performs the authorization itself, you approve it in
your browser, and the surface stores the grant.

## Install it

**Claude Code** — add the plugin from this repository, then run `/dibbla:connect`.
The browser opens, you approve, and the connection is verified for you.

**Claude Cowork and claude.ai** — add https://mcp.dibbla.com/platform as a
connector in your account's connector settings and approve there.

**Codex CLI** — add the same URL as a remote MCP server; the browser step runs
over a loopback callback on first use.

**ChatGPT** — add the same URL as a connector.

A loopback callback may use `127.0.0.1`, `[::1]` or `localhost`, over plain
`http`. Nothing else is accepted: a LAN address, or a hostname that merely
contains "localhost", is refused at registration and again at authorization.

## The consent page has two buttons

The authorization page says who is asking, which organization the connection
will act in, and what it wants to do. It ends in **"Allow read-only"** and
**"Allow full access"**. Read-only grants the reads and nothing else, however
much was asked for.

This matters later rather than immediately: a read-only connection looks
completely healthy until the first write answers `INSUFFICIENT_SCOPE`. That is
not a fault — it is the choice that was made on that page. Reconnect and choose
full access. Ask the connection what it holds with `platform_whoami` before
concluding anything else.

## One connection is one user in one organization

Every tool acts in the organization the grant was made for and nowhere else.
Something in another organization is reported as **not found**, never as
forbidden — so a `NOT_FOUND` for an app you are sure exists is usually the wrong
organization rather than a typo. `platform_whoami` lists the organizations you
belong to and marks the granted one; connect the right one instead of trying the
name again.

## What this connection can and cannot do

It can read the source of the revision that is actually running, change it,
deploy, follow the deploy to a live URL, and manage the applications, databases,
storage buckets, secrets, workflows and checks around it.

It cannot touch your filesystem, run a shell, or reach anything outside the
granted organization. Long work — deploys, database provisioning, workflow runs
— is asynchronous: it answers an operation id immediately, and the result is
read from that operation rather than from the call that started it.

An organization can require a deploy to be approved by a different person. Where
that is on, a deploy is recorded as pending and nothing is live until somebody
else approves it in the Dibbla console. You cannot approve your own.

## Self-hosting

A self-hosted Dibbla has its own MCP URL. Point your client at that URL instead;
nothing else about this package changes. The published package always names the
production endpoint and never ships an internal address.

## Revoking

Revoke in the same place you approved: the connector settings of claude.ai or
Cowork, `/mcp` in Claude Code, the client's own settings in Codex or ChatGPT.
Revoking there ends the grant on that surface, and the connector's own
revocation route ends it on the Dibbla side. https://dibbla.com/terms carries the
published terms and the revocation route; https://dibbla.com/privacy says what is
processed.

## Support

contact@dibbla.com

---

Connector contract version 1.0.0.
