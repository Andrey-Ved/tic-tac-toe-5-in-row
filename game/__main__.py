from game.ioc import container as ioc_container

from game.core.services import Game


def entrypoint():
    g = Game(
        ioc_container=ioc_container
    )
    g.main_loop()


if __name__ == '__main__':
    entrypoint()
