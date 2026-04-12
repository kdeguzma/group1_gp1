from setuptools import find_packages, setup

package_name = "group1_gp1"

setup(
    name=package_name,
    version="1.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]), ("share/" + package_name + "/launch", ["launch/system.launch.py"])
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="kdeguzma",
    maintainer_email="kdeguzma@umd.edu",
    description="This package dispatches tasks to a fleet of mobile robots.",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "dispatcher = scripts.main_dispatcher:main",
            "robot_1 = scripts.main_robot_1:main",
            "robot_2 = scripts.main_robot_2:main",
            "robot_3 = scripts.main_robot_3:main",
            "monitor = scripts.main_monitor:main",
            "debug_logger = scripts.main_debug_logger:main"
            
        ],
    },
)
