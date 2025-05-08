#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "core.h"

int main(int argc, char **argv)
{
  if (argc < 2)
  {
    fprintf(stderr, "Usage: %s <prog.bin> [--dump-mem|--dump-regs]\n", argv[0]);
    return 1;
  }

  const char *path = argv[1];
  bool dump_mem = argc >= 3 && strcmp(argv[2], "--dump-mem") == 0;
  bool dump_regs = argc >= 3 && strcmp(argv[2], "--dump-regs") == 0;

  // DO NOT reset_cpu() here — it's already done in load_program()

  if (!load_program(path))
  {
    perror("load_program");
    return 1;
  }

  execute_program(dump_mem, dump_regs);

  if (!dump_mem && !dump_regs)
  {
    printf("[\n");
    printf("A = %u\n", A);
    printf("PC = %u\n", PC);
    printf("RUNNING = %u\n", running ? 1 : 0);
    printf("]\n");

    if (memory[0x10] != 0)
      printf("memory[0x10]=[%02X]\n", memory[0x10]);
  }

  return 0;
}
