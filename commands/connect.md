---
description: Connect this session to Dibbla and confirm who it is acting as
---

<!-- DIBBLA-GENERATED
This file is generated from the Dibbla connector skill source. Do not edit it by
hand: edit the source and regenerate, or your change is gone at the next release.
source: app-hosting-service/mcp-server/skillset/dibbla-platform
source-version: 1.0.0
source-digest: sha256:b712061da97e82b2f5ea7725ed593241665aa788144b87d3895b881f12f78fa9
generator: app-hosting-service/mcp-server/connectorpkg
-->
Connect the Dibbla connector and verify it, then tell the person plainly what
they are connected as.

1. Call `platform_whoami`. If the tool is not there at all, this surface has not
   added the MCP server yet: point at https://mcp.dibbla.com/platform and at
   SETUP.md for this surface's way of adding it, and stop.
2. If the call fails because the connection is not authorized, say that the
   browser will open, and let the surface run its own authorization against
   https://mcp.dibbla.com/platform. Do not ask for a token; there is none.
3. When it answers, report in one short paragraph: the user it acts as, the
   organization it acts in, the role, and whether the grant holds writes or
   reads only.
4. If it holds reads only, say so explicitly and say what it means: every read
   works, and the first write will answer `INSUFFICIENT_SCOPE`. That is the
   "Allow read-only" button on the consent page, not a fault. Offer to reconnect
   with full access.
5. If the person expected a different organization, do not retry with another
   name — a connection acts in one organization and reports everything else as
   not found. `platform_whoami` lists the organizations they belong to; name the
   one they should connect instead.

Then, if the connection is healthy, call `platform_apps` once and tell them how
many applications they have and which of them are not running. That is the proof
the connection works, in something they recognize.
