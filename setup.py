"""
md2pdf-mermaid - Markdown to PDF Converter with Mermaid Support
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="md2pdf-mermaid",
    version="1.3.1",
    author="Roberto Butinar",
    author_email="roberto.butinar@gmail.com",
    description="Convert Markdown to PDF with Mermaid diagram rendering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rbutinar/md2pdf-mermaid",
    packages=find_packages(),
    package_data={
        'md2pdf': ['fonts/*.ttf'],
    },
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Documentation",
        "Topic :: Text Processing :: Markup",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "reportlab>=4.0.0",
        "playwright>=1.40.0",
        "pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "md2pdf=md2pdf.cli:main",
        ],
    },
    keywords="markdown pdf mermaid diagram converter documentation",
    project_urls={
        "Bug Reports": "https://github.com/rbutinar/md2pdf-mermaid/issues",
        "Source": "https://github.com/rbutinar/md2pdf-mermaid",
    },
)
