#Terminal settings
export LC_CTYPE=en_US.utf-8
export CLICOLOR=1
export HISTCONTROL=ignoreboth
export HISTTIMEFORMAT="[%F %T] "
export PROMPT_COMMAND="history -a; $PROMPT_COMMAND"

#Git in prompt
export GIT_PS1_SHOWDIRTYSTATE="1"
export GIT_PS1_SHOWUPSTREAM="auto"

#Prompt
BOLD="\[$(tput bold)\]"
UNBOLD="\[$(tput sgr0)\]"
STANDOUT="\[$(tput smso)\]"
UNSTANDOUT="\[$(tput rmso)\]"
export PS1="$BOLD(\d, \@)$UNBOLD\$(__git_ps1)\n$BOLD[\u@\h:$STANDOUT \w $UNSTANDOUT]$UNBOLD\n$ "
unset BOLD UNBOLD STANDOUT UNSTANDOUT


#Autocomplete
bind "set completion-ignore-case on"
bind "set show-all-if-ambiguous on"


#Tab completion for Git
if [ -f $(brew --prefix)/etc/bash_completion ]; then
    . $(brew --prefix)/etc/bash_completion
fi

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
                        grep -v "\[" ;
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
