# small-scripts
A connection of small but usefull scripts for various uses.

## 1. Bash oneliners

#### 1.1 Regex replace row in file
```bash
sed -i 's/\<regex that matches row>/<string to replace matched row with>/' </file/to/replace/in>
```
#### 1.2 Replace all occurences of string in file
```bash
sed -i 's/<string to replace>/<string to insert>/g' </file/to/replace/in>
```

## 2. Docker

#### 2.1 Add commands to delete unused images and containers

The following should be added to `.bashrc`. It will add the following two commands:
* `docker clear`
* `docker images clear`

```bash
docker() {
    if [[ $* == "clear" ]]; then
        docker ps --filter "status=exited" | awk '{print $1}' | xargs --no-run-if-empty docker rm
    elif [[ $* == "images clear" ]]; then
        docker rmi -f $(docker images | grep "<none>" | awk "{print \$3}")
    else
        command docker "$@"
    fi
}
```

## 3. Git

#### 3.1 Checkout and switch to <remote_branch>
git checkout -b <local_branch> origin/<remote_branch>

#### 3.2 Get single file from <local_branch>
git checkout <local_branch> <path/to/file>

#### 3.3 Create <local_branch> from current branch
git checkout -b <local_branch>

#### 3.4 Create <remote_branch> for current branch
git push -u origin <remote_branch>

#### 3.5 Delete <local_branch>
git branch -d <local_branch>

#### 3.6 Delete <remote_branch>
git push origin --delete <remote_branch>

#### 3.7 Merge selected commit with <hash>
git cherry-pick <hash>

#### 3.8 Show unpublished commits
git cherry -v

#### 3.9 List changed files comparing <local_branch> to <remote_branch>
git log origin/<local_branch>..<remote_branch> --name-only --pretty="format:" | sort | uniq

#### 3.10 Show changed files in commit <hash>
git diff-tree --no-commit-id --name-only -r <hash>

#### 3.11 Reset local branch to <remote_branch>
git reset --hard origin/<remote_branch>

#### 3.12 Interattive stash
git stash --patch

#### 3.13 Apply stash
git stash apply

#### 3.14 Set remote tracking branch
git branch -u origin/<remote_branch> <local_branch>

#### 3.15 Update list of remote branches
git remote update origin --prune

## 4. Git Postgres

#### 4.1 Connect to database
psql <database> <user>

#### 4.2 List databases
psql -U <user> -l

#### 4.3 Disconnect
\q

#### 4.4 Print table info
\d+ <table_name>

## 5. Descriptive movie links

#### 5.1 Reload
https://www.youtube.com/watch?v=jk3Z-MVoUg4&version=3&start=17

#### 5.2 Die
https://www.youtube.com/watch?v=rmZOWW70ycQ&start=3

#### 5.3 Lot's of shooting
https://www.youtube.com/watch?v=wgzxSr6l9Y4&start=66
