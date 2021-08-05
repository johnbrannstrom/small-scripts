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

#### 2.21 Screw you guys I'm going home
https://www.youtube.com/watch?v=MTc3zcnIZOw

#### 2.22 Splendid well done!
https://www.youtube.com/watch?v=JexO-N39Nzg&start=96

#### 2.23 Tha's gold Jerry, Gold!
https://www.youtube.com/watch?v=CF7OnW4XDck

#### 2.24 You can't handle the truth
https://www.youtube.com/watch?v=MMzd40i8TfA

#### 2.25 Lawers, guns & money
https://www.youtube.com/watch?v=lP5Xv7QqXiM&start=110

#### 2.26 Fuck you motherfucker
https://www.youtube.com/watch?v=n5BrLfbCoGQ

#### 2.27 Pretend not to hear
https://www.youtube.com/watch?v=S4AmLcBLZWY&start=43&app=desktop

#### 2.28 Beerfest
https://www.youtube.com/watch?v=aDaxX_bGsDc&t=50s

#### 2.29 FUBAR
https://www.youtube.com/watch?v=KhHQcsev9lo&start=70

#### 2.30 Bullshit
https://www.youtube.com/watch?v=zKX4LGlF_Mo

#### 2.31 Whazaaaaa
https://www.youtube.com/watch?v=W16qzZ7J5YQ

#### 2.32 Bridge is up
https://www.youtube.com/watch?v=Clz9ykXMkeM

#### 2.33 Do it, do it now!
https://www.youtube.com/watch?v=a6P40wLThbc

#### 2.34 Terrible dance
https://www.youtube.com/watch?v=HQu_NLRvULM&start=14

#### 2.35 Gooood morning Vietnam
https://www.youtube.com/watch?v=BIikfdNIHQE&t=4s

#### 2.36 Good morning 2
https://www.youtube.com/watch?v=qu4v5hB1dKk

#### 2.37 Good morning 3
https://www.youtube.com/watch?v=9bMqDykDxeg&t=2s

#### 2.38 Good morning 4
https://www.youtube.com/watch?v=2UwMOEnmGZg&t=7s

#### 2.39 TPS report
https://www.youtube.com/watch?v=Fy3rjQGc6lA

#### 2.40 Welcome to the world of tomorrow
https://www.youtube.com/watch?v=aiwA0JrGfjA

#### 2.41 Case of the mondays
https://www.youtube.com/watch?v=2AB9zPfXqQQ
https://www.youtube.com/watch?v=guv5LUT1AFw

#### 2.42 Hell yeah
https://www.youtube.com/watch?v=psiH5-zCW8g
