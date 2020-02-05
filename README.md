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

#### 2.5 Woopsy Daisy
https://www.youtube.com/watch?v=Nbc1Fs3Om-0

#### 2.6 We're screwed
https://m.youtube.com/watch?v=KyoElzBhbXg

#### 2.7 Disagree
https://www.youtube.com/watch?v=_uHBFiAnpZs

#### 2.8 Move desk
https://www.youtube.com/watch?v=Vsayg_S4pJg&%252=&start=24

#### 2.9 Because we want to
https://www.youtube.com/watch?v=D_XI_290cfw&start=22

#### 2.10 Piece of cake
https://www.youtube.com/watch?v=scmuWX3kHjA&start=2

#### 2.11 Yes got dam it yes
https://www.youtube.com/watch?v=cMoowJQLJ10&start=34

#### 2.12 For a moment there i thought we were in trouble
https://www.youtube.com/watch?v=UucXz3ZGmF4&start=131

#### 2.13 Boring
https://www.youtube.com/watch?v=-Bxlolvjyx8

#### 2.14 Negative waves
https://www.youtube.com/watch?v=aT9Lm4Y886k

#### 2.15 We have liftoff
https://www.youtube.com/watch?v=lMtWWls4oas&start=157

#### 2.16 Huston we have a problem
https://www.youtube.com/watch?v=C3J1AO9z0tA&start=80

#### 2.17 Wait
https://www.youtube.com/watch?v=QyFw6yvNiKk&start=246

#### 2.18 Yes that's awesome
https://www.youtube.com/watch?v=PDXLjQBp0D0

#### 2.19 Nooooo
https://www.youtube.com/watch?v=wcz4u3Lv9ko

#### 2.20 Fix it
https://www.youtube.com/watch?v=QCniMXdbO6c
