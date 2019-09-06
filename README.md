# small-scripts
A connection of small but usefull scripts for various uses.

## 1. Docker

#### 1.1 Add commands to delete unused images and containers

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

## 2. Descriptive movie links

#### 2.1 Reload
https://www.youtube.com/watch?v=jk3Z-MVoUg4&version=3&start=17

#### 2.2 Die
https://www.youtube.com/watch?v=rmZOWW70ycQ&start=3

#### 2.3 Lot's of shooting
https://www.youtube.com/watch?v=wgzxSr6l9Y4&start=66

#### 2.4 Mistake
https://www.youtube.com/watch?v=eFmuO6xJ36g

#### 2.5 We're screwed
https://m.youtube.com/watch?v=KyoElzBhbXg

#### 2.6 Disagree
https://www.youtube.com/watch?v=_uHBFiAnpZs

#### 2.7 Move desk
https://www.youtube.com/watch?v=Vsayg_S4pJg&%252=&start=24

#### 2.8 Because we want to
https://www.youtube.com/watch?v=D_XI_290cfw&start=22
