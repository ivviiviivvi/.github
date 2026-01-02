## 2024-02-14 - [Command Injection Mitigation in Workflows]
**Vulnerability:** Found a Command Injection vulnerability in `.github/workflows/reusable-api-retry.yml` where `eval` was used to execute a dynamically constructed `curl` command. User input (like `API_ENDPOINT`) could potentially break out of the string and execute arbitrary commands.
**Learning:** `eval` is extremely dangerous when handling user input in shell scripts. String concatenation for command construction is brittle and prone to injection if quotes are not handled perfectly (which is hard).
**Prevention:** Use Bash arrays to build commands dynamically. Arrays handle argument separation safely. Execute the command using `"${array[@]}"`.
