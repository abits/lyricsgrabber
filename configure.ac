# -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.63])
AC_INIT([lyricsgrabber], [0.1.2], [Chris <accidentalbits@googlemail.com>])
PACKAGE_RELEASE_QUALITY=pre-alpha
AC_SUBST([PACKAGE_RELEASE_QUALITY])
AM_INIT_AUTOMAKE([foreign])
#use this when making your own dist target
#AM_INIT_AUTOMAKE([gnu],[foreign],[no-dist])
AC_COPYRIGHT([GNU GPL])
AC_PREFIX_PROGRAM(python)

# Checks for programs.
AM_PATH_PYTHON([2.5],,AC_MSG_ERROR([Cannot find recent enough Python interpreter.]))
AC_PATH_PROG([EYED3],[eyeD3],[missing])
if test "$EYED3" = "missing"; then
   AC_MSG_ERROR([Cannot find Python library eyeD3.])
fi

# Checks for libraries.

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

AC_CONFIG_FILES(Makefile setup.py)

AC_OUTPUT
