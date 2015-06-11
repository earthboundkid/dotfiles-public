# Import paths and other universal environmental variables
[ -r $HOME/.profile ] && source $HOME/.profile

#Aliases
if [ ls -w ]
then # This a Mac
  alias "ll"="ls -AlFhew"
else # This is Linux
  alias "ll"="ls -alF --color=auto"
fi
alias mkdir='mkdir -p'
# -> Prevents accidentally clobbering files.
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Dev server aliases
alias nginx-launch='sudo launchctl start homebrew.mxcl.nginx'

# Pretty tail logs
function console () {
  if [[ $# > 0 ]]; then
    query=$(echo "$*"|tr -s ' ' '|')
    tail -f /var/log/system.log|grep -i --color=auto -E "$query"
  else
    tail -f /var/log/system.log
  fi
}

# cd to current Finder window
function cd-finder() {
    appscript='tell application "Finder" to get POSIX path of (target of front Finder window as text)'
    cd "$(osascript -e "$appscript")"
}


# Set tab name
function tabname {
  printf "\e]1;$@\a"
}

function winname {
  printf "\e]2;$@\a"
}

tabname $(pwd)

# Import slow, interactive shell things
case $- in
   *i*) [ -r $HOME/.bashrc ] && source $HOME/.bashrc
esac


# Import secret keys, if available
[ -f $HOME/.keys ] && source $HOME/.keys
