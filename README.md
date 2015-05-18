# WatchDog

## Summary
Used for Watching a single server and reporting its statistics to the central server. The intent of this software is to monitor server stats. These could be custom or the default ones out of the box.

Data Collector sets up the classes based on the config in the config file. These classes will be load and the run method will be called per frequency. The main loop runs every second, but eash class determines how often it will run based on the frequency that was passed it.

## Installation

git clone 

## Config

Configuration out of the box only needs a few changes.

> collector_server_name=localhost.jax.org
> collector_server_port=80
> server_name=localhost
> server_arch=mac


## Running

