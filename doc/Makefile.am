man8_MANS = sl2d.man
man5_MANS = sl2d.conf.man
DISTCLEANFILES = sl2d.man sl2d.conf.man
EXTRA_DIST = sl2d.t2t sl2d.conf.t2t

SUFFIXES = .t2t

.t2t.man:
	$(TXT2TAGS) -o $@ $<
