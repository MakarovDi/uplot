
if __name__ == '__main__':
    # import info without executing __init__
    import sys
    sys.path.append('uplot')
    import info

    # load dependencies
    with open('requirements.txt') as f:
        dependencies = f.read().splitlines()

    # run setup
    import setuptools

    setuptools.setup(
        name='uplot',
        packages=setuptools.find_namespace_packages(),

        version=info.__version__,
        description=info.__description__,
        author=info.__author__,
        author_email=info.__email__,
        license=info.__license__,
        url='https://github.com/MakarovDi/uplot',

        python_requires='>=3.10',
        install_requires=dependencies,
        extras_require={
            'matplotlib': [ 'matplotlib >= 3.7, < 4.0' ],
            'plotly5':    [ 'plotly >= 5.17, < 6.0', 'kaleido' ],
            'all':        [ 'matplotlib >= 3.7, < 4.0', 'plotly >= 5.17, < 6.0', 'kaleido' ]
        },
    )