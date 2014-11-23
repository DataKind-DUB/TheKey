# build package - don't forget to increment version number in setup.py
curpath=`pwd`
rm ${curpath}/sdist/*.gz
# Build
python ${curpath}/setup.py sdist

ver=`cat setup.py |grep version|cut -d'=' -f2|sed s/\'//g|sed s/,//`
echo "Install with..."
echo "easy_install -v file:${curpath}/dist/Textprep-${ver}.tar.gz"
