# Local clone setup on Linux — a copy-paste prompt

The same guided clone as [`clone-setup-prompt.md`](clone-setup-prompt.md), adjusted for Linux: it
asks where the repo should go, checks the filesystem and disk, shows the layout, and clones with both
submodules — while being clear that a Linux checkout is for reading, editing and git work, not for
building the game.

Use the [Windows/main prompt](clone-setup-prompt.md) instead if the machine can build StarDrive.

## What a Linux checkout is for

Every project in the solution targets `net8.0-windows` with `UseWindowsForms`, references
`MonoGame.Framework.WindowsDX`, and the tests copy `SDNative.dll` and `libfbxsdk.dll` out of `game/`.
`StarDrive.sln` also carries the MSVC-only `SDNative`/`SDNativeTests` `.vcxproj` projects, and CI
builds on `windows-2022` with `msbuild`. The test harness additionally needs a real graphics device:
[`ship-strategy-brief.md`](ship-strategy-brief.md#platform-caveat) puts it plainly — it "does not run
on Linux or macOS… that is a port, not a flag."

So on Linux you can:

- clone, branch, rebase, review and open PRs;
- read and search all the C# (editors, `rg`, language servers, source navigation);
- edit content — `game/Content` YAML/XML, `.hull`, `.design` — and docs;
- run the repo's Python tooling (e.g. `docs/codex-entry-leads.py`) and plain shell/git checks.

You cannot: build `StarDrive.exe`, build or run `SDUnitTests`, or launch the game from this checkout.
For those, push to a Windows machine (or a Windows VM) and clone there. To *play* on Linux, install
the itch.io build and run it under Steam Proton — that is the shipped game, not your edits.

## Why the details matter on Linux specifically

- **The submodules are still the trap.** Same pinned commits, same fork: `SDNative/NanoMesh` comes
  from `gkapulis/NanoMesh` on purpose (see `.gitmodules`). Do not "fix" the URL.
- **Size.** ~1.1 GB working tree plus ~1.3 GB `.git`, so ~2.5 GB free.
- **Line endings are already handled.** `.gitattributes` normalizes to LF for source and content but
  forces CRLF for `*.fx` and `*.config`. A checkout therefore shows CRLF in those two kinds of file
  and that is correct — do not renormalize them or add `core.autocrlf=input` fixes.
- **Filesystem matters.** Keep the clone on a native Linux filesystem (ext4/xfs/btrfs/zfs). Cloning
  onto an NTFS/exFAT/SMB mount — including `/mnt/c` under WSL — makes git slow, loses the executable
  bit, and reintroduces Windows' case-insensitive path behavior, so the tree stops matching what CI
  builds.
- **Case.** Windows is case-insensitive; a Linux checkout is not. If a path is referenced with the
  wrong casing it will surface here and not there. Report it; don't rename files to silence it.
- **No git-lfs.** Nothing in `.gitattributes` is LFS-tracked, so `git-lfs` is not needed.

## The prompt

Copy everything between the rules.

```text
You are setting up a local development copy of StarDrive BlackBox for me, on Linux.
Repository: https://github.com/TeamStarDrive/StarDrive.git  (default branch: main)
Work interactively: ask me first, show me the plan, and only create things after I confirm.

STEP 1 — Interview me (ask all of these in one go, then stop and wait)
1. Where should the repo live? Propose ~/Projects/BlackBox as the default and let me give the
   exact path. If I name a path under /mnt/ (WSL Windows drive), an SMB/NFS mount, or a
   non-native filesystem, say why that is a bad place for a git checkout before doing anything.
2. Check out the git submodules now, or leave them empty for later?
3. Should you also verify what this Linux checkout can and cannot do for me afterwards?

Do not guess my answers, do not create directories, and do not clone until I have confirmed
the path and the options.

STEP 2 — Preflight checks (report only, change nothing)
- git --version, my distro and CPU arch
- filesystem type of the destination (`df -T`); warn if it is not native Linux
- free space: allow ~2.5 GB minimum (about 1.1 GB working tree plus about 1.3 GB of .git)
- whether the target path already exists and is non-empty — if so, stop and ask instead of
  cloning into it or deleting anything
- git config --get core.autocrlf (should be unset or false; the repo's .gitattributes does the
  normalization)
- whether dotnet is installed, purely informational: this checkout cannot build the projects
  or run the tests on Linux even with the .NET 8 SDK

STEP 3 — Show me what will be created, before creating it
- the exact command, e.g.
    git clone --recurse-submodules https://github.com/TeamStarDrive/StarDrive.git "<path>"
- a preview tree of the top-level layout, marking which parts arrive as submodules:
  StarDrive.sln, StarDrive.csproj, SDGraphics/, SDUtils/, SDAnalyzers/, Ship_Game/,
  UnitTests/, SDNative/ (contains the two submodules), game/Content, game/Mods,
  docs/, x64Migration/, .github/, .claude/
- note that SDNative has two pinned submodules: SDNative/ReCpp (RedFox20/ReCpp) and
  SDNative/NanoMesh (deliberately the gkapulis fork, pinned ahead of upstream) — do not
  rewrite those URLs
- state plainly what a Linux clone can and cannot do: read/edit/search the C# and content,
  git and PR work — but no build of StarDrive.exe, no unit tests, no game launch; playing on
  Linux means the itch.io build under Proton, and building means a Windows machine
Then wait for my explicit go-ahead.

STEP 4 — Clone, then verify
- clone with submodules; if anything is missing, finish with
    git submodule update --init --recursive
- verify and report: git branch --show-current == main; git submodule status with no leading
  '-' or '+'; git status --short is empty (CRLF in *.fx and *.config is expected and is not a
  change); StarDrive.sln and game/Content exist; the commit hash you ended up on; the real
  on-disk size
- do not run dotnet build, dotnet test, or msbuild; do not add EnableWindowsTargeting or any
  other property to the project files to make them build here

RULES
- Never delete, overwrite or push anything; do not modify repo files after cloning.
- If a preflight check or verification fails, stop and tell me — do not work around it,
  skip it, or guess a different repository or branch.
```

## What to change per audience

- **Reviewing PRs only:** drop step 1.2 and 1.3, and use `--depth 1` — but note that shallow
  history breaks `git log -S` across the migration, so unshallow if you plan to search history.
- **Editors and writers working on content:** they only need `game/` and a text editor, plus the
  writer path in [`ship-content-reference.md`](ship-content-reference.md); `--depth 1` is fine.
- **A build box that happens to be Linux:** there isn't one for this repo. Point them at a Windows
  machine or a Windows VM instead of tuning the prompt.

## After the clone

Working-tree rules are in [`../AGENTS.md`](../../AGENTS.md). If a submodule shows as modified or
detached, `git submodule update --init --recursive` restores the pinned commit; bump a pin
deliberately rather than committing a dirty submodule. Before pushing an edit you could not compile
locally, say so in the PR — CI and the reviewer are the first things to build it on Windows.
