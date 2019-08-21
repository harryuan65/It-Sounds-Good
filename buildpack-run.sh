# echo 'Please leave me alone, soundfile.'
# pip uninstall Soundfile
tar xzvf libsndfile-1.0.27.tar.gz

cd libsndfile-1.0.27
./configure
make -s
make install