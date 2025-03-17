# Dynamic Memory Management Visualizer

## Overview
This project is a **Dynamic Memory Management Visualizer**, designed to simulate and visualize memory management techniques like **paging, segmentation, and virtual memory**. It allows users to experiment with different memory allocation strategies, page replacement algorithms, and analyze page faults through interactive visualizations.

## Features
- **Paging Simulation:**
  - Simulates **FIFO (First-In-First-Out)** and **LRU (Least Recently Used)** page replacement algorithms.
  - Visualizes page faults and memory frames.
  - Allows user-defined input for page reference strings and frame count.
- **Segmentation Simulation:**
  - Simulates dynamic memory allocation and fragmentation.
  - Implements **First-Fit allocation** strategy.
  - Enables memory allocation, deallocation, and visualization of free and allocated memory blocks.

## Technologies Used
- **Python** (for simulation logic)
- **Matplotlib** (for visualization)

## Installation & Usage
### Prerequisites
Ensure you have Python installed on your system.

```sh
python --version  # Check Python installation
```

### Clone the Repository
```sh
git clone https://github.com/SURAJJJJJ11111/OS.git
cd Dynamic-Memory-Visualizer
```

### Install Dependencies
```sh
pip install matplotlib
```

### Run the Program
```sh
python memory_visualizer.py
```

### Usage Instructions
1. Choose a simulation mode:
   - **1:** Paging Simulation
   - **2:** Segmentation Simulation
2. Follow on-screen instructions to provide input and observe the results.

## Example Input & Output
### **Paging Simulation Example**
```sh
Enter page reference string (comma separated): 7,0,1,2,0,3,0,4,2,3,0,3,2
Enter number of frames: 3
Choose replacement algorithm (FIFO or LRU): FIFO
```
**Output:**
- Total page faults displayed.
- Step-by-step visualization of page frame contents.

### **Segmentation Simulation Example**
```sh
Enter total memory size: 100
Commands:
  allocate segment1 30
  allocate segment2 40
  deallocate segment1
  show
  exit
```
**Output:**
- Displays allocated and free memory blocks.
- Visualizes memory layout graphically.


---
Developed by **Suraj Kumar Prajapati**

