SHELL = /bin/bash

PACKAGE_SERVER=tank.densho.org

PIP_CACHE_DIR=/usr/local/src/pip-cache
VIRTUALENV=/usr/local/src/env/psms
INSTALLDIR=/usr/local/src/encyc-psms
MEDIA_BASE=/var/www/html/psms
MEDIA_ROOT=$(MEDIA_BASE)/media
STATIC_ROOT=$(MEDIA_BASE)/static

.PHONY: help

help:
	@echo "encyc-psms Install Helper"
	@echo "See: make howto-install"

help-all:
	@echo "install - Do a fresh install"

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
	@echo "    # git clone git@github.com:densho/encyc-psms.git /usr/local/src/encyc-psms"
	@echo "    # cd /usr/local/src/encyc-psms/psms"
	@echo ""
	@echo "If not running the master branch, switch to it now::"
	@echo ""
	@echo "    # git checkout -b develop origin/develop && git pull"
	@echo ""
	@echo "Install encyc-psms software, dependencies, and configs::"
	@echo ""
	@echo "    # make install"
	@echo ""
	@echo "Adjust configs to fit the local environment. Values in /etc/encyc/psms-local.cfg"
	@echo "override those in psms.cfg::"
	@echo ""
	@echo "    # vi /etc/encyc/psms-local.cfg"
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



install: install-prep install-daemons install-psms install-static install-configs

update: update-psms

uninstall: uninstall-psms

clean: clean-psms


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


install-daemons: install-nginx install-mysql install-memcached

install-nginx:
	@echo ""
	@echo "Nginx ------------------------------------------------------------------"
	apt-get --assume-yes install nginx

install-mysql:
	@echo ""
	@echo "MySQL ------------------------------------------------------------------"
	apt-get --assume-yes install mysql-server mysql-client

install-memcached:
	@echo ""
	@echo "Memcached --------------------------------------------------------------"
	apt-get --assume-yes install memcached


install-psms: install-encyc-psms

update-psms: update-encyc-psms install-configs

uninstall-psms: uninstall-encyc-psms

clean-psms: clean-encyc-psms


install-encyc-psms:
	@echo ""
	@echo "encyc-psms --------------------------------------------------------------"
#	apt-get --assume-yes install imagemagick libjpeg62-turbo-dev libxml2 libxslt1.1 libxslt1-dev python-dev python-pip python-virtualenv supervisor zlib1g-dev
	apt-get --assume-yes install imagemagick libjpeg-dev libmysqlclient-dev libxml2 libxslt1.1 libxslt1-dev python-dev python-pip python-virtualenv supervisor
	test -d $(VIRTUALENV) || virtualenv $(VIRTUALENV)
	source $(VIRTUALENV)/bin/activate; \
	pip install -U --download-cache=$(PIP_CACHE_DIR) setuptools
	source $(VIRTUALENV)/bin/activate; \
	pip install -U --download-cache=$(PIP_CACHE_DIR) -r $(INSTALLDIR)/psms/requirements/production.txt
	-mkdir /var/log/encyc
	chown -R psms.root /var/log/encyc
	chmod -R 755 /var/log/encyc
	-mkdir -p $(MEDIA_ROOT)
	-mkdir -p $(STATIC_ROOT)
	chown -R psms.root $(STATIC_ROOT)
	chmod -R 755 $(STATIC_ROOT)
	cp -R $(INSTALLDIR)/psms/tansu/static/tansu/* $(STATIC_ROOT)/
	chown -R psms.root $(MEDIA_BASE)
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
	pip install -U --download-cache=$(PIP_CACHE_DIR) -r $(INSTALLDIR)/psms/requirements/production.txt

uninstall-encyc-psms:
	cd $(INSTALLDIR)/psms
	source $(VIRTUALENV)/bin/activate; \
	-pip uninstall -r $(INSTALLDIR)/psms/requirements/production.txt
	-rm /usr/local/lib/python2.7/dist-packages/psms-*
	-rm -Rf /usr/local/lib/python2.7/dist-packages/psms

restart-psms:
	/etc/init.d/supervisor restart psms

clean-encyc-psms:
	-rm -Rf $(INSTALLDIR)/psms/env/
	-rm -Rf $(INSTALLDIR)/psms/src

clean-pip:
	-rm -Rf $(PIP_CACHE_DIR)/*


install-static: 

clean-static:


install-configs:
	@echo ""
	@echo "installing configs ----------------------------------------------------"
# web app settings - psms.cfg
	-mkdir /etc/encyc
	cp $(INSTALLDIR)/debian/conf/psms.cfg /etc/encyc/
	chown root.psms /etc/encyc/psms.cfg
	chmod 640 /etc/encyc/psms.cfg
	touch /etc/encyc/psms-local.cfg
	chown root.psms /etc/encyc/psms-local.cfg
	chmod 640 /etc/encyc/psms-local.cfg
# web app settings - settings.py
	cp $(INSTALLDIR)/debian/conf/settings.py $(INSTALLDIR)/psms/
	chown root.root $(INSTALLDIR)/psms/settings.py
	chmod 644 $(INSTALLDIR)/psms/settings.py
# supervisord - gunicorn_psms.conf
	cp $(INSTALLDIR)/debian/conf/gunicorn_psms.conf /etc/supervisor/conf.d/
	chown root.root /etc/supervisor/conf.d/gunicorn_psms.conf
	chmod 644 /etc/supervisor/conf.d/gunicorn_psms.conf
# nginx settings - psms.conf
	cp $(INSTALLDIR)/debian/conf/psms.conf /etc/nginx/sites-available
	chown root.root /etc/nginx/sites-available/psms.conf
	chmod 644 /etc/nginx/sites-available/psms.conf
	-ln -s /etc/nginx/sites-available/psms.conf /etc/nginx/sites-enabled/psms.conf
	-rm /etc/nginx/sites-enabled/default

uninstall-configs:
	-rm /etc/nginx/sites-available/psms.conf
	-rm /etc/nginx/sites-enabled/psms.conf
	-rm /etc/supervisor/conf.d/gunicorn_psms.conf
	-rm $(INSTALLDIR)/psms/settings.py
	-rm /etc/encyc/psms.conf


reload: reload-nginx reload-supervisor

reload-nginx:
	/etc/init.d/nginx reload

reload-supervisor:
	supervisorctl reload


restart: restart-nginx restart-mysql restart-memcached restart-supervisor

restart-nginx:
	/etc/init.d/nginx restart

restart-mysql:
	/etc/init.d/mysql restart

restart-memcached:
	/etc/init.d/memcached restart

restart-supervisor:
	/etc/init.d/supervisor restart


status:
	@echo [`systemctl is-active nginx`] nginx
	@echo [`systemctl is-active mysql`] mysql
	@echo [`systemctl is-active memcached`] memcached
	@echo [`systemctl is-active supervisor`] supervisor
	@supervisorctl status

git-status:
	@echo "------------------------------------------------------------------------"
	cd $(INSTALLDIR) && git status
