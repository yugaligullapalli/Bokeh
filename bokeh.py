#!/usr/bin/env python3

import argparse
import processing_modes.shapefiles as shapefile
import processing_modes.lineOfSight as lineOfSight
import anonymizers.tier3.lineOfSightRandomizer as lineOfSightRandomizer
import anonymizers.tier1.geocentric as geocentric
import anonymizers.tier1.accuracyFuzzing as accuracyFuzzing
import anonymizers.tier1.precisionTruncation as precisionTruncation
import anonymizers.tier2.tcpdPrivLike as tcpdPrivLike
import anonymizers.tier2.cryptographic as cryptographic
import anonymizers.distanceTracker as distanceTracker

anonymizers = {
    'geocentric': geocentric,
    'accuracy-fuzzing': accuracyFuzzing,
    'precision-truncation': precisionTruncation,
    'tcpdpriv-like': tcpdPrivLike,
    'cryptographic': cryptographic,
}

class NullAnonymizer:
    def __init__(self):
        self.seed = lambda x: None
        self.anonymize = lambda lat, lon,_: (lat, lon)

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--anonymizer', help='Obfuscator to use on the graph', type=str, choices=anonymizers.keys())
parser.add_argument('-d', '-p', '--decimals', dest='decimals', type=int, nargs='?', default=0)
parser.add_argument('-s', '--seed', dest='seed', help='Seed for randomization', type=int, nargs='?')
parser.add_argument('-cdf', type = argparse.FileType('w'), help='Output file for distance changes.')

subparsers = parser.add_subparsers(dest='input type', description='input type')
subparsers.required = True
shapefiles = subparsers.add_parser('shapefile', help='ESRI Shapefiles')
shapefiles.add_argument('shapefileIn', type=argparse.FileType('rb'), help='Input shapefile.')
shapefiles.add_argument('-o', required=True, dest='shapefileOut', type=argparse.FileType('wb'), help='Output shapefile.')
los = subparsers.add_parser('los', help='Line-of-sight networks represented in CSV files')
los.add_argument('-n', required=True, dest='nodesInput', type=argparse.FileType('r'), help='Input nodes file.')
los.add_argument('-e', required=True, dest='edgesInput', type=argparse.FileType('r'), help='Input edges file.')
los.add_argument('-N', required=True, dest='nodesOutput', type=argparse.FileType('w'), help='Output nodes file.')
los.add_argument('-E', required=True, dest='edgesOutput', type=argparse.FileType('w'), help='Output edges file.')
randomizerGroup = los.add_argument_group(title='Line of Sight Tier 3 Options')
randomizerGroup.add_argument('-np', help='Goal Node Probability', type=float, nargs='?', default=1.0)
randomizerGroup.add_argument('-ep', help='Goal Edge Probability', type=float, nargs='?', default=1.0)

arguments = parser.parse_args()

shapefileMode = hasattr(arguments, 'shapefileIn')
network = None
processor = None

if shapefileMode:
    print("Using shapefileMode")
    network = shapefile.read(arguments.shapefileIn)
    processor = shapefile.process
else:
    network = lineOfSight.read(arguments.nodesInput, arguments.edgesInput)
    network = lineOfSightRandomizer.randomize(network, arguments.np, arguments.ep)
    processor = lineOfSight.process

anonymizer = NullAnonymizer()

if arguments.anonymizer:
    anonymizer = anonymizers[arguments.anonymizer]

needToFlush = False

if arguments.cdf:
    anonymizer = distanceTracker.DistanceTracker(anonymizer, arguments.cdf)
    needToFlush = True

if arguments.seed:
    anonymizer.seed(arguments.seed)
print("About to start processing")
outNetwork = processor(network, anonymizer.anonymize, arguments.decimals,arguments)


if shapefileMode:
    shapefile.write(outNetwork, arguments.shapefileOut)
else:
    lineOfSight.write(outNetwork, arguments.nodesOutput, arguments.edgesOutput)

if needToFlush:
    anonymizer.flush()
