PROJECT=encyc
APP=encycpsms
USER=encyc

SHELL = /bin/bash
DEBIAN_CODENAME := $(shell lsb_release -sc)
DEBIAN_RELEASE := $(shell lsb_release -sr)
VERSION := $(shell cat VERSION)

GIT_SOURCE_URL=https://github.com/densho/encyc-psms
PACKAGE_SERVER=ddr.densho.org/static/encycpsms

INSTALL_BASE=/opt
INSTALLDIR=$(INSTALL_BASE)/encyc-psms
DOWNLOADS_DIR=/tmp/$(APP)-install
REQUIREMENTS=$(INSTALLDIR)/requirements.txt
PIP_CACHE_DIR=$(INSTALL_BASE)/pip-cache

VIRTUALENV=$(INSTALLDIR)/venv/psms
SETTINGS=$(INSTALLDIR)/psms/settings.py

CONF_BASE=/etc/encyc
CONF_PRODUCTION=$(CONF_BASE)/psms.cfg
CONF_LOCAL=$(CONF_BASE)/psms-local.cfg
CONF_SECRET=$(CONF_BASE)/psms-secret-key.txt

LOG_BASE=/var/log/encyc

MEDIA_BASE=/var/www/encycpsms
MEDIA_ROOT=$(MEDIA_BASE)/media
STATIC_ROOT=$(MEDIA_BASE)/static

SUPERVISOR_CONF=/etc/supervisor/conf.d/psms.conf
NGINX_CONF=/etc/nginx/sites-available/psms.conf
NGINX_CONF_LINK=/etc/nginx/sites-enabled/psms.conf

FPM_BRANCH := $(shell git rev-parse --abbrev-ref HEAD | tr -d _ | tr -d -)
FPM_ARCH=amd64
FPM_NAME=$(APP)-$(FPM_BRANCH)
FPM_FILE=$(FPM_NAME)_$(VERSION)_$(FPM_ARCH).deb
FPM_VENDOR=Densho.org
FPM_MAINTAINER=<geoffrey.jost@densho.org>
FPM_DESCRIPTION=Encyclopedia Primary Source Management System
FPM_BASE=opt/encyc-psms


.PHONY: help

help:
	@echo "encyc-psms Install Helper"
	@echo ""
	@echo "install - Does a complete install. Idempotent, so run as many times as you like."
	@echo "          IMPORTANT: Run 'adduser encyc' first to install encycddr user and group."
	@echo ""
	@echo "syncdb  - Initialize or update Django app's database tables."
	@echo ""
	@echo "update  - Updates ddr-workbench and re-copies config files."
	@echo ""
	@echo "branch BRANCH=[branch] - Switches encyc-psms and supporting repos to [branch]."
	@echo ""
	@echo "reload  - Reloads supervisord and nginx configs"
	@echo "reload-nginx"
	@echo "reload-supervisors"
	@echo ""
	@echo "restart - Restarts all servers"
	@echo "restart-redis"
	@echo "restart-nginx"
	@echo "restart-supervisord"
	@echo ""
	@echo "status  - Server status"
	@echo ""
	@echo "uninstall - Deletes 'compiled' Python files. Leaves build dirs and configs."
	@echo "clean   - Deletes files created by building the program. Leaves configs."
	@echo ""
	@echo "See also: make howto-install, make help-all"
	@echo ""

help-all:
	@echo "install - Do a fresh install"
	@echo "install-prep    - git-config, add-user, apt-update, install-misc-tools"
	@echo "install-app     - install-encyc-psms"
	@echo "install-configs - "
	@echo "install-static  - "
	@echo "install-daemons - install-nginx install-redis"
	@echo "install-daemons-configs"
	@echo "update  - Do an update"
	@echo "restart - Restart servers"
	@echo "status  - Server status"
	@echo "update-ddr - "
	@echo "uninstall - "
	@echo "clean - "

howto-install:
	@echo "Installation"
	@echo "============"
	@echo ""
	@echo "Basic Debian server netinstall; see ddr-manual."
	@echo "Install SSH keys for root."
	@echo "(see https://help.github.com/articles/generating-ssh-keys/)::"
	@echo ""
	@echo "    # ssh-keygen -t rsa -b 4096 -C \"your_email@example.com\""
	@echo "    # cat ~/.ssh/id_rsa.pub"
	@echo "    Cut and paste public key into GitHub."
	@echo "    # ssh -T git@github.com"
	@echo ""
	@echo "Prepare for install::"
	@echo ""
	@echo "    # apt-get install make"
	@echo "    # adduser psms"
	@echo "    # git clone git@github.com:densho/encyc-psms.git $(INSTALL_BASE)/encyc-psms"
	@echo "    # cd $(INSTALL_BASE)/encyc-psms/psms"
	@echo ""
	@echo "If not running the master branch, switch to it now::"
	@echo ""
	@echo "    # git checkout -b develop origin/develop && git pull"
	@echo ""
	@echo "Install encyc-psms software, dependencies, and configs::"
	@echo ""
	@echo "    # make install"
	@echo ""
	@echo "Adjust configs to fit the local environment. Values in $(CONF_LOCAL)"
	@echo "override those in $(CONF_PRODUCTION)::"
	@echo ""
	@echo "    # vi $(CONF_LOCAL)"
	@echo ""
	@echo "Reload an existing database::"
	@echo ""
	@echo "	   # mysql -p -u root psms < DATABASE_BACKUP_FILE.mysql"
	@echo ""
	@echo "Or create a new database::"
	@echo ""
	@echo "	   # mysql -p -u root"
	@echo "    mysql> create database psms;"
	@echo "    mysql> grant all privileges on psms.* to psms@localhost identified by 'PASSWORD';"
	@echo "    mysql> flush privileges;"
	@echo "    mysql> update django_site set domain='10.0.4.15:8000', name='densho front' where id=1;"
	@echo "    mysql> insert into django_site (domain, name) values ('10.0.4.15:8080', 'densho psms');"
	@echo "    mysql> exit"
	@echo ""
	@echo "...or reload an existing one::"
	@echo ""
	@echo "	   # mysql -p -u root psms < DATABASE_BACKUP_FILE.mysql"
	@echo ""
	@echo "Apply any database updates that need applying::"
	@echo ""
	@echo "    # make syncdb"
	@echo ""
	@echo "Insert some records::"
	@echo ""
	@echo "	   # mysql -p -u root"
	@echo "    mysql> use psms;"
	@echo "    mysql> update django_site set domain='10.0.4.15:8000', name='densho front' where id=1;"
	@echo "    mysql> insert into django_site (domain, name) values ('10.0.4.15:8080', 'densho psms');"
	@echo "    mysql> exit"
	@echo ""
	@echo "Restart::"
	@echo ""
	@echo "    # make restart"
	@echo "    # make status"



install: install-prep install-app install-configs install-static

update: update-app

uninstall: uninstall-app

clean: clean-app


install-prep: apt-update install-core git-config install-misc-tools


apt-update:
	@echo ""
	@echo "Package update ---------------------------------------------------------"
	apt-get --assume-yes update

apt-upgrade:
	@echo ""
	@echo "Package upgrade --------------------------------------------------------"
	apt-get --assume-yes upgrade

install-core:
	apt-get --assume-yes install bzip2 curl gdebi-core git-core logrotate ntp p7zip-full wget

git-config:
	git config --global alias.st status
	git config --global alias.co checkout
	git config --global alias.br branch
	git config --global alias.ci commit

install-misc-tools:
	@echo ""
	@echo "Installing miscellaneous tools -----------------------------------------"
	apt-get --assume-yes install ack-grep byobu elinks htop iftop iotop mg multitail


install-daemons: install-nginx install-redis install-supervisor

install-nginx:
	@echo ""
	@echo "Nginx ------------------------------------------------------------------"
	apt-get --assume-yes install nginx

install-mysql:
	@echo ""
	@echo "MySQL ------------------------------------------------------------------"
	apt-get --assume-yes install mysql-server mysql-client

install-redis:
	@echo ""
	@echo "Redis ------------------------------------------------------------------"
	apt-get --assume-yes install redis-server

install-supervisor:
	@echo ""
	@echo "Supervisor -------------------------------------------------------------"
	apt-get --assume-yes install supervisor


install-virtualenv:
	apt-get --assume-yes install python-pip python-virtualenv
	test -d $(VIRTUALENV) || virtualenv --distribute --setuptools $(VIRTUALENV)

install-setuptools: install-virtualenv
	@echo ""
	@echo "install-setuptools -----------------------------------------------------"
	apt-get --assume-yes install python-dev
	source $(VIRTUALENV)/bin/activate; \
	pip install -U --download-cache=$(PIP_CACHE_DIR) bpython setuptools


install-app: install-encyc-psms

update-app: update-encyc-psms install-configs

uninstall-app: uninstall-encyc-psms

clean-app: clean-encyc-psms


install-encyc-psms: install-virtualenv install-setuptools
	@echo ""
	@echo "encyc-psms --------------------------------------------------------------"
	apt-get --assume-yes install imagemagick libjpeg-dev libmysqlclient-dev libxml2 libxslt1.1 libxslt1-dev
	source $(VIRTUALENV)/bin/activate; \
	pip install -U --download-cache=$(PIP_CACHE_DIR) -r $(INSTALLDIR)/requirements/production.txt
# logs dir
	-mkdir $(LOG_BASE)
	chown -R encyc.root $(LOG_BASE)
	chmod -R 755 $(LOG_BASE)
# static dir
	-mkdir -p $(STATIC_ROOT)
	chown -R encyc.root $(STATIC_ROOT)
	chmod -R 755 $(STATIC_ROOT)
# media dir
	-mkdir -p $(MEDIA_ROOT)
	chown -R encyc.root $(MEDIA_BASE)
	chmod -R 755 $(MEDIA_BASE)

syncdb:
	cd $(INSTALLDIR)/psms
	source $(VIRTUALENV)/bin/activate; \
	python manage.py syncdb --noinput
	chown -R psms.root /var/log/encyc
	chmod -R 755 /var/log/encyc

update-encyc-psms:
	@echo ""
	@echo "encyc-psms --------------------------------------------------------------"
	git fetch && git pull
	source $(VIRTUALENV)/bin/activate; \
	pip install -U --download-cache=$(PIP_CACHE_DIR) -r $(INSTALLDIR)/requirements/production.txt

uninstall-encyc-psms:
	cd $(INSTALLDIR)/psms
	source $(VIRTUALENV)/bin/activate; \
	-pip uninstall -r $(INSTALLDIR)/requirements/production.txt
	-rm /usr/local/lib/python2.7/dist-packages/psms-*
	-rm -Rf /usr/local/lib/python2.7/dist-packages/psms

restart-psms:
	/etc/init.d/supervisor restart psms

clean-encyc-psms:
	-rm -Rf $(INSTALLDIR)/psms/env/
	-rm -Rf $(INSTALLDIR)/psms/src

clean-pip:
	-rm -Rf $(PIP_CACHE_DIR)/*


branch:
	cd $(INSTALLDIR)/psms; python ./bin/git-checkout-branch.py $(BRANCH)


install-configs:
	@echo ""
	@echo "installing configs ----------------------------------------------------"
	-mkdir $(CONF_BASE)
	python -c 'import random; print "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])' > $(CONF_SECRET)
	chown encyc.encyc $(CONF_SECRET)
	chmod 640 $(CONF_SECRET)
# web app settings
	cp $(INSTALLDIR)/conf/settings.py $(SETTINGS)
	chown root.root $(SETTINGS)
	chmod 644 $(SETTINGS)
# web app settings
	cp $(INSTALLDIR)/conf/psms.cfg $(CONF_BASE)
	chown root.encyc $(CONF_PRODUCTION)
	chmod 640 $(CONF_PRODUCTION)
	touch $(CONF_LOCAL)
	chown root.encyc $(CONF_LOCAL)
	chmod 640 $(CONF_LOCAL)

uninstall-configs:
	-rm $(SETTINGS)
	-rm $(CONF_PRODUCTION)
	-rm $(CONF_LOCAL)
	-rm $(CONF_SECRET)

install-daemons-configs:
	@echo ""
	@echo "configuring daemons -------------------------------------------------"
# nginx
	cp $(INSTALLDIR)/conf/psms.conf $(NGINX_CONF)
	chown root.root $(NGINX_CONF)
	chmod 644 $(NGINX_CONF)
	-ln -s $(NGINX_CONF) $(NGINX_CONF_LINK)
	-rm /etc/nginx/sites-enabled/default
# supervisord
	cp $(INSTALLDIR)/conf/gunicorn_psms.conf $(SUPERVISOR_CONF)
	chown root.root $(SUPERVISOR_CONF)
	chmod 644 $(SUPERVISOR_CONF)

uninstall-daemons-configs:
	-rm $(NGINX_CONF_LINK) 
	-rm $(NGINX_CONF) 
	-rm $(SUPERVISOR_CONF)


install-static: collectstatic

collectstatic:
	@echo ""
	@echo "collectstatic -------------------------------------------------------"
	source $(VIRTUALENV)/bin/activate; \
	python $(INSTALLDIR)/psms/manage.py collectstatic --noinput


reload: reload-nginx reload-supervisor

reload-nginx:
	/etc/init.d/nginx reload

reload-supervisor:
	supervisorctl reload


restart: restart-nginx restart-mysql restart-redis restart-supervisor

restart-nginx:
	/etc/init.d/nginx restart

restart-mysql:
	/etc/init.d/mysql restart

restart-redis:
	/etc/init.d/redis-server restart

restart-supervisor:
	/etc/init.d/supervisor restart


status:
	@echo [`systemctl is-active nginx`] nginx
	@echo [`systemctl is-active mysql`] mysql
	@echo [`systemctl is-active supervisor`] supervisor
	@supervisorctl status

git-status:
	@echo "------------------------------------------------------------------------"
	cd $(INSTALLDIR) && git status


# http://fpm.readthedocs.io/en/latest/
# https://stackoverflow.com/questions/32094205/set-a-custom-install-directory-when-making-a-deb-package-with-fpm
# https://brejoc.com/tag/fpm/
deb:
	@echo ""
	@echo "FPM packaging ----------------------------------------------------------"
	-rm -Rf $(FPM_FILE)
	virtualenv --python=python3 --relocatable $(VIRTUALENV)  # Make venv relocatable
	fpm   \
	--verbose   \
	--input-type dir   \
	--output-type deb   \
	--name $(FPM_NAME)   \
	--version $(VERSION)   \
	--package $(FPM_FILE)   \
	--url "$(GIT_SOURCE_URL)"   \
	--vendor "$(FPM_VENDOR)"   \
	--maintainer "$(FPM_MAINTAINER)"   \
	--description "$(FPM_DESCRIPTION)"   \
	--depends "mariadb-server"   \
	--depends "mariadb-client"   \
	--depends "redis-server"   \
	--depends "supervisor"   \
	--depends "nginx"   \
	--chdir $(INSTALLDIR)   \
	conf=$(FPM_BASE)   \
	COPYRIGHT=$(FPM_BASE)   \
	debian=$(FPM_BASE)   \
	.git=$(FPM_BASE)   \
	.gitignore=$(FPM_BASE)   \
	INSTALL.rst=$(FPM_BASE)   \
	LICENSE=$(FPM_BASE)   \
	Makefile=$(FPM_BASE)   \
	NOTES=$(FPM_BASE)   \
	psms=$(FPM_BASE)  \
	README.rst=$(FPM_BASE)   \
	requirements=$(FPM_BASE)  \
	venv=$(FPM_BASE)   \
	VERSION=$(FPM_BASE)  \
	conf/psms.cfg=etc/encyc/psms.cfg   \
	conf/gunicorn_psms.conf=etc/supervisor/conf.d/psms.conf \
	conf/psms.conf=etc/nginx/sites-available/psms.conf   \
	conf/settings.py=$(FPM_BASE)/psms
