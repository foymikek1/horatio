#include <stdio.h>
#include <string.h>
#include "core.h"

uint8_t memory[MEM_SIZE];
uint8_t A;
uint16_t PC;
bool running;

static void dump_memory(void)
{
  for (size_t i = 0; i < MEM_SIZE; ++i)
    printf("%02X\n", memory[i]);
}

static void dump_registers(void)
{
  printf("A = %u\n", A);
  printf("PC = %u\n", PC);
  printf("RUNNING = %u\n", running ? 1 : 0);
}

void reset_cpu(void)
{
  memset(memory, 0, sizeof(memory));
  A = 0;
  PC = 0;
  running = true;
}

bool load_program(const char *path)
{
  if (!path)
    return false;

  FILE *f = fopen(path, "rb");
  if (!f)
    return false;

  fread(memory, 1, MEM_SIZE, f);
  fclose(f);
  return true;
}

void execute_program(bool dump_mem, bool dump_regs)
{
  while (running)
  {
    if (PC >= MEM_SIZE)
    {
      fprintf(stderr, "PC out of bounds: %u\n", PC);
      running = false;
      break;
    }

    uint8_t opcode = memory[PC++];

    switch (opcode)
    {
    case OP_NOP:
      break;

    case OP_LOAD_A_IMM:
      A = memory[PC++];
      break;

    case OP_ADD_A_IMM:
      A += memory[PC++];
      break;

    case OP_STORE_A:
    {
      uint8_t addr = memory[PC++];
      memory[addr] = A;
      break;
    }

    case OP_JMP:
    {
      uint8_t target = memory[PC++];
      PC = target;
      break;
    }

    case OP_JZ:
    {
      uint8_t target = memory[PC++];
      if (A == 0)
        PC = target;
      break;
    }

    case OP_HALT:
      running = false;
      break;

    default:
      running = false;
      break;
    }
  }

  if (dump_mem)
    dump_memory();
  if (dump_regs)
    dump_registers();
}
