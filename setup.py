import setuptools

setuptools.setup(
    name='PyPactia',
    version='0.0.1',
    author='Analítica Pactia',
    description='Paquete de utilidades de Pactia',
    url='https://github.com/Pactia/PyPactia',
    license='MIT',
    packages=['ayudantes'],
    install_requires=['requests', 'xmltodict', 'json==2.0.9', 'pandas'],
)