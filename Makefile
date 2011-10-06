ven := $(shell pwd)/ven
dep := dep
patch := $(dep)/patch
pip := $(ven)/bin/pip
marker := $(ven)/var/install

config := $(or $(wildcard .Makefile.config), \
	$(error Please run ./configure before make))
include $(config)

.PHONY: all povray gevent
all: $(povray) $(gevent) $(marker)/requirements.txt

$(marker)/requirements.txt: $(dep)/requirements.txt | $(ven)
	PIP_DOWNLOAD_CACHE=$(dep) $(pip) install -r $(dep)/requirements.txt
	cp $(dep)/requirements.txt $(marker)/requirements.txt

gevent: $(marker)/gevent
$(marker)/gevent: | $(ven)
	PIP_DOWNLOAD_CACHE=$(dep) $(pip) install greenlet
	tar -xzf $(dep)/libevent-2.0.14-stable.tar.gz -C $(ven)/tmp
	PIP_DOWNLOAD_CACHE=$(dep) $(pip) install \
	   --install-option="--libevent" \
	   --install-option="$(ven)/tmp/libevent-2.0.14-stable" \
	   gevent
	rm $(ven)/tmp/libevent-2.0.14-stable -rf
	touch $(marker)/gevent

# XXX remove 
#
#libevent: $(ven)/include/event.h
#$(ven)/include/event.h: | $(ven)
#	tar -xzf $(dep)/libevent-2.0.14-stable.tar.gz -C $(ven)/tmp
#	cd $(ven)/tmp/libevent-2.0.14-stable && \
#		./configure --prefix=$(ven) -q && \
#		make -s -j `grep -c processor /proc/cpuinfo` && \
#		make -s install
#	rm $(ven)/tmp/libevent-2.0.14-stable -rf
#

povray: $(ven)/bin/povray
$(ven)/bin/povray: | $(ven)
	tar -xzf $(dep)/povlinux-3.6.tgz -C $(ven)/tmp
	patch $(ven)/tmp/povray-3.6/install < $(patch)/povray-set-default-dir.patch
	cd $(ven)/tmp/povray-3.6 && ./install >../povinstall.log
	rm $(ven)/tmp/povray-3.6 -rf

$(ven):
	python $(dep)/virtualenv.py \
		--no-site-packages \
		--distribute \
		--extra-search-dir=$(dep) \
		--never-download \
		$(ven)
	mkdir $(ven)/var
	mkdir $(ven)/var/run
	mkdir $(ven)/var/log
	mkdir $(ven)/var/install
	mkdir $(ven)/tmp

