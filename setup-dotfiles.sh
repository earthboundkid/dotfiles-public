# Get the directory that this script file is in
DOT_FILES_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

function backup-file() {
	local SRC="$HOME/.$1"
	local DST="$HOME/.$1.$(date "+%Y-%m-%d %H:%M:%S").bak"
	echo "Backing up $SRC to $DST"
	cp -v "$SRC" "$DST"
}

function symlink-file() {
	local SRC="$DOT_FILES_DIR/$1"
	local DST="$HOME/.$1"
	echo "Linking $SRC to $DST"
	ln -isv "$SRC" "$DST"
}

function backup-and-symlink() {
	echo "Checking ~/.$1..."
	if [ -e "$HOME/.$1" ]; then
		if [ "$HOME/.$1" -ef "$DOT_FILES_DIR/$1" ]; then
			echo "Already linked $1"
		else
			backup-file $1
			symlink-file $1
		fi
	else
		echo "No such file as ~/.$1"
		symlink-file "$1"
	fi
}

backup-and-symlink "pythonstartup.py"
backup-and-symlink "bashrc"
backup-and-symlink "bash_profile"
backup-and-symlink "profile"
backup-and-symlink "gitconfig"
backup-and-symlink "gitignore"
backup-and-symlink "tmux.conf"
