// TEST PURPOSE: simple.js
// Verifies the basic JavaScript path of the chunker:
//   - Module-level imports and constants are grouped into a module-level chunk.
//   - A small function_declaration stays as one chunk.
//   - A small class_declaration (2 methods) stays as one chunk.
//   - An export_statement wrapping a function stays as one chunk.
// Nothing here is large, so no splitting should be triggered.

import fs from "fs";
import path from "path";

const DEFAULT_ENCODING = "utf-8";
const MAX_RETRIES = 3;

function formatName(first, last) {
  const fullName = `${first} ${last}`.trim();
  return fullName.toUpperCase();
}

class Counter {
  count = 0;

  increment(step = 1) {
    this.count += step;
    return this.count;
  }

  reset() {
    this.count = 0;
  }
}

export function readText(filePath) {
  const resolved = path.resolve(filePath);
  return fs.readFileSync(resolved, DEFAULT_ENCODING);
}
