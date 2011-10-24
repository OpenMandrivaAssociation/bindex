# SVN info
%global svnRev 96

# Prevent brp-java-repack-jars from being run.
%define __jar_repack %{nil}

Name:    bindex
Version: 2.2
Release: 3.svn96.2
Summary: Bundle Manifest Header Mapper

Group:   Development/Java 
License: ASL 2.0
URL:     http://www.osgi.org/Repository/BIndex

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export -r ${svnRev} \
#    http://www.osgi.org/svn/public/trunk/org.osgi.impl.bundle.bindex \
#    bindex
#  tar -czvf bindex.r${svnRev}.svn.tar.gz bindex
Source0: %{name}.r%{svnRev}.svn.tar.gz

BuildArch: noarch

BuildRequires: ant
BuildRequires: aqute-bndlib
BuildRequires: felix-osgi-obr
BuildRequires: felix-osgi-core
BuildRequires: java-devel >= 0:1.6.0
BuildRequires: jpackage-utils
BuildRequires: junit4
BuildRequires: kxml

Requires: java >= 0:1.6.0

%description
A Java program that implements the manifest header to repository 
format mapping as described in the RFC-0112 Bundle Repository.

%prep
%setup -q -n %{name}
find . -type f -iname "*.jar" | xargs -t %__rm -f ;
%__mkdir_p bin

%build
export CLASSPATH=$(build-classpath ant kxml junit \
                                   felix/org.osgi.service.obr \
                                   felix/org.osgi.core)
javac -d bin $(find src -name *.java)
pushd jar
  %__ln_s $(build-classpath ant.jar)
  %__ln_s $(build-classpath kxml.jar) kxml2-min.jar
  %__ln_s $(build-classpath felix/org.osgi.service.obr.jar)
popd
java -jar $(build-classpath aqute-bndlib.jar) \
     build -output %{name}-%{version}.jar bindex.bnd

%install
%__rm -rf %{buildroot}
%__install -d -m 0755 %{buildroot}%{_javadir}
%__install -m 644 %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && %__ln_s %{name}-%{version}.jar %{name}.jar)

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README
%{_javadir}/*

