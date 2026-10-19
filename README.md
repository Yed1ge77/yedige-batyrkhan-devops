# devops-lab-1

DevOps Laboratory Work 1: Linux fundamentals and a Python HTTP application.

## Student

| Field | Value |
| --- | --- |
| Full name | Batyrkhan Yedige Yerlanuly |
| Student ID | 38419 |
| Group | IT2-2302 |
| University | IITU |
| Course | DevOps |

These details are stored in `config/student_info.json`.
Repository: https://github.com/Yed1ge77/yedige-batyrkhan-devops.
Further pushes require explicit approval.
Do not add passwords, tokens, or private keys. Before a future public push,
review all files and Git history for secrets and obtain permission to publish.

## Overview and structure

The application uses only Python's standard library. No pip packages are needed.
The Bash scripts show Linux commands safely. Generated files belong in `logs/`
and `backup/`, separate from source code.

```text
devops-lab/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── student.py
├── scripts/
│   ├── system_info.sh
│   └── linux_demo.sh
├── config/
│   └── student_info.json
├── logs/
│   └── .gitkeep
├── backup/
│   └── .gitkeep
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── .gitignore
└── README.md
```

## Requirements

- Ubuntu 24.04 / WSL2, Bash, and standard Linux commands (`ps`, `find`, `grep`, etc.).
- Python 3.12. No external Python libraries.
- `curl` for optional manual HTTP checks.
- Docker Engine and Compose for containers; Jenkins with Pipeline/Git plugins for CI.

## Run the application

In your normal Ubuntu terminal:

```bash
cd /home/batyr/devops/yedige_batyrkhan
python3 -m app.main
```

The default address is `http://127.0.0.1:8000`. Stop the server with Ctrl+C.
Run module commands from the project root. To choose other settings:

```bash
APP_ENV=lab HOST=127.0.0.1 PORT=8001 python3 -m app.main
```

`APP_ENV` defaults to `development`. `HOST` defaults to `127.0.0.1` for local use.
`PORT` defaults to `8000` and must be an integer from 1 to 65535.
The container uses `HOST=0.0.0.0` to accept connections through its mapped port.
Environment values are read at startup. Restart the app after changing them.

In a second terminal, check the default server:

```bash
curl -i http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/unknown
```

Expected behavior:

- `/`: HTTP 200, HTML page with all five student fields and the environment.
- `/health`: HTTP 200, `application/json`, body like:
  `{"status": "ok", "environment": "development"}`.
- `/unknown`: HTTP 404, plain text `Not found`.
- Request logs appear in the server terminal. The app does not write log files.
- Missing or invalid student configuration causes a clear startup error and exit status 1.

This is a teaching server for local use, not a public production server.

## Automated checks

```bash
cd /home/batyr/devops/yedige_batyrkhan
python3 -m unittest discover -s tests -v
python3 -m compileall -q app tests
bash -n scripts/system_info.sh
bash -n scripts/linux_demo.sh
```

Tests cover student data, invalid/missing configuration, HTTP responses, JSON,
environment settings, and HTML escaping. They send in-memory HTTP requests to
Python's real request handler. They need no running server or network sockets.
They do not verify TCP listening; use the manual curl checks above for that.
Compilation creates ignored `__pycache__/` directories.

If ShellCheck is already available:

```bash
if command -v shellcheck >/dev/null 2>&1; then
    shellcheck scripts/system_info.sh scripts/linux_demo.sh
else
    printf 'ShellCheck is not installed; optional check skipped.\n'
fi
```

## Linux scripts

```bash
cd /home/batyr/devops/yedige_batyrkhan
./scripts/system_info.sh
./scripts/linux_demo.sh
```

The scripts also work from another directory:

```bash
cd /home/batyr/devops/yedige_batyrkhan/app
../scripts/system_info.sh
../scripts/linux_demo.sh
```

`system_info.sh` prints student data, username, hostname, kernel, OS, time,
working directory, and a short process list. It checks required files and
folders relative to the script location. Missing items produce exit status 1.
Other command failures also stop the script with a nonzero exit status.

`linux_demo.sh` creates a unique temporary folder under `logs/` and removes
only that folder on exit. It starts, inspects, and stops only its own `sleep`
process. Do not use sudo.

| Command | What the demo shows |
| --- | --- |
| `pwd`, `ls` | Show the temporary location and files |
| `mkdir`, `touch` | Create a folder and an empty file |
| `cp`, `mv` | Copy and rename a file |
| `find`, `grep` | Find files and search text |
| `chmod`, `stat`, `ls -l` | Set and show permissions |
| `rm` | Remove the demo copy |
| `ps`, `kill`, `wait` | Inspect, stop, and collect the demo child process |

The example permission `640` means owner read/write, group read, others no
access. Scripts use `755`: the owner can edit; everyone can read and execute.

### Interactive job control

`jobs`, `fg`, and Ctrl+Z work in an interactive shell. They are separate from
the script. In a normal terminal, run:

```bash
sleep 60 &
demo_pid=$!
jobs -l
ps -p "$demo_pid" -o pid,ppid,stat,comm
kill "$demo_pid"
wait "$demo_pid"
```

`wait` may return 143 because you stopped the sleep process with SIGTERM.
For foreground practice, run `sleep 60`, press Ctrl+Z, run `jobs`, then `fg`,
and press Ctrl+C. Only stop the process you started for this exercise.

## Troubleshooting

- **Operation not permitted when starting the server:** a restricted sandbox
  may block sockets. Run the app and curl checks in your normal WSL terminal.
  Do not change system permissions to bypass the sandbox.
- **Address already in use:** choose `PORT=8001` and use port 8001 in curl.
- **No module named app:** run `python3 -m app.main` from the project root.
- **Missing student configuration:** restore `config/student_info.json` with
  the five string fields shown in the student table. Student ID is a string.
- **Invalid configuration:** check JSON syntax and nonempty string values.
- **Script not executable:** use `bash scripts/system_info.sh`, or restore
  the script permission with `chmod u+x scripts/system_info.sh`.
- **Required file check fails:** read the `MISSING` line and restore that item.
- **Demo cannot create a temporary folder:** check that `logs/` exists and is writable.

## Verification and submission

Run `./scripts/verify.sh` for unit tests, Python compilation and Bash checks.
Run `sudo bash scripts/docker_verify.sh` in your normal Ubuntu terminal when
Docker needs sudo. This builds an isolated image, tests real HTTP responses
and the container user, and removes only its temporary container.

See [submission checklist and PDF evidence](docs/SUBMISSION.md) and
[15-minute video script](docs/VIDEO.md). Jenkins preparation is available with
`python3 scripts/jenkins_job.py`; credentials are prompted without echo.
No successful Jenkins build is assumed until the helper reports SUCCESS.

## Submission demonstration: instructor names

Project directory: `~/devops/yedige_batyrkhan`.
GitHub repository name: `yedige-batyrkhan-devops` (publication needs approval).
Student text file: `Yedige_Batyrkhan_info.txt`.
The original JSON configuration remains the Python application's default data.

### Linux

```bash
cd ~/devops/yedige_batyrkhan
cat Yedige_Batyrkhan_info.txt
./scripts/generate_sample_log.sh
wc -l logs/application.log
grep -E 'ERROR|WARNING' logs/application.log
./scripts/Yedige_Batyrkhan_system.sh
./scripts/linux_demo.sh
chmod 600 private.txt
chmod 644 public.txt
ls -l private.txt public.txt
```

The generated log contains simulated examples, not actual application failures.
It is ignored by Git and can be recreated with the generator. Permissions 600
mean owner read/write only; 644 adds read access for group and others. Git does
not preserve these numeric permission differences; run chmod after cloning.

Load the shell-compatible application configuration explicitly:

```bash
set -a
source config/app.conf
set +a
python3 -m app.main
```

`STUDENT_NAME` and `STUDENT_SURNAME` override the displayed full name when set.
`STUDENT_GROUP` and `STUDENT_ID` override those fields. Without overrides, all
original JSON values remain unchanged. Example:

```bash
STUDENT_NAME=Batyrkhan STUDENT_SURNAME=Yedige STUDENT_GROUP=IT2-2302 STUDENT_ID=38419 python3 -m app.main
```

### Local Git workflow

`main` and `development` already exist. Preserve the published initial commit.
Make useful changes on `development`, run tests before each descriptive commit,
and merge reviewed work into `main`. Do not create empty commits or rewrite history.

```bash
git status --short --branch
git diff --check
git log --graph --oneline --decorate --all
git branch -vv
git rev-list --count main
```

Never commit logs, backups, credentials or `.env` files. Review the staged diff
before commits. Push only after explicit approval and a secret review.

### Docker (normal Ubuntu terminal)

Stop any local Python server using port 8000 first. Docker currently needs sudo
in your terminal; the following commands are for you to run manually.

```bash
cd ~/devops/yedige_batyrkhan
sudo docker build -t yedige-batyrkhan-devops .
sudo docker run -d --name yedige-batyrkhan-container -p 127.0.0.1:8000:8000 -e APP_ENV=lab -e STUDENT_NAME=Batyrkhan -e STUDENT_SURNAME=Yedige -e STUDENT_GROUP=IT2-2302 -e STUDENT_ID=38419 yedige-batyrkhan-devops
curl -i http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/unknown
sudo docker logs yedige-batyrkhan-container
sudo docker stop yedige-batyrkhan-container
sudo docker rm yedige-batyrkhan-container
sudo docker compose config
sudo docker compose up -d --build
sudo docker compose ps
curl -i http://127.0.0.1:8000/health
sudo docker compose down
```

Expected HTTP statuses are 200, 200, 404. Both the image and Compose configuration
use a non-root user. Compose publishes port 8000 only on localhost.

### Jenkins

Required job name: `Yedige_Batyrkhan_DevOps`.
The Jenkinsfile uses Checkout, Build, Test, Docker Build, Docker Run.
Docker Run starts an isolated container, checks its health endpoint inside the
container, and removes it on exit. It does not reserve host port 8000.

Manual setup: create a Pipeline job with that name, choose Pipeline script from
SCM, choose Git, set an approved repository URL/path, branch `*/main`, and script
path `Jenkinsfile`. Save and run Build Now. A real committed SCM source is needed
for `checkout scm`; this will not run as an unconfigured inline pipeline.
Local Git paths may be restricted by Jenkins; use an approved SCM source rather
than disabling Jenkins security. The repository already exists; additional pushes still require approval.

The Jenkins agent needs Python 3, Bash, Git, Docker CLI, and authorized Docker
daemon access. Your user's sudo access does not give access to Jenkins. This
setup is not changed by this project. If Docker Build fails with permission
denied, ask the administrator to provide an authorized build agent.

Terminal checks on your machine:

```bash
curl -I http://localhost:8080/login
python3 -m unittest discover -s tests -v
python3 -m compileall -q app tests
for script in scripts/*.sh; do bash -n "$script"; done
```

Pipeline success must be checked in Jenkins console output. The Jenkinsfile has
not been executed merely because the Python and Bash checks pass.
