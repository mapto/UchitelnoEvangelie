Main difference between `integrator` and `indexgenerator` is that they respectively depend on `exporter` and `generator`. Otherwise, they follow a similar pipeline.

```mermaid
graph LR
  importer --> merger --> aggregator --> generator/exporter
```

Below an explanation of the columns in a table, as documented in [setup.py](setup.py#L33).

![An image showing a explanation of the table columns](../docs/table-demo.gif)

The below animation illustrates how a completed table is being converted into a list.

![An animation showing an example of what the integrator does](../docs/integrator-demo.gif) 

This image shows what in the index is different from the list.

![An image showing an example of what the index generator does](../docs/indexgenerator-demo.gif) [src](https://docs.google.com/presentation/d/1QJGfndGEz3s0MTzaVZ7T3PywzJ_DmIANtfSbkfgmQBs)

See futher examples for both in [test](test/)

The range of sources are provided in [`sl-sources.txt`](sl-sources.txt) and [`gr-sources.txt`](gr-sources.txt). The first line in each contains the main manuscript reference. For the way how default (implicit) variant source is indicated, see implementation in [`config.py`](config.py), lines [`DEFAULT_SL: str = "".join(VAR_SL)`](config.py#L52) and [`DEFAULT_GR: str = VAR_GR[0]`](config.py#L54).

Here is the data model that the aggregator embeds in the tree leaves of the dictionaries ([generated](../docs/usage.uxf) with [umlet](https://www.umlet.com)):

![An image showing the aggregator data model](../docs/usage.png) 

# Dependency Tree

```mermaid
graph LR
  const --> config
  regex --> const
  util --> const
  util --> alphabet 
  source --> config

  subgraph Model
    model --> source
    usage --> address
    usage --> model
    counter --> usage
  end
  semantics_util --> usage
  lang --> regex
  lang --> util
  lang --> usage
  
  subgraph Semantics
    semantics_util --> semantics_const
    semabs --> semantics_util
    semmain --> semantics_util
    semvar --> semantics_util
    lang --> semabs
    lang --> semmain
    lang --> semvar
    table --> lang 
  end
  setup --> lang

  grouper --> lang
  merger --> grouper

  aggregator --> source
  aggregator --> lang

  importer --> table

  wordproc --> config
  exporter --> usage

  exporter & generator --> util & wordproc
  integrator --> exporter
  generator --> counter
  indexgenerator --> generator
  indexgenerator & integrator -->  setup & importer & merger & aggregator
```
