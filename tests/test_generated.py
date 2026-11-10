"""The final publication exemption is smaller than the bundle or build roots."""

import unittest

from helper_support import source
import native


class GeneratedOutputTests(unittest.TestCase):
    def test_exact_native_files_and_controlled_directory_descendants(self):
        expected = (
            "test/Plugins/Bonjour.bundle/Contents/MacOS/Bonjour",
            "test/Plugins/Bonjour.bundle/Contents/Info.plist",
            "test/Plugins/Bonjour.bundle/Contents/Resources/English.lproj/InfoPlist.strings",
            "test/Plugins/Bonjour.bundle/Contents/_CodeSignature/CodeResources",
            "test/Plugins/Bonjour.bundle/Contents/Resources/constants.xlf",
            "test/Plugins/Bonjour.bundle/Contents/Resources/manifest.json",
            "test/Plugins/XCBuildData/build.db",
            "test/Plugins/XCBuildData/build.db-wal",
            "test/Plugins/XCBuildData/build.db-shm",
            "test/Plugins/XCBuildData/0123456789abcdef0123456789abcdef.xcbuilddata/build-request.json",
            "test/Plugins/Bonjour.build/Objects-normal/arm64/main.o",
            "test/Plugins/Bonjour.build/Default/Bonjour.build/build.db",
            "test/Plugins/Bonjour.build/Objects/file.o",
        )
        for path in expected:
            with self.subTest(path=path):
                self.assertTrue(native.generated(path))

    def test_every_resource_source_or_unproven_output_stays_protected(self):
        excluded = (
            "test/Plugins/Bonjour.bundle/Contents/Windows/Bonjour.4DX",
            "test/Plugins/Bonjour.bundle/Contents/Windows64/Bonjour.4DX",
            "test/Plugins/Bonjour.bundle/Contents/MacOS/runtime.dylib",
            "test/Plugins/Bonjour.bundle/Contents/QuickLook/Thumbnail.png",
            "test/Plugins/Default/Bonjour.bundle/Contents/Info.plist",
            "test/Plugins/Default/keep", "test/Plugins/XCBuildData-evil/build.db",
            "test/Plugins/Default/Bonjour.build/Objects/file.o",
            "build/Bonjour.build/Objects/file.o",
            "build/XCBuildData/build.db",
            "test/Plugins/ExplicitPrecompiledModules/evil.cpp",
            "test/Plugins/SwiftExplicitPrecompiledModules/evil.cpp",
            "test/Plugins/EagerLinkingTBDs/Default/evil.cpp",
            "build/unexpected-source.cpp",
            "test/Plugins/XCBuildData/unexpected-source.cpp",
            "test/Plugins/XCBuildData/build.db-evil",
            "test/Plugins/XCBuildData/evil.xcbuilddata/build-request.json",
            "test/Plugins/Bonjour.build-evil/injected.cpp",
            "test/Plugins/Bonjour.bundle/Contents/_CodeSignature-evil/file",
            "test/Plugins/Bonjour.bundle/Contents/Info.plist.backup",
            *map(str, source.SOURCE_PATHS),
        )
        for path in excluded:
            with self.subTest(path=path):
                self.assertFalse(native.generated(path))
