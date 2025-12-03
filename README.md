# Manim Animations Repository

A collection of Manim animations for machine learning and data science concepts.

## Contents

### `manim_animations/`
Source code for ~80+ Manim animation files covering:
- Decision Trees
- Random Forests
- Gradient Boosting
- PCA (Principal Component Analysis)
- K-Nearest Neighbors (KNN)
- Logistic Regression
- Bias-Variance Tradeoff
- GLM (Generalized Linear Models)
- Clustering (K-Means)
- And many more ML/statistics concepts

### `manim-mcp-server/`
MCP (Model Context Protocol) server for executing Manim code, plus rendered outputs:
- **19 rendered animations** (1080p60 MP4 format)
- MCP server implementation
- Demo GIF

## Rendered Animations

The following animations are available as rendered MP4 files in `manim-mcp-server/src/media/manim_tmp/media/videos/scene/1080p60/`:

- Decision Tree (3 videos: DetailedFlow, Flowchart, Structure)
- Random Forest (3 videos)
- Gradient Boosting (3 videos)
- PCA (4 videos, including 3D animation)
- K-Nearest Neighbors (3 videos)
- Logistic Regression (3 videos)

## Requirements

- Python 3.8+
- Manim: `pip install manim`
- NumPy: `pip install numpy`
- scikit-learn: `pip install scikit-learn`

## Usage

### Running Individual Animations

```bash
manim -pql manim_animations/decision_tree_animation.py DecisionTreeAnimation
```

### Using the MCP Server

The MCP server allows programmatic execution of Manim code. See `manim-mcp-server/README.md` for details.

## License

See individual files for licensing information.

