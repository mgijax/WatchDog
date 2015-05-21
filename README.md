# WatchDog

## Summary
Used for Watching a single server and reporting its statistics to the central server. The intent of this software is to monitor server stats. These could be custom or the default ones out of the box.

Data Collector sets up the classes based on the config in the config file. These classes will be load and the run method will be called per frequency. The main loop runs every second, but eash class determines how often it will run based on the frequency that was passed it.

## Installation

```
> git clone git@github.com:mgijax/WatchDog.git
> cd WatchDog
```

## Config

Configuration out of the box only needs a few changes.

```
> cp host_setup_default.cfg host_setup.cfg
> vim host_setup.cfg

collector_server_name=localhost.jax.org
collector_server_port=80
client_name=localhost
client_arch=mac
```
Change collector_server_name to be the <a href="https://github.com/mgijax/wildfly-8.2.0-servermonitoring">jboss server</a> running the <a href="https://github.com/mgijax/ServerMonitoring">Server Monitoring</a> code. Most of the time jboss runs on port 8080 or if you have apache in front of jboss port 80.

Client_name is the name that this node is going to report as. It will log to the server as "client_name". It is suggested that no two clients share the same name however there is nothing to stop it from happening. Also change the client_arch to one of "linux" or "solaris" those are the only supported types right now. However if running on other unix / linux systems the general stats will run (uptime, users) but not the disk or network.

## Running

Once configured run the main.py script

```
> ./main.py
```

There will be no output and this stays in the foreground, it is suggested to run this via screen or ./main.py & and then log out. There is nothing that is checking the status of the main.py however when viewing the graphs it will be clearly seen which clients are not updating.

## Debugging

If there is errors or it does not appear to be working, the script can be run in debug mode which will output a lot of messsages. To run the script in debug mode:

```
> ./main.py -d
```

