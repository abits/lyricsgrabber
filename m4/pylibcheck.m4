dnl based on macros written by Glen Starchman
dnl <http://www.mail-archive.com/autoconf@gnu.org/msg05111.html>

dnl figure out the path to our python libraries
AC_DEFUN([AC_PY_LIB_PATH], 
[ac_cv_py_lib_path="`python -c "import distutils.sysconfig; print distutils.sysconfig.get_python_lib()"`"; 
PY_LIB_PATH=$ac_cv_py_lib_path;
])

dnl main test routine: returns result boolean flag
dnl takes module name without *.py extension as argument
AC_DEFUN([AC_PY_CHECK_LIB],[ dnl
AC_MSG_CHECKING(Python module $1)
AC_PY_LIB_PATH
ac_cv_py_have_$1=false;
if test -e $PY_LIB_PATH/$1.py; then
    ac_cv_py_have_$1=true;
fi;
AC_MSG_RESULT($ac_cv_py_have_$1)
HAVE_PY_LIB_$1=$ac_cv_py_have_$1;
])

dnl alternate test routine, calling AC_PY_CHECK_LIB
dnl aborts the configure script if needed
AC_DEFUN([AC_PY_CHECK_REQUIRED], [dnl
AC_PY_CHECK_LIB($1)
if [[ $HAVE_PY_LIB_$1 == false ]]; then
{
    echo "Required Python module $1 not found... aborting.";
    exit
}
fi;
])
