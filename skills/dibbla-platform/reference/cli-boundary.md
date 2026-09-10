<!-- DIBBLA-GENERATED
This file is generated from the Dibbla connector skill source. Do not edit it by
hand: edit the source and regenerate, or your change is gone at the next release.
source: app-hosting-service/mcp-server/skillset/dibbla-platform
source-version: 1.0.0
source-digest: sha256:596c9d3da59ef8cb0e763b373c3b2e1399ecb6586cffe64baa0c7791079c8b08
generator: app-hosting-service/mcp-server/connectorpkg
-->

# When the Dibbla CLI is the better tool, and why

Dibbla also ships a command-line program, with its own skill aimed at a surface
that has a shell. This file exists so that you can tell the two apart.

**The default is this surface.** Parity is the platform's rule: what a signed-in
human can do with the CLI, a grant with the right scope can do over the
connector. Reaching for a shell for something the connector already does costs
an install, a login, a keychain prompt and a second identity, and gets the same
result. Publishing, patching, reading source, logs, deployments, checks,
secrets, databases, buckets, workflows and every irreversible change are all
here.

There is a short list of work that is genuinely local, and it is local for the
same reason each time: **one end of it is the caller's own machine**, and
nothing remote can reach that.

| The work | Why it cannot be done from here |
|---|---|
| Packing a source directory into an upload archive | It reads the caller's filesystem to build the archive. Sending the tree inline is the connector's answer, up to 200 files and 2 MB |
| Cloning an application's git repository to disk | It creates a working copy using the caller's own git binary and credentials. Reading the same source is exposed here, as `platform_files` |
| Scaffolding a project from a template onto disk | It writes files into a directory and reads what is already there to avoid clobbering it. Nothing remote can write a file on somebody's machine |
| Running a task pipeline | It executes commands on the caller's machine |
| Dumping a database to a file | It streams through the caller's own PostgreSQL client into a file on their disk. Both ends are local |
| Bulk-loading secrets from a `.env` file | It walks a file on the caller's disk. Setting the same secrets one at a time is exposed here |
| Validating a manifest with no network | The offline walk reads a local file. The server-side equivalent — the deploy path's real parse, resolution and quota rules — is `platform_deployment_preflight`, and it is the stricter of the two |
| Printing a secret value, a bucket key or a database connection string | It hands credential material to a terminal. Keeping credential material out of a model's context is a platform invariant, so this half of each family has no remote form even though listing and setting do |
| Signing in, switching CLI context or organization, updating the binary, writing an MCP client's config | All local state on that machine. Remotely, the connector URL selects the installation and the OAuth grant selects the user and organization — a model-chosen context or organization switch is refused by design |
| Pointing a local AI assistant at Dibbla's AI gateway | It prints environment settings for the caller's own process and diagnoses their network path. A remote answer would describe our machine instead |
| An operator's orphan-resource sweep | It is gated by a platform-operator marker that lives outside the grant model entirely. No scope carries it, and inventing one would put operator authority inside a customer's consent screen |

## What to do when you land on one of these

Say which of the two it is and why, in one sentence, and let the person decide.
"This is more than 2 MB of source, so it needs the Dibbla CLI's deploy path,
which packs the directory locally — I cannot read your filesystem from here" is
useful. Handing over a command line for them to paste is not: you cannot see
whether the program is installed, which context or organization it is signed in
to, or what it would do on their machine, and a command that is wrong about any
of those is worse than no command. The CLI has its own skill, and it is the
thing that knows the commands.

If the surface you are running in *does* have a shell and the CLI is already
present and signed in, that skill takes over from here. This one stops at the
boundary.

## The one that looks like an exception

Reading an application's source. There is a local way to do it — a working copy
on disk — and it is the right answer when somebody wants to work in an editor
over many files for an hour. But for finding a thing, reading a few files and
changing them, `platform_files` reads the deployed revision directly with
nothing downloaded, and `platform_deployment_start` with `mode=patch` writes it
back. That is the loop the connector was built for, and it needs no filesystem
at all.
