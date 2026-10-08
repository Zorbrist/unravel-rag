// TEST PURPOSE: exports.js
// Exercises the JavaScript export_statement handling with several export forms:
//   - export function / export class / export const
//   - export default
//   - export { ... } list
// Also includes NON-exported function, class, and constants so you can see
// how exported and non-exported definitions are chunked relative to each other
// and how they are separated from module-level code.

import { createHash } from "crypto";

const SALT = "demo-salt";
const internalCache = new Map();

export const VERSION = "1.0.0";

export const DEFAULT_OPTIONS = {
  verbose: false,
  timeoutMs: 5000,
};

export function hashValue(value) {
  return createHash("sha256").update(SALT + value).digest("hex");
}

export class Registry {
  constructor() {
    this.entries = new Map();
  }

  register(key, value) {
    this.entries.set(key, value);
  }

  lookup(key) {
    return this.entries.get(key);
  }
}

function normalizeKey(key) {
  return String(key).trim().toLowerCase();
}

class InternalHelper {
  describe() {
    return `cache size: ${internalCache.size}`;
  }
}

const helper = new InternalHelper();

export { normalizeKey, helper };

export default function main() {
  const registry = new Registry();
  registry.register(normalizeKey(" Hello "), hashValue("world"));
  return registry;
}
