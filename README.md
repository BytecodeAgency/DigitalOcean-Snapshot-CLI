# DigitalOcean Snapshot CLI

## Requirements

* Python 3
* Pipenv

## Make commands

* `make sync`: Syncs pipenv
* `make run`: Runs application

## Features

* [ ] List all droplets (only pagination needs to be implemented)
* [ ] List all droplets, but just basic data (id, name, status) (only pagination needs to be implemented)
* [x] List droplet by ID
* [ ] List all snapshots made (only pagination needs to be implemented)
* [ ] List all automatically created snapshots
* [x] Create droplet snapshot
* [ ] Delete automatic snapshots older than x days
* [ ] Be able to set a flag to create snapshots with shutdowns

## TODO

* Improve names of snapshots
* Improve notification, show Success/Failed instead of True/False
* Auto delete old snapshots
* Add CLI script
* Write CLI documentation
* Write technical documentation for development
* Add install script for CLI
* Add easy cron support
* Replace external dependencies with self-written ones
* Add open source/free (as in freedom) software license