from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimizes the 3D printing queue according to the priorities and limitations of the printer

    Args:
        print_jobs: List of print jobs
        constraints: Printer limitations

    Returns:
        Dict with print order and total time
    """
    jobs = [PrintJob(**job) for job in print_jobs]                  # Convert to a list of PrintJob objects
    jobs.sort(key=lambda job: (job.priority, job.print_time))       # Sort by priority (highest - first), then by print time
    
    print_order = []
    total_time = 0
    
    while jobs:
        batch = []                                                  # Group of models for simultaneous printing
        batch_volume = 0
        batch_time = 0
        
        for job in jobs[:]:                                         # Go through a copy of the list
            if len(batch) < constraints['max_items'] and batch_volume + job.volume <= constraints['max_volume']:
                batch.append(job)
                batch_volume += job.volume
                batch_time = max(batch_time, job.print_time)
                jobs.remove(job)
        
        print_order.extend([job.id for job in batch])               # Add to the print order and update the total time
        total_time += batch_time
    
    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Testing
if __name__ == "__main__":
    def test_printing_optimization():
        constraints = {
            "max_volume": 300,
            "max_items": 2
        }

        test1_jobs = [
            {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
            {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
            {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
        ]

        test2_jobs = [
            {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
            {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
            {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
        ]

        test3_jobs = [
            {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
            {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
            {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
        ]

        print("Test 1 (equal priority):")
        result1 = optimize_printing(test1_jobs, constraints)
        print(f"Print order: {result1['print_order']}")
        print(f"Total time: {result1['total_time']} minutes")

        print("\nTest 2 (different priorities):")
        result2 = optimize_printing(test2_jobs, constraints)
        print(f"Print order: {result2['print_order']}")
        print(f"Total time: {result2['total_time']} minutes")

        print("\nTest 3 (exceeding limits):")
        result3 = optimize_printing(test3_jobs, constraints)
        print(f"Print order: {result3['print_order']}")
        print(f"Total time: {result3['total_time']} minutes")

    test_printing_optimization()
