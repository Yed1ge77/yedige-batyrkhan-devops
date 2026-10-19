# Submission checklist and evidence

Only mark items complete after running the command and saving its real output.
The instructor repository is https://github.com/Yed1ge77/yedige-batyrkhan-devops.
Do not put Jenkins tokens, passwords, SSH keys or authentication headers in a report.

## Checklist

- [ ] Student information and personalized Linux filenames are visible.
- [ ] Linux system script shows kernel, OS, processes, disk and memory.
- [ ] Sample log has at least 10 lines, ERROR and WARNING (simulated examples).
- [ ] Private/public file modes are 600/644 on the demonstration machine.
- [ ] Python unit tests, compilation and Bash syntax checks pass.
- [ ] Main HTML, health JSON and unknown route return 200/200/404.
- [ ] Docker image builds, runs as non-root, and passes HTTP smoke checks.
- [ ] Compose container is healthy and exposes the page on localhost:8000.
- [ ] Git graph shows at least five real commits, development and main, and merge.
- [ ] GitHub contains both reviewed branches after explicit push approval.
- [ ] Jenkins job Yedige_Batyrkhan_DevOps reports SUCCESS in all five stages.
- [ ] PDF contains command outputs and references to repository and video.
- [ ] Video runs 10–20 minutes and shows actual results.

## Evidence commands for the PDF

```bash
cd ~/devops/yedige_batyrkhan
mkdir -p logs/evidence
{
  date --iso-8601=seconds
  pwd
  cat Yedige_Batyrkhan_info.txt
  ./scripts/generate_sample_log.sh
  ./scripts/Yedige_Batyrkhan_system.sh
  wc -l logs/application.log
  grep -E 'ERROR|WARNING' logs/application.log
  chmod 600 private.txt
  chmod 644 public.txt
  stat -c '%a %n' private.txt public.txt
  ./scripts/linux_demo.sh
} > logs/evidence/linux.txt 2>&1
./scripts/verify.sh > logs/evidence/tests.txt 2>&1
{
  git log --graph --oneline --decorate --all
  git branch -vv
  git rev-list --count main
  git status --short --branch
} > logs/evidence/git.txt
```

Check each exit status directly; do not treat a saved text file as proof of success.
Open the evidence text in your terminal with `cat`. Capture it for the PDF.
Git does not store 600 versus 644; restore permissions on each demonstration machine.

Manual Docker commands (sudo only if your normal terminal requires it):

```bash
sudo bash scripts/docker_verify.sh
sudo docker compose up -d --build --wait
sudo docker compose ps
curl -i http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/unknown
sudo docker compose logs --tail=30
```

The isolated verifier does not stop your Compose container or publish host ports.
Compose up uses the existing project configuration. Stop conflicting local servers first.
Run `sudo docker compose down` when you finish demonstrating Compose.

Jenkins job preparation and execution, from your normal terminal:

```bash
python3 scripts/jenkins_job.py
```

Enter your Jenkins username and API token at the prompts. The token is hidden,
never stored in project files, and sent only to localhost:8080. Use an existing
API token from your secure credential store; do not put one in a shell command.
The helper creates the job only if it is absent, preserves any existing job,
triggers one build, waits up to 20 minutes, and reports the real result.
A new job checks out the development branch on GitHub. It therefore executes
only pushed code: local changes need separate review and push approval first.
The already pushed initial Jenkinsfile can be tested before publishing updates.
An existing job may use another branch; inspect its SCM settings if necessary.

Required plugins: Pipeline and Git. The selected Jenkins agent must have Bash,
Python 3, Git, Docker CLI and authorized daemon access. User sudo access does
not grant Jenkins Docker access. Do not disable security or enable passwordless
sudo to make a build pass. Ask the administrator for an authorized build agent
if needed. This repository does not modify services or account permissions.

For the PDF, record job name, build number, commit hash, stage results, final
SUCCESS/FAILURE, and console output with no secrets. A prepared Jenkinsfile is
not evidence of a successful build. PDF assembly and video recording are manual.
