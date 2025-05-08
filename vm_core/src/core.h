#ifndef CORE_H
#define CORE_H

#include <stdint.h>
#include <stdbool.h>
#include "config.h"

/* ──────────────────────────────
   Global CPU / memory state
   ────────────────────────────── */
extern uint8_t memory[MEM_SIZE];
extern uint8_t A;    /* Accumulator                  */
extern uint16_t PC;  /* Program Counter (wraps)      */
extern bool running; /* main loop flag               */

/* ──────────────────────────────
   Instruction set
   ────────────────────────────── */
typedef enum
{
  OP_NOP = 0x00,
  OP_LOAD_A_IMM = 0x01,
  OP_ADD_A_IMM = 0x02,
  OP_STORE_A = 0x03,
  OP_JMP = 0x04,
  OP_JZ = 0x05,
  OP_HALT = 0xFF
} opcode_t;

/* ──────────────────────────────
   Public API
   ────────────────────────────── */
void reset_cpu(void);                                /* zero regs & RAM   */
bool load_program(const char *path);                 /* file → RAM        */
void execute_program(bool dump_mem, bool dump_regs); /* fetch/execute     */

#endif /* CORE_H */
