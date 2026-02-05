#!/usr/bin/env python3
"""Auto-documentation Generator.

Extracts docstrings from Python files and generates Markdown documentation.
Designed for rapid development workflows where documentation must stay
synchronized with code.

Features:
    - Extracts module, class, and function docstrings using AST
    - Generates API documentation in Markdown format
    - Updates README.md with module summaries
    - Handles missing docstrings gracefully
    - Supports type hints and function signatures
    - Creates table of contents
    - Includes dated documentation headers

Usage:
    # Generate API docs from source directory
    python scripts/auto-docs.py --src-dir src --output-dir docs/api

    # Update README with module summary
    python scripts/auto-docs.py --src-dir src --update-readme

    # Generate docs and update README
    python scripts/auto-docs.py --src-dir src --output-dir docs/api --update-readme  # noqa: E501

Requirements:
    Python 3.11+

Author: AI-accelerated development workflow
Version: 1.0.0
"""

import argparse
import ast
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class DocstringExtractor(ast.NodeVisitor):
    """Extract docstrings from Python AST nodes."""

    def __init__(self) -> None:
        """Initialize the extractor."""
        self.modules: list[dict[str, Any]] = []
        self.classes: list[dict[str, Any]] = []
        self.functions: list[dict[str, Any]] = []
        self.current_class: Optional[str] = None

    def visit_Module(self, node: ast.Module) -> None:  # noqa: N802
        """Visit module node and extract module docstring.

        Args:
            node: AST module node

        """
        docstring = ast.get_docstring(node)
        if docstring:
            self.modules.append({"docstring": docstring, "lineno": 1})
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        """Visit class definition and extract class docstring.

        Args:
            node: AST class definition node

        """
        docstring = ast.get_docstring(node)
        bases = [self._get_name(base) for base in node.bases]

        self.classes.append(
            {
                "name": node.name,
                "docstring": docstring,
                "bases": bases,
                "lineno": node.lineno,
                "methods": [],
            }
        )

        # Track current class for method association
        prev_class = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = prev_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        """Visit function definition and extract function docstring.

        Args:
            node: AST function definition node

        """
        docstring = ast.get_docstring(node)

        # Extract function signature
        args = self._extract_arguments(node.args)
        returns = self._get_name(node.returns) if node.returns else None

        func_info = {
            "name": node.name,
            "docstring": docstring,
            "args": args,
            "returns": returns,
            "lineno": node.lineno,
            "is_async": isinstance(node, ast.AsyncFunctionDef),
        }

        # Associate with class if inside a class
        if self.current_class:
            for cls in self.classes:
                if cls["name"] == self.current_class:
                    cls["methods"].append(func_info)
                    break
        else:
            self.functions.append(func_info)

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
        """Visit async function definition.

        Args:
            node: AST async function definition node

        """
        self.visit_FunctionDef(node)  # type: ignore[arg-type]

    def _get_name(self, node: Optional[ast.expr]) -> str:
        """Get string representation of an AST node.

        Args:
            node: AST expression node

        Returns:
            String representation of the node

        """
        if node is None:
            return ""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Constant):
            return repr(node.value)
        if isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        if isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[{self._get_name(node.slice)}]"
        if isinstance(node, ast.List):
            elements = ", ".join(self._get_name(e) for e in node.elts)
            return f"[{elements}]"
        if isinstance(node, ast.Tuple):
            elements = ", ".join(self._get_name(e) for e in node.elts)
            return f"({elements})"
        return ast.unparse(node)

    def _extract_arguments(self, args: ast.arguments) -> list[dict[str, str]]:
        """Extract function arguments with type hints.

        Args:
            args: AST arguments node

        Returns:
            List of argument dictionaries with name and type

        """
        result = []

        # Regular arguments
        for arg in args.args:
            arg_type = self._get_name(arg.annotation) if arg.annotation else "Any"
            result.append({"name": arg.arg, "type": arg_type})

        # *args
        if args.vararg:
            arg_type = self._get_name(args.vararg.annotation) if args.vararg.annotation else "Any"
            result.append({"name": f"*{args.vararg.arg}", "type": arg_type})

        # **kwargs
        if args.kwarg:
            arg_type = self._get_name(args.kwarg.annotation) if args.kwarg.annotation else "Any"
            result.append({"name": f"**{args.kwarg.arg}", "type": arg_type})

        return result


class DocumentationGenerator:
    """Generate Markdown documentation from extracted docstrings."""

    def __init__(self, src_dir: Path, output_dir: Optional[Path] = None) -> None:
        """Initialize the documentation generator.

        Args:
            src_dir: Source directory containing Python files
            output_dir: Output directory for generated documentation

        """
        self.src_dir = Path(src_dir)
        self.output_dir = Path(output_dir) if output_dir else None
        self.modules_info: list[dict[str, Any]] = []

    def generate(self) -> None:
        """Generate documentation for all Python files in source directory."""
        if not self.src_dir.exists():
            print(f"❌ Error: Source directory '{self.src_dir}' does not exist")
            sys.exit(1)

        print(f"📚 Generating documentation from: {self.src_dir}")

        # Find all Python files
        python_files = list(self.src_dir.rglob("*.py"))
        if not python_files:
            print(f"⚠️  Warning: No Python files found in {self.src_dir}")
            return

        print(f"📝 Found {len(python_files)} Python files")

        # Process each file
        for py_file in python_files:
            self._process_file(py_file)

        # Generate documentation files
        if self.output_dir:
            self._generate_docs()

    def _process_file(self, file_path: Path) -> None:
        """Process a single Python file and extract documentation.

        Args:
            file_path: Path to Python file

        """
        print(f"  ├─ Processing: {file_path.relative_to(self.src_dir)}")

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))
            extractor = DocstringExtractor()
            extractor.visit(tree)

            # Store module information
            module_name = self._get_module_name(file_path)
            self.modules_info.append(
                {
                    "name": module_name,
                    "path": file_path,
                    "modules": extractor.modules,
                    "classes": extractor.classes,
                    "functions": extractor.functions,
                }
            )

            # Warn about missing docstrings
            if not extractor.modules:
                print("    ⚠️  Warning: No module docstring")

        except SyntaxError as e:
            print(f"    ❌ Error parsing file: {e}")
        except Exception as e:
            print(f"    ❌ Error processing file: {e}")

    def _get_module_name(self, file_path: Path) -> str:
        """Convert file path to module name.

        Args:
            file_path: Path to Python file

        Returns:
            Module name (e.g., 'src.utils.helpers')

        """
        rel_path = file_path.relative_to(self.src_dir)
        parts = list(rel_path.parts[:-1]) + [rel_path.stem]
        return ".".join(parts)

    def _generate_docs(self) -> None:
        """Generate Markdown documentation files."""
        if not self.output_dir:
            return

        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📄 Generating documentation in: {self.output_dir}")

        # Generate index file
        self._generate_index()

        # Generate individual module docs
        for module_info in self.modules_info:
            self._generate_module_doc(module_info)

        print("✅ Documentation generated successfully!")

    def _generate_index(self) -> None:
        """Generate index.md with table of contents."""
        assert self.output_dir is not None  # nosec B101
        index_path = self.output_dir / "index.md"

        with open(index_path, "w", encoding="utf-8") as f:
            f.write("# API Documentation\n\n")
            f.write(
                f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"  # noqa: E501
            )
            f.write("## Modules\n\n")

            for module_info in sorted(self.modules_info, key=lambda x: x["name"]):
                module_name = module_info["name"]
                doc_file = f"{module_name.replace('.', '_')}.md"

                # Get module docstring summary
                summary = "No description"
                if module_info["modules"]:
                    docstring = module_info["modules"][0]["docstring"]
                    summary = docstring.split("\n")[0] if docstring else "No description"

                f.write(f"- [{module_name}]({doc_file}) - {summary}\n")

        print(f"  ├─ Generated: {index_path.name}")

    def _generate_module_doc(self, module_info: dict[str, Any]) -> None:
        """Generate documentation for a single module.

        Args:
            module_info: Module information dictionary

        """
        module_name = module_info["name"]
        doc_file = f"{module_name.replace('.', '_')}.md"
        assert self.output_dir is not None  # nosec B101
        doc_path = self.output_dir / doc_file

        with open(doc_path, "w", encoding="utf-8") as f:
            # Header
            f.write(f"# {module_name}\n\n")

            # Module docstring
            if module_info["modules"]:
                docstring = module_info["modules"][0]["docstring"]
                if docstring:
                    f.write(f"{docstring}\n\n")

            # Classes
            if module_info["classes"]:
                f.write("## Classes\n\n")
                for cls in module_info["classes"]:
                    self._write_class_doc(f, cls)

            # Functions
            if module_info["functions"]:
                f.write("## Functions\n\n")
                for func in module_info["functions"]:
                    self._write_function_doc(f, func)

        print(f"  ├─ Generated: {doc_file}")

    def _write_class_doc(self, f: Any, cls: dict[str, Any]) -> None:
        """Write class documentation to file.

        Args:
            f: File object
            cls: Class information dictionary

        """
        f.write(f"### `{cls['name']}`\n\n")

        # Bases
        if cls["bases"]:
            bases = ", ".join(cls["bases"])
            f.write(f"**Bases:** `{bases}`\n\n")

        # Docstring
        if cls["docstring"]:
            f.write(f"{cls['docstring']}\n\n")

        # Methods
        if cls["methods"]:
            f.write("**Methods:**\n\n")
            for method in cls["methods"]:
                self._write_function_doc(f, method, indent="#### ")

    def _write_function_doc(self, f: Any, func: dict[str, Any], indent: str = "### ") -> None:
        """Write function documentation to file.

        Args:
            f: File object
            func: Function information dictionary
            indent: Markdown heading level

        """
        # Signature
        async_prefix = "async " if func.get("is_async") else ""
        args_str = ", ".join(f"{arg['name']}: {arg['type']}" for arg in func.get("args", []))
        returns = func.get("returns", "None")

        f.write(
            f"{indent}`{async_prefix}{func['name']}({args_str}) -> {returns}`\n\n"  # noqa: E501
        )

        # Docstring
        if func["docstring"]:
            f.write(f"{func['docstring']}\n\n")
        else:
            f.write("_No documentation available._\n\n")

    def generate_readme_summary(self) -> str:
        """Generate module summary for README.

        Returns:
            Markdown-formatted summary of modules

        """
        if not self.modules_info:
            return ""

        summary = "## Modules\n\n"
        summary += "| Module | Description |\n"
        summary += "|--------|-------------|\n"

        for module_info in sorted(self.modules_info, key=lambda x: x["name"]):
            module_name = module_info["name"]
            description = "No description"

            if module_info["modules"]:
                docstring = module_info["modules"][0]["docstring"]
                if docstring:
                    description = docstring.split("\n")[0]

            summary += f"| `{module_name}` | {description} |\n"

        return summary


def update_readme(readme_path: Path, summary: str) -> None:
    """Update README.md with module summary.

    Args:
        readme_path: Path to README.md file
        summary: Module summary to insert

    """
    if not readme_path.exists():
        print(f"⚠️  Warning: {readme_path} does not exist, creating new file")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# Project Documentation\n\n")
            f.write(summary)
        print(f"✅ Created {readme_path} with module summary")
        return

    with open(readme_path, encoding="utf-8") as f:
        content = f.read()

    # Look for module section
    if "## Modules" in content:
        # Replace existing module section
        # Use a simpler, non-backtracking pattern to avoid ReDoS
        # Split content into sections by ## headers
        sections = re.split(r"\n(?=##\s)", content)
        found = False

        for i, section in enumerate(sections):
            if section.startswith("## Modules"):
                sections[i] = summary.rstrip() + "\n"
                found = True
                break

        if found:
            content = "\n".join(sections)
            print(f"✅ Updated module section in {readme_path}")
        else:
            # Fallback: append to end
            content += "\n\n" + summary
            print(f"✅ Added module section to {readme_path}")
    else:
        # Append module section
        content += "\n\n" + summary
        print(f"✅ Added module section to {readme_path}")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    """Main entry point for the documentation generator."""
    parser = argparse.ArgumentParser(
        description="Auto-generate documentation from Python docstrings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate API docs
  python scripts/auto-docs.py --src-dir src --output-dir docs/api

  # Update README
  python scripts/auto-docs.py --src-dir src --update-readme

  # Both
  python scripts/auto-docs.py --src-dir src --output-dir docs/api --update-readme  # noqa: E501
        """,
    )

    parser.add_argument(
        "--src-dir",
        type=Path,
        required=True,
        help="Source directory containing Python files",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory for generated documentation",
    )

    parser.add_argument(
        "--update-readme",
        action="store_true",
        help="Update README.md with module summary",
    )

    parser.add_argument(
        "--readme-path",
        type=Path,
        default=Path("README.md"),
        help="Path to README.md file (default: README.md)",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.output_dir and not args.update_readme:
        parser.error("At least one of --output-dir or --update-readme is required")

    # Generate documentation
    generator = DocumentationGenerator(args.src_dir, args.output_dir)
    generator.generate()

    # Update README if requested
    if args.update_readme:
        print("\n📝 Updating README...")
        summary = generator.generate_readme_summary()
        if summary:
            update_readme(args.readme_path, summary)


if __name__ == "__main__":
    main()
