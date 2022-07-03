django-skeleton
=======================

**djang-skeleton** is a skeleton for Django projects. It provides a
directory structure for Django projects during development and deployment.


Meta
----
Status:
    maintained, in development

Version:
    0.0.0

Django Version:
    4.0, 3.2, 3.0, 2.2, 2.1, 2.0, 1.11


Usage
-----

To use this repository just use the ``template`` option of `django-admin
<https://docs.djangoproject.com/en/3.2/ref/django-admin/#startproject>`_::

    $ django-admin startproject --template=https://github.com/handyXx/django-skeleton/archive/refs/heads/main.zip [projectname]

If you wish to automagically fill the ``apache2_vhost.sample`` the command is::

    $ django-admin startproject --template=https://github.com/handyXx/django-skeleton/archive/refs/heads/main.zip --name apache2_vhost.sample [projectname]
