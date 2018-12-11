#!/usr/bin/env python3

from __future__ import print_function
from argparse import ArgumentParser
from tabulate import tabulate
import csv
import sys

# Parameters

# Year
Y = 20
# Total
P = 166
# Rate of year
R = 0.049
# N month
N = 12 * Y
# Rate of tong huo peng zhang
Rtz = 0.03 / 12

HEADERS = ["Term", "Total pay", "Interest pay"]
# Return table column ["Term", "Total pay", "Interest pay"]
# Equal principle interest
def CalcEqualPrincipleInterest(year, rate, principle):
    result = []
    sumtotal, suminterest = 0, 0
    n, r, p = year * 12, rate, principle
    xtotal = p*(r*((1+r)**n)/((1+r)**n-1))
    for i in range(1, n+1):
        xinterest = p*r*((1+r)**n-(1+r)**i)/((1+r)**n-1)
        sumtotal += xtotal
        suminterest += xinterest
        result.append([i, xtotal, xinterest])
    result.append([None, sumtotal, suminterest])
    return result

# Equal principle
def CalcEqualPrinciple(year, rate, principle):
    result = []
    sumtotal, suminterest = 0, 0
    n, r, p = year * 12, rate, principle
    for i in range(1, n+1):
        xtotal = p/n+(n-i+1)/n*p*r
        xinterest = (n-i+1)/n*p*r
        sumtotal += xtotal
        suminterest += xinterest
        result.append([i, xtotal, xinterest])
    result.append([None, sumtotal, suminterest])
    return result

def PrintTableResult(result, filename=""):
    table = tabulate(result,
                     headers=HEADERS,
                     tablefmt='orgtbl')
    if (filename):
        with open(filename+".txt", "w") as f:
            print(table, file=f)
    else:
        print(table)

def PrintCsvResult(result, filename=""):
    if (filename):
        csvfile = open(filename+'.csv', 'w', newline='')
        resultwriter = csv.writer(csvfile)
    else:
        resultwriter = csv.writer(sys.stdout)
    resultwriter.writerow(HEADERS)
    for r in result:
        resultwriter.writerow(r)


if __name__ == "__main__":
    parser = ArgumentParser(description="The DaiKuang Calculator")
    parser.add_argument("--method", "-m", choices=["p", "i", ""], default="",
                        help="Method to pay (equal principle'p', equal principle interest'i', both'')")
    parser.add_argument("--formatter", "-f", choices=["t", "c"], default="t",
                        help="Format of the output (table't', csv'c')")
    parser.add_argument("--outputfile", "-o", type=str, default="",
                        help="Filename to output")

    parser.add_argument("--year", "-y", type=int, default=Y,
                        help="Years")
    parser.add_argument("--principle", "-p", type=int, default=P,
                        help="Total principle")
    parser.add_argument("--rate", "-r", type=float, default=R,
                        help="Rate")

    parser.add_argument("--debug", action="store_true",
                        help="print debug info if enabled")

    options = parser.parse_args()
    if (options.debug):
        print(options)

    result1, result2 = None, None
    if (options.method == 'p'):
        result2 = CalcEqualPrinciple(options.year, options.rate/12, options.principle)
    elif (options.method == 'i'):
        result1 = CalcEqualPrincipleInterest(options.year, options.rate/12, options.principle)
    else:
        result2 = CalcEqualPrinciple(options.year, options.rate/12, options.principle)
        result1 = CalcEqualPrincipleInterest(options.year, options.rate/12, options.principle)

    if (result1):
        print("\nEqual principle interest")
        if (options.formatter == "t"):
            PrintTableResult(result1, options.outputfile)
        elif (options.formatter == "c"):
            PrintCsvResult(result1, options.outputfile)
    if (result2):
        print("\nEqual principle")
        PrintTableResult(result2, options.outputfile)
        if (options.formatter == "t"):
            PrintTableResult(result2, options.outputfile)
        elif (options.formatter == "c"):
            PrintCsvResult(result2, options.outputfile)
