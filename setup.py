from setuptools import setup

setup(
    name='youtube_to_dfpwm',
    version='1.0.0',
    description='Download YouTube audio and convert it to DFPWM format',
    author='IceliosGit',
    py_modules=['youtube_to_dfpwm'],
    install_requires=[
        'yt-dlp>=2024.3.10',
    ],
    entry_points={
        'console_scripts': [
            'ytd = your_module:main',
        ],
    },
    python_requires='>=3.7',
)
