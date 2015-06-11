# Import paths and other universal environmental variables
[ -r $HOME/.profile ] && source $HOME/.profile

# Import slow, interactive shell things
case $- in
   *i*) [ -r $HOME/.bashrc ] && source $HOME/.bashrc
esac
