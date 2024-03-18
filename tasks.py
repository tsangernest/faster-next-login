from invoke import task


@task
def logs(c):
    cmd = f"docker logs -f fastapi"
    c.run(cmd)


@task
def exec(c):
    cmd = f"docker exec -it fastapi /bin/bash"
    c.run(cmd, pty=True)


@task
def startapp(c):
    cmd = (f"docker run "
           f"--detach "
           f"--name fastapi "
           f"-p 80:80 fastapi:latest")
    c.run(cmd)


@task
def down(c):
    cmd = f"docker kill fastapi"
    c.run(cmd)

    rm_cmd = f"docker rm fastapi"
    c.run(rm_cmd)


@task
def build(c):
    cmd = f"docker build -t fastapi ."
    c.run(cmd)

