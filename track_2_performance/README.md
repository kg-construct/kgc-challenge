# Track 2: Performance Challenge

Performance Challenge for Knowledge Graph (KG) Construction Workshop 2026
uses the [KROWN](https://github.com/kg-construct/KROWN) benchmark to evaluate
the performance of existing KG materialization systems under different
predefined scenarios, using the latest [RML specifications](https://kg-construct.github.io/rml-resources/portal/).

## Benchmark structure

The benchmark is structured into two main components:

1) `data-generator`: scales different benchmark scenarios under the folder
`./data-generator/resources/scenarios-config/` with multiple
parameters that are configurable through a set of JSON configuration files. 

2) `execution-framework`: executes the generated scenarios from the
data-generator component with a specified engine in
a Docker-based pipeline while collecting performance metrics.


## Quick Start KGCW Challenge 2026

1. Install system dependencies

```
# Ubuntu dependencies, this may differ for your Linux distro
sudo apt install zlib1g zlib1g-dev libpq-dev libjpeg-dev 
```


2. Install python dependencies

```
# Python3 requires virtual environments for installing dependencies so let's
activate one 

python3 -m venv .venv
source .venv/bin/activate 

# Install python dependencies to the .venv folder
pip3 install -r requirements.txt
```

3. Make a docker image of your mapping engine, 
and implement `Executor`, from the `bench_executor` module, for your engine. 
Check out the implementation and docker image creation under the section
[Adding your own tool](#tutorial-adding-your-own-tool). 

4. Edit all the scenarios JSON configuration files under `./resources/scenarios-config/` folder
by changing the `engine` attribute of each `instances` to the chosen pretty name
of your engine that you used for implementing the `Executor` class in Step 3. 

5. Execute the example pipeline included in the challenge:
```
./exectool run --runs=5 
```
The tool will execute all cases in the
challenge's root folder 
five times (`--runs=5`) and report its progress to stdout of your command line.

:bulb: You can end the execution by pressing `CTRL+C`. Pressing it once will gracefully end the current item by letting it finish and exit.
Pressing it again will forcefully kill the execution and exit as quickly as possible.

:bulb: If you want to keep it running while also disconnect from the machine, you can first start a Screen session:

```
# Start a Screen session with name 'eswc-kgc-challenge-2026
screen -S eswc-kgc-challenge-2026

# You enter the session, execute any command you want such as the challenge:
./exectool run --runs=5 --root=downloads/eswc-kgc-challenge-2024

# Leave the session while letting it run by pressing: 1) CTRL+a  2) CTRL+d
```

You can re-enter the session by running `screen -r`.


For detailed usage of this tool, please have a look at the 
[README](https://github.com/kg-construct/KROWN/README.md)
in the KROWN repository.

## Tutorial: Generating summaries of results

Once you have executed your experiments, you can generate summaries with
the tool through the 'stats' command:

```
./exectool stats 
```

This will generate the following files for each experiment:
- `aggregated.csv`: For each step, the median of the step duration for each run
is calculated and the step of the run with the median duration is used
to generate this file. This way, outliers are avoided.
- `summary.csv`: Calculates the diff for each measured metric for each step
from `aggregated.csv`. This way, the duration, consumed CPU/RAM/... 
for each step is generated.

Besides these files, a ZIP archive `results.zip` of all experiments with 
these files is also generated.

## Tutorial: Running a specific part of the Challenge

If you want to be precise and only execute a specific scaling, you
can specify this as well. For example: `mappings` with scaling `mapping_15tm_1pom`
looks as followed:

```
./exectool run --runs=5 --root=[Your Engine Name]/csv/mapping_15tm_1pom
```

Through the CLI `--root` parameter you can specify where the tool starts looking
for parts to execute.

If you want to have a list of all possible parts in the challenge, you can
use the `list` command:

```
./exectool list 
```


## Tutorial: Where are the results?

During execution, a directory called `results` will be created for each
item executed. In this directory, each run of the item gets its own 
directory `run_{$NUMBER}` where the results, metrics, and logs for that run are
stored:

```
.
├── data
│   └── shared
├── metadata.json
└── results
    └── run_1
        ├── case-info.txt
        ├── log.txt
        ├── metrics.csv
        └── rmlmapper
            └── out.nt
```

Each tool involved in the pipeline specified in `metadata.json` has
its own directory in the `run_{$NUMBER}` directory. In case of the RMLMapper,
this is `rmlmapper` and contains the generated Knowledge Graph in RDF N-Triples
in a file `out.nt` as specified in `metadata.json`. The captured output
from the Docker containers is available in `log.txt` 
while the information about your hardware is stored in `case-info.txt`.
The measured metrics can be found in `metrics.csv` such as CPU usage,
memory usage, etc. of the whole system on which EXEC executed the pipeline from
`metadata.json`.

## Tutorial: Adding your own tool

Adding your tool to exectool requires the following parts:

1. **Required**: Package your tool as a Docker image and publish it on Docker Hub (optional publish).
2. **Required**: Create a Python class for your tool in the `bench_executor` folder.
3. **Preferred**: Add some test cases for your tool, the test data goes in `bench_executor/data/test-cases` and the actual test goes into `tests`.

:warning: If possible, **please supply the Docker image and the Python class to
make sure your experiments are reproducible** with the exact same parameters as
on your machine.

We will go through these steps for the RMLMapper:

**Step 1: package your tool as a Docker image**

Each tool _must_ expose a folder on `/data` where the tool can exchange data
such as mappings, files, etc. with the host system.
In case of the RMLMapper, the Dockerfile looks like this:

```
################################################################################
# RMLMapper
# https://github.com/RMLio/rmlmapper-java
################################################################################
FROM ubuntu:22.04
# Configure the RMLMapper version to use
ARG RMLMAPPER_VERSION
ARG RMLMAPPER_BUILD

# Install latest updates and dependencies
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y openjdk-8-jdk less vim wget unzip

# Download RMLMapper release
RUN mkdir rmlmapper && wget -O rmlmapper/rmlmapper.jar https://github.com/RMLio/rmlmapper-java/releases/download/v${RMLMAPPER_VERSION}/rmlmapper-${RMLMAPPER_VERSION}-r${RMLMAPPER_BUILD}-all.jar

# Expose data folder
RUN mkdir /data

# Silent
CMD ["tail", "-f", "/dev/null"]
```

This Dockerfile uses Ubuntu 22.04 LTS as base and installs the dependencies for
the RMLMapper. After that, it downloads the RMLMapper jar from GitHub, the version
is made configurable through the `RMLMAPPER_VERSION` and `RMLMAPPER_BUILD` variables.
The Dockerfile also creates a folder in the root: `/data` which is used to exchange data with the host system.
:warning: This folder is crucial, and every tool must use and expose this path for exchange data!

Now we can build and publish our Docker image to Docker Hub:

```
# Build RMLMapper 6.0.0
docker build --build-arg RMLMAPPER_VERSION=6.0.0 --build-arg RMLMAPPER_BUILD=363 -t kgconstruct/rmlmapper:v6.0.0 .

# Optional: Publish Docker image, replace $USERNAME with your Docker Hub username
docker push $USERNAME/rmlmapper:v6.0.0
```

**Step 2: Create a Python class in the bench_executor folder**

Each tool has a slightly different interface to execute a RML mapping,
some tools can only handle R2RML or RML mappings,
or require certain configuration files to operate.
These differences are abstracted by the Python class for each tool.

Below, an example Python class of the RMLMapper is given, you can copy this and
adjust it to your tool, you need to adjust it in the following places:

- [ ] **Required**: Name of the class matching with your tool: `class RMLMapper(Container)`
- [ ] **Required**: Docker image and its pretty name: 
`super().__init__(f'kgconstruct/rmlmapper:v{VERSION}', 'RMLMapper'`.
`kgconstruct/rmlmapper:v{VERSION}` is the Docker image name with tag
and `RMLMapper` is the pretty name.
- [ ] **Preferred**: The inline code documentation to your tool.

The following parts heavily depend on your tool and how your tool executes mappings.
Some tools use commandline arguments while others use configuration files:

- [ ] **Required**: The `_execute_with_timeout` method executes your tool with the specified
timeout (defined by the `TIMEOUT` variable in seconds at the top of the class file).
Here you can specify arguments that are necessary to ensure a proper execution
of your tool such as the Java heap (in case of the RMLMapper).
Some tool won't require such additional arguments and can just leave the method
empty as followed:

```
@timeout(TIMEOUT)
def _execute_with_timeout(self, arguments: list) -> bool:
    """Execute a mapping with a provided timeout.

    Returns
    -------
    success : bool
        Whether the execution was successfull or not.
    """
    return self.run_and_wait_for_exit(cmd)
```

- [ ] **Required**: The `execute_mapping` method prepares the provided mapping
and pass it to your tool. Here, you can add tool specific arguments 
for executing the mapping such as the credentials of a relational database,
generating the configuration file for your tool, etc.
For the RMLMapper, we add the necessary commandline arguments here
to access relational databases such as the username, password, host, port of the
relational database.

The Python class of the RMLMapper looks like this:

```
#!/usr/bin/env python3

"""
The RMLMapper executes RML rules to generate high quality Linked Data
from multiple originally (semi-)structured data sources.

**Website**: https://rml.io<br>
**Repository**: https://github.com/RMLio/rmlmapper-java
"""

import os
import psutil
from typing import Optional
from timeout_decorator import timeout, TimeoutError  # type: ignore
from bench_executor.container import Container
from bench_executor.logger import Logger

VERSION = '6.0.0'
TIMEOUT = 6 * 3600  # 6 hours


class RMLMapper(Container):
    """RMLMapper container for executing R2RML and RML mappings."""

    def __init__(self, data_path: str, config_path: str, directory: str,
                 verbose: bool):
        """Creates an instance of the RMLMapper class.

        Parameters
        ----------
        data_path : str
            Path to the data directory of the case.
        config_path : str
            Path to the config directory of the case.
        directory : str
            Path to the directory to store logs.
        verbose : bool
            Enable verbose logs.
        """
        self._data_path = os.path.abspath(data_path)
        self._config_path = os.path.abspath(config_path)
        self._logger = Logger(__name__, directory, verbose)
        self._verbose = verbose

        os.makedirs(os.path.join(self._data_path, 'rmlmapper'), exist_ok=True)
        super().__init__(f'kgconstruct/rmlmapper:v{VERSION}', 'RMLMapper',
                         self._logger,
                         volumes=[f'{self._data_path}/rmlmapper:/data',
                                  f'{self._data_path}/shared:/data/shared'])

    @property
    def root_mount_directory(self) -> str:
        """Subdirectory in the root directory of the case for RMLMapper.

        Returns
        -------
        subdirectory : str
            Subdirectory of the root directory for RMLMapper.

        """
        return __name__.lower()

    @timeout(TIMEOUT)
    def _execute_with_timeout(self, arguments: list) -> bool:
        """Execute a mapping with a provided timeout.

        Returns
        -------
        success : bool
            Whether the execution was successfull or not.
        """
        if self._verbose:
            arguments.append('-vvvvvvvvvvv')

        self._logger.info(f'Executing RMLMapper with arguments '
                          f'{" ".join(arguments)}')

        # Set Java heap to 1/2 of available memory instead of the default 1/4
        max_heap = int(psutil.virtual_memory().total * (1/2))

        # Execute command
        cmd = f'java -Xmx{max_heap} -Xms{max_heap} ' + \
              '-jar rmlmapper/rmlmapper.jar ' + \
              f'{" ".join(arguments)}'
        return self.run_and_wait_for_exit(cmd)

    def execute(self, arguments: list) -> bool:
        """Execute RMLMapper with given arguments.

        Parameters
        ----------
        arguments : list
            Arguments to supply to RMLMapper.

        Returns
        -------
        success : bool
            Whether the execution succeeded or not.
        """
        try:
            return self._execute_with_timeout(arguments)
        except TimeoutError:
            msg = f'Timeout ({TIMEOUT}s) reached for RMLMapper'
            self._logger.warning(msg)

        return False

    def execute_mapping(self,
                        mapping_file: str,
                        output_file: str,
                        serialization: str,
                        rdb_username: Optional[str] = None,
                        rdb_password: Optional[str] = None,
                        rdb_host: Optional[str] = None,
                        rdb_port: Optional[int] = None,
                        rdb_name: Optional[str] = None,
                        rdb_type: Optional[str] = None) -> bool:
        """Execute a mapping file with RMLMapper.

        N-Quads and N-Triples are currently supported as serialization
        format for RMLMapper.

        Parameters
        ----------
        mapping_file : str
            Path to the mapping file to execute.
        output_file : str
            Name of the output file to store the triples in.
        serialization : str
            Serialization format to use.
        rdb_username : Optional[str]
            Username for the database, required when a database is used as
            source.
        rdb_password : Optional[str]
            Password for the database, required when a database is used as
            source.
        rdb_host : Optional[str]
            Hostname for the database, required when a database is used as
            source.
        rdb_port : Optional[int]
            Port for the database, required when a database is used as source.
        rdb_name : Optional[str]
            Database name for the database, required when a database is used as
            source.
        rdb_type : Optional[str]
            Database type, required when a database is used as source.

        Returns
        -------
        success : bool
            Whether the execution was successfull or not.
        """
        arguments = ['-m', os.path.join('/data/shared/', mapping_file),
                     '-s', serialization,
                     '-o', os.path.join('/data/shared/', output_file),
                     '-d']  # Enable duplicate removal

        if rdb_username is not None and rdb_password is not None \
                and rdb_host is not None and rdb_port is not None \
                and rdb_name is not None and rdb_type is not None:

            arguments.append('-u')
            arguments.append(rdb_username)
            arguments.append('-p')
            arguments.append(rdb_password)

            parameters = ''
            if rdb_type == 'MySQL':
                protocol = 'jdbc:mysql'
                parameters = '?allowPublicKeyRetrieval=true&useSSL=false'
            elif rdb_type == 'PostgreSQL':
                protocol = 'jdbc:postgresql'
            else:
                raise ValueError(f'Unknown RDB type: "{rdb_type}"')
            rdb_dsn = f'{protocol}://{rdb_host}:{rdb_port}/' + \
                      f'{rdb_name}{parameters}'
            arguments.append('-dsn')
            arguments.append(rdb_dsn)

        return self.execute(arguments)
```

The Python class for the RMLMapper abstracts the following items so they are
configured consistently:

- Java heap size: set to 50% of the available RAM memory.
This avoids differences among Java versions and Java configurations among different operating systems.
- CLI arguments: provide the path to the mapping file in the exposed `/data/` directory and the verbosity of the logs.
In case of an R2RML mapping, the required CLI arguments to access the database e.g. username, password, host, port are automatically added as well.

**Step 3: add tests for your tool (Optional)**

It is preferable to add some tests for your tool so you know
that the tool is executed correctly.

2 directories are important for adding tests:

- `bench_executor/data/test-cases`: add here the data necessary to execute your test.
Have a look there, several tests are already created and use data from there.
- `tests`: add here your actual test e.g. execute a mapping to transform a CSV file into N-Triples.

For the RMLMapper, several test cases exist from executing 
the Python abstraction class to perform a complete execution of a pipeline.
Have a look around in the mentioned directories to see how to add your tool.

**Step 4: try it out!**

You can try out your tool by having a `metadata.json` file with a description
of the tasks you want to execute.
The `metadata.json` can be generated by using `exgentool` to generate scenarios' 
data. 

## License

Licensed under the [MIT license](./LICENSE)<br>
Written by Dylan Van Assche (dylan.vanassche@ugent.be)
Edited by Sitt Min Oo (x.sittminoo@ugent.be)

