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

Descriptive movie links

#### Reload
https://www.youtube.com/watch?v=jk3Z-MVoUg4&version=3&start=17

#### Die
https://www.youtube.com/watch?v=rmZOWW70ycQ&start=3

#### Lot's of shooting
https://www.youtube.com/watch?v=wgzxSr6l9Y4&start=66

#### Mistake
https://www.youtube.com/watch?v=eFmuO6xJ36g

#### Woopsy Daisy
https://www.youtube.com/watch?v=Nbc1Fs3Om-0

#### We're screwed
https://m.youtube.com/watch?v=KyoElzBhbXg

#### Disagree
https://www.youtube.com/watch?v=_uHBFiAnpZs

#### Move desk
https://www.youtube.com/watch?v=Vsayg_S4pJg&%252=&start=24

#### Because we want to
https://www.youtube.com/watch?v=D_XI_290cfw&start=22

#### Piece of cake
https://www.youtube.com/watch?v=scmuWX3kHjA&start=2

#### Yes got dam it yes
https://www.youtube.com/watch?v=cMoowJQLJ10&start=34

#### For a moment there i thought we were in trouble
https://www.youtube.com/watch?v=UucXz3ZGmF4&start=131

#### Boring
https://www.youtube.com/watch?v=-Bxlolvjyx8

#### Negative waves
https://www.youtube.com/watch?v=aT9Lm4Y886k

#### We have liftoff
https://www.youtube.com/watch?v=lMtWWls4oas&start=157

#### Huston we have a problem
https://www.youtube.com/watch?v=C3J1AO9z0tA&start=80

#### Wait
https://www.youtube.com/watch?v=QyFw6yvNiKk&start=246

#### Yes that's awesome
https://www.youtube.com/watch?v=PDXLjQBp0D0

#### Nooooo
https://www.youtube.com/watch?v=wcz4u3Lv9ko

#### Fix it
https://www.youtube.com/watch?v=QCniMXdbO6c

#### Screw you guys I'm going home
https://www.youtube.com/watch?v=MTc3zcnIZOw

#### Splendid well done!
https://www.youtube.com/watch?v=JexO-N39Nzg&start=96

#### Tha's gold Jerry, Gold!
https://www.youtube.com/watch?v=CF7OnW4XDck

#### You can't handle the truth
https://www.youtube.com/watch?v=MMzd40i8TfA

#### Lawers, guns & money
https://www.youtube.com/watch?v=lP5Xv7QqXiM&start=110

#### Fuck you motherfucker
https://www.youtube.com/watch?v=n5BrLfbCoGQ

#### Pretend not to hear
https://www.youtube.com/watch?v=S4AmLcBLZWY&start=43&app=desktop

#### Beerfest
https://www.youtube.com/watch?v=aDaxX_bGsDc&t=50s

#### FUBAR
https://www.youtube.com/watch?v=KhHQcsev9lo&start=70

#### Bullshit
https://www.youtube.com/watch?v=zKX4LGlF_Mo

#### Whazaaaaa
https://www.youtube.com/watch?v=W16qzZ7J5YQ

#### Bridge is up
https://www.youtube.com/watch?v=Clz9ykXMkeM

#### Do it, do it now!
https://www.youtube.com/watch?v=a6P40wLThbc

#### Terrible dance
https://www.youtube.com/watch?v=HQu_NLRvULM&start=14

#### Gooood morning Vietnam
https://www.youtube.com/watch?v=BIikfdNIHQE&t=4s

#### Good morning 2
https://www.youtube.com/watch?v=qu4v5hB1dKk

#### Good morning 3
https://www.youtube.com/watch?v=9bMqDykDxeg&t=2s

#### Good morning 4
https://www.youtube.com/watch?v=2UwMOEnmGZg&t=7s

#### Good morning 5
https://www.youtube.com/watch?v=CuI_p7a9VGs

#### TPS report
https://www.youtube.com/watch?v=Fy3rjQGc6lA

#### Welcome to the world of tomorrow
https://www.youtube.com/watch?v=aiwA0JrGfjA

#### ase of the mondays
https://www.youtube.com/watch?v=2AB9zPfXqQQ<br>
https://www.youtube.com/watch?v=guv5LUT1AFw

#### Hell yeah
https://www.youtube.com/watch?v=psiH5-zCW8g
