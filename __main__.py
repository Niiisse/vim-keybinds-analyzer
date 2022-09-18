import argparse
from rich import box
from rich.table import Table
from rich.console import Console

# Parsing
desc = "Parse (neo)vim config file and list all detected keybinds."
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("-i", "--input", help="Input file", required=True)
args = parser.parse_args()

configFile = open(args.input, 'r')
lines = configFile.readlines()
configFile.close()

table = Table(title="Keybinds", box=box.MINIMAL_DOUBLE_HEAD)
table.add_column("ID", justify="right", style="bright_cyan")
table.add_column("Category", justify="right", style="bright_green")
table.add_column("Mode", justify="right", style="bright_magenta")
table.add_column("Keys", justify="center", style="bold")
table.add_column("Command")

count = 1
lastCategory = ""

for idx, line in enumerate(lines):
    strippedLine = line.strip()

    if len(strippedLine) > 0:
        if "\" parse: " in strippedLine:
            lastCategory = strippedLine[9:]
        elif strippedLine[0] != "\"":
            if "remap" in strippedLine:
                splitLine = strippedLine.split(" ")

                if "<silent>" in splitLine[1]:
                    del splitLine[1]

                table.add_row(str(count), lastCategory, splitLine[0], splitLine[1], ''.join(
                    [str(item) for item in splitLine[2:]]))

                count += 1

console = Console()
console.print(table)
