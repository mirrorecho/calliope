from distutils.core import setup

install_requires = [
    # 'uqbar==0.3.2', # TO DO EVENTUALLY: remove (fixes issue with uqbar 0.4?)
    # 'abjad[development,ipython]>=3.1',
    'abjad>=3.1',
    'abjad-ext-rmakers>=3.1',
    'pandas>=0.25',
    'jupyterlab>=1.2',
    'pytest>=5.3',
    'pytest-cov>=2.8',
    ]

def main():
    setup(
        author='Randall West',
        author_email='info@randallwest.com',
        install_requires=install_requires,
        name='calliope',
        packages=('calliope',),
        url='https://github.com/mirrorecho/calliope/',
        version='3.1',
        zip_safe=False,
        )

if __name__ == '__main__':
    main()