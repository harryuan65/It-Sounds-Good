# echo 'Please leave me alone, soundfile.'
# pip uninstall Soundfile
tar xzvf libsndfile-1.0.28.tar.gz

cd libsndfile-1.0.28
./configure
make -s
make install