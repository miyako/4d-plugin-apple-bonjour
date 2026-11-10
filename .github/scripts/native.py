"""Rebuild only original Default outputs; preserve all other selected inputs."""

import argparse
import os
from pathlib import Path
import re
import shutil
import stat


PRODUCT = "Bonjour"
BASE = Path("test/Plugins")
BUNDLE = BASE / (PRODUCT + ".bundle")
FILES = tuple(BUNDLE / relative for relative in (
    f"Contents/MacOS/{PRODUCT}", "Contents/Info.plist",
    "Contents/Resources/English.lproj/InfoPlist.strings",
    "Contents/Resources/constants.xlf", "Contents/Resources/manifest.json",
    "Contents/_CodeSignature/CodeResources",
))
PRESERVED = tuple(BUNDLE / relative for relative in (
    "Contents/Windows/Bonjour.4DX", "Contents/Windows64/Bonjour.4DX",
    "Contents/QuickLook/Thumbnail.png",
))
XCODE_DATA = BASE / "XCBuildData"
DIRECTORIES = (BASE / "Bonjour.build",)
EMPTY_DIRECTORIES = tuple(BASE / name for name in (
    "SwiftExplicitPrecompiledModules", "ExplicitPrecompiledModules",
    "EagerLinkingTBDs/Default", "Default",
))


def generated(path):
    return (path in set(map(str, FILES))
            or bool(re.fullmatch(
                r"test/Plugins/XCBuildData/(?:build\.db(?:-wal|-shm)?|"
                r"[0-9a-f]{32}\.xcbuilddata/.+)", path))
            or any(path.startswith(str(directory) + "/")
                   for directory in DIRECTORIES))


def node(path):
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def validate_paths(paths):
    root = Path.cwd().resolve()
    for path in map(Path, paths):
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Output escapes checkout: {path}")
        for parent in (*reversed(path.parents), path):
            if parent == Path("."):
                continue
            info = node(parent)
            if info is not None and stat.S_ISLNK(info.st_mode):
                raise ValueError(f"Refusing symlink output: {parent}")
            if parent != path and info is not None and not stat.S_ISDIR(info.st_mode):
                raise ValueError(f"Output ancestor is not a directory: {parent}")
        if not path.resolve().is_relative_to(root):
            raise ValueError(f"Output escapes checkout: {path}")
        info = node(path)
        if info is None:
            continue
        pending = [path]
        while pending:
            current = pending.pop()
            info = current.lstat()
            if current.name == ".git":
                raise ValueError(f"Refusing nested Git marker: {current}")
            if stat.S_ISLNK(info.st_mode):
                raise ValueError(f"Refusing symlink output: {current}")
            if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
                raise ValueError(f"Refusing nonregular output: {current}")
            if stat.S_ISDIR(info.st_mode):
                if not info.st_mode & 0o444 or not info.st_mode & 0o111:
                    raise ValueError(f"Unreadable output directory: {current}")
                pending.extend(current.iterdir())
            else:
                if not info.st_mode & 0o444:
                    raise ValueError(f"Unreadable output file: {current}")
                with current.open("rb"):
                    pass


def prepare():
    validate_paths((*FILES, *DIRECTORIES, XCODE_DATA))
    for path in FILES:
        info = node(path)
        if info is not None and not stat.S_ISREG(info.st_mode):
            raise ValueError(f"Cleanup leaf must be a regular file: {path}")
    for path in (*DIRECTORIES, XCODE_DATA):
        info = node(path)
        if info is not None and not stat.S_ISDIR(info.st_mode):
            raise ValueError(f"Cleanup root must be a directory: {path}")
    # A selected/indexed input under an intermediate root must never be deleted.
    import repository
    tracked = repository.run("git", "ls-files", "-z", "--", *map(str, DIRECTORIES))
    selected = repository.run("git", "ls-tree", "-r", "--name-only", "-z", "HEAD",
                              "--", *map(str, DIRECTORIES))
    if tracked or selected:
        raise ValueError("Tracked input inside native intermediate cleanup root")
    for path in (*FILES, *DIRECTORIES):
        if node(path) is None:
            continue
        directories = [path.parent]
        if path.is_dir():
            directories += [path, *(child for child in path.rglob("*") if child.is_dir())]
        for directory in directories:
            mode = directory.stat().st_mode
            if not mode & 0o222 or not mode & 0o111 \
                    or not os.access(directory, os.W_OK | os.X_OK):
                raise ValueError(f"Inaccessible cleanup directory: {directory}")
    for path in FILES:
        path.unlink(missing_ok=True)
    for path in DIRECTORIES:
        if path.exists():
            shutil.rmtree(path)


def require_file(path):
    validate_paths((path,))
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"Missing or empty native output: {path}")


def verify_resources():
    for name in ("manifest.json", "constants.xlf"):
        copied = BUNDLE / "Contents/Resources" / name
        require_file(copied)
        if copied.read_bytes() != Path(name).read_bytes():
            raise ValueError(f"Copied resource differs from source: {copied}")


def verify_unsigned():
    for path in (*FILES[:-1], *PRESERVED):
        require_file(path)
    verify_resources()


def verify_final():
    verify_unsigned()
    require_file(FILES[-1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=(
        "clean-macos", "verify-resources", "verify-unsigned", "verify-final",
    ))
    phase = parser.parse_args().phase
    {"clean-macos": prepare, "verify-resources": verify_resources,
     "verify-unsigned": verify_unsigned, "verify-final": verify_final}[phase]()
