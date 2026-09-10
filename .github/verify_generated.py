#!/usr/bin/env python3
"""Verify that this repository is exactly what the generator produced.

WHY THIS EXISTS. dibbla-platform-connector is distribution-only: every file in
it is generated from the Dibbla connector skill source by
app-hosting-service/mcp-server/connectorpkg, and Anthropic's directory mirrors
this repository automatically. So a hand-edit here is not a local mistake — it
is a change that reaches users and is silently erased at the next release, with
the two directories disagreeing in between. This script is the gate that makes
that hand-edit a failed build instead of a surprise.

WHAT IT CAN AND CANNOT SEE. The generator lives in a private repository and
cannot run here, so this checks the repository against the provenance manifest
the generator wrote beside it: every file's digest and size, the package digest
over all of them, that nothing extra has appeared, and that every file names the
same source digest. That catches an edit. It cannot, alone, catch an edit whose
author also rewrote SOURCE.json to match; the authoritative check for that is
`just connector-package-check <checkout>` in app-hosting-service, which a
release runs before it pushes.

Only .git and .github are outside the generator's output — this directory is the
gate, not the payload.
"""

import hashlib
import json
import os
import sys

MANIFEST = "SOURCE.json"
EXEMPT_DIRS = {".git", ".github"}
PROVENANCE_MARKER = "DIBBLA-GENERATED"


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def repo_files(root: str) -> set[str]:
    found = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if os.path.relpath(os.path.join(dirpath, d), root) not in EXEMPT_DIRS
        ]
        for name in filenames:
            found.add(os.path.relpath(os.path.join(dirpath, name), root))
    return found


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    problems: list[str] = []

    try:
        with open(os.path.join(root, MANIFEST), "rb") as fh:
            manifest = json.load(fh)
    except (OSError, ValueError) as err:
        print(f"{MANIFEST} is missing or not readable JSON: {err}")
        print("This repository is generated; without its manifest nothing here can be trusted.")
        return 1

    source_digest = manifest.get("sourceDigest", "")
    entries = manifest.get("files", [])
    if not entries:
        print(f"{MANIFEST} lists no files")
        return 1

    listed = set()
    package = hashlib.sha256()
    for entry in entries:
        path = entry["path"]
        listed.add(path)
        full = os.path.join(root, path)
        try:
            with open(full, "rb") as fh:
                content = fh.read()
        except OSError:
            problems.append(f"{path}: listed in {MANIFEST} but missing from the repository")
            continue

        got = digest(content)
        package.update(f"{path}\x00{got}\n".encode())
        if got != entry["digest"]:
            problems.append(
                f"{path}: does not match the generator's output "
                f"(manifest {entry['digest']}, file {got}). "
                "Nothing here is edited by hand: change the skill source in "
                "app-hosting-service and regenerate."
            )
            continue
        if len(content) != entry["bytes"]:
            problems.append(f"{path}: is {len(content)} bytes, the manifest says {entry['bytes']}")

        text = content.decode("utf-8", errors="replace")
        if path.endswith(".md"):
            if PROVENANCE_MARKER not in text:
                problems.append(f"{path}: carries no {PROVENANCE_MARKER} provenance comment")
            elif source_digest and source_digest not in text:
                problems.append(
                    f"{path}: names a different source digest than {MANIFEST}; "
                    "this tree is a mix of two releases"
                )
        elif path.endswith(".json") and source_digest and source_digest not in text:
            problems.append(
                f"{path}: does not carry {MANIFEST}'s source digest in its metadata; "
                "this tree is a mix of two releases"
            )

    got_package = "sha256:" + package.hexdigest()
    if got_package != manifest.get("packageDigest"):
        problems.append(
            f"packageDigest: the files add up to {got_package}, "
            f"{MANIFEST} says {manifest.get('packageDigest')}"
        )

    for extra in sorted(repo_files(root) - listed - {MANIFEST}):
        problems.append(
            f"{extra}: is in the repository but not in {MANIFEST}. "
            "The generator writes the whole content and prunes the rest, so this "
            "file would disappear at the next release."
        )

    if problems:
        print("This repository does not match the generator's output:\n")
        for p in problems:
            print(f"  - {p}")
        print(
            "\nEvery file here is generated. Edit "
            "app-hosting-service/mcp-server/skillset/dibbla-platform, run "
            "`just connector-release <checkout of this repo>`, and push the result."
        )
        return 1

    print(f"{len(entries)} generated files match {MANIFEST}")
    print(f"  source        {manifest.get('source')} @ {manifest.get('sourceVersion')}")
    print(f"  sourceDigest  {source_digest}")
    print(f"  packageDigest {got_package}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
