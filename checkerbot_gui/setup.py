from setuptools import setup, find_packages

setup(
    name="checkerbot_gui",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'requests',
        'python-docx'
    ],
    entry_points={
        'console_scripts': [
            'checkerbot_gui=checkerbot_gui.main:main'
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
