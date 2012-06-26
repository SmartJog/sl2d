bin_SCRIPTS = \
	sl2d \
	rtp2udp

edit = $(SED) \
	-e 's|@PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g' \
	-e 's|@pkgdatadir[@]|$(pkgdatadir)|g'

$(bin_SCRIPTS): $(bin_SCRIPTS:=.in) Makefile
	$(edit) $(srcdir)/$@.in > $(builddir)/$@

CLEANFILES = $(bin_SCRIPTS)

EXTRA_DIST = $(bin_SCRIPTS:=.in)
