#!/usr/bin/env python3

"""
The MappingWeaver-java executes RML rules to generate high quality Linked Data
from multiple originally (semi-)structured data sources in a streaming way.

**Website**: https://rml.io<br>
**Repository**: https://github.com/RMLio/MappingWeaver-java
"""

import os
import errno
import shutil
import psutil
from glob import glob
from typing import Optional
from timeout_decorator import timeout, TimeoutError  # type: ignore
from rdflib import Graph, BNode, Namespace, Literal, RDF
from bench_executor.container import Container
from bench_executor.logger import Logger
R2RML = Namespace('http://www.w3.org/ns/r2rml#')
RML = Namespace('http://semweb.mmlab.be/ns/rml#')
D2RQ = Namespace('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#')

VERSION = '1.1.0'  # standalone mode with RDB support
TIMEOUT = 6 * 3600  # 6 hours
IMAGE = f'kg-construct/mappingweaver-java:v{VERSION}'


class MappingWeaver(Container):
    """MappingWeaver container for executing RML mappings."""

    def __init__(self, data_path: str, config_path: str, directory: str,
                 verbose: bool):
        """Creates an instance of the MappingWeaver class.

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
        super().__init__(IMAGE, 'MappingWeaver-java', self._logger,
                         volumes=[f'{self._data_path}/mappingweaver-java:/data',
                                  f'{self._data_path}/shared:/data/shared'])

    @property
    def root_mount_directory(self) -> str:
        """Subdirectory in the root directory of the case for mappingweaver-java.

        Returns
        -------
        subdirectory : str
            Subdirectory of the root directory for mappingweaver-java.

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
        # Set Java heap to 50% of available memory instead of the default 1/4
        max_heap = int(psutil.virtual_memory().total * 0.5)

        # Execute command
        cmd = f'java -Xmx{max_heap} -Xms{max_heap}' + \
              ' -jar weaver/weaver.jar'
        cmd += f' {" ".join(arguments)}'

        self._logger.debug(f'Executing MappingWeaver-java with arguments '
                           f'{" ".join(arguments)}')

        return self.run_and_wait_for_exit(cmd)

    def execute(self, arguments: list) -> bool:
        """Execute mappingweaver-java with given arguments.

        Parameters
        ----------
        arguments : list
            Arguments to supply to mappingweaver-java.

        Returns
        -------
        success : bool
            Whether the execution succeeded or not.
        """
        try:
            return self._execute_with_timeout(arguments)
        except TimeoutError:
            msg = f'Timeout ({TIMEOUT}s) reached for mappingweaver-java'
            self._logger.warning(msg)

        return False

    def execute_mapping(self,
                        mapping_file: str,
                        output_file: str,
                        serialization: str) -> bool:
        """Execute a mapping file with mappingweaver-java.

        N-Quads/N-Triples is the only currently supported as serialization
        format for mappingweaver-java.

        Parameters
        ----------
        mapping_file : str
            Path to the mapping file to execute.
        output_file : str
            Name of the output file to store the triples in.
        serialization : str
            Serialization format to use.

        Returns
        -------
        success : bool
            Whether the execution was successfull or not.
        """
        arguments = ['toFile', ' ',
                     '-o', '/data/output']
        mapping_file = os.path.join('/data/shared/', mapping_file)

        arguments.append('-m')
        arguments.append(mapping_file)
        arguments.append('-p 4') 

        os.makedirs(os.path.join(self._data_path, 'mappingweaver-java', 'output'),
                    exist_ok=True)
        status_code = self.execute(arguments)

        # Combine all output into a single file.
        # Duplicates may exist because mappingweaver-java does not support duplicate
        # removal
        output_path = os.path.join(self._data_path, 'shared', output_file)
        try:
            os.remove(output_path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        with open(output_path, 'a') as out_file:
            files = list(glob(os.path.join(self._data_path, 'mappingweaver-java',
                                           'output', '.*')))
            files += list(glob(os.path.join(self._data_path, 'mappingweaver-java',
                                            'output', '*')))
            for gen_file in files:
                with open(gen_file, 'r') as f:
                    out_file.write(f.read())

        shutil.rmtree(os.path.join(self._data_path, 'mappingweaver-java', 'output'),
                      ignore_errors=True)

        return status_code
