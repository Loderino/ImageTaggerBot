from setuptools import setup, find_packages

setup(
    name="Image-tagger-bot",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        "aiofiles==24.1.0",
        "numpy==1.26.4",
        "pillow==10.4.0",
        "scikit-learn==1.5.2",
        "tensorflow==2.17.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Linux",
    ],
    python_requires=">=3.11",
)
