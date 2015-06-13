  1. Update your system (yum update)
> 2. Install Subversion
    * yum install subversion
> 3. Download GridLab-D source using Subversion
    * svn checkout
http://gridlab-d.svn.sourceforge.net/svnroot/gridlab-d gridlab-d
      * This will run for a while and download approximately
2.3 GB of files
> 4. Ensure following RPMs are installed
    1. gcc
> > 2. gcc-c++
> > 3. autoconf
> > 4. automake
> > 5. libtool
> > 6. xerces-c
> > 7. xerces-c-devel
> > 8. cppunit
> > 9. cppunit-devel
    1. . doxygen

> 5. cd gridlab-d/trunk
> 6. Execute following commands:
    1. autoreconf -isf
      * Ensure there are no errors reported
> > 2. ./configure
      * Ignore error messages re: "cannot remove core"
      * Review final report. It should report "yes" to
everything (e.g. libcppunit: yes)
> > 3. make -j 2 (if you have a dual-core machine)
      * It should compile and link gridlab-d successfully
> > 4. make install DESTDIR=<wherever you want to install under $HOME>
> > 5. cd 

&lt;install-dir&gt;

/usr/bin
> > 6. ./gridlabd