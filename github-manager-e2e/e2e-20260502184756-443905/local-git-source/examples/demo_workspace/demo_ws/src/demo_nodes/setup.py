from setuptools import setup

package_name = 'demo_nodes'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/demo.launch.py']),
        ('share/' + package_name + '/config', ['config/demo_params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ROS2-Agent',
    maintainer_email='demo@example.com',
    description='Minimal demo package for ROS2-Agent',
    license='MIT',
    entry_points={
        'console_scripts': [
            'talker = demo_nodes.talker:main',
        ],
    },
)
