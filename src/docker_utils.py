import sys

from subprocess import run
from pathlib import Path
from textwrap import dedent
from typing import List
from .github_utils import create_release
from .version_utils import get_version


def build_and_push_client_img(
    *,
    src: Path,
    tag_prefix: str,
    image_name: str,
    docker_username: str,
    docker_password: str,
    github_access_token: str,
    pack_args: List[str] = [],
    ignore: List[str] = [],
):
    build_and_push_img(
        src=src,
        tag_prefix=tag_prefix,
        image_name=image_name,
        pack_args=[
            '--builder',   'paketobuildpacks/builder:base',
            '--buildpack', 'paketo-buildpacks/web-servers',
            '--buildpack', 'paketo-buildpacks/source-removal',
            '--buildpack', 'gcr.io/paketo-buildpacks/health-checker',
            '--env',       'BP_NODE_RUN_SCRIPTS=build',
            '--env',       'BP_WEB_SERVER=nginx',
            '--env',       'BP_WEB_SERVER_ROOT=dist',
            '--env',       'BP_WEB_SERVER_ENABLE_PUSH_STATE=true',
            '--env',       'BP_NGINX_STUB_STATUS_PORT=8033',
            '--env',       'BP_INCLUDE_FILES=nginx.conf:dist/**',
            '--env',       'BP_HEALTH_CHECKER_ENABLED=true',
            '--env',       'BPE_PORT=80',
            '--env',       'THC_PATH=/stub_status',
            '--env',       'THC_PORT=8033',
            *pack_args,
        ],
        docker_username=docker_username,
        docker_password=docker_password,
        github_access_token=github_access_token,
        ignore=[
            'node_modules',
            'dist',
            *ignore
        ]
    )


def build_and_push_server_img(
    *,
    src: Path,
    tag_prefix: str,
    image_name: str,
    docker_username: str,
    docker_password: str,
    github_access_token: str,
    pack_args: List[str] = [],
    ignore: List[str] = [],
):
    build_and_push_img(
        src=src,
        tag_prefix=tag_prefix,
        image_name=image_name,
        pack_args=[
            '--builder',   'paketobuildpacks/builder:base',
            '--buildpack', 'paketo-buildpacks/java',
            '--buildpack', 'gcr.io/paketo-buildpacks/health-checker',
            '--env',       'BP_JVM_VERSION=17',
            '--env',       'BP_HEALTH_CHECKER_ENABLED=true',
            '--env',       'BPE_SPRING_PROFILES_ACTIVE=prod',
            '--env',       'THC_PATH=/actuator/health/liveness',
            '--env',       'THC_PORT=8082',
            *pack_args,
        ],
        docker_username=docker_username,
        docker_password=docker_password,
        github_access_token=github_access_token,
        ignore=[
            'target',
            *ignore
        ]
    )

def build_and_push_python_img(
    *,
    src: Path,
    tag_prefix: str,
    image_name: str,
    docker_username: str,
    docker_password: str,
    github_access_token: str,
    pack_args: List[str] = [],
    ignore: List[str] = [],
):
    build_and_push_img(
        src=src,
        tag_prefix=tag_prefix,
        image_name=image_name,
        pack_args=[
            '--builder',   'paketobuildpacks/builder:base',
            '--buildpack', 'paketo-buildpacks/python',
            *pack_args,
        ],
        docker_username=docker_username,
        docker_password=docker_password,
        github_access_token=github_access_token,
        ignore=[
            'target',
            *ignore
        ]
    )


def build_and_push_img(
    *,
    src: Path,
    tag_prefix: str,
    image_name: str,
    docker_username: str,
    docker_password: str,
    github_access_token: str,
    pack_args: List[str] = [],
    ignore: List[str] = [],
):
    if not github_access_token:
        print('GitHub access token is missing', flush=True, file=sys.stderr)
        exit(1)

    changed, version = get_version(
        src=src, tag_prefix=tag_prefix, ignore=ignore)

    if not changed:
        return

    run(['docker', 'login', '--username', docker_username,
        '--password-stdin'], input=docker_password.encode(), check=True)
    run(['pack', 'build', f'{image_name}:latest', '--path', str(src), '--tag',
        f'{image_name}:{version}', '--publish', *pack_args], check=True)

    create_release(
        tag_prefix=tag_prefix,
        version=version,
        access_token=github_access_token,
        body=dedent(f'''
            [Docker image on DockerHub](https://hub.docker.com/repository/docker/{image_name})

            ```yaml
            image: {image_name}:{version}
            ```
        ''')
    )
    print(
        f'Docker image pushed successfully for {tag_prefix}:{version}', flush=True)
    
def build_and_push_docker_img(
    *,
    src: Path,
    tag_prefix: str,
    image_name: str,
    docker_username: str,
    docker_password: str,
    github_access_token: str,
    ignore: List[str] = [],
):
    if not github_access_token:
        print('GitHub access token is missing', flush=True, file=sys.stderr)
        exit(1)

    changed, version = get_version(
        src=src, tag_prefix=tag_prefix, ignore=ignore)

    if not changed:
        return

    run(['docker', 'login', '--username', docker_username,
        '--password-stdin'], input=docker_password.encode(), check=True)
    run(['docker', 'buildx', 'create', '--use'])
    run(['docker', 'buildx', 'build', '--platform', 'linux/amd64,linux/arm64/v8', '--tag', f'{image_name}:latest', '--tag',
        f'{image_name}:{version}', '--push', '.'], cwd=src, check=True)

    create_release(
        tag_prefix=tag_prefix,
        version=version,
        access_token=github_access_token,
        body=dedent(f'''
            [Docker image on DockerHub](https://hub.docker.com/repository/docker/{image_name})

            ```yaml
            image: {image_name}:{version}
            ```
        ''')
    )
    print(
        f'Docker image pushed successfully for {tag_prefix}:{version}', flush=True)