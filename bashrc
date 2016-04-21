# Import paths, etc.
[ -r $HOME/.profile ] && source $HOME/.profile

# If not running interactively, don't do anything else
case $- in
    *i*) ;;
      *) return;;
esac

#Aliases
PLATFORM="$(uname)"
if [ $PLATFORM == "Darwin" ]
then # This a Mac
  alias "ll"="ls -AlFhew"
else # This is Linux
  alias "ll"="ls -alF --color=auto"
fi
alias mkdir='mkdir -p'
# Nice for making noise at the end of a long task, like do-this && bell
alias bell="echo $'\a'"
# -> Prevents accidentally clobbering files.
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias clear-pyc='find . -name '\''*.pyc'\'' -delete'
alias clear-empty-dir='find . -type d -empty -delete'

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

#Terminal settings
export LC_CTYPE=en_US.utf-8
export CLICOLOR=1
export HISTCONTROL=ignoreboth
export HISTTIMEFORMAT="[%F %T] "
export PROMPT_COMMAND="history -a"

# From /etc/bashrc on OS X
# Tell the terminal about the working directory at each prompt.
if [ "$TERM_PROGRAM" == "Apple_Terminal" ] && [ -z "$INSIDE_EMACS" ]; then
    update_terminal_cwd() {
        # Identify the directory using a "file:" scheme URL,
        # including the host name to disambiguate local vs.
        # remote connections. Percent-escape spaces.
        local SEARCH=' '
        local REPLACE='%20'
        local PWD_URL="file://$HOSTNAME${PWD//$SEARCH/$REPLACE}"
        printf '\e]7;%s\a' "$PWD_URL"
    }
    PROMPT_COMMAND="update_terminal_cwd; $PROMPT_COMMAND"
fi


#Tab completion for Git
if [ -n "$(which brew)" ] && [ -f $(brew --prefix)/etc/bash_completion ]; then
    . $(brew --prefix)/etc/bash_completion
fi


#Git in prompt
export GIT_PS1_SHOWDIRTYSTATE="1"
export GIT_PS1_SHOWUPSTREAM="auto"


#Prompt
BOLD="\[$(tput bold)\]"
UNBOLD="\[$(tput sgr0)\]"
STANDOUT="\[$(tput smso)\]"
UNSTANDOUT="\[$(tput rmso)\]"
GIT_STATUS='$(declare -f -F __git_ps1 > /dev/null && __git_ps1)'
export PS1="$BOLD(\d, \@)$UNBOLD$GIT_STATUS\n$BOLD[\u@\h:$STANDOUT \w $UNSTANDOUT]$UNBOLD\n$ "
unset BOLD UNBOLD STANDOUT UNSTANDOUT GIT_STATUS


# Import autoenv
[ -f ~/.autoenv/activate.sh ] && source ~/.autoenv/activate.sh


#Autocomplete
bind "set completion-ignore-case on"
bind "set show-all-if-ambiguous on"


#Tab completion for SSH
_complete_ssh_hosts ()
{
        COMPREPLY=()
        cur="${COMP_WORDS[COMP_CWORD]}"
        comp_ssh_hosts=`cat ~/.ssh/known_hosts | \
                        cut -f 1 -d ' ' | \
                        sed -e s/,.*//g | \
                        grep -v ^# | \
                        uniq | \
                        grep -v "[\[\|]" ;
                cat ~/.ssh/config | \
                        grep "^Host " | \
                        awk '{print $2}'
                `
        COMPREPLY=( $(compgen -W "${comp_ssh_hosts}" -- $cur))
        return 0
}
complete -F _complete_ssh_hosts ssh

#Tab completion for Amazon
complete -C aws_completer aws

# Import secret keys, if available
[ -f $HOME/.keys ] && source $HOME/.keys

# Import other miscellaneous local settings
[ -f $HOME/.misc ] && source $HOME/.misc
