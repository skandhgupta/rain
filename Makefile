dep := dep
ven := ven
patch := $(dep)/patch

config := $(or $(wildcard .Makefile.config), \
	$(error Please run ./configure before make))
include $(config)

.PHONY: all $(povray)
all: $(povray)

povray: $(ven)/bin/povray
$(ven)/bin/povray: $(ven)
	tar -xzf $(dep)/povlinux-3.6.tgz -C $(ven)/tmp
	patch $(ven)/tmp/povray-3.6/install < $(patch)/povray-set-default-dir.patch
	cd $(ven)/tmp/povray-3.6 && ./install >../povinstall.log

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
	mkdir $(ven)/tmp

