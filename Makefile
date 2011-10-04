dep := dep
ven := ven

setup-ven:
	python $(dep)/virtualenv.py \
		--no-site-packages \
		--distribute \
		--extra-search-dir=$(dep) \
		--never-download \
		$(ven)

