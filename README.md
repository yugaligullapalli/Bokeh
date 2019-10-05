# Bokeh Graph Obfuscator

## Pip Prerequisites

* pyproj
* pyshp
* numpy
* bitstring

## Command-Line Interface

### Global Parameters

* `-s 123` or `-seed 123`: The `-s` parameter allows you to specify a seed to use for randomization. This allows obfuscating with repeatable results. This feature is very useful for obfuscating two shapefiles that each contain nodes or edges but represent the same network. By using the same seed, the edges will still correspond to where the nodes are obfuscated.
* `-d 123` or `-p 123` or `--decimals 123`: This parameter represents the `d` or `p` variables used in the Bokeh paper.
* `-a abc` or `--anonymizer abc`: This argument sets which anonymization technique to use. Your options are:
  * geocentric
  * accuracy-fuzzing
  * precision-truncation
  * tcpdpriv-like
  * cryptographic
* `-cdf path`: The path to an output file of moved distances for each of the nodes in the obfuscated network.

### Line-of-Sight Networks

Use the `los` argument and the arguments below to specify that you are processing a line-of-sight network. 

* `-n`: Node file input
* `-e`: Edge file input
* `-N`: Node file output
* `-E`: Edge file output

#### Randomization Options

* `-np`: The node goal probability for tier 3 randomization.
* `-ep`: The edge goal probability for tier 3 randomization.

### Shapefile Networks

Use the `shapefile` argument, followed by the path to the input shapefile. Use the `-o path/to/output` argument to specify the shapefile output.