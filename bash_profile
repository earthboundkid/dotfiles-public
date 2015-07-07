case $- in
    # Interactive shell: Import slow shell things
    *i*)
        [ -r $HOME/.bashrc ] && source $HOME/.bashrc
    ;;
    # Non-interactive shell: Import paths, universal environmental variables
    *)
        [ -r $HOME/.profile ] && source $HOME/.profile
    ;;
esac
