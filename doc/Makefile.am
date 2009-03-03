man8_MANS = sl2d.man
DISTCLEANFILES = sl2d.man
EXTRA_DIST = sl2d.t2t

SUFFIXES = .t2t

.t2t.man:
	txt2tags -o $@ $<
