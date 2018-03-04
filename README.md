# What is it?
Django template for cookiecutter.

Using vagrant and ansible for quiking local deployment of the new project.

List of items:
* Python 3.6
* Django 2.0
* Django REST Framework 3.7
* JWT
* PostgreSQL 9.6
* PostGIS 2.3
* Memcached
* RabbitMQ latest
* Redis latest
* ElasticSearch 6.2.2

## Dependencies Installation
For project installation you need Vagrant, VirtualBox, cookiecutter, git.

Check whether these components are installed.

If these components have not installed, please install them.

## VirtualBox Installation
Download the latest version from the website 
[Virtualbox](https://www.virtualbox.org/wiki/Downloads)  or use the package manager.

### Linux:

* ``sudo apt-get update``
* ``sudo apt-get install virtualbox``
* ``sudo apt-get install virtualbox-dkms``

### Mac OS:

* ``brew cask install virtualbox``

Vagrant installation
====================

### Linux:

Don't try install vagrant from official OS repositories.
Use [official site](https://www.vagrantup.com/downloads.html).

Then install nfs-utils

* ``sudo apt-get update``
* ``sudo apt-get install nfs-utils nfs-utils-lib``

If the last doesn't work use these commands

* ``sudo apt-get install nfs-kernel-server``
* ``sudo apt-get install nfs-common``
* ``sudo service nfs-kernel-server start``

### Сookiecutter installation

* ``sudo pip install -U cookiecutter``

### Ansible installation

#### For linux:

* ``sudo apt-get install software-properties-common``
* ``sudo apt-add-repository ppa:ansible/ansible``
* ``sudo apt-get update``
* ``sudo apt-get install ansible``

#### For MacOS:

* ``sudo easy_install pip`` 
* ``sudo pip install ansible`` 

If you are installing on OS X Mavericks, you may encounter some noise from your compiler. 
A workaround is to do the following:
* ``sudo CFLAGS=-Qunused-arguments CPPFLAGS=-Qunused-arguments pip install ansible`` 


### Git installation

Use instruction from [official site](https://git-scm.com/book/en/v1/Getting-Started-Installing-Git)

### Linux:

* ``$ sudo apt-get install git``

### Mac OS:

* ``$ brew install git``

### Project template installation

For project installation we use cookiecutter. Execute the following command:

* ``$ cookiecutter https://github.com/digitalashes/django2.0-template.git``

Then follow instructions from command line.

The template includes ansible configuration, choose roles, necessary for the project.

### Start project

* ``$ vagrant up``
* ``$ vagrant ssh``
* ``$ cd /vagrant``
* ``$ python manage.py runserver 0.0.0.0:8000``

### Git initialisation

* ``$ git init``
* ``$ git remote add origin {{ repo_url }}``
* ``$ git add -A``
* ``$ git commit -m "Init commit"``
* ``$ git push origin -u master``
