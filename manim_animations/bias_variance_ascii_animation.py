#!/usr/bin/env python3
"""
ASCII Animation: Bias-Variance-Complexity Changes
Shows animated progression of bias, variance, and training error as complexity decreases
"""

import time
import sys
import os

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_bar_chart(value, max_val, width=20, char='█'):
    """Create a simple ASCII bar chart"""
    bar_length = int((value / max_val) * width)
    bar = char * bar_length + '░' * (width - bar_length)
    return bar

def animate_bias_variance_complexity():
    """Create ASCII animation showing bias-variance tradeoff"""
    
    # Model data (decreasing complexity)
    models = [
        {"name": "Very Complex (Degree 15)", "params": 16, "bias": 0.020, "variance": 0.450, "train": 0.080},
        {"name": "High Complex (Degree 10)", "params": 11, "bias": 0.050, "variance": 0.280, "train": 0.120},
        {"name": "Moderate (Degree 6)", "params": 7, "bias": 0.120, "variance": 0.150, "train": 0.180},
        {"name": "Simple (Degree 3)", "params": 4, "bias": 0.250, "variance": 0.080, "train": 0.280},
        {"name": "Linear (Degree 1)", "params": 2, "bias": 0.450, "variance": 0.040, "train": 0.480},
        {"name": "Constant (Degree 0)", "params": 1, "bias": 0.680, "variance": 0.010, "train": 0.670},
    ]
    
    max_val = 0.7  # Maximum value for scaling bars
    
    print("🎬 BIAS-VARIANCE-COMPLEXITY ANIMATION")
    print("=" * 60)
    print("Press Ctrl+C to stop the animation")
    print("=" * 60)
    time.sleep(2)
    
    try:
        # Animation loop
        for cycle in range(3):  # Repeat 3 times
            for i, model in enumerate(models):
                clear_screen()
                
                # Header
                print("🎬 BIAS-VARIANCE-COMPLEXITY ANIMATION")
                print("=" * 60)
                print(f"Cycle {cycle + 1}/3 | Step {i + 1}/{len(models)}")
                print("=" * 60)
                
                # Current model info
                print(f"\n📊 CURRENT MODEL: {model['name']}")
                print(f"Parameters: {model['params']} | Complexity: {'High' if model['params'] > 7 else 'Medium' if model['params'] > 2 else 'Low'}")
                print("-" * 60)
                
                # Create bars with animation effect
                bias_bar = create_bar_chart(model['bias'], max_val)
                variance_bar = create_bar_chart(model['variance'], max_val)
                train_bar = create_bar_chart(model['train'], max_val)
                
                # Display metrics with bars
                print(f"\n🔴 BIAS²      {model['bias']:.3f} |{bias_bar}|")
                print(f"🔵 VARIANCE   {model['variance']:.3f} |{variance_bar}|")
                print(f"🟢 TRAIN ERR  {model['train']:.3f} |{train_bar}|")
                
                # Show trends
                if i > 0:
                    prev = models[i-1]
                    bias_trend = "↗️" if model['bias'] > prev['bias'] else "↘️"
                    var_trend = "↘️" if model['variance'] < prev['variance'] else "↗️"
                    train_trend = "↗️" if model['train'] > prev['train'] else "↘️"
                    
                    print(f"\n📈 TRENDS FROM PREVIOUS:")
                    print(f"   Bias²:    {bias_trend} {model['bias'] - prev['bias']:+.3f}")
                    print(f"   Variance: {var_trend} {model['variance'] - prev['variance']:+.3f}")
                    print(f"   Training: {train_trend} {model['train'] - prev['train']:+.3f}")
                
                # Show progress through all models so far
                print(f"\n📊 COMPLEXITY JOURNEY:")
                print("-" * 25)
                for j in range(len(models)):
                    if j <= i:
                        marker = "👉" if j == i else "✅"
                        status = "CURRENT" if j == i else "DONE"
                    else:
                        marker = "⏳"
                        status = "PENDING"
                    
                    model_short = models[j]['name'].split()[0]
                    print(f"{marker} {model_short:<12} ({models[j]['params']:2d} params) - {status}")
                
                # Mathematical insight
                print(f"\n🧠 KEY INSIGHT:")
                if model['params'] > 7:
                    insight = "High complexity → Low bias, High variance (Overfitting risk)"
                elif model['params'] > 2:
                    insight = "Moderate complexity → Balanced bias-variance tradeoff"
                else:
                    insight = "Low complexity → High bias, Low variance (Underfitting)"
                
                print(f"   {insight}")
                
                # Summary at end
                if i == len(models) - 1:
                    print(f"\n🎯 SUMMARY - AS COMPLEXITY DECREASED:")
                    print(f"   📈 Bias²:      {models[0]['bias']:.3f} → {model['bias']:.3f} (↗️ INCREASED)")
                    print(f"   📉 Variance:   {models[0]['variance']:.3f} → {model['variance']:.3f} (↘️ DECREASED)")
                    print(f"   📈 Train Err:  {models[0]['train']:.3f} → {model['train']:.3f} (↗️ INCREASED)")
                    
                    # Find optimal (minimum test error approximation)
                    optimal_idx = 2  # Moderate complexity
                    optimal = models[optimal_idx]
                    print(f"\n⭐ OPTIMAL BALANCE: {optimal['name']}")
                    print(f"   Sweet spot between bias and variance!")
                
                # Wait before next frame
                time.sleep(2.5)
        
        # Final summary screen
        clear_screen()
        print("🎉 ANIMATION COMPLETE!")
        print("=" * 40)
        print("\n🔑 KEY LEARNINGS:")
        print("1. 📈 Decreasing complexity → Bias ↑, Variance ↓, Training Error ↑")
        print("2. ⚖️  Optimal model balances bias and variance")
        print("3. 🎯 Too simple = underfitting, Too complex = overfitting")
        print("4. 📊 Use validation to find the sweet spot")
        
        print(f"\n🏆 REMEMBER THE FORMULA:")
        print(f"   Expected Test Error = Bias² + Variance + Irreducible Error")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Animation stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    """Run the ASCII animation"""
    try:
        animate_bias_variance_complexity()
        return True
    except Exception as e:
        print(f"❌ Animation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)