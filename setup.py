from setuptools import setup, find_packages

setup(
    name='orchidea',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.2',
    ],
    description='A reusable Django app for managing spa services and recruitment.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/orchidea',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
