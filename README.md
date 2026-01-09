# Steampunk Mechanical Clock — Python / Tkinter

This project is an **interactive mechanical clock application** developed in **Python using Tkinter**.  
It combines a functional time system with a **steampunk-inspired visual design**, featuring animated gears, analog clock hands, and a digital time display.

The goal of this project is to demonstrate the implementation of **real-time animation**, **event-driven user interaction**, and **custom graphical rendering** within a desktop GUI application.

---

## Project Overview

The application displays the current time through:
- an **analog clock face** with hour, minute, and second hands,
- a **digital display** synchronized with the analog system,
- continuously rotating **mechanical gears** to simulate a physical clock mechanism.

The clock can operate using:
- the **system time**, or
- a **custom user-defined time** that advances autonomously second by second.

---

## Core Features

- Real-time animated clock rendered on a Tkinter `Canvas`
- Steampunk mechanical design with dynamic rotating gears
- Analog and digital time synchronization
- 12-hour and 24-hour display modes (AM/PM support)
- Pause and resume functionality
- Manual time configuration through a dedicated interface
- Alarm system with precise time triggering and popup notification

---

## Technical Approach

- The graphical elements (clock face, hands, gears) are rendered using **mathematical angle calculations**.
- Animation is achieved through a periodic refresh loop using Tkinter’s `after()` method.
- User interactions are handled via event-driven callbacks.
- The alarm system continuously compares the current time state with a user-defined target time.
- The entire interface is built without external libraries, relying solely on Python’s standard modules.

---

## Design Philosophy

The steampunk aesthetic was intentionally chosen to move beyond a basic functional clock and deliver a **visually distinctive application**.  
Dark tones, metallic colors, visible mechanical components, and layered rendering create a cohesive industrial atmosphere inspired by mechanical timepieces.

---

## Learning Objectives

This project was designed to:
- Strengthen understanding of **GUI development** with Tkinter
- Apply **real-time animation techniques**
- Practice **time management logic** and state handling
- Explore **mathematical transformations** for graphical rendering
- Develop a complete, self-contained desktop application

---

## Author

**Lukas Haulet**  
Personal project developed in Python  
