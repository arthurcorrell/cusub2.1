from setuptools import find_packages, setup

package_name = 'cortex'

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
    maintainer='arthurcorrell',
    maintainer_email='arthurcorrell@gmail.com',
    description='Behavior tree instance and decision logic',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'compute_heading_test = cortex.controller.computeHeadingTest:main'
        ],
    },
)
