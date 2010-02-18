#  Copyright (C) 2010  Chris Martel <accidentalbits@googlemail.com>

#man1_MANS = doc/lyricsgrabber.man

#.PHONY: all install clean dist-clean maintainer-clean dist changelog \
#        tags TAGS rpm rpm-clean release docs docs-clean \
#        www push-www

DIST_NAME=@PACKAGE_TARNAME@-@PACKAGE_VERSION@
MD5SUM=md5sum
SIGNPACKAGE=gpg --detach-sign --armor --local-user "<accidentalbits@googlemail.com>" 
EXTRA_DIST= doc/README.t2t src ChangeLog

all: module docs ChangeLog

module:
	touch src/LyricsGrabber/__init__.py
	${PYTHON} setup.py build
	
install:
	${PYTHON} setup.py install ${SETUP_ARGS}
	
	install -m 755 -d ${docdir}
	install -m 644 README ${docdir}
	install -m 644 AUTHORS ${docdir}
	install -m 644 NEWS ${docdir}
	install -m 644 COPYING ${docdir}
	install -m 644 TODO ${docdir}
	gzip -f -9 ${docdir}/COPYING
	install -m 644 ChangeLog ${docdir}
	gzip -f -9 ${docdir}/ChangeLog

	install -m 755 -d ${mandir}/man1
	install -m 644 doc/lyricsgrabber.1 ${mandir}/man1
	gzip -f -9 ${mandir}/man1/lyricsgrabber.1

uninstall:
	-rm -f ${bindir}/lyricsgrabber
	-rm -rf ${pythondir}/LyricsGrabber
	-rm -rf ${docdir}
	-rm -f ${mandir}/man1/lyricsgrabber.1.gz

docs:
	@if test -f doc/README.t2t; then\
		${MAKE} README;\
		${MAKE} MAN;\
	fi

README: doc/README.t2t
	txt2tags -t txt -o README doc/README.t2t

MAN: doc/README.t2t
	txt2tags -t man -o doc/lyricsgrabber.1 doc/README.t2t

# jumping through some loops to get traditional GNU-style ChangeLog
ChangeLog:
	@if test -d "${srcdir}/.git"; then\
		rm -f ChangeLog &\
		echo Creating ChangeLog &&\
    	git log --date-order --date=short | \
    	sed -e '/^commit.*$$/d' | \
    	awk '/^Author/ {sub(/\\$$/,""); getline t; print $$0 t; next}; 1' | \
    	sed -e 's/^Author: //g' | \
    	sed -e 's/>Date:   \([0-9]*-[0-9]*-[0-9]*\)/>\t\1/g' | \
    	sed -e 's/^\(.*\) \(<.*@.*>\)\t\(.*\)/\3    \1    \2/g' > ${srcdir}/ChangeLog;\
	fi

sign-dist:
#	mkdir -p -m 755 dist/${DIST_NAME}
#	mkdir -p -m 755 dist/${DIST_NAME}/src/LyricsGrabber
#	mkdir -p -m 755 dist/${DIST_NAME}/doc
#	cp AUTHORS Changelog configure.ac COPYING MAKEFILE.am INSTALL \
#	INSTALL.sh MANIFEST.in missing NEWS setup.py.in TODO dist/${DIST_NAME}
#	cp -r src/LyricsGrabber/*.py dist/${DIST_NAME}/src/LyricsGrabber
#	cp src/lyricsgrabber dist/${DIST_NAME}/src
#	cp doc/README dist/${DIST_NAME}/doc
#	cp doc/lyricsgrabber.1 dist/${DIST_NAME}/doc
#	tar cvf dist/${DIST_NAME}.tar.gz dist/${DIST_NAME}
	${MD5SUM} ${DIST_NAME}.tar.gz > ${DIST_NAME}.tar.gz.md5
	${SIGNPACKAGE} -o ${DIST_NAME}.tar.gz.asc ${DIST_NAME}.tar.gz	

dist-hook: ChangeLog
	cp ChangeLog dist/${DIST_NAME}

docs-clean:
	-rm -f README
	-rm -f doc/lyricsgrabber.*

clean-local: docs-clean
	find . -name \*~ -exec rm '{}' \;
	-rm -rf build
	-rm -f src/LyricsGrabber/__init__.py
	find . -name \*.pyc -exec rm '{}' \;

distclean-local:
	find . -name \*~ -exec rm '{}' \;
	-rm -f config.* Makefile
	-rm -f setup.py

maintainer-clean-local:
	-rm -rf ${DIST_NAME}.tar.g*
	-rm -rf autom4te*.cache
	find . -name \*~ -exec rm '{}' \;
	-rm -f config.* Makefile
	-rm -f setup.py

