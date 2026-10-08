// TEST PURPOSE: large_class.js
// Observes how the CURRENT chunker handles a JavaScript class_declaration
// that is well over 2000 bytes. The Python chunker splits large classes into
// members; JavaScript splitting is NOT assumed to exist. Check whether the
// class stays as a single oversized chunk, or is split in some way.
// The class contains a constructor, a static method, a getter, a private
// method, async methods, and regular methods.

import { EventEmitter } from "events";

const DEFAULT_CONCURRENCY = 2;

class TaskScheduler extends EventEmitter {
  constructor(options = {}) {
    super();
    this.concurrency = options.concurrency ?? DEFAULT_CONCURRENCY;
    this.queue = [];
    this.running = 0;
    this.completed = [];
    this.failed = [];
    this.nextId = 1;
  }

  static fromTasks(tasks, options = {}) {
    const scheduler = new TaskScheduler(options);
    for (const task of tasks) {
      scheduler.addTask(task.name, task.run, task.priority);
    }
    return scheduler;
  }

  get pendingCount() {
    return this.queue.length;
  }

  addTask(name, run, priority = 0) {
    if (typeof run !== "function") {
      throw new TypeError(`Task "${name}" must provide a run function`);
    }
    const task = { id: this.nextId++, name, run, priority };
    this.queue.push(task);
    this.queue.sort((a, b) => b.priority - a.priority);
    this.emit("added", task);
    return task.id;
  }

  removeTask(id) {
    const index = this.queue.findIndex((task) => task.id === id);
    if (index === -1) {
      return false;
    }
    const [removed] = this.queue.splice(index, 1);
    this.emit("removed", removed);
    return true;
  }

  async runAll() {
    const workers = [];
    for (let i = 0; i < this.concurrency; i++) {
      workers.push(this.#worker());
    }
    await Promise.all(workers);
    this.emit("drained", this.summary());
    return this.summary();
  }

  async #worker() {
    while (this.queue.length > 0) {
      const task = this.queue.shift();
      this.running += 1;
      try {
        const result = await task.run();
        this.completed.push({ id: task.id, name: task.name, result });
        this.emit("completed", task);
      } catch (error) {
        this.failed.push({ id: task.id, name: task.name, error });
        this.emit("failed", task, error);
      } finally {
        this.running -= 1;
      }
    }
  }

  summary() {
    return {
      pending: this.queue.length,
      running: this.running,
      completed: this.completed.length,
      failed: this.failed.length,
    };
  }

  retryFailed() {
    const toRetry = this.failed.splice(0, this.failed.length);
    for (const item of toRetry) {
      const task = { id: item.id, name: item.name, run: async () => item.result, priority: 0 };
      this.queue.push(task);
      this.emit("retry", task);
    }
    return toRetry.length;
  }

  toJSON() {
    return {
      concurrency: this.concurrency,
      queue: this.queue.map((task) => ({ id: task.id, name: task.name })),
      summary: this.summary(),
    };
  }

  clearHistory() {
    this.completed = [];
    this.failed = [];
  }
}

export default TaskScheduler;
