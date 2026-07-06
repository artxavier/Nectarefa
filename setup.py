from setuptools import find_packages, setup

package_name = 'nectarefa'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='arthur-xavier',
    maintainer_email='arthuraxribeiro@gmail.com',
    description='Autonomous drone mission using YASMIN state machines and Nectar SDK',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'mangalarga = nectarefa.mangalarga:main',
        ],
    },
)
