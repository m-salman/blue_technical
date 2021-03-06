# Article API 

An API to add, update and retrieve articles and doing simple aggregations. The API is written in Python 3 using Bottle microservices framework. The backend is implemented using ElasticSearch.

## Setup
You need the following to get up and running:
* Python 3
* Docker and Docker Compose

Once you have these installed, there are 2 ways you can run the project.

## Running

####Running in Docker
It is recommedYou can start the entire project in Docker by going

```shell
$ docker-compose up -d
```
OR
```shell
$ docker-compose up
```

This will start an instance of ElasticSearch in a Docker container and start the app locally. The ElasticSearch container has 
a volume mounted on your local drive. It should be a folder named 'es-data' in the project folder. Data is persisted this way when 
you spin the containers up and down.

It is always advised to bring container down after using it:

```
$ docker-compose down
```

####Running locally
it is recommeded to setup a [virtualenv](https://virtualenv.pypa.io/en/stable/). You should run `pip install -r requirements.txt`
to install all the python dependencies.

Python [invoke](http://www.pyinvoke.org/) is used as our task runner and provides easier access to start API locally and 
run tests.

To get a list of all the things you can do with it:
```shell
$ invoke -l
```

To bring up the API locally, simply run
```shell
$ invoke start
```

## Developing
### Swagger
The API is specified using [Swagger](http://swagger.io/).
The Swagger definitions can be found in `swagger.yml`.

You can browse and interact with the API using [Swagger UI](http://swagger.io/swagger-ui/). The Swagger plugin is 
automatically installed when API is started.

Simply start the API (`invoke start`) and browse to `http://localhost:8080/api-docs`.


## Working With ElasticSearch
You need a instance of ElasticSearch to run the application against.
`invoke start` starts an instance of [local ElasticSearch](https://hub.docker.com/_/elasticsearch/) running on localhost:9200 for you in a Docker container.
You can also start one separately with:
```shell
$ invoke start_elasticsearch
```

You should now be able to access the local ElasticSearch at http://localhost:8000/shell

You can also run against a prod grade ElasticSearch. You can configure a different cluster by putting up a 
a section in `src/config/config.yml'


## Testing
To run the unit tests:
```
$ invoke test
```

You can also run the tests in a Docker container
```shell
$ docker-compose run api invoke test
```

## Configuring

Config files are located in `src/config`. The configuration system defaults to `docker` environment. You can
change this by setting `ENV=<your-env>` environment variable.
Initially, the settings in `docker` get applied. These are then overriden by the value of your `ENV` environment variable,  (say `prod`) if `ENV=prod` environment variable is set.

## Assumptions
The date field is not enough to get last 10 items returned by the /tags endpoint. To overcome this issue,
an epoch time feild is attached to each article. When articles are fetched for a single date, the articles within are sorted using epoch time.

## Caveats
ElasticSearch builds an inverted index and as such the concept of nested types and arrays is different than normal data stores.Please refer to [Array Types](https://www.elastic.co/guide/en/elasticsearch/reference/current/array.html) and [Nested Type](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html)

To build an inverted index an analyzer is run on top of each item in tags list. This can cause problems with tags like `health-soda`, the anaylyzer will break it up as `health` and `soda` and searching for either one will bring back tags marked as 'health', 'soda' and 'health-soda' as well.

This can easily be fixed by mapping the tags field as `not_analyzed` when building the index. As of now, this hasn't been done as part of this build.