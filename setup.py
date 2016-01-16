from setuptools import find_packages, setup

setup(
    name="tcg - terminal card games",
    version="1.0",
    description="Collection of card games for the command line.",
    install_requires=[
        "colored==1.4.2",
    ],
    entry_points={
        "console_scripts": [
            "tcg-blackjack = tcg.blackjack:main",
        ],
    },
)
