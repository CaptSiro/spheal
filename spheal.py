import sys
import os
import cmd
from io import StringIO


os.chdir(os.path.dirname(os.path.realpath(__file__)))


def generate_help(program):
    builder = StringIO()
    builder.write(f"Usage: {program} <commands>")
    for _, entry in cmd.__dict__.items():
        if cmd.is_cmd(entry):
            builder.write("\n\t")
            builder.write(entry.command_name)
            builder.write(" ")
            builder.write(entry.arguments)
            builder.write("\n\t\t")
            builder.write(entry.description)
            builder.write("\n")

    return builder.getvalue()


def dispatch_command(name, args: cmd.Args):
    for _, entry in cmd.__dict__.items():
        if cmd.is_cmd(entry) and entry.command_name == name:
            entry(args)
            exit(0)


def main():
    program = sys.argv[0] or "<program>"

    if len(sys.argv) < 2:
        print(generate_help(program))
        return

    _, command, *arg_list = sys.argv
    if command == "help":
        print(generate_help(program))
        return

    dispatch_command(command, cmd.Args.parse(arg_list))
    # failed to dispatch command
    print(f"Unknown command: <{command}>")


if __name__ == "__main__":
    main()