"""Create a missing localhost SCM job and run it using a hidden API token prompt.

Never updates an existing job. Default SCM branch is development so unpublished
local improvements are not needed to test the already pushed pipeline.
"""
import base64
import getpass
import json
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, ProxyHandler, HTTPRedirectHandler

BASE = 'http://127.0.0.1:8080/'
JOB = 'Yedige_Batyrkhan_DevOps'
CONFIG = b'''<?xml version="1.0" encoding="UTF-8"?>
<flow-definition plugin="workflow-job">
  <description>DevOps Laboratory Work 1</description><keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps">
    <scm class="hudson.plugins.git.GitSCM" plugin="git">
      <configVersion>2</configVersion>
      <userRemoteConfigs><hudson.plugins.git.UserRemoteConfig>
        <url>https://github.com/Yed1ge77/yedige-batyrkhan-devops.git</url>
      </hudson.plugins.git.UserRemoteConfig></userRemoteConfigs>
      <branches><hudson.plugins.git.BranchSpec><name>*/development</name></hudson.plugins.git.BranchSpec></branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="empty-list"/><extensions/>
    </scm><scriptPath>Jenkinsfile</scriptPath><lightweight>true</lightweight>
  </definition><triggers/><disabled>false</disabled>
</flow-definition>'''


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward Authorization to a redirected host.


def main():
    username = input('Jenkins username: ')
    token = getpass.getpass('Jenkins API token (hidden): ')
    authorization = 'Basic ' + base64.b64encode(f'{username}:{token}'.encode()).decode()
    client = build_opener(ProxyHandler({}), NoRedirect())
    headers = {'Authorization': authorization}

    def request(path, data=None, content_type=None):
        url = BASE + path.lstrip('/')
        outgoing = dict(headers)
        if content_type:
            outgoing['Content-Type'] = content_type
        return client.open(Request(url, data=data, headers=outgoing), timeout=30)

    def read_json(path):
        with request(path) as response:
            return json.load(response)

    try:
        crumb = read_json('crumbIssuer/api/json')
        headers[crumb['crumbRequestField']] = crumb['crumb']
    except HTTPError as error:
        if error.code != 404:
            raise
    try:
        read_json(f'job/{JOB}/api/json')
        print('Existing job preserved. Its current SCM configuration will be used.')
    except HTTPError as error:
        if error.code != 404:
            raise
        with request(f'createItem?name={JOB}', CONFIG, 'application/xml'):
            pass
        print('Created SCM job on development branch.')
    with request(f'job/{JOB}/build', b'') as response:
        queue_url = response.headers.get('Location', '')
    # Jenkins absolute URLs may use localhost instead of 127.0.0.1.
    parsed = urlsplit(queue_url)
    if parsed.hostname not in ('localhost', '127.0.0.1') or parsed.port != 8080:
        raise RuntimeError('Unexpected queue location; inspect Jenkins manually')
    queue_path = parsed.path.strip('/')
    deadline = time.monotonic() + 1200
    build_path = None
    while time.monotonic() < deadline:
        if build_path is None:
            queued = read_json(queue_path + '/api/json')
            if queued.get('cancelled'):
                raise RuntimeError('Build cancelled in queue')
            if 'executable' in queued:
                number = queued['executable']['number']
                build_path = f'job/{JOB}/{number}'
                print(f'Build #{number} started')
        else:
            build = read_json(build_path + '/api/json')
            if not build['building']:
                print(f"Jenkins result: {build['result']}; {BASE}{build_path}/console")
                return 0 if build['result'] == 'SUCCESS' else 1
        time.sleep(3)
    raise RuntimeError('Timed out; build may still be running. Inspect Jenkins.')


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        # Avoid printing request objects, headers, tokens or server response bodies.
        print(f'Jenkins operation failed: {type(error).__name__}. Check service, permissions and job status.')
        raise SystemExit(1)
