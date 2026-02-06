"""Unit tests for automation/scripts/auto_docs.py

Focus: AST-based docstring extraction and documentation generation.
"""

import ast
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation" / "scripts"))

# Import with hyphenated filename workaround
import importlib.util

spec = importlib.util.spec_from_file_location(
    "auto_docs",
    Path(__file__).parent.parent.parent / "src" / "automation" / "scripts" / "auto_docs.py",
)
auto_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auto_docs)

DocstringExtractor = auto_docs.DocstringExtractor
DocumentationGenerator = auto_docs.DocumentationGenerator
update_readme = auto_docs.update_readme


@pytest.mark.unit
class TestDocstringExtractor:
    """Test AST-based docstring extraction."""

    def test_extracts_module_docstring(self):
        """Test extracts module-level docstring."""
        code = '"""This is the module docstring."""\n\ndef foo(): pass'
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        assert len(extractor.modules) == 1
        assert "module docstring" in extractor.modules[0]["docstring"]

    def test_extracts_function_docstring(self):
        """Test extracts function docstrings."""
        code = '''
def hello():
    """Say hello."""
    pass

def goodbye():
    """Say goodbye."""
    pass
'''
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        assert len(extractor.functions) == 2
        func_names = [f["name"] for f in extractor.functions]
        assert "hello" in func_names
        assert "goodbye" in func_names

    def test_extracts_class_docstring(self):
        """Test extracts class docstrings."""
        code = '''
class MyClass:
    """This is MyClass."""
    pass
'''
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        assert len(extractor.classes) == 1
        assert extractor.classes[0]["name"] == "MyClass"
        assert "MyClass" in extractor.classes[0]["docstring"]

    def test_extracts_method_docstrings(self):
        """Test extracts method docstrings within classes."""
        code = '''
class MyClass:
    """Class docstring."""

    def method(self):
        """Method docstring."""
        pass
'''
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        assert len(extractor.classes) == 1
        assert len(extractor.classes[0]["methods"]) == 1
        assert extractor.classes[0]["methods"][0]["name"] == "method"

    def test_extracts_function_arguments(self):
        """Test extracts function arguments with types."""
        code = '''
def greet(name: str, count: int = 1) -> str:
    """Greet someone."""
    pass
'''
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        func = extractor.functions[0]
        assert len(func["args"]) == 2
        assert func["args"][0]["name"] == "name"
        assert func["args"][0]["type"] == "str"
        assert func["returns"] == "str"

    def test_extracts_async_function(self):
        """Test extracts async function docstrings."""
        code = '''
async def fetch_data():
    """Fetch data asynchronously."""
    pass
'''
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        assert len(extractor.functions) == 1
        assert extractor.functions[0]["is_async"] is True

    def test_extracts_class_bases(self):
        """Test extracts class base classes."""
        code = '''
class Child(Parent, Mixin):
    """Child class."""
    pass
'''
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        bases = extractor.classes[0]["bases"]
        assert "Parent" in bases
        assert "Mixin" in bases

    def test_handles_missing_docstring(self):
        """Test handles functions without docstrings."""
        code = """
def no_doc():
    pass
"""
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        assert len(extractor.functions) == 1
        assert extractor.functions[0]["docstring"] is None

    def test_extracts_varargs(self):
        """Test extracts *args parameter."""
        code = '''
def variadic(*args: int):
    """Variadic function."""
    pass
'''
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        args = extractor.functions[0]["args"]
        vararg = [a for a in args if a["name"].startswith("*")]
        assert len(vararg) == 1
        assert vararg[0]["name"] == "*args"

    def test_extracts_kwargs(self):
        """Test extracts **kwargs parameter."""
        code = '''
def keyword(**kwargs: str):
    """Keyword function."""
    pass
'''
        tree = ast.parse(code)
        extractor = DocstringExtractor()
        extractor.visit(tree)

        args = extractor.functions[0]["args"]
        kwarg = [a for a in args if a["name"].startswith("**")]
        assert len(kwarg) == 1
        assert kwarg[0]["name"] == "**kwargs"


@pytest.mark.unit
class TestDocumentationGenerator:
    """Test documentation generation."""

    @pytest.fixture
    def mock_src_dir(self, tmp_path):
        """Create mock source directory with Python files."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        return src_dir

    @pytest.fixture
    def mock_output_dir(self, tmp_path):
        """Create mock output directory."""
        output_dir = tmp_path / "docs"
        return output_dir

    def test_generates_index_file(self, mock_src_dir, mock_output_dir):
        """Test generates index.md file."""
        py_file = mock_src_dir / "module.py"
        py_file.write_text('"""Module docstring."""\n\ndef func(): pass')

        generator = DocumentationGenerator(mock_src_dir, mock_output_dir)
        generator.generate()

        index_file = mock_output_dir / "index.md"
        assert index_file.exists()
        assert "API Documentation" in index_file.read_text()

    def test_generates_module_docs(self, mock_src_dir, mock_output_dir):
        """Test generates documentation for each module."""
        py_file = mock_src_dir / "mymodule.py"
        py_file.write_text('"""My module."""\n\ndef func(): pass')

        generator = DocumentationGenerator(mock_src_dir, mock_output_dir)
        generator.generate()

        # Should have module doc file
        files = list(mock_output_dir.glob("*.md"))
        assert len(files) >= 2  # index.md + module doc

    def test_handles_missing_src_dir(self, tmp_path, capsys):
        """Test exits when source directory doesn't exist."""
        generator = DocumentationGenerator(tmp_path / "nonexistent", tmp_path / "docs")

        with pytest.raises(SystemExit):
            generator.generate()

        captured = capsys.readouterr()
        assert "does not exist" in captured.out

    def test_handles_empty_directory(self, mock_src_dir, mock_output_dir, capsys):
        """Test handles empty source directory."""
        generator = DocumentationGenerator(mock_src_dir, mock_output_dir)
        generator.generate()

        captured = capsys.readouterr()
        assert "No Python files" in captured.out

    def test_warns_about_missing_docstrings(self, mock_src_dir, mock_output_dir, capsys):
        """Test warns about files without module docstrings."""
        py_file = mock_src_dir / "nodoc.py"
        py_file.write_text("def func(): pass")

        generator = DocumentationGenerator(mock_src_dir, mock_output_dir)
        generator.generate()

        captured = capsys.readouterr()
        assert "Warning" in captured.out or "No module docstring" in captured.out

    def test_processes_nested_directories(self, mock_src_dir, mock_output_dir):
        """Test processes Python files in nested directories."""
        nested = mock_src_dir / "subpackage"
        nested.mkdir()

        py_file = nested / "nested.py"
        py_file.write_text('"""Nested module."""\n')

        generator = DocumentationGenerator(mock_src_dir, mock_output_dir)
        generator.generate()

        assert len(generator.modules_info) >= 1

    def test_generates_readme_summary(self, mock_src_dir):
        """Test generates README summary markdown."""
        py_file = mock_src_dir / "module.py"
        py_file.write_text('"""Module description here."""\n')

        generator = DocumentationGenerator(mock_src_dir)
        generator.generate()

        summary = generator.generate_readme_summary()

        assert "## Modules" in summary
        assert "Module description here" in summary

    def test_handles_syntax_errors(self, mock_src_dir, mock_output_dir, capsys):
        """Test handles Python syntax errors gracefully."""
        py_file = mock_src_dir / "broken.py"
        py_file.write_text("def broken(\n")  # Syntax error

        generator = DocumentationGenerator(mock_src_dir, mock_output_dir)
        generator.generate()

        captured = capsys.readouterr()
        assert "Error parsing" in captured.out


@pytest.mark.unit
class TestUpdateReadme:
    """Test README update functionality."""

    def test_creates_readme_if_missing(self, tmp_path, capsys):
        """Test creates README.md if it doesn't exist."""
        readme_path = tmp_path / "README.md"
        summary = "## Modules\n| Module | Description |\n"

        update_readme(readme_path, summary)

        assert readme_path.exists()
        content = readme_path.read_text()
        assert "## Modules" in content

        captured = capsys.readouterr()
        assert "Created" in captured.out

    def test_updates_existing_module_section(self, tmp_path, capsys):
        """Test updates existing ## Modules section."""
        readme_path = tmp_path / "README.md"
        readme_path.write_text("# My Project\n\n## Modules\n\nOld content\n\n## Other\n")

        new_summary = "## Modules\n\n| Module | Description |\n|---|---|\n"

        update_readme(readme_path, new_summary)

        content = readme_path.read_text()
        assert "| Module | Description |" in content
        assert "Old content" not in content

    def test_appends_section_if_not_present(self, tmp_path, capsys):
        """Test appends Modules section if not present."""
        readme_path = tmp_path / "README.md"
        readme_path.write_text("# My Project\n\nSome content.\n")

        summary = "## Modules\n\n| Module | Description |\n"

        update_readme(readme_path, summary)

        content = readme_path.read_text()
        assert "## Modules" in content
        assert "Some content" in content

        captured = capsys.readouterr()
        assert "Added" in captured.out

    def test_preserves_other_sections(self, tmp_path):
        """Test preserves other sections when updating."""
        readme_path = tmp_path / "README.md"
        readme_path.write_text(
            "# Project\n\n## Installation\n\nInstall steps.\n\n## Modules\n\nOld.\n\n## License\n\nMIT\n"
        )

        summary = "## Modules\n\n| New | Table |\n"

        update_readme(readme_path, summary)

        content = readme_path.read_text()
        assert "## Installation" in content
        assert "Install steps" in content
        assert "## License" in content
        assert "MIT" in content


@pytest.mark.unit
class TestGetName:
    """Test AST node name extraction."""

    def test_handles_name_node(self):
        """Test handles ast.Name nodes."""
        extractor = DocstringExtractor()
        node = ast.Name(id="MyType")

        result = extractor._get_name(node)

        assert result == "MyType"

    def test_handles_constant_node(self):
        """Test handles ast.Constant nodes."""
        extractor = DocstringExtractor()
        node = ast.Constant(value="literal")

        result = extractor._get_name(node)

        assert result == "'literal'"

    def test_handles_attribute_node(self):
        """Test handles ast.Attribute nodes."""
        extractor = DocstringExtractor()
        # Create typing.Optional
        node = ast.Attribute(value=ast.Name(id="typing"), attr="Optional")

        result = extractor._get_name(node)

        assert result == "typing.Optional"

    def test_handles_none(self):
        """Test handles None input."""
        extractor = DocstringExtractor()

        result = extractor._get_name(None)

        assert result == ""


@pytest.mark.unit
class TestExtractArguments:
    """Test argument extraction from function signatures."""

    def test_extracts_regular_args(self):
        """Test extracts regular positional arguments."""
        extractor = DocstringExtractor()
        args = ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg="x", annotation=ast.Name(id="int")),
                ast.arg(arg="y", annotation=ast.Name(id="str")),
            ],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        )

        result = extractor._extract_arguments(args)

        assert len(result) == 2
        assert result[0]["name"] == "x"
        assert result[0]["type"] == "int"

    def test_extracts_without_annotations(self):
        """Test extracts arguments without type annotations."""
        extractor = DocstringExtractor()
        args = ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="x", annotation=None)],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        )

        result = extractor._extract_arguments(args)

        assert result[0]["type"] == "Any"


@pytest.mark.unit
class TestGetNameAdvanced:
    """Test advanced AST node name extraction."""

    def test_handles_subscript_node(self):
        """Test handles ast.Subscript nodes like List[int]."""
        extractor = DocstringExtractor()
        # Create List[int]
        node = ast.Subscript(
            value=ast.Name(id="List"),
            slice=ast.Name(id="int"),
        )

        result = extractor._get_name(node)

        assert result == "List[int]"

    def test_handles_list_node(self):
        """Test handles ast.List nodes."""
        extractor = DocstringExtractor()
        node = ast.List(elts=[ast.Name(id="int"), ast.Name(id="str")])

        result = extractor._get_name(node)

        assert result == "[int, str]"

    def test_handles_tuple_node(self):
        """Test handles ast.Tuple nodes."""
        extractor = DocstringExtractor()
        node = ast.Tuple(elts=[ast.Name(id="int"), ast.Name(id="str")])

        result = extractor._get_name(node)

        assert result == "(int, str)"

    def test_handles_complex_type_annotation(self):
        """Test handles complex type like Optional[List[str]]."""
        extractor = DocstringExtractor()
        # Create Optional[List[str]]
        node = ast.Subscript(
            value=ast.Name(id="Optional"),
            slice=ast.Subscript(value=ast.Name(id="List"), slice=ast.Name(id="str")),
        )

        result = extractor._get_name(node)

        assert result == "Optional[List[str]]"


@pytest.mark.unit
class TestDocumentationGeneratorAdvanced:
    """Test advanced documentation generation."""

    @pytest.fixture
    def mock_src_dir(self, tmp_path):
        """Create mock source directory with Python files."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        return src_dir

    @pytest.fixture
    def mock_output_dir(self, tmp_path):
        """Create mock output directory."""
        output_dir = tmp_path / "docs"
        return output_dir

    def test_write_class_doc_with_bases(self, mock_src_dir, mock_output_dir):
        """Test writes class documentation with bases."""
        py_file = mock_src_dir / "module.py"
        py_file.write_text(
            '''"""Module."""

class Child(Parent, Mixin):
    """Child class inheriting from Parent and Mixin."""
    pass
'''
        )

        generator = DocumentationGenerator(mock_src_dir, mock_output_dir)
        generator.generate()

        # Check the generated documentation
        module_doc = mock_output_dir / "module.md"
        content = module_doc.read_text()
        assert "Bases" in content or "Parent" in content

    def test_write_function_doc_with_async(self, mock_src_dir, mock_output_dir):
        """Test writes async function documentation."""
        py_file = mock_src_dir / "module.py"
        py_file.write_text(
            '''"""Module."""

async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    pass
'''
        )

        generator = DocumentationGenerator(mock_src_dir, mock_output_dir)
        generator.generate()

        # Check the generated documentation
        module_doc = mock_output_dir / "module.md"
        content = module_doc.read_text()
        assert "async" in content

    def test_write_function_doc_without_docstring(self, mock_src_dir, mock_output_dir):
        """Test writes function documentation without docstring."""
        py_file = mock_src_dir / "module.py"
        py_file.write_text(
            '''"""Module."""

def no_doc():
    pass
'''
        )

        generator = DocumentationGenerator(mock_src_dir, mock_output_dir)
        generator.generate()

        # Check the generated documentation
        module_doc = mock_output_dir / "module.md"
        content = module_doc.read_text()
        assert "No documentation available" in content

    def test_generate_readme_summary_empty(self, mock_src_dir):
        """Test generate_readme_summary with no modules."""
        generator = DocumentationGenerator(mock_src_dir)
        # Don't call generate, so modules_info is empty

        summary = generator.generate_readme_summary()

        assert summary == ""

    def test_generate_with_output_dir_none(self, mock_src_dir):
        """Test generate creates modules_info but no output files."""
        py_file = mock_src_dir / "module.py"
        py_file.write_text('"""Module docstring."""\n')

        generator = DocumentationGenerator(mock_src_dir, None)
        generator.generate()

        assert len(generator.modules_info) >= 1

    def test_process_file_with_exception(self, mock_src_dir, capsys):
        """Test _process_file handles general exceptions."""
        py_file = mock_src_dir / "module.py"
        py_file.write_text('"""Module."""\n')

        generator = DocumentationGenerator(mock_src_dir)

        # Mock ast.parse to raise an exception
        with patch("ast.parse", side_effect=ValueError("Test error")):
            generator._process_file(py_file)

        captured = capsys.readouterr()
        assert "Error processing file" in captured.out

    def test_get_module_name_nested(self, mock_src_dir):
        """Test _get_module_name with nested directories."""
        nested = mock_src_dir / "subpackage" / "nested"
        nested.mkdir(parents=True)
        py_file = nested / "module.py"
        py_file.write_text('"""Nested module."""\n')

        generator = DocumentationGenerator(mock_src_dir)
        result = generator._get_module_name(py_file)

        assert "subpackage" in result
        assert "nested" in result
        assert "module" in result


@pytest.mark.unit
class TestMainFunction:
    """Test main function."""

    def test_main_no_args(self, monkeypatch, capsys):
        """Test main with no arguments."""
        monkeypatch.setattr(sys, "argv", ["auto_docs.py"])

        with pytest.raises(SystemExit) as exc:
            auto_docs.main()

        assert exc.value.code == 2

    def test_main_missing_required_args(self, monkeypatch, capsys):
        """Test main without output-dir or update-readme."""
        monkeypatch.setattr(sys, "argv", ["auto_docs.py", "--src-dir", "/some/path"])

        with pytest.raises(SystemExit) as exc:
            auto_docs.main()

        assert exc.value.code == 2

    def test_main_with_output_dir(self, tmp_path, monkeypatch, capsys):
        """Test main with output-dir argument."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        py_file = src_dir / "module.py"
        py_file.write_text('"""Module docstring."""\n')

        output_dir = tmp_path / "docs"

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "auto_docs.py",
                "--src-dir",
                str(src_dir),
                "--output-dir",
                str(output_dir),
            ],
        )

        auto_docs.main()

        assert output_dir.exists()

    def test_main_with_update_readme(self, tmp_path, monkeypatch, capsys):
        """Test main with update-readme argument."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        py_file = src_dir / "module.py"
        py_file.write_text('"""Module docstring."""\n')

        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Project\n\n")

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "auto_docs.py",
                "--src-dir",
                str(src_dir),
                "--update-readme",
                "--readme-path",
                str(readme_path),
            ],
        )

        auto_docs.main()

        content = readme_path.read_text()
        assert "## Modules" in content

    def test_main_with_both_args(self, tmp_path, monkeypatch, capsys):
        """Test main with both output-dir and update-readme."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        py_file = src_dir / "module.py"
        py_file.write_text('"""Module docstring."""\n')

        output_dir = tmp_path / "docs"
        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Project\n\n")

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "auto_docs.py",
                "--src-dir",
                str(src_dir),
                "--output-dir",
                str(output_dir),
                "--update-readme",
                "--readme-path",
                str(readme_path),
            ],
        )

        auto_docs.main()

        assert output_dir.exists()
        content = readme_path.read_text()
        assert "## Modules" in content


@pytest.mark.unit
class TestUpdateReadmeAdvanced:
    """Test advanced README update functionality."""

    def test_updates_found_but_not_matching(self, tmp_path, capsys):
        """Test updates when section found but pattern doesn't match."""
        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Project\n\n## Modules\n\n## Other Section\n")

        summary = "## Modules\n\n| New | Content |\n"

        update_readme(readme_path, summary)

        content = readme_path.read_text()
        assert "| New | Content |" in content
        assert "## Other Section" in content

    def test_fallback_append_when_section_not_found(self, tmp_path, capsys):
        """Test fallback to append when no ## Modules found."""
        readme_path = tmp_path / "README.md"
        readme_path.write_text("# Project\n\nSome content here.\n")

        summary = "## Modules\n\n| Module | Description |\n"

        update_readme(readme_path, summary)

        content = readme_path.read_text()
        assert "## Modules" in content
        assert "Some content here" in content

        captured = capsys.readouterr()
        assert "Added" in captured.out
