// TEST PURPOSE: decorated.ts
// Tests TypeScript decorators (requires "experimentalDecorators" to type-check,
// but parses fine with Tree-sitter regardless). Python's decorated_definition
// is supported by your chunker; TypeScript decorators attach differently:
// the decorator may be a child of class_declaration (or of export_statement
// when written before `export`). Check:
//   - non-exported decorated class (@sealed)
//   - exported decorated class (@Component(...) export class)
//   - method decorators inside a class (@logCall)
// Decorators are defined locally so no external packages are needed.

function sealed(constructor: Function): void {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

function Component(options: { selector: string }) {
  return function (constructor: Function): void {
    (constructor as any).selector = options.selector;
  };
}

function logCall(
  target: Object,
  propertyKey: string,
  descriptor: PropertyDescriptor,
): PropertyDescriptor {
  const original = descriptor.value;
  descriptor.value = function (...args: unknown[]) {
    console.log(`Calling ${propertyKey}`, args);
    return original.apply(this, args);
  };
  return descriptor;
}

@sealed
class Greeter {
  constructor(private greeting: string) {}

  @logCall
  greet(name: string): string {
    return `${this.greeting}, ${name}!`;
  }

  shout(name: string): string {
    return this.greet(name).toUpperCase();
  }
}

@Component({ selector: "app-report" })
export class ReportView {
  private lines: string[] = [];

  addLine(line: string): void {
    this.lines.push(line);
  }

  @logCall
  render(): string {
    return this.lines.join("\n");
  }
}
