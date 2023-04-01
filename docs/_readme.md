install
`sudo apt-get install ruby-full`
`sudo apt-get install ruby2.7-dev`
`sudo gem install jekyll bundler`

run locally:
`bundle exec jekyll serve`
or
`bundler exec jekyll build && bash -c 'cd _site && python -m http.server 3000'`