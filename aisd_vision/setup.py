from setuptools import find_packages, setup
import os   #kt added
from glob import glob  #kt added

package_name = 'aisd_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install data files from the resource/data folder
        (os.path.join('share', package_name, 'resource', 'data'), glob('resource/data/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aisd',
    maintainer_email='aisd@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "py_node = aisd_vision.my_first_node:main",
            "test_hands_listener = aisd_vision.test_listener:main",
            'image_publisher = aisd_vision.image_publisher:main',
            'hands = aisd_vision.hands:main',

        ],
    },
)
