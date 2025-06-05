from setuptools import setup

setup(
    name='youtube_to_dfpwm',
    version='1.0.0',
    description='Download YouTube audio and convert it to DFPWM format',
    author='Your Name',
    author_email='your.email@example.com',
    py_modules=['youtube_to_dfpwm'],  # your script filename without .py
    install_requires=[
        'yt-dlp>=2024.3.10',
    ],
    entry_points={
        'console_scripts': [
            'youtube-to-dfpwm = youtube_to_dfpwm:main',
        ],
    },
    python_requires='>=3.7',
)
