#OS SELECted

import matplotlib.pyplot as plt

# ================= Paging Simulation Functions =================

def simulate_fifo(page_seq, frame_count):
    """
    Simulate page replacement using FIFO.
    Returns:
      - states: a list of lists showing the content of each frame after every page request.
      - faults: total number of page faults.
      - fault_flags: list of booleans indicating if a fault occurred at each request.
    """
    
    frames = []
    states = []
    fault_flags = []
    faults = 0
    queue = []  # to maintain FIFO order

    for page in page_seq:
        if page in frames:
            fault_flags.append(False)
        else:
            faults += 1
            fault_flags.append(True)
            if len(frames) < frame_count:
                frames.append(page)
                queue.append(page)
            else:
                # Replace the oldest page in FIFO order.
                old_page = queue.pop(0)
                index = frames.index(old_page)
                frames[index] = page
                queue.append(page)
        # Capture the snapshot of current frames (fill unused frames with '-')
        state_snapshot = frames.copy()
        while len(state_snapshot) < frame_count:
            state_snapshot.append('-')
        states.append(state_snapshot)
    return states, faults, fault_flags

def simulate_lru(page_seq, frame_count):
    """
    Simulate page replacement using LRU.
    Returns:
      - states: a list of lists showing the content of each frame after every page request.
      - faults: total number of page faults.
      - fault_flags: list of booleans indicating if a fault occurred at each request.
    """
    frames = []
    states = []
    fault_flags = []
    faults = 0
    usage_order = []  # to track recency of use

    for page in page_seq:
        if page in frames:
            fault_flags.append(False)
            # Move page to the end to mark it as most recently used.
            usage_order.remove(page)
            usage_order.append(page)
        else:
            faults += 1
            fault_flags.append(True)
            if len(frames) < frame_count:
                frames.append(page)
                usage_order.append(page)
            else:
                # Remove the least recently used page.
                lru_page = usage_order.pop(0)
                index = frames.index(lru_page)
                frames[index] = page
                usage_order.append(page)
        state_snapshot = frames.copy()
        while len(state_snapshot) < frame_count:
            state_snapshot.append('-')
        states.append(state_snapshot)
    return states, faults, fault_flags

def plot_paging_simulation(states, page_seq, fault_flags, algorithm_name, total_faults, frame_count):
    """
    Create a table visualization showing the state of memory frames after each page request.
    Each column corresponds to a page request (with an indication if a page fault occurred),
    and each row corresponds to a frame.
    """
    num_steps = len(page_seq)
    fig, ax = plt.subplots(figsize=(num_steps * 0.7, frame_count * 0.7 + 2))
    ax.axis('off')
    
    # Prepare table data: rows represent frames.
    table_data = []
    for r in range(frame_count):
        row = []
        for state in states:
            row.append(state[r])
        table_data.append(row)
    
    # Column labels: show the page number and indicate "Fault" if a page fault occurred.
    col_labels = [f"{p}\n{'Fault' if fault_flags[i] else ''}".strip() 
                  for i, p in enumerate(page_seq)]
    row_labels = [f"Frame {i+1}" for i in range(frame_count)]
    
    the_table = ax.table(cellText=table_data, colLabels=col_labels, rowLabels=row_labels, 
                         loc='center', cellLoc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    the_table.scale(1.2, 1.2)
    
    # Highlight columns where a page fault occurred.
    for col in range(num_steps):
        if fault_flags[col]:
            for row in range(frame_count):
                cell = the_table[(row, col)]
                cell.set_facecolor('#FF9999')  # light red highlight
    
    plt.title(f"{algorithm_name} Paging Simulation\nTotal Page Faults: {total_faults}", pad=20)
    plt.show()

def paging_simulation():
    print("=== Paging Simulation ===")
    # Get the page reference string.
    input_seq = input("Enter page reference string (comma separated, e.g., 7,0,1,2,0,3,0,4): ").strip()
    if not input_seq:
        page_seq = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    else:
        try:
            page_seq = [int(x.strip()) for x in input_seq.split(',')]
        except Exception as e:
            print("Invalid input format. Using default sequence.")
            page_seq = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    
    # Get the number of frames.
    try:
        frame_count = int(input("Enter number of frames: ").strip())
    except:
        print("Invalid input. Using default number of frames = 3.")
        frame_count = 3
    
    # Choose the replacement algorithm.
    algo_choice = input("Choose replacement algorithm (FIFO or LRU): ").strip().lower()
    if algo_choice == "fifo":
        states, faults, fault_flags = simulate_fifo(page_seq, frame_count)
        algo_name = "FIFO"
    elif algo_choice == "lru":
        states, faults, fault_flags = simulate_lru(page_seq, frame_count)
        algo_name = "LRU"
    else:
        print("Invalid choice. Defaulting to FIFO.")
        states, faults, fault_flags = simulate_fifo(page_seq, frame_count)
        algo_name = "FIFO"
    
    print(f"\n{algo_name} Paging Simulation complete. Total page faults: {faults}")
    for i, state in enumerate(states):
        print(f"After page {page_seq[i]}: {state} {'Fault' if fault_flags[i] else ''}")
    
    # Visualize the simulation.
    plot_paging_simulation(states, page_seq, fault_flags, algo_name, faults, frame_count)


# ================= Segmentation Simulation Functions =================

def merge_free_list(free_list):
    """
    Merge contiguous free blocks.
    free_list: list of tuples (start, size)
    Returns a merged free list.
    """
    free_list.sort(key=lambda x: x[0])
    merged = []
    for block in free_list:
        if not merged:
            merged.append(block)
        else:
            last_start, last_size = merged[-1]
            current_start, current_size = block
            if last_start + last_size == current_start:
                merged[-1] = (last_start, last_size + current_size)
            else:
                merged.append(block)
    return merged

def allocate_segment(free_list, size):
    """
    Use first-fit allocation to allocate a segment of given size.
    Returns the starting address for the allocated segment and updates the free_list.
    If allocation fails, returns None.
    """
    for i, (start, free_size) in enumerate(free_list):
        if free_size >= size:
            allocated_start = start
            # Update the free block.
            if free_size == size:
                free_list.pop(i)
            else:
                free_list[i] = (start + size, free_size - size)
            return allocated_start, free_list
    return None, free_list

def segmentation_simulation():
    print("=== Segmentation Simulation ===")
    try:
        memory_size = int(input("Enter total memory size (in units): ").strip())
    except:
        print("Invalid input. Using default memory size = 100.")
        memory_size = 100

    # Initially, all memory is free.
    free_list = [(0, memory_size)]
    allocated_segments = {}  # Dictionary: key = segment id, value = (start, size)

    print("\nCommands:")
    print("  allocate <segment_id> <size>  - Allocate memory for a segment")
    print("  deallocate <segment_id>       - Deallocate a segment")
    print("  show                          - Show current memory allocation")
    print("  exit                          - Finish simulation and visualize memory")
    
    while True:
        command = input("Enter command: ").strip().lower()
        if command == "exit":
            break
        parts = command.split()
        if not parts:
            continue
        if parts[0] == "allocate":
            if len(parts) != 3:
                print("Invalid command format. Use: allocate <segment_id> <size>")
                continue
            seg_id = parts[1]
            try:
                size = int(parts[2])
            except:
                print("Invalid size. Must be an integer.")
                continue
            if seg_id in allocated_segments:
                print(f"Segment {seg_id} is already allocated.")
                continue
            alloc_start, free_list = allocate_segment(free_list, size)
            if alloc_start is not None:
                allocated_segments[seg_id] = (alloc_start, size)
                print(f"Allocated segment {seg_id} at address {alloc_start} with size {size}.")
            else:
                print("Allocation failed: Not enough free memory.")
        elif parts[0] == "deallocate":
            if len(parts) != 2:
                print("Invalid command format. Use: deallocate <segment_id>")
                continue
            seg_id = parts[1]
            if seg_id not in allocated_segments:
                print(f"Segment {seg_id} not found.")
                continue
            start, size = allocated_segments.pop(seg_id)
            free_list.append((start, size))
            free_list = merge_free_list(free_list)
            print(f"Deallocated segment {seg_id} from address {start} with size {size}.")
        elif parts[0] == "show":
            print("Allocated segments:")
            for seg, (start, size) in sorted(allocated_segments.items(), key=lambda x: x[1][0]):
                print(f"  {seg}: Address {start}, Size {size}")
            print("Free memory blocks:")
            for start, size in sorted(free_list, key=lambda x: x[0]):
                print(f"  Address {start}, Size {size}")
        else:
            print("Unknown command. Valid commands: allocate, deallocate, show, exit.")

    print("\nFinal Memory Allocation:")
    print("Allocated segments:")
    for seg, (start, size) in sorted(allocated_segments.items(), key=lambda x: x[1][0]):
        print(f"  {seg}: Address {start}, Size {size}")
    print("Free memory blocks:")
    for start, size in sorted(free_list, key=lambda x: x[0]):
        print(f"  Address {start}, Size {size}")

    draw_segmentation(memory_size, allocated_segments, free_list)

def draw_segmentation(memory_size, allocated, free_list):
    """
    Visualize the memory layout after segmentation allocation.
    Allocated segments are shown as colored blocks, while free segments appear in light grey.
    """
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(0, memory_size)
    ax.set_ylim(0, 50)
    ax.set_xlabel('Memory Address')
    ax.set_yticks([])
    ax.set_title("Memory Layout - Segmentation")
    
    # Draw allocated segments with different colors.
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
    i = 0
    for seg_id, (start, size) in sorted(allocated.items(), key=lambda x: x[1][0]):
        color = colors[i % len(colors)]
        ax.broken_barh([(start, size)], (20, 10), facecolors=color)
        # Label the segment in the middle of the block.
        ax.text(start + size / 2, 25, str(seg_id), ha='center', va='center', color='white', fontsize=10)
        i += 1
    
    # Draw free segments in light grey.
    for (start, size) in free_list:
        ax.broken_barh([(start, size)], (5, 10), facecolors='lightgrey')
    
    plt.show()


# ================= Main Menu =================

def main():
    print("=== Dynamic Memory Management Visualizer ===")
    print("Choose simulation mode:")
    print("  1. Paging Simulation (simulate page faults using replacement algorithms)")
    print("  2. Segmentation Simulation (simulate dynamic memory allocation and fragmentation)")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        paging_simulation()
    elif choice == "2":
        segmentation_simulation()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
