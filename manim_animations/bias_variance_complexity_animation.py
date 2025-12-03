#!/usr/bin/env python3
"""
Bias-Variance-Complexity Animation
Shows how bias, variance, and training error change as model complexity decreases
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Use a compatible backend
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

class BiasVarianceComplexityAnimator:
    def __init__(self):
        np.random.seed(42)
        
        # True function: quadratic with noise
        self.x_true = np.linspace(0, 1, 100)
        self.y_true = 2 * self.x_true**2 + 0.5 * self.x_true + 0.1
        
        # Generate training datasets (multiple for variance calculation)
        self.n_datasets = 50
        self.n_samples = 30
        self.datasets = []
        
        for _ in range(self.n_datasets):
            x = np.random.uniform(0, 1, self.n_samples)
            y = 2 * x**2 + 0.5 * x + 0.1 + np.random.normal(0, 0.15, self.n_samples)
            self.datasets.append((x, y))
        
        # Model complexities (decreasing)
        self.complexities = [15, 12, 9, 6, 4, 3, 2, 1]  # Polynomial degrees
        self.complexity_names = [f"Degree {d}" for d in self.complexities]
        
        # Pre-compute metrics for all complexities
        self.compute_all_metrics()
    
    def compute_all_metrics(self):
        """Pre-compute bias, variance, and training error for all complexities"""
        self.bias_values = []
        self.variance_values = []
        self.training_errors = []
        self.all_predictions = []
        
        for complexity in self.complexities:
            predictions_all_datasets = []
            training_errs = []
            
            # Train models on all datasets
            for x_train, y_train in self.datasets:
                # Fit polynomial of given degree
                coeffs = np.polyfit(x_train, y_train, min(complexity, len(x_train)-1))
                
                # Predict on test points
                y_pred = np.polyval(coeffs, self.x_true)
                predictions_all_datasets.append(y_pred)
                
                # Calculate training error
                y_train_pred = np.polyval(coeffs, x_train)
                train_err = np.mean((y_train - y_train_pred)**2)
                training_errs.append(train_err)
            
            # Calculate bias and variance
            predictions_all_datasets = np.array(predictions_all_datasets)
            mean_prediction = np.mean(predictions_all_datasets, axis=0)
            
            # Bias: how far is mean prediction from true function
            bias = np.mean((mean_prediction - self.y_true)**2)
            
            # Variance: how much do predictions vary across datasets
            variance = np.mean(np.var(predictions_all_datasets, axis=0))
            
            # Average training error
            avg_training_error = np.mean(training_errs)
            
            self.bias_values.append(bias)
            self.variance_values.append(variance)
            self.training_errors.append(avg_training_error)
            self.all_predictions.append(predictions_all_datasets)
    
    def create_animation(self):
        """Create the bias-variance-complexity animation"""
        fig = plt.figure(figsize=(20, 12))
        fig.suptitle('Bias-Variance Tradeoff: Effect of Decreasing Model Complexity', 
                    fontsize=24, fontweight='bold', y=0.95)
        
        # Create subplots
        ax1 = plt.subplot(2, 4, (1, 2))  # Model predictions
        ax2 = plt.subplot(2, 4, 3)       # Bias-Variance plot
        ax3 = plt.subplot(2, 4, 4)       # Training error
        ax4 = plt.subplot(2, 4, (5, 8))  # Mathematical explanation
        
        def animate(frame):
            # Clear axes
            ax1.clear()
            ax2.clear()
            ax3.clear()
            ax4.clear()
            
            # Current complexity
            complexity_idx = frame % len(self.complexities)
            current_complexity = self.complexities[complexity_idx]
            current_predictions = self.all_predictions[complexity_idx]
            
            # 1. Model Predictions Plot
            ax1.set_title(f'Model Predictions - {self.complexity_names[complexity_idx]}', 
                         fontsize=16, fontweight='bold')
            
            # Plot true function
            ax1.plot(self.x_true, self.y_true, 'k-', linewidth=4, label='True Function', alpha=0.8)
            
            # Plot sample predictions (show variability)
            for i in range(min(20, len(current_predictions))):
                alpha = 0.1 if i > 0 else 0.3
                color = 'red' if i == 0 else 'blue'
                label = 'Sample Predictions' if i == 1 else None
                ax1.plot(self.x_true, current_predictions[i], color=color, 
                        alpha=alpha, linewidth=1.5, label=label)
            
            # Plot mean prediction
            mean_pred = np.mean(current_predictions, axis=0)
            ax1.plot(self.x_true, mean_pred, 'r-', linewidth=3, label='Mean Prediction')
            
            # Show some training data
            x_sample, y_sample = self.datasets[0]
            ax1.scatter(x_sample, y_sample, color='green', alpha=0.6, s=40, label='Training Data')
            
            ax1.set_xlabel('X', fontsize=12)
            ax1.set_ylabel('Y', fontsize=12)
            ax1.legend(fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # 2. Bias-Variance Plot
            ax2.set_title('Bias vs Variance', fontsize=16, fontweight='bold')
            
            # Plot all values up to current frame
            complexities_so_far = self.complexities[:complexity_idx+1]
            bias_so_far = self.bias_values[:complexity_idx+1]
            variance_so_far = self.variance_values[:complexity_idx+1]
            
            ax2.plot(complexities_so_far, bias_so_far, 'ro-', linewidth=3, markersize=8, 
                    label='Bias²', alpha=0.8)
            ax2.plot(complexities_so_far, variance_so_far, 'bo-', linewidth=3, markersize=8, 
                    label='Variance', alpha=0.8)
            
            # Highlight current point
            ax2.scatter([current_complexity], [self.bias_values[complexity_idx]], 
                       color='red', s=150, zorder=5)
            ax2.scatter([current_complexity], [self.variance_values[complexity_idx]], 
                       color='blue', s=150, zorder=5)
            
            ax2.set_xlabel('Model Complexity (Polynomial Degree)', fontsize=12)
            ax2.set_ylabel('Error', fontsize=12)
            ax2.legend(fontsize=12)
            ax2.grid(True, alpha=0.3)
            ax2.set_xlim(0, 16)
            
            # 3. Training Error Plot
            ax3.set_title('Training Error', fontsize=16, fontweight='bold')
            
            train_err_so_far = self.training_errors[:complexity_idx+1]
            ax3.plot(complexities_so_far, train_err_so_far, 'go-', linewidth=3, markersize=8, 
                    label='Training Error', alpha=0.8)
            
            # Highlight current point
            ax3.scatter([current_complexity], [self.training_errors[complexity_idx]], 
                       color='green', s=150, zorder=5)
            
            ax3.set_xlabel('Model Complexity (Polynomial Degree)', fontsize=12)
            ax3.set_ylabel('Training Error', fontsize=12)
            ax3.legend(fontsize=12)
            ax3.grid(True, alpha=0.3)
            ax3.set_xlim(0, 16)
            
            # 4. Mathematical Explanation
            ax4.set_title('Mathematical Analysis', fontsize=18, fontweight='bold')
            ax4.axis('off')
            
            current_bias = self.bias_values[complexity_idx]
            current_variance = self.variance_values[complexity_idx]
            current_train_err = self.training_errors[complexity_idx]
            
            explanation = f"""
📊 BIAS-VARIANCE DECOMPOSITION

Current Model: {self.complexity_names[complexity_idx]}

📈 BIAS² = {current_bias:.4f}
   • Measures systematic error
   • How far is E[f̂(x)] from f(x)?
   • ↑ As complexity decreases (underfitting)

📉 VARIANCE = {current_variance:.4f}
   • Measures prediction variability
   • How much does f̂(x) vary across datasets?
   • ↓ As complexity decreases (more stable)

🎯 TRAINING ERROR = {current_train_err:.4f}
   • Error on training data
   • ↑ As complexity decreases (worse fit)

⚖️ FUNDAMENTAL TRADEOFF:
   • Complex models: Low bias, high variance
   • Simple models: High bias, low variance
   • Goal: Find optimal balance

🧮 MATHEMATICAL RELATIONSHIP:
   Expected Test Error = Bias² + Variance + Noise

   As Model Complexity Decreases:
   ✅ Bias²: {self.bias_values[0]:.4f} → {current_bias:.4f} (↑)
   ✅ Variance: {self.variance_values[0]:.4f} → {current_variance:.4f} (↓)
   ✅ Training Error: {self.training_errors[0]:.4f} → {current_train_err:.4f} (↑)

💡 INTERPRETATION:
   • Simpler models make systematic errors (high bias)
   • But predictions are more consistent (low variance)
   • Training error increases as model becomes less flexible
            """
            
            ax4.text(0.05, 0.95, explanation.strip(), transform=ax4.transAxes, 
                    fontsize=14, verticalalignment='top', fontfamily='monospace',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
            
            plt.tight_layout()
            
        # Create animation
        frames = len(self.complexities) * 2  # Show each complexity twice
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=2000, 
                                     repeat=True, blit=False)
        
        return fig, anim

def main():
    """Create and save the bias-variance-complexity animation"""
    print("🌟 Creating Bias-Variance-Complexity Animation...")
    
    try:
        animator = BiasVarianceComplexityAnimator()
        fig, anim = animator.create_animation()
        
        # Save as MP4 video
        print("💾 Saving animation as MP4...")
        anim.save('bias_variance_complexity.mp4', writer='ffmpeg', fps=0.5, bitrate=1800)
        print("✅ Animation saved as 'bias_variance_complexity.mp4'")
        
        # Also save as GIF for compatibility
        print("💾 Saving animation as GIF...")
        anim.save('bias_variance_complexity.gif', writer='pillow', fps=0.5)
        print("✅ Animation saved as 'bias_variance_complexity.gif'")
        
        # Save static summary plot
        print("📊 Creating summary plot...")
        create_summary_plot(animator)
        
        print("\n🎉 ANIMATION COMPLETE!")
        print("\nKey Insights Demonstrated:")
        print("1. 📈 Bias increases as complexity decreases")
        print("2. 📉 Variance decreases as complexity decreases") 
        print("3. 🎯 Training error increases as complexity decreases")
        print("4. ⚖️ Optimal complexity balances bias and variance")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating animation: {e}")
        return False

def create_summary_plot(animator):
    """Create a static summary plot"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Bias-Variance-Complexity Relationship Summary', fontsize=16, fontweight='bold')
    
    complexities = animator.complexities
    
    # Plot 1: Bias and Variance
    ax1.plot(complexities, animator.bias_values, 'ro-', linewidth=3, markersize=8, label='Bias²')
    ax1.plot(complexities, animator.variance_values, 'bo-', linewidth=3, markersize=8, label='Variance')
    ax1.set_xlabel('Model Complexity (Polynomial Degree)')
    ax1.set_ylabel('Error')
    ax1.set_title('Bias² vs Variance')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.invert_xaxis()  # Show decreasing complexity
    
    # Plot 2: Training Error
    ax2.plot(complexities, animator.training_errors, 'go-', linewidth=3, markersize=8, label='Training Error')
    ax2.set_xlabel('Model Complexity (Polynomial Degree)')
    ax2.set_ylabel('Training Error')
    ax2.set_title('Training Error')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.invert_xaxis()  # Show decreasing complexity
    
    # Plot 3: Total Expected Error
    total_error = np.array(animator.bias_values) + np.array(animator.variance_values)
    ax3.plot(complexities, total_error, 'mo-', linewidth=3, markersize=8, label='Bias² + Variance')
    ax3.plot(complexities, animator.bias_values, 'r--', alpha=0.7, label='Bias²')
    ax3.plot(complexities, animator.variance_values, 'b--', alpha=0.7, label='Variance')
    ax3.set_xlabel('Model Complexity (Polynomial Degree)')
    ax3.set_ylabel('Error')
    ax3.set_title('Total Expected Error')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.invert_xaxis()  # Show decreasing complexity
    
    plt.tight_layout()
    plt.savefig('bias_variance_complexity_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("📊 Summary plot saved as 'bias_variance_complexity_summary.png'")

if __name__ == "__main__":
    success = main()
    if not success:
        print("❌ Animation creation failed")
        exit(1)