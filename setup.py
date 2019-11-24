from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def requires():
    with open('requirements.txt') as f:
        return f.read().split('\n')


setup(name="cloud-ocr",
      version="1.0",
      author="yimian group",
      author_email="data@yimian.com.cn",
      description="Use the same api to call the third party cloud_ocr apis, such as xunfei, baidu.",
      long_description=readme(),
      long_description_content_type="text/markdown",
      url="https://github.com/yimian/cloud-ocr.git",
      packages=['cloud_ocr'],
      install_requires=requires(),
      include_package_data=True,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"
      ],
      python_requires='>=3.6.6',
      zip_safe=False)
