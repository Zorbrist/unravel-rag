from dataclasses import dataclass
from pathlib import Path

from tree_sitter_language_pack import get_parser

# extension -> (tree-sitter language, node types that count as a "definition")
LANGUAGES = {
    ".py": ("python", {"function_definition", "class_definition", "decorated_definition"}),
    ".js": ("javascript", {"function_declaration", "class_declaration", "export_statement"}),
    ".ts": ("typescript", {"function_declaration", "class_declaration", "export_statement"}),
}

MAX_BYTES = 2000


@dataclass
class Chunk:
    file_path: str
    start_line: int  # 1-indexed
    end_line: int
    content: str


def _text(src: bytes, node) -> str:
    return src[node.start_byte:node.end_byte].decode("utf-8", errors="replace")


def _make_chunk(path: Path, src: bytes, nodes: list, prefix: str = "") -> Chunk:
    content = "\n".join(_text(src, n) for n in nodes)
    if prefix:
        content = prefix + "\n" + content
    return Chunk(
        file_path=str(path),
        start_line=nodes[0].start_point[0] + 1,
        end_line=nodes[-1].end_point[0] + 1,
        content=content,
    )


def _split_big_class(path: Path, src: bytes, node) -> list[Chunk]:
    # decorators / export wrappers hide the real class node one level down
    inner = (
        node.child_by_field_name("definition")
        or node.child_by_field_name("declaration")
        or node
    )
    body = inner.child_by_field_name("body")

    # only classes get split; a big function or a weird node stays whole
    if "class" not in inner.type or body is None or not body.named_children:
        return [_make_chunk(path, src, [node])]

    header = src[inner.start_byte:body.start_byte].decode("utf-8", errors="replace").strip()
    return [_make_chunk(path, src, [member], prefix=header) for member in body.named_children]


def chunk_file(path: str | Path) -> list[Chunk]:
    path = Path(path)
    if path.suffix not in LANGUAGES:
        return []

    language, definitions = LANGUAGES[path.suffix]
    src = path.read_bytes()
    root = get_parser(language).parse(src).root_node

    chunks: list[Chunk] = []
    module_level = []  # imports, constants, comments, ...

    for node in root.children:
        if node.type not in definitions:
            module_level.append(node)
        elif node.end_byte - node.start_byte <= MAX_BYTES:
            chunks.append(_make_chunk(path, src, [node]))
        else:
            chunks.extend(_split_big_class(path, src, node))

    if module_level:
        chunks.insert(0, _make_chunk(path, src, module_level))
    return chunks


if __name__ == "__main__":
    import sys

    for c in chunk_file(sys.argv[1]):
        print(f"--- {c.file_path}:{c.start_line}-{c.end_line}")
        print(c.content)