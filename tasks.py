from invoke import task


_CONTAINER_NAME = "fastapi"


# not quite working
@task
def logs(c):
    cmd = f"docker logs -f {_CONTAINER_NAME}"
    c.run(cmd)

# same as above cuz container name is longer for these two
@task
def exec(c, target: str = f"/bin/bash"):

    cmd = f"docker exec -it {_CONTAINER_NAME} {target}"
    c.run(cmd, pty=True)


@task
def startapp(c, no_build=False):
    if not no_build:
        c.run(f"docker compose build --pull")
    c.run(f"docker compose up")


@task
def down(c, hard=False):
    c.run(f"docker compose down")
    if hard:
        c.run(f"docker system prune -a")

# Shelving it here,
# @task
# def startapp(c, rebuild=True):
#
#     if rebuild:
#         build(c)
#
#     cmd = (f"docker run "
#            f"--detach "
#            f"--name {_CONTAINER_NAME} "
#            f"-p 80:80 fastapi:latest")
#     c.run(cmd)
#
#
# @task
# def down(c):
#     cmd = f"docker kill {_CONTAINER_NAME}"
#     c.run(cmd)
#
#     rm_cmd = f"docker rm {_CONTAINER_NAME}"
#     c.run(rm_cmd)


# @task
# def build(c):
#     cmd = f"docker build -t {_CONTAINER_NAME} ."
#     c.run(cmd)

