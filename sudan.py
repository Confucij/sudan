import getopt
import json
import os
import re

import sys

############################ Renderers ######################################

def render_default(fchains):

    conn = []
    for func, chains in fchains.items():
        local_conn = []
        for chain in chains:
            if not chain:
                continue
            stack = chain[0][1]
            for i in range(0, len(chain) - 1):
                stack += chain[i+1][1]
                local_conn.append('"{}:{}" -> "{}:{}" [label={}, style=solid];'.format(
                    chain[i][0], chain[i][1], chain[i+1][0], chain[i+1][1], stack))
        local_conn = ['"{}:{}" [style=filled,fillcolor=green];\n'.format(func[0], func[1])] + list(set(local_conn))
        conn += local_conn
    return 'digraph callgraph {\nrankdir=LR;\n' + "".join(conn) + "\n}"



############################ General Functions ################################

def parse_su_file(path):
    su_file = open(path, 'r')
    pattern = re.compile(".*:(.*)\s(\d+)\s(static|dynamic).*$")
    stacks = {}
    for line in su_file:
        match = pattern.match(line)
        if match:
            stacks[match.group(1)] = int(match.group(2))
        else:
            print(line)
    return stacks

def parse_egypt_call_data(path):
    su_file = open(path, 'r')
    pattern = re.compile('"(.+)"\s->\s"(.+)"\s\[style=solid\];')
    calls = []
    for line in su_file:
        match = pattern.match(line)
        if match:
            calls.append((match.group(1),match.group(2)))
    return calls

def build_call_chains(ftuples, depth=10, finterest=None, fstacks=None, fexcept=None):
    """

    :type ftuples: list
    :type depth: int
    :type finterest: list
    :type fstacks: dict
    :return: dict
    """

    if not fstacks:
        fstacks = {}

    top_functions = {}

    for caller, calle in ftuples:
        top_functions.setdefault(caller, []).append(calle)

    if not finterest:
        finterest = [x for x in top_functions.keys()]

    chains = {}
    for func in finterest:
        fchain = []
        chains[(func, fstacks.setdefault(func, 0))] = fchain
        try:
            callees = top_functions[func].copy()
        except KeyError:
            continue

        cur_depth = depth
        stack = []
        chain = [(func, fstacks[func])]
        while True:
            try:
                callee = callees.pop()
            except IndexError:
                try:
                    callees = stack.pop()
                    chain.pop()
                    cur_depth += 1
                except IndexError:
                    break

            chain.append((callee, fstacks.setdefault(callee, -1)))
            if callee in fexcept:
                fchain.append(chain.copy())
                chain.pop()
                continue

            if callee in top_functions:
                if cur_depth:
                    cur_depth -= 1
                    stack.append(callees)
                    callees = top_functions[callee].copy()
                else:
                    fchain.append(chain.copy())
                    chain.pop()
                    continue
            else:
                fchain.append(chain.copy())
                chain.pop()

    return chains

############################# Main function ##############################################

if __name__ == '__main__':

    options, args = getopt.getopt(sys.argv[1:], "d:f:e:", ["su=", "exp=", "except="])
    stack_sizes = None
    calls = []
    fexcept = []
    finterest = []
    depth = 5

    for opt, arg in options:
        if opt == "--su":
            stack_sizes = parse_su_file(arg)
        if opt == "--exp":
            calls = parse_egypt_call_data(arg)
        if opt == "--except":
            fexcept.append(arg)
        if opt == "-d":
            depth = int(arg)
        if opt == "-f":
            finterest.append(arg)
        if opt == "-e":
            fexcept.append(arg)


    if not calls:
        print("Nothing to do", file=sys.stderr)
        exit(0)
    if not stack_sizes:
        stack_sizes = {}

    chains = build_call_chains(calls, depth, finterest, stack_sizes, fexcept)
    print(render_default(chains))

    exit(0)