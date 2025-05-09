class Process:
    def __init__(self, number, burst_time, priority, arrival_time, memory_needed):
        self.number = number
        self.burst_time = burst_time
        self.priority = priority  
        self.arrival_time = arrival_time
        self.waiting_time = 0 
        self.memory_needed = memory_needed
        self.turnaround_time = 0
        self.remaining_time = burst_time
        self.state = "waiting"

class MemoryBlock:
    def __init__(self, start, size, process=None):
        self.start = start  
        self.size = size
        self.process = process

    def is_free(self):
        return self.process is None

    def __repr__(self):
        status = "Free" if self.is_free() else f"Used by {self.process.number}"
        return f"[{self.start} - {self.start + self.size - 1}] {status}"

class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size          # Total memory size
        self.blocks = [MemoryBlock(0, total_size)]  # Initialize memory blocks

    def allocate(self, process):
        # Attempt to allocate memory for a process
        for i, block in enumerate(self.blocks):
            if block.is_free() and block.size >= process.memory_needed:
                # Split the block if necessary
                self.blocks[i:i+1] = [MemoryBlock(block.start, process.memory_needed, process)] + \
                                     ([MemoryBlock(block.start + process.memory_needed, block.size - process.memory_needed)] 
                                      if block.size > process.memory_needed else [])
                print(f"Allocated {process.number} at [{block.start} - {block.start + process.memory_needed - 1}]")
                return True
        return False

    def deallocate(self, process):
        # Deallocate memory from a process
        self.blocks = [MemoryBlock(b.start, b.size) if b.process == process else b for b in self.blocks]
        print(f"Deallocated {process.number}")
        self.merge_free_blocks() 

    def merge_free_blocks(self):
        # combin free blocks into larger blocks
        merged = []
        i = 0
        while i < len(self.blocks):
            if self.blocks[i].is_free():
                start, size = self.blocks[i].start, self.blocks[i].size
                while i + 1 < len(self.blocks) and self.blocks[i + 1].is_free():
                    size += self.blocks[i + 1].size
                    i += 1
                merged.append(MemoryBlock(start, size))
            else:
                merged.append(self.blocks[i])
            i += 1
        self.blocks = merged

def priority_scheduling(processes):
    time = 0
    finished = 0  
    total_processes = len(processes)
    ready_queue = [] 
    current = None

    print("Time | Process | State")

    while finished < total_processes:
        for p in processes:
            if p.arrival_time == time:
                ready_queue.append(p)

        ready_queue.sort(key=lambda p: p.priority)

        if ready_queue:
            if current != ready_queue[0]:
                if current and current.state == "running":
                    print(f"{time:>4} | {current.number:^7} | Preempted")
                    current.state = "waiting"
                current = ready_queue[0]
                if current.state != "running":
                    print(f"{time:>4} | {current.number:^7} | Started running")
                    current.state = "running"

            current.remaining_time -= 1

            for p in ready_queue:
                if p != current and p.state != "completed":
                    p.waiting_time += 1

            # If current process finished
            if current.remaining_time == 0:
                current.turnaround_time = time + 1 - current.arrival_time
                print(f"{time + 1:>4} | {current.number:^7} | Finished running")
                current.state = "completed"
                ready_queue.remove(current)
                finished += 1
                current = None
        else:
            print(f"{time:>4} | {'-':^7} | CPU is idle")

        time += 1

    print("\nPriority Simulation Table:")
    print("Process | Burst | Arrival | Priority | Waiting | Turnaround")
    for p in processes:
        print(f"{p.number:^7} | {p.burst_time:^5} | {p.arrival_time:^7} | {p.priority:^8} | {p.waiting_time:^7} | {p.turnaround_time:^10}")

    avg_waiting = sum(p.waiting_time for p in processes) / total_processes
    avg_turnaround = sum(p.turnaround_time for p in processes) / total_processes
    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")

processes = [
    Process("P1", 10, 4, 0, 5),
    Process("P2", 3, 8, 1, 2),
    Process("P3", 2, 5, 2, 1),
    Process("P4", 4, 1, 4, 3)
]
priority_scheduling(processes)