# Video demonstration: approximately 15 minutes

Use a terminal. Prepare readable font size and hide unrelated windows and secrets.
Do not record login tokens. Explain commands before running them.

| Time | Show and explain |
| --- | --- |
| 0:00–1:00 | Introduce Batyrkhan Yedige Yerlanuly, 38419, IT2-2302, IITU, DevOps. Run `pwd`, `cat Yedige_Batyrkhan_info.txt`, and `ls`. |
| 1:00–3:30 | Run `scripts/generate_sample_log.sh`, `scripts/Yedige_Batyrkhan_system.sh`, `wc -l logs/application.log`, and `grep -E 'ERROR|WARNING' logs/application.log`. Explain that log events are simulated. |
| 3:30–5:00 | Run `scripts/linux_demo.sh`. Explain copy, move, find, chmod, process PID and safe cleanup. Run `stat -c '%a %n' private.txt public.txt`; explain 600/644. |
| 5:00–7:00 | Show JSON and Python source. Run `scripts/verify.sh`. Explain port 8000, default development environment, /health and 404. |
| 7:00–8:30 | Run `git log --graph --oneline --decorate --all`, `git branch -vv`, `git status --short --branch`. Explain the initial commit, four real improvements and merge. Show the repository link in README. |
| 8:30–11:30 | Show Dockerfile instructions and Compose environment. Run `sudo bash scripts/docker_verify.sh`, `sudo docker compose up -d --build --wait`, `sudo docker compose ps` and curl all three routes. Explain localhost port mapping and non-root user. |
| 11:30–14:30 | Show Jenkinsfile and all five stages. Show actual Jenkins build number, commit and final result from saved output or run the terminal helper with credentials entered off recording. Never claim SUCCESS unless Jenkins reports it. |
| 14:30–15:30 | Show the submission checklist and explain one problem solved, sandbox limitations, and any remaining incomplete items. Stop the Compose project if no longer needed. |

A slow image build or Jenkins queue can exceed this schedule. Build ahead of
recording, then show genuine logs with timestamps and commit IDs. Do not edit
failure output to suggest success. No browser automation is required.
