# import uvicorn
from uvicorn.main import *

serv = None

def extension_run(app, **kwargs):
    global serv
    print("extension run")
    config = Config(app, **kwargs)
    serv = Server(config=config)

    if (config.reload or config.workers > 1) and not isinstance(app, str):
        logger = logging.getLogger("uvicorn.error")
        logger.warning(
            "You must pass the application as an import string to enable 'reload' or "
            "'workers'."
        )
        sys.exit(1)

    if config.should_reload:
        sock = config.bind_socket()
        supervisor = ChangeReload(config, target=serv.run, sockets=[sock])
        supervisor.run()
    elif config.workers > 1:
        sock = config.bind_socket()
        supervisor = Multiprocess(config, target=serv.run, sockets=[sock])
        supervisor.run()
    else:
        serv.run()



run = extension_run
print(uvicorn.run)
