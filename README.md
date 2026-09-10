<!-- DIBBLA-GENERATED
This file is generated from the Dibbla connector skill source. Do not edit it by
hand: edit the source and regenerate, or your change is gone at the next release.
source: app-hosting-service/mcp-server/skillset/dibbla-platform
source-version: 1.0.0
source-digest: sha256:596c9d3da59ef8cb0e763b373c3b2e1399ecb6586cffe64baa0c7791079c8b08
generator: app-hosting-service/mcp-server/connectorpkg
-->

# Dibbla platform connector

This repository is the public distribution package for the Dibbla connector: the
manifests, the skill and the prompts that let Claude Code, Claude Cowork,
claude.ai, Codex and ChatGPT connect to https://mcp.dibbla.com/platform.

**Every file here is generated. Do not edit anything by hand.** The source is the
connector skill inside Dibbla's own service repository
(app-hosting-service/mcp-server/skillset/dibbla-platform), and the whole
content of this repository is produced from it by a generator at release. A
hand-edit survives exactly until the next release, and then it is gone without a
trace. To change something, change the source.

## What is in here

    .claude-plugin/plugin.json   the Claude Code / Cowork plugin manifest
    .codex-plugin/plugin.json    the OpenAI plugin manifest, with starter prompts
    .mcp.json                    the remote connector definition
    skills/dibbla-platform/      the connector skill: how to work with Dibbla over MCP
    skills/dibbla-setup/         connecting, consent, scopes, self-hosting, revoking
    commands/                    /dibbla:connect and /dibbla:deploy
    SETUP.md                     the same setup document, for people and reviewers
    SOURCE.json                  what this was generated from, and a digest per file

## What is deliberately not in here

No code. No script. No install hook. No token, key, header or credential of any
kind — the endpoint is OAuth-protected and every client performs its own
authorization. No internal hostname and no non-production address. This
repository is manifests, skill text and prompts, and nothing that can run.

## Provenance

Every file names the source, the source version and the source digest it was
generated from: in an HTML comment for markdown, in the `metadata` object for the
JSON manifests. SOURCE.json lists a digest for each generated file plus one
digest for the package as a whole. The generator is deterministic — the same
source produces the same bytes — so two releases that claim the same source
version and disagree about a digest are a bug, and a visible one.

## Installing

See [SETUP.md](SETUP.md).

## Support

contact@dibbla.com · https://dibbla.com/terms · https://dibbla.com/privacy

---

Connector contract version 1.0.0.
