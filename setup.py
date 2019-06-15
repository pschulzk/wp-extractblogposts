import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='wp-extractblogposts',  

     version='0.1',

     scripts=['wp-extractblogposts'] ,

     author="Philip Schulz-Klingauf",

     author_email="",

     description="Extract WordPress blog posts and their featured images ",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/pschulzk/wp-extractblogposts",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 2.7",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )