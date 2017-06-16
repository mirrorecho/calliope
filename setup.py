from distutils.core import setup

install_requires = [
    'abjad',
    'pandas',
    ]

def main():
    setup(
        author='Randall West',
        author_email='info@randallwest.com',
        install_requires=install_requires,
        name='calliope',
        packages=('calliope',),
        url='https://github.com/mirrorecho/calliope/',
        version='2.2',
        zip_safe=False,
        )

if __name__ == '__main__':
    main()