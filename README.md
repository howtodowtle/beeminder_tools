# Beeminder Tools

This repo contains tools that help me use Beeminder. I absolutely love Beeminder for me do what I want to do. It works best with automatic integrations (Strava, Garmin, Project Euler, ...). For tools that have no automatic Beeminder integration but an API (or we can scrape the data), we can use the Beeminder API to automate the process.

## Tools

- 750 Words: Track total number of pages finished.

## How to use

This is how I use the tools:

- add personal usernames, passwords, auth tokens
- create a cronjob that runs the tool regularly (e.g., `* 07-09 * * * /usr/local/bin/python3 /path/to/tool/beemind_750words.py`)
