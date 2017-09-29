try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst', format='md')
    long_description = long_description.replace("\r","") # Do not forget this line
except OSError:
    print("Pandoc not found. Long_description conversion failure.")
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()
setup(
    name='twocaptcha-wrapper',
    version='0.1.0',
    packages=['twocaptcha'],
    package_dir={'twocaptcha': 'src/twocaptcha'},
    install_requires=['requests', 'simplejson'],
    description='2Captcha Wrapper - ReCaptchaV2 token based',
    long_description=long_description,
    author='Tiago Cardoso',
    author_email='tiagocardosoweb@gmail.com',
    url='https://github.com/tiagocardosoweb/2captcha-wrapper',
    download_url='https://github.com/tiagocardosoweb/2captcha-wrapper/tarball/0.1',
    keywords=['2captcha', 'captcha', 'Image Recognition', 'reRecaptcha', 'reRecaptcha V2'],
    classifiers=["Topic :: Scientific/Engineering :: Image Recognition"],
)