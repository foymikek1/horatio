Horatio was experimental nature: it didn’t fully work, but the lessons learned made it a valuable learning experience fueling curiosity and learning.



---
# Horatio

**Status:** Experimental / Incomplete

## Overview

Horatio is a passion project born out of a desire to understand how virtual machines (VMs) and SSH servers operate at a fundamental level. By building both sides of the interaction from scratch, the goal was to observe and learn how the client and server agents communicate live over the TCP protocol.

## Goals

* Implement a minimal VM core capable of running basic instructions.
* Build a simple SSH server to handle TCP handshakes and client authentication.
* Explore the interplay between networking, system calls, and subprocess I/O buffering.

## Project Status

This project did not reach a fully working state as intended. However, the process uncovered valuable insights and learning opportunities.

## Lessons Learned

* Deep dive into Paramiko’s `ServerInterface` and the SSH handshake process.
* Mapping abstract machine concepts to real-world networked systems.
* Coordinating asynchronous I/O, buffering, and subprocess management in Python.
* The importance of clear protocol diagrams and explicit state management when designing networked systems.

## Future Work

* Refactor to separate VM core logic from networking components for better modularity.
* Add comprehensive tests for packet parsing, state transitions, and error handling.
* Extend the VM instruction set and integrate a lab environment for interactive experimentation.

---


