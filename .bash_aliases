# Aliases
alias ls='ls -lah --color=auto'

# Environment variables
export GIT_EDITOR=nano

# PATH
PATH=${PATH}:~/bin

# Custom prompt with git or mercurial branch
function parse_hg_git_branch {
    HG_BRANCH=$(hg branch 2> /dev/null | sed -e "s/\(.*\)/ (\1)/")
    if [ "$HG_BRANCH" = "" ]; then
        git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
    else
        echo "$HG_BRANCH"
    fi
}
export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_hg_git_branch)\[\033[00m\] $ "

# Add the "docker clear" and "docker images clear" commands
docker() {
    if [[ $* == "clear" ]]; then
        docker ps --filter "status=exited" | awk '{print $1}' | xargs --no-run-if-empty docker rm
    elif [[ $* == "images clear" ]]; then
        docker rmi -f $(docker images | grep "<none>" | awk "{print \$3}")
    else
        command docker "$@"
    fi
}

# Add the "rmi" command to delete a file or directory by inode number
rmi () {
    find / -inum ${1}  -exec rm -ir {} \;
}
