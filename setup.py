from setuptools import setup, find_packages

setup(
    name='sales-insight-eda',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'streamlit',        # For creating data applications
        'pandas',           # For data manipulation and analysis
        'numpy',            # For numerical computations
        'matplotlib',       # For creating static, animated, and interactive visualizations
        'scikit-learn',     # For machine learning algorithms
        'seaborn',          # For statistical data visualization
        'plotly',           # For interactive visualizations
        'scipy',            # For scientific and technical computing
        'requests',         # For making HTTP requests
        'flask',            # For web application development (if you're using it)
        'sqlalchemy',       # For SQL database connection (if needed)
        'pytest',           # For testing
        'pillow',           # For image processing
        'pyarrow',          # For working with Apache Arrow
        'gitpython',        # For interacting with Git repositories
        'altair',           # For declarative data visualization
        'blinker',          # For fast object attribute lookup and signal handling
        'cachetools',       # For caching strategies
        'tornado',          # For asynchronous networking
        'typing-extensions' # For backward compatibility with type hinting
    ],
)
