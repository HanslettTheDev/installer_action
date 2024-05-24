# Steps to recreate the github installers

1.  Design a basic NSIS installer
2.  Test the basic NSIS installer using the nsis command line tool
3.  Write a small yaml config that downloads makensis from the official website and then runs
    the command
4.  build the installler and add it as a release artifact
5.  Improve the nsis installer to allow freedom to customize
6.  Test the capabilities of it in an actual project

End goal-> Yaml file that builds an installer for an existing executable
