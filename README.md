# Data Engineer Project

## deproj
    deproj [-h] -B BRAND [-Y YEAR] -P PERSON_ID [-LL LOG_LEVEL] {console,csv,json,png} ...

Generate baseball card info for a given **brand**, **year**, and **player** and output the data to the console or to a file.
Supported formats include csv and json (png forthcoming), where the filenames are output.

> **_NOTE:_** Only cards for year 2023 are supported in this demo

### System requirements

brew or apt install: `autoconf automake libtool jq`
### Installation

```shell
make install
```

### Run
```shell
deproj ...
# deproj -B 'panini-donruss-baseball' -P 605113 console -O json | jq
```

> **_NOTE:_** Only brands `panini-donruss-baseball` and `topps-series-1-baseball` are supported in this demo

#### Docker

```shell
make docker-build

docker run deproj ...
# docker run deproj deproj -B 'topps-series-1-baseball' -P 605135 console -O csv
```

### Testing

```shell
make test
```

#### Test in Docker 

```shell
make docker-build-test
docker run deproj-test
```

### Configuration

Card data are configured under [src/deproj/configs/cards](src/deproj/configs/cards)
based on the `{brand}/{year}-{group}.yml`, where the group is `batting` or `pitching`.

For example, see [panini-donruss-baseball/2023-batter.yml](src/deproj/configs/cards/panini-donruss-baseball/2023-batter.yml).

Cards are represented as a list of info `boxes`, where each box has a list of `values` defining each datapoint.
Each of these elements needs a `script` to run against a `value` in [pyjq](https://pypi.org/project/pyjq/)
to process the json data from the MLB Stats API.

Boxes are of a `basic` or `frame` **kind** depending on if the _script_ returns a single value or a list.

Hydration rues for each kind of `value` are also defined in the config file. 


#### Adding a new brand

To add a brand, add to the **configs/cards** for the year for both batter and pitcher.

#### Adding a new value

The basic value from which most data are gathered is the `person` response.

Additional values would be added like the `vsTeamTotal`, see [deproj.cards.factory:add_vs_team_total](src/deproj/cards/factory.py),
where a value can be named, hydrated, and connected to a new query method in the card factory.

---

# Instructions
## Objective

The objective of this project is to create your own baseball card, minus the graphic design part.
Using the MLB Stats API and any other publicly available information,
your task is to retrieve any information required for your card and organize it in an intuitive fashion. 

The information you include is up to you,
i.e. you can choose to include the statistics you think are most relevant,
use a traditional card as your model, or anything in between.
Please provide a description of what you decided to include and why in your write-up.

## Requirements

- The code can be written in the language of your choice, but it should be working.
An incomplete, runnable project is better than code that will not run.

- The code can be designed for one player,
but please be prepared to outline the changes that would be required to make it flexible to other players.

- The code should not only make API calls, 
but also transform the data into how it would look on the card
(remove unnecessary fields, perform any transformations, join data sources, etc.).
    - The output file format is up to you (CSV, JSON, etc.).
    
## Resources

- MLB Stats API OpenAPI Specification
    - I recommend downloading Postman and importing the json file to view it.

## Deliverables
- Code used to retrieve information
- Write-up of methodology
- Sample data for 1+ players
- (Optional) Diagram with layout of baseball card


## Evaluation Criteria

The goal of this project is evaluate not only your technical skills,
but also your ability to think critically and make decisions based on your technical and baseball knowledge.
Creativity is encouraged.
There is no right or wrong answer for what information you choose to include in your project,
as long as the code quality is there, and it is well-reasoned. 

If you have any questions or any part of the instructions are unclear,
please do not hesitate to reach out to bplexico@raysbaseball.com.


---


# Write-Up

## Explanation

I chose to design a config driven app that can generate data for a card and output this in multiple formats.
The example config are derived from some 2001 Fleer Triple Crown and 1991 Topps Bowman cards.
These two were different enough to present some basic challenges in abstracting the query for the data.
Specifically, the Triple Crown cards show year-by-year stats while Bowman shows a prior year breakdown by teams.
(The Fleer cards I renamed `panini-donruss-baseball`, and Bowman `topps-series-1-baseball` in the **deproj/configs/cards**.)
I abstracted these cards by noting that each one contained multiple boxes of info.

Therefor this project aims to satisfy the generation of the data within each box on the card,
based on query expressions to run against named responses from the MLB Stats API.
It assumes that each box of values would be placed in some spot on the card by the image-generating consumer downstream.
As of now each box is not identified by anything other than their position in the config's `boxes`.

The project is set up anticipating that each brand would need an extended class of Card,
so that the forthcoming to_png methods would be implemented on a per-brand basis.
In this enhancement, the card config would also be developed to indicate visual rules about each box,
like orientation and location.

## Methodology

The card configs allow for simpler, abstracted python code,
for users to add isolated functionality for any new value and query,
and for faster development and testing in shell with `jq` or python with `pyjq`.

**For example,**
the [panini-donruss-baseball/2023-batter](src/deproj/configs/cards/panini-donruss-baseball/2023-batter.yml) config
queries for `BB` as `'[ .stats[] | select(.type.displayName == "yearByYear") | .splits[] | .stat.baseOnBalls ]'`
from the `person` value:

```shell
export NAME=BB
export PEOPLE='tests/resources/statsapi/person/api/v1/people'
export PERSON=605113
export HYDRATE='currentTeam,team,stats(type=[yearByYear,yearByYearAdvanced,careerRegularSeason,careerAdvanced,availableStats](team(league)),leagueListId=mlb_hist)&site=en'
export FILENAME="${PEOPLE}/${PERSON}?hydrate=${HYDRATE}.json.gz"

# config `script` assumes the v1/people response is pre-transformed as such
export PERSON='.people[0]'
export SCRIPT='[ .stats[] | select(.type.displayName == "yearByYear") | .splits[] | .stat.baseOnBalls ]'

# with jq:
<"$FILENAME" gunzip | jq "{ $NAME: ${PERSON} | ${SCRIPT} }"

# with pyjq
python <<EOF
import os
import gzip
import json
import pyjq

filename = os.environ["FILENAME"]
script = os.environ["SCRIPT"]
name = os.environ["NAME"]

with gzip.open(filename, "r") as f:
  data = json.load(f)

val = pyjq.first(script, data["people"][0])
print(json.dumps({name: val}, indent=2))
EOF
```


### MBL Stats API

This is the only datasource used in the project.
I was able to reuse a fair amount of prior work around the MLB Stats API in order to get started.
For example, the deproj.statsapi.StatsAPI is generated from configs/statsapi files
and contains rules on all the endpoints and methods in the MLB Stats API.
Additionally, the deproj.utils.StatsAPIObject wrapper is handy for getting, loading, and saving the api responses.
It is also handy for testing purposes!
In prior work and exploration, this StatsAPI response wrapper helped to manage an S3 data lake of baseball data!

#### `v1/people`

This endpoint, in combination with different hydration rules,
yields most of the required information for any card. 

#### `v1/teams`

The v1/teams response for `sportId=1` is needed to get all teamId for the **vsTeamTotal** values,
where the `v1/people` responses for each `opposingTeamId` are collected.

### Output Data Model

The program can output to the console, or write the data to a JSON or CSV file (and return the filename(s)).
The base output path where these files are written can be set in the environment with `DEPROJ__OUTPUT_PATH`.

#### JSON

Cards can `write_json` as a list of the data box elements.
Cards are saved as JSON like `{OUTPUT_PATH}/{brand}/{year}-{nameSlug}.json`

#### CSV

Cards can `write_csv` by calling to_df().to_csv(...) on each box in the card.
Cards are saved as CSV like `{OUTPUT_PATH}/{brand}/{year}-{nameSlug}-{i}.csv`
where `i` is the index of the box in the config.

#### PNG, JPG

With more development, cards could `write_png` or `write_jpg` to save the front and back images of a card.
These formats were omitted in favor of showcasing other development on the project vs. image generation techniques. 


### Issues and Future Development

- The program doesn't explicitly validate the `--person-id`
- The year param is not entirely functional yet
  - The program only works for 2023, due to its configurations...
  - but also due to limited logic in the program for querying the Stats API with year-based filters
- Queries, and scripts in the config, may need to also filter for `gameType == "R"`
- Redundant parts of card config
  - A lot of the script expressions could be abstracted into splits or stats lookups 
  - Perhaps the `boxes[].values[].value` element could be moved higher into the box element,
  to `boxes[].value`
  - Likewise with the redundant `select` statements,
  such as in [panini-donruss-baseball](src/deproj/configs/cards/panini-donruss-baseball/2023-batter.yml),
  could go to `boxes[].select`
- Scrappy `factory`, and `build` method, of `deproj.cards`
  - Could create some config classes to wrap the card configs
  - Feels not abstracted enough, but at the same time,
  python is still needed to curate the vsTeamTotal value from multiple calls to the StatsAPI, right?
- Develop more logic for special cards like Rookie, Limited Editions, Inserts
- Add images or image generation to the program
  - Card configs do have some elements to define images and their url,
  but this is not used by the python
