from invoke import task


_CONTAINER_NAME = "fastapi"


@task
def logs(c):
    cmd = f"docker logs -f {_CONTAINER_NAME}"
    c.run(cmd)


@task
def exec(c, target: str = f"/bin/bash"):

    cmd = f"docker exec -it {_CONTAINER_NAME} {target}"
    c.run(cmd, pty=True)


@task
def startapp(c, rebuild=True):

    if rebuild:
        build(c)

    cmd = (f"docker run "
           f"--detach "
           f"--name {_CONTAINER_NAME} "
           f"-p 80:80 fastapi:latest")
    c.run(cmd)


@task
def down(c):
    cmd = f"docker kill {_CONTAINER_NAME}"
    c.run(cmd)

    rm_cmd = f"docker rm {_CONTAINER_NAME}"
    c.run(rm_cmd)


@task
def build(c):
    cmd = f"docker build -t {_CONTAINER_NAME} ."
    c.run(cmd)

