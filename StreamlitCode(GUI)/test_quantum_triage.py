"""
✅ Test & Demo Script for Quantum Triage System
Run this to verify the module works correctly
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from quantum_triage import QuantumTriageOptimizer, PatientCase, format_optimization_report

def demo_quantum_triage():
    """Run a demonstration of the Quantum Triage System"""
    
    print("\n" + "="*70)
    print("⚛️  QUANTUM TRIAGE SYSTEM - DEMO".center(70))
    print("="*70 + "\n")
    
    # Create sample patients (simulating a hospital during COVID-19 surge)
    patients = [
        PatientCase(
            patient_id="P001",
            name="Ahmed Mohamed",
            severity_score=0.85,
            needs_ventilator=True,
            expected_duration_hours=24,
            age=65,
            has_alternative_treatment=False,
            priority_factor=0.95
        ),
        PatientCase(
            patient_id="P002",
            name="Fatima Hassan",
            severity_score=0.72,
            needs_ventilator=True,
            expected_duration_hours=36,
            age=58,
            has_alternative_treatment=False,
            priority_factor=0.88
        ),
        PatientCase(
            patient_id="P003",
            name="Ali Ibrahim",
            severity_score=0.55,
            needs_ventilator=True,
            expected_duration_hours=18,
            age=42,
            has_alternative_treatment=True,
            priority_factor=0.70
        ),
        PatientCase(
            patient_id="P004",
            name="Noor Saleh",
            severity_score=0.68,
            needs_ventilator=True,
            expected_duration_hours=48,
            age=75,
            has_alternative_treatment=False,
            priority_factor=0.92
        ),
        PatientCase(
            patient_id="P005",
            name="Omar Al-Rashid",
            severity_score=0.45,
            needs_ventilator=False,
            expected_duration_hours=12,
            age=35,
            has_alternative_treatment=True,
            priority_factor=0.60
        ),
        PatientCase(
            patient_id="P006",
            name="Layla Mansour",
            severity_score=0.78,
            needs_ventilator=True,
            expected_duration_hours=30,
            age=48,
            has_alternative_treatment=False,
            priority_factor=0.85
        ),
    ]
    
    print("📋 PATIENT DATABASE:")
    print("-" * 70)
    for p in patients:
        print(f"{p.patient_id}: {p.name:20} | Severity: {p.severity_score:.0%} | "
              f"Priority: {p.priority_factor:.0%} | Age: {p.age} | Duration: {p.expected_duration_hours}h")
    print()
    
    # Configure resources (limited ventilators)
    num_ventilators = 4  # Only 4 ventilators for 6 patients!
    max_hours = 120  # Limited total hours
    
    print(f"🏥 HOSPITAL RESOURCES:")
    print(f"   Available Ventilators: {num_ventilators}")
    print(f"   Maximum Hours: {max_hours}")
    print(f"   Patients Needing Ventilators: {sum(1 for p in patients if p.needs_ventilator)}")
    print()
    
    # Initialize optimizer
    print("⚙️  Initializing Quantum-Inspired Optimizer...")
    optimizer = QuantumTriageOptimizer(
        num_ventilators=num_ventilators,
        max_total_hours=max_hours
    )
    print("   ✅ Ready\n")
    
    # Run optimization
    print("🚀 Running Quantum-Inspired Optimization (Simulated Annealing)...")
    result = optimizer.optimize(patients)
    print("   ✅ Optimization Complete\n")
    
    # Print results
    print(format_optimization_report(result))
    
    # Additional insights
    print("\n📊 KEY INSIGHTS:")
    print("-" * 70)
    print(f"• System allocated {result['total_ventilators_used']}/{result['available_ventilators']} "
          f"ventilators")
    print(f"• Used {result['total_hours_used']} of {max_hours} available ventilator-hours")
    print(f"• Estimated lives saved: {result['estimated_lives_saved']}")
    print(f"• Algorithm: {result['algorithm']}")
    print()
    
    # Compare allocation vs non-optimized approach
    print("🔍 ALGORITHM COMPARISON:")
    print("-" * 70)
    greedy_estimate = sum(
        (1.0 - p.severity_score) if i < num_ventilators else 0
        for i, p in enumerate(sorted(patients, key=lambda x: x.severity_score, reverse=True))
    )
    improvement = ((result['estimated_lives_saved'] - greedy_estimate) / max(greedy_estimate, 0.1) * 100) \
        if greedy_estimate > 0 else 0
    print(f"• Greedy approach (severity only): ~{greedy_estimate:.2f} lives saved")
    print(f"• Quantum-inspired approach: {result['estimated_lives_saved']} lives saved")
    print(f"• Improvement: +{improvement:.1f}%")
    print()
    
    print("="*70)
    print("✅ Demo completed successfully!".center(70))
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        demo_quantum_triage()
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
