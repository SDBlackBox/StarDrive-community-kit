# Local clone setup — a copy-paste prompt

A single prompt you can hand to a coding agent (or follow yourself) to get a working StarDrive
BlackBox checkout on a new machine: it asks where the repo should go, checks the basics, shows the
directory layout first, and only then clones — with both submodules.

Use it for onboarding, for a fresh machine, or for a second checkout alongside an existing one.
On Linux or macOS use the variant instead: [`clone-setup-prompt-linux.md`](clone-setup-prompt-linux.md).

## Why this exists

`git clone` on this repository is not one step, and the failure modes are quiet:

- **The submodules.** `SDNative/NanoMesh` and `SDNative/ReCpp` are pinned submodule commits. A plain
  clone leaves both empty and the native build fails with errors that point at include files, not at
  the missing checkout. `--recurse-submodules` (or `git submodule update --init --recursive` after)
  is the whole difference.
- **`NanoMesh` comes from a fork on purpose.** `.gitmodules` points at `gkapulis/NanoMesh` on the
  `blackbox-migration` branch, ahead of upstream, because the migration's FBX skin/animation work
  lives there. The odd-looking URL is correct — do not "helpfully" rewrite it to `RedFox20/NanoMesh`.
- **The size.** Around 1.1 GB of working tree plus around 1.3 GB of `.git` before any build output,
  so about 2.5 GB free is the floor. A clone that dies at 90% because the disk filled is a slow way
  to learn that.
- **Windows for everything that compiles.** The game targets Windows 10 1803+ / x64, and the full
  build needs the C++ workload for `SDNative`. The unit tests build without that workload, but they
  still need Windows: their project targets `net8.0-windows` with MonoGame `WindowsDX`, and they copy
  `SDNative.dll` out of `game/`. On Linux, clone with [`clone-setup-prompt-linux.md`](clone-setup-prompt-linux.md)
  instead — same repository, but read/edit/git work only.
- **The branch.** Active development is `main` (Jupiter line). `mars-1.51` is the frozen Mars line;
  a clone that lands somewhere else wastes a review cycle.

The prompt makes the agent say all of this back before it writes anything to disk.

## The prompt

Copy everything between the rules.

```text
You are setting up a local development copy of StarDrive BlackBox for me.
Repository: https://github.com/TeamStarDrive/StarDrive.git  (default branch: main)
Work interactively: ask me first, show me the plan, and only create things after I confirm.

STEP 1 — Interview me (ask all of these in one go, then stop and wait)
1. Where should the repo live? Propose a sensible default for my OS (e.g. C:\Projects\BlackBox
   on Windows, ~/Projects/BlackBox on Linux/macOS) and let me give the exact path.
2. Check out the git submodules now, or leave them empty for later?
3. Should you also verify build prerequisites and run a test build afterwards?

Do not guess my answers, do not create directories, and do not clone until I have confirmed
the path and the options.

STEP 2 — Preflight checks (report only, change nothing)
- git --version; dotnet --list-sdks (the repo needs .NET 8 SDK; no global.json pins a version)
- my OS and CPU arch (the game itself targets Windows 10 1803+ / x64)
- free space at the destination: allow ~2.5 GB minimum (about 1.1 GB working tree plus
  about 1.3 GB of .git, and more once submodules and build output exist)
- whether the target path already exists and is non-empty — if so, stop and ask instead of
  cloning into it or deleting anything

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
Then wait for my explicit go-ahead.

STEP 4 — Clone, then verify
- clone with submodules; if anything is missing, finish with
    git submodule update --init --recursive
- verify and report: git branch --show-current == main; git submodule status with no leading
  '-' or '+'; git status --short is empty; StarDrive.sln and game/Content exist; the commit
  hash you ended up on; the real on-disk size
- print the next steps for me: open StarDrive.sln in Visual Studio 2022 and build Release|x64,
  or run `dotnet build UnitTests/SDUnitTests.csproj` then
  `dotnet test UnitTests/SDUnitTests.csproj --no-build`. Mention that only the tests build
  without the "Desktop development with C++" workload (MSVC v143), which SDNative needs.

RULES
- Never delete, overwrite or push anything; do not modify repo files after cloning.
- If a preflight check or verification fails, stop and tell me — do not work around it,
  skip it, or guess a different repository or branch.
```

## What to change per audience

- **Just want to read the code:** drop step 1.3, and add `--depth 1` to the clone. Shallow history
  is fine for browsing; tell the reader they will need `git fetch --unshallow` before anything that
  walks history (blame across the migration, `git log -S`).
- **CI or a scripted box:** steps 1–3 are the manual path; use the plain
  `git clone --recurse-submodules <url> <dir>` from step 3 and nothing else.
- **Modders rather than developers:** they want `game/` and the itch.io install, not this checkout —
  point them at the README's download section instead.
- **Linux or WSL:** see [`clone-setup-prompt-linux.md`](clone-setup-prompt-linux.md); the only
  difference that matters is that nothing builds there.

## After the clone

The rules for working in the tree are in [`../AGENTS.md`](../../AGENTS.md); the build and test commands
are in [`../README.md`](../../README.md#how-do-i-get-set-up-for-development). If a submodule ever shows
as modified or detached, `git submodule update --init --recursive` puts it back on the pinned commit;
commit the pin bump deliberately rather than leaving a dirty submodule in a PR.
