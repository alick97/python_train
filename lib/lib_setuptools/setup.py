from setuptools import setup, find_packages
setup(
    name="myhelloworld",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},   # tell distutils packages are under src
	scripts=["src/mypkg/say_hello.py"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # install_requires=["docutils>=0.3"],
    install_requires=[],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"],
        # And include any *.msg files found in the "hello" package, too:
        "mypkg": ["data/*.dat"],
    },
    # metadata to display on PyPI
    author="Me",
    author_email="me@example.com",
    description="This is an Example Package",
    keywords="hello world example examples",
    url="http://example.com/HelloWorld/",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ],

    # could also include long_description, download_url, etc.
    # other arguments here...
    entry_points={
        "console_scripts": [
            "my_show = say_hello:show",
        ]
    }

)
