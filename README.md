# Knowledge Graph Construction Challenge 2026


Knowledge Graph Construction has seen a wide uptake among academics and industry. Previous editions of Knowledge Graph Construction Workshop have focused on either benchmarking the performance of knowledge graph construction implementations or the conformance of the implementations according to the latest RML modules. For this year, the W3C Community Group on Knowledge Graph Construction introduces 3 challenges, which aim to cover the three dimensions of knowledge graph construction of heterogeneous data; i) conformance, ii) performance, and iii) mapping methodology.



## Track 1: Conformance
The set of new specification for the RDF Mapping Language (RML) established by the W3C Community Group on Knowledge Graph Construction provide a set of test-cases for each module:

> [!NOTE]  
> Although the test cases are published on their corresponding websites and available in their GitHub repositories, we recommend downloading them directly from the DOI, as the other resources may be subject to change.

- [RML-Core](http://w3id.org/rml/core/test-cases): https://doi.org/10.5281/zenodo.19049860
- [RML-IO](http://w3id.org/rml/io/test-cases): https://doi.org/10.5281/zenodo.19049774
- [RML-CC](http://w3id.org/rml/cc/test-cases): https://doi.org/10.5281/zenodo.19055451
- [RML-FNML](http://w3id.org/rml/fnml/test-cases): https://doi.org/10.5281/zenodo.19055650
- [RML-LV](http://w3id.org/rml/lv/test-cases): https://doi.org/10.5281/zenodo.19055778

These test-cases are evaluated in this Track of the Challenge to determine their feasibility, correctness, etc. by applying them in implementations. If you find problems with the mappings, output, etc. please report them to the corresponding repository of each module (https://w3id.org/rml/portal).

Through this Track we aim to spark development of implementations for the new specifications and improve the test-cases. Let us know your problems with the test-cases and we will try to find a solution.

**Results:** There is a template available in this [folder](./track_1_conformance/) for reporting your results. Once completed, please submit it to this repository via a Pull Request.

> [!IMPORTANT]
> RML-star is not included in this year’s challenge, as RDF 1.2 has evolved considerably and the specification needs to be adapted to the final recommendation.

## Track 2: Performance

Knowledge graph construction of heterogeneous data has seen a lot of uptake in 
the last decade from compliance to performance optimizations with respect to execution time. 
Besides execution time as a metric for comparing knowledge graph construction, other metrics e.g. CPU or memory usage are not considered. 

This challenge aims at sparking interest among RDF graph construction systems 
to comply with the new RML specifications and its modules 
while benchmarking them regarding e.g. execution time, CPU, memory usage, or a combination of these metrics.

Participants will be provided with a virtual machine with uniform hardware
resources to ensure a fair comparison of all the mapping implementations. 

> [!IMPORTANT]
> Please keep an eye out for an email from the organizers for login details to the virtual machines

The performance challenge aims to evaluate the materialization capabilities
under the following scenarios: 

**Data**

* Number of data records: scaling the data size vertically by the number of records with a fixed number of data properties (10K, 100K, 1M, 10M records).
* Number of data properties: scaling the data size horizontally by the number of data properties with a fixed number of data records (1, 10, 20, 30 columns).
* Number of duplicate values: scaling the number of duplicate values in the dataset (0%, 25%, 50%, 75%, 100%).
* Number of empty values: scaling the number of empty values in the dataset (0%, 25%, 50%, 75%, 100%).

**Mappings**

* Number of subjects: scaling the number of subjects with a fixed number of predicates and objects (1, 10, 20, 30 TMs).
* Number of predicates and objects: scaling the number of predicates and objects with a fixed number of subjects (1, 10, 20, 30 POMs).
* Number of named graphs: scaling the number of named graphs either in subject maps or predicate-object maps. 
* Number of and type of joins: scaling the number of joins and type of joins (1-1, N-1, 1-N, N-M)

**RML-CC: Collections and Containers (New!)**

* Scaling number of records while keeping a fixed-size list of values per record (10k to 10M records). 

* Scaling number of values inside the list per data record. 

* Scaling percentage of matching keys inside the list of values per record to
  measure collections and containers join performance.  

* Scaling percentage of data duplication inside the list of values for testing
  performance when handling redundancy.


> [!NOTE]
> A more detailed instruction for running the challenge can be found in the [README](./track_2_performance/README.md) under the `./track_2_performance/` folder. 



## Track 3: Mapping Methodology

Although RML has become the de facto standard for constructing knowledge graphs from heterogeneous data sources, the design space for defining and executing mappings is far from closed. There remains significant potential to explore alternative approaches to generating knowledge graphs from heterogeneous data, including improvements in automation, optimization, maintainability, and expressiveness.

This challenge track invites participants to push beyond existing approaches and propose novel solutions for knowledge graph generation. Participants may build upon RML and its ecosystem, introduce extensions or optimizations, or depart from RML entirely in favor of new mapping models, languages, automation techniques, or execution strategies. The focus is on innovation in how mappings are defined, generated, and executed, as well as on demonstrating practical benefits such as reusability, maintainability, scalability, or expressiveness.

By encouraging a broad range of approaches, this track aims to foster comparative insights into alternative techniques for knowledge graph construction from heterogeneous data sources.

Submissions may explore different dimensions of innovation, including (but not limited to):

- Mapping language or model design
- Mapping automation or generation
- Reusability and modularization of mappings

### Scenario 1:  Public Procurement Data Space

The first scenario is derived from the Public Procurement Data Space (PPDS). Participants are provided with public procurement notices extracted from the Tenders Electronic Daily (TED) platform in XML format.

The task consists of generating an RDF knowledge graph compliant with a subset of the ePO ontology, which is provided as part of the challenge resources.

To facilitate evaluation and reproducibility, the expected output graph is also provided in Turtle format.

Participants must transform the XML input data into RDF according to the ontology specification so that the generated graph matches the provided reference output.


### Scenario 2:

The second scenario is provided by Meemo. Participants must transform the provided JSON files into the expected RDF graphs provided.

Relevant RDFS and SHACL documentation can be found in
- https://developer.meemoo.be/docs/metadata/knowledge-graph/1.1.0/description/en/
- https://developer.meemoo.be/docs/metadata/knowledge-graph/1.0.0/objects/en/
- https://developer.meemoo.be/docs/metadata/knowledge-graph/1.0.0/events/en/

### Scenario 3:

TBA soon
