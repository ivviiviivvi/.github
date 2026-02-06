# Link Check Categorization (2026-01-14)

## Summary

- Total broken links: 870
- Placeholder/template links: 41
- Real regressions: 829
  - Local path missing: 701
  - Auth-required links: 3
  - Malformed URLs: 1
  - External HTTP/URL errors: 124

## Placeholder Examples (Top 25)

- /workspace/.github/ISSUE_TEMPLATE/documentation.yml:
  https://docs.example.com/authentication (URLError: \<urlopen error \[Errno
  -5\] No address associated with hostname>)
- /workspace/.github/ISSUE_TEMPLATE/walkthrough-request.yml:
  https://github.com/organization/repository (HTTPError 404)
- /workspace/docs/AGENTSPHERE_SETUP.md: https://api.example.com (URLError:
  \<urlopen error \[Errno -5\] No address associated with hostname>)
- /workspace/docs/AGENTSPHERE_SETUP.md: https://demo-owner-repo.agentsphere.dev
  (URLError: \<urlopen error \[Errno -2\] Name or service not known>)
- /workspace/docs/AGENTSPHERE_SETUP.md: https://demo-yourrepo.agentsphere.dev
  (URLError: \<urlopen error \[Errno -2\] Name or service not known>)
- /workspace/docs/AGENT_ARCHITECTURE_GUIDE.md: https://... (UnicodeError:
  encoding with 'idna' codec failed (UnicodeError: label empty or too long))
- /workspace/docs/AGENT_REGISTRY.md: https://api.example.com/mcp (URLError:
  \<urlopen error \[Errno -5\] No address associated with hostname>)
- /workspace/docs/AUTONOMOUS_ECOSYSTEM_GUIDE.md:
  https://agentsphere.example.com/demo/your-repo (URLError: \<urlopen error
  \[Errno -5\] No address associated with hostname>)
- /workspace/docs/CHANGELOG.md:
  https://github.com/username/repo/compare/v0.9.0...v1.0.0 (HTTPError 404)
- /workspace/docs/CHANGELOG.md:
  https://github.com/username/repo/compare/v1.0.0...HEAD (HTTPError 404)
- /workspace/docs/CHANGELOG.md:
  https://github.com/username/repo/releases/tag/v0.9.0 (HTTPError 404)
- /workspace/docs/CODE_SERVER_SETUP.md: http://code-server:8080 (URLError:
  \<urlopen error \[Errno -2\] Name or service not known>)
- /workspace/docs/CODE_SERVER_SETUP.md: http://code-server; (URLError: \<urlopen
  error \[Errno -2\] Name or service not known>)
- /workspace/docs/CODE_SERVER_SETUP.md: http://code-server; (URLError: \<urlopen
  error \[Errno -2\] Name or service not known>)
- /workspace/docs/CODE_SERVER_SETUP.md: https://$server_name$request_uri;
  (URLError: \<urlopen error \[Errno -2\] Name or service not known>)
- /workspace/docs/CODE\*SERVER_SETUP.md:
  https://github.com/coder/code-server/releases/download/v$VERSION/code-server*${VERSION}\_amd64.deb
  (HTTPError 404)
- /workspace/docs/COMPLETE_DEPLOYMENT_README.md:
  https://{org}.github.io/.github/apps/my-app (URLError: \<urlopen error \[Errno
  -2\] Name or service not known>)
- /workspace/docs/COMPLETE_DEPLOYMENT_README.md:
  https://{org}.github.io/.github\` (URLError: \<urlopen error \[Errno -2\] Name
  or service not known>)
- /workspace/docs/DEPLOYMENT_ANNOUNCEMENT.md:
  https://github.com/{{ORG_NAME}}/.github/pull/[NUMBER (HTTPError 404)
- /workspace/docs/DRAFT_TO_READY_AUTOMATION_FIX.md: https://github.com/${{
  (HTTPError 404)
- /workspace/docs/MCP_SERVER_SETUP.md: https://your-server.example.com/mcp
  (URLError: \<urlopen error \[Errno -5\] No address associated with hostname>)
- /workspace/docs/WIKI_GUIDE.md: https://blog.example.com (URLError: \<urlopen
  error \[Errno -5\] No address associated with hostname>)
- /workspace/docs/WIKI_GUIDE.md: https://blog.example.com (URLError: \<urlopen
  error \[Errno -5\] No address associated with hostname>)
- /workspace/docs/WIKI_GUIDE.md: https://forum.example.com (URLError: \<urlopen
  error \[Errno -5\] No address associated with hostname>)
- /workspace/docs/WIKI_GUIDE.md: https://forum.example.com (URLError: \<urlopen
  error \[Errno -5\] No address associated with hostname>)
- ... 16 more

## Real Regression Examples (Top 25)

- /workspace/docs/AGENTSPHERE_SETUP.md: https://github.com/4444JPP (HTTPError
  404\)
- /workspace/docs/AGENTSPHERE_SETUP.md: https://github.com/4444JPP (HTTPError
  404\)
- /workspace/docs/AGENT_ARCHITECTURE_GUIDE.md: ../agents/ (missing:
  /workspace/docs/../agents)
- /workspace/docs/AGENT_ARCHITECTURE_GUIDE.md: https://api.dynatrace.com/mcp
  (HTTPError 404)
- /workspace/docs/AGENT_REGISTRY.md: ../../discussions (missing:
  /workspace/docs/../../discussions)
- /workspace/docs/AGENT_REGISTRY.md: ../../issues/new?template=bug_report.md
  (missing: /workspace/docs/../../issues/new?template=bug_report.md)
- /workspace/docs/AGENT_REGISTRY.md:
  ../../issues/new?template=feature_request.md (missing:
  /workspace/docs/../../issues/new?template=feature_request.md)
- /workspace/docs/AGENT_REGISTRY.md: ../AI_RAPID_WORKFLOW.md (missing:
  /workspace/docs/../AI_RAPID_WORKFLOW.md)
- /workspace/docs/AGENT_REGISTRY.md: ../AUTOMATION_MASTER_GUIDE.md (missing:
  /workspace/docs/../AUTOMATION_MASTER_GUIDE.md)
- /workspace/docs/AGENT_REGISTRY.md: ../BEST_PRACTICES.md (missing:
  /workspace/docs/../BEST_PRACTICES.md)
- /workspace/docs/AGENT_REGISTRY.md: ../QUICK_START.md (missing:
  /workspace/docs/../QUICK_START.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/CSharpExpert.agent.md (missing:
  /workspace/docs/../agents/CSharpExpert.agent.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/CSharpExpert.agent.md (missing:
  /workspace/docs/../agents/CSharpExpert.agent.md)
- /workspace/docs/AGENT_REGISTRY.md:
  ../agents/House-Keeping--Pull-Request--Branch--Deep-Cleaner.agent.md (missing:
  /workspace/docs/../agents/House-Keeping--Pull-Request--Branch--Deep-Cleaner.agent.md)
- /workspace/docs/AGENT_REGISTRY.md:
  ../agents/House-Keeping--Pull-Request--Branch--Deep-Cleaner.agent.md (missing:
  /workspace/docs/../agents/House-Keeping--Pull-Request--Branch--Deep-Cleaner.agent.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/WinFormsExpert.agent.md (missing:
  /workspace/docs/../agents/WinFormsExpert.agent.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/WinFormsExpert.agent.md (missing:
  /workspace/docs/../agents/WinFormsExpert.agent.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/adr-generator.agent.md (missing:
  /workspace/docs/../agents/adr-generator.agent.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/adr-generator.agent.md (missing:
  /workspace/docs/../agents/adr-generator.agent.md)
- /workspace/docs/AGENT_REGISTRY.md:
  ../agents/amplitude-experiment-implementation.agent.md (missing:
  /workspace/docs/../agents/amplitude-experiment-implementation.agent.md)
- /workspace/docs/AGENT_REGISTRY.md:
  ../agents/amplitude-experiment-implementation.agent.md (missing:
  /workspace/docs/../agents/amplitude-experiment-implementation.agent.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/arm-migration.agent.md (missing:
  /workspace/docs/../agents/arm-migration.agent.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/arm-migration.agent.md (missing:
  /workspace/docs/../agents/arm-migration.agent.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/completionism-specialist.agent.md
  (missing: /workspace/docs/../agents/completionism-specialist.agent.md)
- /workspace/docs/AGENT_REGISTRY.md: ../agents/completionism-specialist.agent.md
  (missing: /workspace/docs/../agents/completionism-specialist.agent.md)
- ... 804 more

## Notes

- Placeholder classification is based on template token patterns (example.com,
  {org}, \<...>, $TOKEN, etc.).
- Real regressions include missing local paths and non-placeholder external
  URLs.
