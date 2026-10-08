// TEST PURPOSE: simple.ts
// Verifies the basic TypeScript path of the chunker:
//   - Imports and constants go into the module-level chunk.
//   - interface_declaration / type_alias_declaration are TypeScript-only nodes
//     NOT in your listed definition types, so see whether they land in the
//     module-level chunk or are handled separately.
//   - A small function_declaration and small class_declaration stay whole.
//   - Exported function and exported class (export_statement) stay whole.

import { readFileSync } from "fs";
import * as path from "path";

const DEFAULT_ROLE = "viewer";

interface User {
  id: number;
  name: string;
  role?: string;
}

type UserMap = Record<number, User>;

function formatUser(user: User): string {
  return `${user.name} (${user.role ?? DEFAULT_ROLE})`;
}

class UserStore {
  private users: UserMap = {};

  add(user: User): void {
    this.users[user.id] = user;
  }

  get(id: number): User | undefined {
    return this.users[id];
  }
}

export function loadUsers(filePath: string): User[] {
  const raw = readFileSync(path.resolve(filePath), "utf-8");
  return JSON.parse(raw) as User[];
}

export class UserService {
  constructor(private store: UserStore) {}

  register(name: string): User {
    const user: User = { id: Date.now(), name };
    this.store.add(user);
    return user;
  }
}
