import getopt, sys
from .excel_processor import ExcelTestCaseProcessor
import signal

# Convenience function for exiting when there's a problem
def errExit(msg: str) -> None:
    print(msg)
    sys.exit()

# Returns a tuple containing the following:
# 0 - skiprows: the number of rows to skip (index 0)
# 1 - nrows: the number of rows to execute starting from skiprows
def getRanges(range_str: str) -> tuple[int, int]:
    try:
        ranges = range_str.split(":")
        if len(ranges) != 2:
            errExit("Invalid range format. Enter <number>:<number>")
        skiprows = int(ranges[0])
        nrows = int(ranges[1])
        if skiprows < 0 or nrows < 0:
            errExit("Range indexes out of bounds.")
        return (skiprows, nrows)
    except Exception as err:
        errExit(str(err))

# Allows for graceful exit when Ctrl + C is pressed during processing
def aborthandler(signum, frame):
    print("\nAborting!", flush=True)
    sys.exit()

def main():
    arg_list = sys.argv[1:]
    input_path = ''
    output_path = ''
    env = ''
    range = None

    signal.signal(signal.SIGINT, aborthandler)

    try:
        opts, args = getopt.getopt(arg_list, "ho:i:e:r:", ["output=", "input=", "env=", "range="])
        for opt, arg in opts:
            if opt in ("-i", "--input"):
                input_path = arg
            elif opt in ("-o", "--output"):
                output_path = arg
            elif opt in ("-e", "--env"):
                env = arg
            elif opt in ("-r", "--range"):
                range = getRanges(arg)
            elif opt in ("-h", "--help"):
                print("""usage: python3 main.py
    -i, --input   Input xlsx file name.
    -e, --env     Environment name. Ensure connection.conf is set up properly.
    -o, --output  Optional. Output xlsx file name. Defaults to output.xlsx.
    -r, --range   Optional. Range of rows, format <number>:<number>. The first
                    number is the starting index and the second number is the
                    number of rows to process.
                """)
                sys.exit()

    except getopt.error as err:
        errExit(str(err))

    if input_path == "":
        errExit("Must provide path to excel input")
    if env == "":
        errExit("Must provide an instance name")

    try:
        ExcelTestCaseProcessor(input_path, output_path, env, range).process()
    except Exception as err:
        errExit(f"\nError: {err}")

if __name__ == "__main__":
    main()