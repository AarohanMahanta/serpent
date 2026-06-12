import sys 
from interpreter.vm import VirtualMachine


if __name__ == "__main__":
    script = sys.argv[1]

with open(script) as f:
    source = f.read()

code = compile(source, script, "exec")

vm = VirtualMachine()
vm.run(code)