// TEST PURPOSE: large_class.ts
// Observes how the CURRENT chunker handles a TypeScript class_declaration
// that is well over 2000 bytes. Check whether it stays as one oversized chunk
// or is split. Includes preceding interfaces/types (module-level handling),
// generics, access modifiers, a constructor, getters, and async methods.

import { EventEmitter } from "events";

export interface CacheEntry<T> {
  value: T;
  expiresAt: number;
  hits: number;
}

export type CacheStats = {
  size: number;
  hits: number;
  misses: number;
};

type Loader<T> = (key: string) => Promise<T>;

export class TtlCache<T> extends EventEmitter {
  private entries: Map<string, CacheEntry<T>> = new Map();
  private hitCount = 0;
  private missCount = 0;

  constructor(
    private readonly ttlMs: number,
    private readonly maxSize: number = 100,
  ) {
    super();
    if (ttlMs <= 0) {
      throw new RangeError("ttlMs must be positive");
    }
  }

  get size(): number {
    return this.entries.size;
  }

  set(key: string, value: T): void {
    if (this.entries.size >= this.maxSize) {
      this.evictOldest();
    }
    this.entries.set(key, {
      value,
      expiresAt: Date.now() + this.ttlMs,
      hits: 0,
    });
    this.emit("set", key);
  }

  get(key: string): T | undefined {
    const entry = this.entries.get(key);
    if (!entry || entry.expiresAt < Date.now()) {
      this.missCount += 1;
      this.entries.delete(key);
      return undefined;
    }
    entry.hits += 1;
    this.hitCount += 1;
    return entry.value;
  }

  async getOrLoad(key: string, loader: Loader<T>): Promise<T> {
    const cached = this.get(key);
    if (cached !== undefined) {
      return cached;
    }
    const loaded = await loader(key);
    this.set(key, loaded);
    return loaded;
  }

  delete(key: string): boolean {
    const removed = this.entries.delete(key);
    if (removed) {
      this.emit("delete", key);
    }
    return removed;
  }

  purgeExpired(): number {
    const now = Date.now();
    let purged = 0;
    for (const [key, entry] of this.entries) {
      if (entry.expiresAt < now) {
        this.entries.delete(key);
        purged += 1;
      }
    }
    return purged;
  }

  stats(): CacheStats {
    return {
      size: this.entries.size,
      hits: this.hitCount,
      misses: this.missCount,
    };
  }

  has(key: string): boolean {
    const entry = this.entries.get(key);
    return entry !== undefined && entry.expiresAt >= Date.now();
  }

  keys(): string[] {
    return Array.from(this.entries.keys());
  }

  clear(): void {
    this.entries.clear();
    this.hitCount = 0;
    this.missCount = 0;
    this.emit("clear");
  }

  private evictOldest(): void {
    const oldestKey = this.entries.keys().next().value;
    if (oldestKey !== undefined) {
      this.entries.delete(oldestKey);
      this.emit("evict", oldestKey);
    }
  }
}
