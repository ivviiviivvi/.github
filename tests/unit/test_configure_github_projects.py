#!/usr/bin/env python3
"""Tests for configure-github-projects.py.

Tests GitHub Projects V2 configuration including GraphQL operations,
field creation, and CLI behavior.
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import the module with hyphens in name
spec = importlib.util.spec_from_file_location(
    "configure_github_projects",
    Path(__file__).parent.parent.parent / "src/automation/scripts/utils/configure-github-projects.py",
)
configure_github_projects = importlib.util.module_from_spec(spec)
sys.modules["configure_github_projects"] = configure_github_projects
spec.loader.exec_module(configure_github_projects)


@pytest.mark.unit
class TestColors:
    """Test ANSI color code constants."""

    def test_color_codes_defined(self):
        """Test all color codes are defined."""
        assert configure_github_projects.Colors.BLUE == "\033[0;34m"
        assert configure_github_projects.Colors.GREEN == "\033[0;32m"
        assert configure_github_projects.Colors.YELLOW == "\033[1;33m"
        assert configure_github_projects.Colors.RED == "\033[0;31m"
        assert configure_github_projects.Colors.NC == "\033[0m"


@pytest.mark.unit
class TestLogFunctions:
    """Test logging helper functions."""

    def test_log_info(self, capsys):
        """Test log_info outputs blue info symbol."""
        configure_github_projects.log_info("Test message")
        captured = capsys.readouterr()
        assert "ℹ" in captured.out
        assert "Test message" in captured.out

    def test_log_success(self, capsys):
        """Test log_success outputs green checkmark."""
        configure_github_projects.log_success("Success message")
        captured = capsys.readouterr()
        assert "✓" in captured.out
        assert "Success message" in captured.out

    def test_log_warning(self, capsys):
        """Test log_warning outputs yellow warning symbol."""
        configure_github_projects.log_warning("Warning message")
        captured = capsys.readouterr()
        assert "⚠" in captured.out
        assert "Warning message" in captured.out

    def test_log_error(self, capsys):
        """Test log_error outputs red X symbol."""
        configure_github_projects.log_error("Error message")
        captured = capsys.readouterr()
        assert "✗" in captured.out
        assert "Error message" in captured.out


@pytest.mark.unit
class TestGitHubProjectsManagerInit:
    """Test GitHubProjectsManager initialization."""

    def test_init_sets_properties(self):
        """Test initialization sets all properties correctly."""
        manager = configure_github_projects.GitHubProjectsManager(
            token="test-token",  # allow-secret
            org="test-org",
        )

        assert manager.token == "test-token"  # allow-secret
        assert manager.org == "test-org"
        assert manager.api_url == "https://api.github.com/graphql"
        assert manager.timeout == 10
        assert "Bearer test-token" in manager.headers["Authorization"]  # allow-secret
        assert manager.headers["Content-Type"] == "application/json"


@pytest.mark.unit
class TestExecuteQuery:
    """Test GraphQL query execution."""

    @pytest.fixture
    def manager(self):
        """Create manager fixture."""
        return configure_github_projects.GitHubProjectsManager(
            token="test-token",  # allow-secret
            org="test-org",
        )

    @patch("requests.post")
    def test_execute_query_success(self, mock_post, manager):
        """Test successful query execution."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"organization": {"id": "org-123"}}}
        mock_post.return_value = mock_response

        result = manager.execute_query("query { test }")

        assert result["data"]["organization"]["id"] == "org-123"
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_execute_query_with_variables(self, mock_post, manager):
        """Test query execution with variables."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"result": "success"}}
        mock_post.return_value = mock_response

        manager.execute_query("query { test }", {"var": "value"})

        call_args = mock_post.call_args
        payload = call_args.kwargs["json"]
        assert payload["variables"] == {"var": "value"}

    @patch("requests.post")
    def test_execute_query_http_error(self, mock_post, manager):
        """Test query execution handles HTTP errors."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            manager.execute_query("query { test }")

        assert "Query failed: 500" in str(exc_info.value)

    @patch("requests.post")
    def test_execute_query_graphql_errors(self, mock_post, manager):
        """Test query execution handles GraphQL errors."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"errors": [{"message": "Field not found"}]}
        mock_post.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            manager.execute_query("query { test }")

        assert "GraphQL errors" in str(exc_info.value)
        assert "Field not found" in str(exc_info.value)


@pytest.mark.unit
class TestGetOrgId:
    """Test organization ID retrieval."""

    @pytest.fixture
    def manager(self):
        """Create manager fixture."""
        return configure_github_projects.GitHubProjectsManager(
            token="test-token",  # allow-secret
            org="test-org",
        )

    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "execute_query",
    )
    def test_get_org_id_success(self, mock_execute, manager):
        """Test successful org ID retrieval."""
        mock_execute.return_value = {"data": {"organization": {"id": "MDEyOk9yZ2FuaXphdGlvbjEyMzQ="}}}

        result = manager.get_org_id()

        assert result == "MDEyOk9yZ2FuaXphdGlvbjEyMzQ="
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args
        assert "login" in str(call_args)


@pytest.mark.unit
class TestCreateProject:
    """Test project creation."""

    @pytest.fixture
    def manager(self):
        """Create manager fixture."""
        return configure_github_projects.GitHubProjectsManager(
            token="test-token",  # allow-secret
            org="test-org",
        )

    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "update_project_description",
    )
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "execute_query",
    )
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "get_org_id",
    )
    def test_create_project_success(self, mock_get_org, mock_execute, mock_update_desc, manager):
        """Test successful project creation."""
        mock_get_org.return_value = "org-id-123"
        mock_execute.return_value = {
            "data": {
                "createProjectV2": {
                    "projectV2": {
                        "id": "proj-123",
                        "number": 1,
                        "title": "Test Project",
                        "url": "https://github.com/orgs/test/projects/1",
                    }
                }
            }
        }

        result = manager.create_project("Test Project", "Test description")

        assert result["id"] == "proj-123"
        assert result["number"] == 1
        assert result["title"] == "Test Project"
        mock_update_desc.assert_called_once_with("proj-123", "Test description")


@pytest.mark.unit
class TestUpdateProjectDescription:
    """Test project description update."""

    @pytest.fixture
    def manager(self):
        """Create manager fixture."""
        return configure_github_projects.GitHubProjectsManager(
            token="test-token",  # allow-secret
            org="test-org",
        )

    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "execute_query",
    )
    def test_update_project_description_success(self, mock_execute, manager):
        """Test successful description update."""
        mock_execute.return_value = {"data": {"updateProjectV2": {"projectV2": {"id": "proj-123"}}}}

        manager.update_project_description("proj-123", "New description")

        mock_execute.assert_called_once()
        call_args = mock_execute.call_args
        assert call_args.args[1]["projectId"] == "proj-123"
        assert call_args.args[1]["readme"] == "New description"


@pytest.mark.unit
class TestCreateSingleSelectField:
    """Test single select field creation."""

    @pytest.fixture
    def manager(self):
        """Create manager fixture."""
        return configure_github_projects.GitHubProjectsManager(
            token="test-token",  # allow-secret
            org="test-org",
        )

    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "execute_query",
    )
    def test_create_single_select_field_success(self, mock_execute, manager):
        """Test successful single select field creation."""
        mock_execute.return_value = {
            "data": {
                "createProjectV2Field": {
                    "projectV2Field": {
                        "id": "field-123",
                        "name": "Status",
                    }
                }
            }
        }

        options = [
            {"name": "Todo", "color": "GRAY"},
            {"name": "Done", "color": "GREEN"},
        ]

        result = manager.create_single_select_field("proj-123", "Status", options)

        assert result == "field-123"
        call_args = mock_execute.call_args
        input_data = call_args.args[1]["input"]
        assert input_data["dataType"] == "SINGLE_SELECT"
        assert input_data["name"] == "Status"
        # Check that options have empty description added
        assert input_data["singleSelectOptions"][0]["description"] == ""


@pytest.mark.unit
class TestCreateTextField:
    """Test text field creation."""

    @pytest.fixture
    def manager(self):
        """Create manager fixture."""
        return configure_github_projects.GitHubProjectsManager(
            token="test-token",  # allow-secret
            org="test-org",
        )

    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "execute_query",
    )
    def test_create_text_field_success(self, mock_execute, manager):
        """Test successful text field creation."""
        mock_execute.return_value = {
            "data": {
                "createProjectV2Field": {
                    "projectV2Field": {
                        "id": "field-456",
                        "name": "Notes",
                    }
                }
            }
        }

        result = manager.create_text_field("proj-123", "Notes")

        assert result == "field-456"
        call_args = mock_execute.call_args
        input_data = call_args.args[1]["input"]
        assert input_data["dataType"] == "TEXT"
        assert input_data["name"] == "Notes"


@pytest.mark.unit
class TestCreateNumberField:
    """Test number field creation."""

    @pytest.fixture
    def manager(self):
        """Create manager fixture."""
        return configure_github_projects.GitHubProjectsManager(
            token="test-token",  # allow-secret
            org="test-org",
        )

    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "execute_query",
    )
    def test_create_number_field_success(self, mock_execute, manager):
        """Test successful number field creation."""
        mock_execute.return_value = {
            "data": {
                "createProjectV2Field": {
                    "projectV2Field": {
                        "id": "field-789",
                        "name": "Score",
                    }
                }
            }
        }

        result = manager.create_number_field("proj-123", "Score")

        assert result == "field-789"
        call_args = mock_execute.call_args
        input_data = call_args.args[1]["input"]
        assert input_data["dataType"] == "NUMBER"
        assert input_data["name"] == "Score"


@pytest.mark.unit
class TestCreateDateField:
    """Test date field creation."""

    @pytest.fixture
    def manager(self):
        """Create manager fixture."""
        return configure_github_projects.GitHubProjectsManager(
            token="test-token",  # allow-secret
            org="test-org",
        )

    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "execute_query",
    )
    def test_create_date_field_success(self, mock_execute, manager):
        """Test successful date field creation."""
        mock_execute.return_value = {
            "data": {
                "createProjectV2Field": {
                    "projectV2Field": {
                        "id": "field-date",
                        "name": "Due Date",
                    }
                }
            }
        }

        result = manager.create_date_field("proj-123", "Due Date")

        assert result == "field-date"
        call_args = mock_execute.call_args
        input_data = call_args.args[1]["input"]
        assert input_data["dataType"] == "DATE"
        assert input_data["name"] == "Due Date"


@pytest.mark.unit
class TestProjectsConfig:
    """Test PROJECTS_CONFIG constant."""

    def test_all_projects_have_required_keys(self):
        """Test all project configs have required keys."""
        for project_key, config in configure_github_projects.PROJECTS_CONFIG.items():
            assert "title" in config, f"{project_key} missing title"
            assert "description" in config, f"{project_key} missing description"
            assert "fields" in config, f"{project_key} missing fields"
            assert isinstance(config["fields"], dict)

    def test_ai_framework_project_config(self):
        """Test ai-framework project configuration."""
        config = configure_github_projects.PROJECTS_CONFIG["ai-framework"]
        assert "AI Framework" in config["title"]
        assert "Status" in config["fields"]
        assert "Priority" in config["fields"]
        assert "Type" in config["fields"]

    def test_documentation_project_config(self):
        """Test documentation project configuration."""
        config = configure_github_projects.PROJECTS_CONFIG["documentation"]
        assert "Documentation" in config["title"]
        assert "Document Type" in config["fields"]

    def test_workflow_automation_project_config(self):
        """Test workflow-automation project configuration."""
        config = configure_github_projects.PROJECTS_CONFIG["workflow-automation"]
        assert "Workflow" in config["title"]
        assert "Trigger" in config["fields"]

    def test_security_compliance_project_config(self):
        """Test security-compliance project configuration."""
        config = configure_github_projects.PROJECTS_CONFIG["security-compliance"]
        assert "Security" in config["title"]
        assert "Severity" in config["fields"]

    def test_infrastructure_devops_project_config(self):
        """Test infrastructure-devops project configuration."""
        config = configure_github_projects.PROJECTS_CONFIG["infrastructure-devops"]
        assert "Infrastructure" in config["title"]
        assert "Environment" in config["fields"]

    def test_community_support_project_config(self):
        """Test community-support project configuration."""
        config = configure_github_projects.PROJECTS_CONFIG["community-support"]
        assert "Community" in config["title"]
        assert "Engagement Type" in config["fields"]

    def test_product_roadmap_project_config(self):
        """Test product-roadmap project configuration."""
        config = configure_github_projects.PROJECTS_CONFIG["product-roadmap"]
        assert "Roadmap" in config["title"]
        assert "Timeline" in config["fields"]

    def test_field_types_are_valid(self):
        """Test all field types are valid."""
        valid_types = {"single_select", "text", "number", "date"}

        for project_key, config in configure_github_projects.PROJECTS_CONFIG.items():
            for field_name, field_config in config["fields"].items():
                field_type = field_config["type"]
                assert field_type in valid_types, f"Invalid field type '{field_type}' in {project_key}.{field_name}"

    def test_single_select_fields_have_options(self):
        """Test single select fields have options list."""
        for project_key, config in configure_github_projects.PROJECTS_CONFIG.items():
            for field_name, field_config in config["fields"].items():
                if field_config["type"] == "single_select":
                    assert "options" in field_config, f"Missing options in {project_key}.{field_name}"
                    assert len(field_config["options"]) > 0


@pytest.mark.unit
class TestMainFunction:
    """Test main function CLI behavior."""

    @patch.dict("os.environ", {"GH_TOKEN": ""}, clear=True)
    def test_main_no_token_exits(self, capsys):
        """Test main exits with error when no token."""
        with patch(
            "sys.argv",
            ["configure-github-projects.py", "--org", "test-org"],
        ):
            with pytest.raises(SystemExit) as exc_info:
                configure_github_projects.main()

            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "GH_TOKEN" in captured.out

    @patch.dict("os.environ", {"GH_TOKEN": "test-token"})  # allow-secret
    def test_main_dry_run(self, capsys):
        """Test main in dry run mode."""
        with patch(
            "sys.argv",
            [
                "configure-github-projects.py",
                "--org",
                "test-org",
                "--projects",
                "ai-framework",
                "--dry-run",
            ],
        ):
            configure_github_projects.main()

        captured = capsys.readouterr()
        assert "DRY RUN" in captured.out
        assert "Would create" in captured.out

    @patch.dict("os.environ", {"GH_TOKEN": "test-token"})  # allow-secret
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_date_field",
    )
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_number_field",
    )
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_text_field",
    )
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_single_select_field",
    )
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_project",
    )
    @patch("time.sleep")
    def test_main_creates_project_with_fields(
        self,
        mock_sleep,
        mock_create_project,
        mock_create_single_select,
        mock_create_text,
        mock_create_number,
        mock_create_date,
        capsys,
    ):
        """Test main creates project with all field types."""
        mock_create_project.return_value = {
            "id": "proj-123",
            "number": 1,
            "title": "Test Project",
            "url": "https://github.com/orgs/test/projects/1",
        }
        mock_create_single_select.return_value = "field-1"
        mock_create_text.return_value = "field-2"
        mock_create_number.return_value = "field-3"
        mock_create_date.return_value = "field-4"

        with patch(
            "sys.argv",
            [
                "configure-github-projects.py",
                "--org",
                "test-org",
                "--projects",
                "documentation",  # Has all field types
            ],
        ):
            configure_github_projects.main()

        mock_create_project.assert_called_once()
        assert mock_create_single_select.call_count > 0
        assert mock_create_date.call_count > 0
        # documentation project has Word Count (number) field
        assert mock_create_number.call_count > 0

    @patch.dict("os.environ", {"GH_TOKEN": "test-token"})  # allow-secret
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_project",
    )
    def test_main_handles_project_creation_error(self, mock_create_project, capsys):
        """Test main handles project creation errors gracefully."""
        mock_create_project.side_effect = Exception("API Error")

        with patch(
            "sys.argv",
            [
                "configure-github-projects.py",
                "--org",
                "test-org",
                "--projects",
                "ai-framework",
            ],
        ):
            configure_github_projects.main()

        captured = capsys.readouterr()
        assert "Failed to create project" in captured.out
        assert "API Error" in captured.out

    @patch.dict("os.environ", {"GH_TOKEN": "test-token"})  # allow-secret
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_single_select_field",
    )
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_project",
    )
    @patch("time.sleep")
    def test_main_handles_field_creation_error(self, mock_sleep, mock_create_project, mock_create_field, capsys):
        """Test main handles field creation errors gracefully."""
        mock_create_project.return_value = {
            "id": "proj-123",
            "number": 1,
            "title": "Test",
            "url": "https://example.com",
        }
        mock_create_field.side_effect = Exception("Field error")

        with patch(
            "sys.argv",
            [
                "configure-github-projects.py",
                "--org",
                "test-org",
                "--projects",
                "ai-framework",
            ],
        ):
            configure_github_projects.main()

        captured = capsys.readouterr()
        assert "Failed to create field" in captured.out

    @patch.dict("os.environ", {"GH_TOKEN": "test-token"})  # allow-secret
    def test_main_all_projects_default(self):
        """Test main uses all projects when none specified."""
        with patch(
            "sys.argv",
            ["configure-github-projects.py", "--org", "test-org", "--dry-run"],
        ):
            configure_github_projects.main()


@pytest.mark.unit
class TestMainFinalOutput:
    """Test main function final output messages."""

    @patch.dict("os.environ", {"GH_TOKEN": "test-token"})  # allow-secret
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_single_select_field",
    )
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_text_field",
    )
    @patch.object(
        configure_github_projects.GitHubProjectsManager,
        "create_project",
    )
    @patch("time.sleep")
    def test_main_outputs_next_steps(
        self,
        mock_sleep,
        mock_create_project,
        mock_create_text,
        mock_create_single_select,
        capsys,
    ):
        """Test main outputs next steps after successful creation."""
        mock_create_project.return_value = {
            "id": "proj-123",
            "number": 1,
            "title": "Test",
            "url": "https://example.com",
        }
        mock_create_single_select.return_value = "field-1"
        mock_create_text.return_value = "field-2"

        with patch(
            "sys.argv",
            [
                "configure-github-projects.py",
                "--org",
                "test-org",
                "--projects",
                "community-support",  # Has text and single_select fields
            ],
        ):
            configure_github_projects.main()

        captured = capsys.readouterr()
        assert "All projects configured" in captured.out
        assert "Next steps" in captured.out
        assert "project views" in captured.out
        assert "automation rules" in captured.out
