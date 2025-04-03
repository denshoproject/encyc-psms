PROJECT=encycpsms
APP=psms
USER=encyc
SHELL = /bin/bash

APP_VERSION := $(shell cat VERSION)
GIT_SOURCE_URL=https://github.com/densho/encyc-psms

# current branch name minus dashes or underscores
PACKAGE_BRANCH := $(shell git rev-parse --abbrev-ref HEAD | tr -d _ | tr -d -)
# current commit hash
PACKAGE_COMMIT := $(shell git log -1 --pretty="%h")
# current commit date minus dashes
PACKAGE_TIMESTAMP := $(shell git log -1 --pretty="%ad" --date=short | tr -d -)

PACKAGE_SERVER=ddr.densho.org/static/encycpsms

SRC_REPO_VOCAB=https://github.com/denshoproject/densho-vocab

INSTALL_BASE=/opt
INSTALLDIR=$(INSTALL_BASE)/encyc-psms
INSTALL_VOCAB=/opt/densho-vocab
DOWNLOADS_DIR=/tmp/$(APP)-install
PIP_REQUIREMENTS=$(INSTALLDIR)/requirements.txt
PIP_CACHE_DIR=$(INSTALL_BASE)/pip-cache

VIRTUALENV=$(INSTALLDIR)/venv/$(APP)

CONF_BASE=/etc/encyc
CONF_PRODUCTION=$(CONF_BASE)/psms.cfg
CONF_LOCAL=$(CONF_BASE)/psms-local.cfg
CONF_SECRET=$(CONF_BASE)/psms-secret-key.txt

LOG_BASE=/var/log/encyc

MEDIA_BASE=/var/www/encycpsms
MEDIA_ROOT=$(MEDIA_BASE)/media
STATIC_ROOT=$(MEDIA_BASE)/static

SUPERVISOR_GUNICORN_CONF=/etc/supervisor/conf.d/encycpsms.conf
NGINX_APP_CONF=/etc/nginx/sites-available/encycpsms.conf
NGINX_APP_CONF_LINK=/etc/nginx/sites-enabled/encycpsms.conf

# Release name e.g. jessie
DEBIAN_CODENAME := $(shell lsb_release -sc)
# Release numbers e.g. 8.10
DEBIAN_RELEASE := $(shell lsb_release -sr)
# Sortable major version tag e.g. deb8
DEBIAN_RELEASE_TAG = deb$(shell lsb_release -sr | cut -c1)

TGZ_BRANCH := $(shell python3 bin/package-branch.py)
TGZ_FILE=$(PROJECT)_$(APP_VERSION)
TGZ_DIR=$(INSTALLDIR)/$(TGZ_FILE)
TGZ_PSMS=$(TGZ_DIR)/encyc-psms
TGZ_VOCAB=$(TGZ_DIR)/densho-vocab

# Adding '-rcN' to VERSION will name the package "ddrlocal-release"
# instead of "ddrlocal-BRANCH"
DEB_BRANCH := $(shell python3 bin/package-branch.py)
DEB_ARCH=amd64
DEB_NAME_BULLSEYE=$(APP)-$(DEB_BRANCH)
DEB_NAME_BOOKWORM=$(APP)-$(DEB_BRANCH)
DEB_NAME_TRIXIE=$(APP)-$(DEB_BRANCH)
# Application version, separator (~), Debian release tag e.g. deb8
# Release tag used because sortable and follows Debian project usage.
DEB_VERSION_BULLSEYE=$(APP_VERSION)~deb11
DEB_VERSION_BOOKWORM=$(APP_VERSION)~deb12
DEB_VERSION_TRIXIE=$(APP_VERSION)~deb13
DEB_FILE_BULLSEYE=$(DEB_NAME_BULLSEYE)_$(DEB_VERSION_BULLSEYE)_$(DEB_ARCH).deb
DEB_FILE_BOOKWORM=$(DEB_NAME_BOOKWORM)_$(DEB_VERSION_BOOKWORM)_$(DEB_ARCH).deb
DEB_FILE_TRIXIE=$(DEB_NAME_TRIXIE)_$(DEB_VERSION_TRIXIE)_$(DEB_ARCH).deb
DEB_VENDOR=Densho.org
DEB_MAINTAINER=<geoffrey.jost@densho.org>
DEB_DESCRIPTION=Encyclopedia Primary Source Management System
DEB_BASE=opt/encyc-psms


.PHONY: help

help:
	@echo "encyc-psms Install Helper"
	@echo ""
	@echo "install - Does a complete install. Idempotent, so run as many times as you like."
	@echo "          IMPORTANT: Run 'adduser encyc' first to install encycddr user and group."
	@echo ""
	@echo "syncdb  - Initialize or update Django app's database tables."
	@echo ""
	@echo "branch BRANCH=[branch] - Switches encyc-psms and supporting repos to [branch]."
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



install: install-app install-configs install-static

test: test-app

uninstall: uninstall-app

clean: clean-app


install-core:
	apt-get --assume-yes install bzip2 curl gdebi-core git-core logrotate ntp p7zip-full python3 wget

git-config:
	git config --global alias.st status
	git config --global alias.co checkout
	git config --global alias.br branch
	git config --global alias.ci commit

install-misc-tools:
	@echo ""
	@echo "Installing miscellaneous tools -----------------------------------------"
	apt-get --assume-yes install ack-grep byobu elinks htop iftop iotop mg multitail


install-daemons: install-mariadb install-nginx install-redis install-supervisor

remove-daemons: remove-mariadb remove-nginx remove-redis remove-supervisor

install-nginx:
	@echo ""
	@echo "Nginx ------------------------------------------------------------------"
	apt-get --assume-yes install nginx

remove-nginx:
	apt-get --assume-yes remove nginx

install-mariadb:
	@echo ""
	@echo "MariaDB ----------------------------------------------------------------"
	apt-get --assume-yes install mariadb-server mariadb-client libmariadb-dev

remove-mariadb:
	apt-get --assume-yes remove mariadb-server mariadb-client libmariadb-dev

install-redis:
	@echo ""
	@echo "Redis ------------------------------------------------------------------"
	apt-get --assume-yes install redis-server

remove-redis:
	apt-get --assume-yes remove redis-server

install-supervisor:
	@echo ""
	@echo "Supervisor -------------------------------------------------------------"
	apt-get --assume-yes install supervisor

remove-supervisor:
	apt-get --assume-yes remove supervisor


install-virtualenv:
	@echo ""
	@echo "install-virtualenv -----------------------------------------------------"
	apt-get --assume-yes install python3-pip python3-venv
	python3 -m venv $(VIRTUALENV)
	source $(VIRTUALENV)/bin/activate; \
	pip3 install -U --cache-dir=$(PIP_CACHE_DIR) uv

install-setuptools: install-virtualenv
	@echo ""
	@echo "install-setuptools -----------------------------------------------------"
	apt-get --assume-yes install python3-dev
	source $(VIRTUALENV)/bin/activate; \
	uv pip install -U --cache-dir=$(PIP_CACHE_DIR) setuptools


install-app: install-encyc-psms

test-app: test-encyc-psms

uninstall-app: uninstall-encyc-psms

clean-app: clean-encyc-psms


git-safe-dir:
	@echo ""
	@echo "git-safe-dir -----------------------------------------------------------"
	sudo -u encyc git config --global --add safe.directory $(INSTALLDIR)

install-encyc-psms: install-configs install-setuptools git-safe-dir
	@echo ""
	@echo "encyc-psms --------------------------------------------------------------"
	apt-get --assume-yes install imagemagick libjpeg-dev $(LIBMARIADB_PKG) libxml2 libxslt1.1 libxslt1-dev python3-dev default-libmysqlclient-dev build-essential pkg-config
	source $(VIRTUALENV)/bin/activate; uv pip install --cache-dir=$(PIP_CACHE_DIR) .
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
	chown -R encyc.root $(MEDIA_ROOT)
	chmod -R 755 $(MEDIA_ROOT)

install-encyc-psms-testing: install-setuptools
	@echo ""
	@echo "install-encyc-psms-testing -------------------------------------------------------"
	source $(VIRTUALENV)/bin/activate; \
	uv pip install --cache-dir=$(PIP_CACHE_DIR) .[testing]

test-encyc-psms: test-encyc-psms-api test-encyc-psms-sources

test-encyc-psms-api:
	@echo ""
	@echo "test-encyc-psms-api -----------------------------------------------------"
	source $(VIRTUALENV)/bin/activate; \
	cd $(INSTALLDIR)/; pytest --disable-warnings psms/psms/

test-encyc-psms-sources:
	@echo ""
	@echo "test-encyc-psms-sources -------------------------------------------------"
	source $(VIRTUALENV)/bin/activate; \
	cd $(INSTALLDIR)/; pytest --disable-warnings --reuse-db psms/sources/

syncdb:
	cd $(INSTALLDIR)/psms
	source $(VIRTUALENV)/bin/activate; \
	python manage.py syncdb --noinput
	chown -R psms.root /var/log/encyc
	chmod -R 755 /var/log/encyc

uninstall-encyc-psms:
	cd $(INSTALLDIR)/psms
	source $(VIRTUALENV)/bin/activate; \
	-pip3 uninstall -r $(INSTALLDIR)/requirements.txt
	-rm /usr/local/lib/python2.7/dist-packages/psms-*
	-rm -Rf /usr/local/lib/python2.7/dist-packages/psms

restart-psms:
	/etc/init.d/supervisor restart psms

shell:
	source $(VIRTUALENV)/bin/activate; \
	python psms/manage.py shell

runserver:
	source $(VIRTUALENV)/bin/activate; \
	python psms/manage.py runserver 0.0.0.0:8082

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
	python3 -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))' > $(CONF_SECRET)
	chown encyc.encyc $(CONF_SECRET)
	chmod 640 $(CONF_SECRET)
# web app settings
	cp $(INSTALLDIR)/conf/psms.cfg $(CONF_BASE)
	chown root.encyc $(CONF_PRODUCTION)
	chmod 640 $(CONF_PRODUCTION)
	touch $(CONF_LOCAL)
	chown root.encyc $(CONF_LOCAL)
	chmod 640 $(CONF_LOCAL)

uninstall-configs:
	-rm $(CONF_PRODUCTION)
	-rm $(CONF_LOCAL)
	-rm $(CONF_SECRET)

install-daemons-configs:
	@echo ""
	@echo "configuring daemons -------------------------------------------------"
# nginx
	cp $(INSTALLDIR)/conf/nginx.conf $(NGINX_APP_CONF)
	chown root.root $(NGINX_APP_CONF)
	chmod 644 $(NGINX_APP_CONF)
	-ln -s $(NGINX_APP_CONF) $(NGINX_APP_CONF_LINK)
	-rm /etc/nginx/sites-enabled/default
# supervisord
	cp $(INSTALLDIR)/conf/supervisor.conf $(SUPERVISOR_GUNICORN_CONF)
	chown root.root $(SUPERVISOR_GUNICORN_CONF)
	chmod 644 $(SUPERVISOR_GUNICORN_CONF)

uninstall-daemons-configs:
	-rm $(NGINX_APP_CONF_LINK) 
	-rm $(NGINX_APP_CONF) 
	-rm $(SUPERVISOR_GUNICORN_CONF)


install-static: collectstatic install-restframework install-swagger

clean-static: clean-restframework clean-swagger

collectstatic:
	@echo ""
	@echo "collectstatic -------------------------------------------------------"
	source $(VIRTUALENV)/bin/activate; \
	python $(INSTALLDIR)/psms/manage.py collectstatic --noinput

install-restframework:
	@echo ""
	@echo "rest-framework assets ---------------------------------------------------"
	-mkdir -p $(MEDIA_BASE)
	cp -R $(VIRTUALENV)/lib/$(PYTHON_VERSION)/site-packages/rest_framework/static/rest_framework/ $(STATIC_ROOT)/

install-swagger:
	@echo ""
	@echo "rest-swagger assets -----------------------------------------------------"
	-mkdir -p $(MEDIA_BASE)
	cp -R $(VIRTUALENV)/lib/$(PYTHON_VERSION)/site-packages/drf_yasg/static/drf-yasg/ $(STATIC_ROOT)/

clean-restframework:
	-rm -Rf $(STATIC_ROOT)/rest_framework/

clean-swagger:
	-rm -Rf $(STATIC_ROOT)/drf_yasg/


tgz-local:
	rm -Rf $(TGZ_DIR)
	git clone $(INSTALLDIR) $(TGZ_PSMS)
	git clone $(INSTALL_VOCAB) $(TGZ_VOCAB)
	cd $(TGZ_PSMS); git checkout develop; git checkout master
#	cd $(TGZ_VOCAB); git checkout develop; git checkout master
	tar czf $(TGZ_FILE).tgz $(TGZ_FILE)
	rm -Rf $(TGZ_DIR)

tgz:
	rm -Rf $(TGZ_DIR)
	git clone $(GIT_SOURCE_URL) $(TGZ_PSMS)
	git clone $(SRC_REPO_VOCAB) $(TGZ_VOCAB)
	cd $(TGZ_PSMS); git checkout develop; git checkout master
#	cd $(TGZ_VOCAB); git checkout develop; git checkout master
	tar czf $(TGZ_FILE).tgz $(TGZ_FILE)
	rm -Rf $(TGZ_DIR)


# http://fpm.readthedocs.io/en/latest/
install-fpm:
	@echo "install-fpm ------------------------------------------------------------"
	apt-get install --assume-yes ruby ruby-dev rubygems build-essential
	gem install --no-document fpm

# https://stackoverflow.com/questions/32094205/set-a-custom-install-directory-when-making-a-deb-package-with-fpm
# https://brejoc.com/tag/fpm/
deb: deb-bullseye

deb-bullseye:
	@echo ""
	@echo "FPM packaging (bullseye) -----------------------------------------------"
	-rm -Rf $(DEB_FILE_BULLSEYE)
# Make package
	fpm   \
	--verbose   \
	--input-type dir   \
	--output-type deb   \
	--name $(DEB_NAME_BULLSEYE)   \
	--version $(DEB_VERSION_BULLSEYE)   \
	--package $(DEB_FILE_BULLSEYE)   \
	--url "$(GIT_SOURCE_URL)"   \
	--vendor "$(DEB_VENDOR)"   \
	--maintainer "$(DEB_MAINTAINER)"   \
	--description "$(DEB_DESCRIPTION)"   \
	--deb-recommends "mariadb-client"   \
	--deb-suggests "mariadb-server"   \
	--depends "libmariadbclient-dev"  \
	--depends "build-essential" \
	--depends "default-libmysqlclient-dev" \
	--depends "python3-dev" \
	--depends "pkg-config" \
	--depends "nginx"   \
	--depends "redis-server"   \
	--depends "supervisor"   \
	--chdir $(INSTALLDIR)   \
	conf=$(DEB_BASE)   \
	COPYRIGHT=$(DEB_BASE)   \
	debian=$(DEB_BASE)   \
	.git=$(DEB_BASE)   \
	.gitignore=$(DEB_BASE)   \
	INSTALL.rst=$(DEB_BASE)   \
	LICENSE=$(DEB_BASE)   \
	Makefile=$(DEB_BASE)   \
	NOTES=$(DEB_BASE)   \
	psms=$(DEB_BASE)  \
	pyproject.toml=$(DEB_BASE)  \
	README.rst=$(DEB_BASE)   \
	static=var/www/encycpsms  \
	venv=$(DEB_BASE)   \
	VERSION=$(DEB_BASE)  \
	conf/psms.cfg=etc/encyc/psms.cfg

deb-bookworm:
	@echo ""
	@echo "FPM packaging (bookworm) -----------------------------------------------"
	-rm -Rf $(DEB_FILE_BOOKWORM)
# Make package
	fpm   \
	--verbose   \
	--input-type dir   \
	--output-type deb   \
	--name $(DEB_NAME_BOOKWORM)   \
	--version $(DEB_VERSION_BOOKWORM)   \
	--package $(DEB_FILE_BOOKWORM)   \
	--url "$(GIT_SOURCE_URL)"   \
	--vendor "$(DEB_VENDOR)"   \
	--maintainer "$(DEB_MAINTAINER)"   \
	--description "$(DEB_DESCRIPTION)"   \
	--deb-recommends "mariadb-client"   \
	--deb-suggests "mariadb-server"   \
	--depends "libmariadb-dev"  \
	--depends "build-essential" \
	--depends "default-libmysqlclient-dev" \
	--depends "python3-dev" \
	--depends "pkg-config" \
	--depends "nginx"   \
	--depends "redis-server"   \
	--depends "supervisor"   \
	--chdir $(INSTALLDIR)   \
	conf=$(DEB_BASE)   \
	COPYRIGHT=$(DEB_BASE)   \
	debian=$(DEB_BASE)   \
	.git=$(DEB_BASE)   \
	.gitignore=$(DEB_BASE)   \
	INSTALL.rst=$(DEB_BASE)   \
	LICENSE=$(DEB_BASE)   \
	Makefile=$(DEB_BASE)   \
	NOTES=$(DEB_BASE)   \
	psms=$(DEB_BASE)  \
	pyproject.toml=$(DEB_BASE)  \
	README.rst=$(DEB_BASE)   \
	static=var/www/encycpsms  \
	venv=$(DEB_BASE)   \
	VERSION=$(DEB_BASE)  \
	conf/psms.cfg=etc/encyc/psms.cfg

deb-trixie:
	@echo ""
	@echo "FPM packaging (trixie) -----------------------------------------------"
	-rm -Rf $(DEB_FILE_TRIXIE)
# Make package
	fpm   \
	--verbose   \
	--input-type dir   \
	--output-type deb   \
	--name $(DEB_NAME_TRIXIE)   \
	--version $(DEB_VERSION_TRIXIE)   \
	--package $(DEB_FILE_TRIXIE)   \
	--url "$(GIT_SOURCE_URL)"   \
	--vendor "$(DEB_VENDOR)"   \
	--maintainer "$(DEB_MAINTAINER)"   \
	--description "$(DEB_DESCRIPTION)"   \
	--deb-recommends "mariadb-client"   \
	--deb-suggests "mariadb-server"   \
	--depends "libmariadb-dev"  \
	--depends "build-essential" \
	--depends "default-libmysqlclient-dev" \
	--depends "python3-dev" \
	--depends "pkg-config" \
	--depends "nginx"   \
	--depends "redis-server"   \
	--depends "supervisor"   \
	--chdir $(INSTALLDIR)   \
	conf=$(DEB_BASE)   \
	COPYRIGHT=$(DEB_BASE)   \
	debian=$(DEB_BASE)   \
	.git=$(DEB_BASE)   \
	.gitignore=$(DEB_BASE)   \
	INSTALL.rst=$(DEB_BASE)   \
	LICENSE=$(DEB_BASE)   \
	Makefile=$(DEB_BASE)   \
	NOTES=$(DEB_BASE)   \
	psms=$(DEB_BASE)  \
	pyproject.toml=$(DEB_BASE)  \
	README.rst=$(DEB_BASE)   \
	static=var/www/encycpsms  \
	venv=$(DEB_BASE)   \
	VERSION=$(DEB_BASE)  \
	conf/psms.cfg=etc/encyc/psms.cfg
