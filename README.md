# small-scripts
A connection of small but usefull scripts for various uses.

## 1. Bash oneliners

#### 1.1 Regex replace row in file
```bash
sed -i 's/\<regex that matches row>/<string to replace matched row with>/' </file/to/replace/in>
```
#### 1.2 Replace all accurences of string in file
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
