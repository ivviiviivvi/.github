#!/usr/bin/env node
/**
 * Version Sync Script
 * Synchronizes version across all version files in the repository
 *
 * Supports: package.json, VERSION, pyproject.toml, Cargo.toml, go.mod
 */

const fs = require("fs");
const path = require("path");

const VERSION_FILES = {
  "package.json": {
    read: (content) => JSON.parse(content).version,
    write: (content, version) => {
      const data = JSON.parse(content);
      data.version = version;
      return JSON.stringify(data, null, 2) + "\n";
    },
  },
  VERSION: {
    read: (content) => content.trim(),
    write: (content, version) => version + "\n",
  },
  "pyproject.toml": {
    read: (content) => {
      const match = content.match(/version\s*=\s*"([^"]+)"/);
      return match ? match[1] : null;
    },
    write: (content, version) => {
      return content.replace(/version\s*=\s*"[^"]+"/, `version = "${version}"`);
    },
  },
  "Cargo.toml": {
    read: (content) => {
      const match = content.match(/version\s*=\s*"([^"]+)"/);
      return match ? match[1] : null;
    },
    write: (content, version) => {
      return content.replace(/version\s*=\s*"[^"]+"/, `version = "${version}"`);
    },
  },
  ".config/schema-org/repository.jsonld": {
    read: (content) => JSON.parse(content).version,
    write: (content, version) => {
      const data = JSON.parse(content);
      data.version = version;
      data.dateModified = new Date().toISOString().split("T")[0];
      return JSON.stringify(data, null, 2) + "\n";
    },
  },
  ".config/schema-org/ai-framework.jsonld": {
    read: (content) => JSON.parse(content).version,
    write: (content, version) => {
      const data = JSON.parse(content);
      data.version = version;
      return JSON.stringify(data, null, 2) + "\n";
    },
  },
  ".config/schema-org/documentation.jsonld": {
    read: (content) => JSON.parse(content).version,
    write: (content, version) => {
      const data = JSON.parse(content);
      data.version = version;
      data.dateModified = new Date().toISOString().split("T")[0];
      return JSON.stringify(data, null, 2) + "\n";
    },
  },
};

function getSourceVersion() {
  // Read version from package.json (source of truth)
  const packageJsonPath = path.join(process.cwd(), "package.json");
  if (fs.existsSync(packageJsonPath)) {
    const content = fs.readFileSync(packageJsonPath, "utf8");
    return VERSION_FILES["package.json"].read(content);
  }

  // Fallback to VERSION file
  const versionPath = path.join(process.cwd(), "VERSION");
  if (fs.existsSync(versionPath)) {
    const content = fs.readFileSync(versionPath, "utf8");
    return VERSION_FILES["VERSION"].read(content);
  }

  throw new Error("No version source found (package.json or VERSION)");
}

function syncVersions() {
  console.log("🔄 Syncing versions across all version files...\n");

  const sourceVersion = getSourceVersion();
  console.log(`📦 Source version: ${sourceVersion}\n`);

  let syncedCount = 0;
  let skippedCount = 0;

  for (const [filename, handlers] of Object.entries(VERSION_FILES)) {
    const filePath = path.join(process.cwd(), filename);

    if (!fs.existsSync(filePath)) {
      console.log(`⏭️  Skipped: ${filename} (file not found)`);
      skippedCount++;
      continue;
    }

    try {
      const content = fs.readFileSync(filePath, "utf8");
      const currentVersion = handlers.read(content);

      if (currentVersion === sourceVersion) {
        console.log(`✅ Up-to-date: ${filename} (${currentVersion})`);
        continue;
      }

      const newContent = handlers.write(content, sourceVersion);
      fs.writeFileSync(filePath, newContent, "utf8");

      console.log(
        `✏️  Updated: ${filename} (${currentVersion} → ${sourceVersion})`,
      );
      syncedCount++;
    } catch (error) {
      console.error(`❌ Error syncing ${filename}: ${error.message}`);
    }
  }

  console.log(`\n📊 Summary:`);
  console.log(`   - Updated: ${syncedCount} files`);
  console.log(`   - Skipped: ${skippedCount} files`);
  console.log(`   - Version: ${sourceVersion}`);
  console.log("\n✨ Version sync complete!");
}

// Run the sync
try {
  syncVersions();
} catch (error) {
  console.error(`\n❌ Error: ${error.message}`);
  process.exit(1);
}
