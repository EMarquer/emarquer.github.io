install
- `sudo apt-get install ruby-full`
- `sudo apt-get install ruby2.7-dev`
- `sudo gem install jekyll bundler`

install with `rvm` (a pain in the a**):
https://github.com/rvm/rvm/issues/5209#issuecomment-1264562996
- `sudo apt install build-essential`
- `cd ~/Downloads`
- `wget https://www.openssl.org/source/openssl-1.1.1t.tar.gz`
- `tar zxvf openssl-1.1.1t.tar.gz`
- `cd openssl-1.1.1t`
- `./config --prefix=$HOME/.openssl/openssl-1.1.1t --openssldir=$HOME/.openssl/openssl-1.1.1t`
- `make`
- `make install`
- `rm -rf ~/.openssl/openssl-1.1.1t/certs`
- `ln -s /etc/ssl/certs ~/.openssl/openssl-1.1.1t/certs`
- `rvm install ruby3.0 --with-openssl-dir=$HOME/.openssl/openssl-1.1.1t`
- `rvm use ruby-3.0`
- `gem install jekyll bundler`
- `bundle install`


run locally:
`bundle exec jekyll serve`
or
`bundler exec jekyll build && bash -c 'cd _site && python -m http.server 3000'`