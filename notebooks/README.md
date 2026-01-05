# Notebooks

## train.ipynb

End-to-end training and evaluation for LOB classification using walk-forward
(expanding-window) cross-validation over pre-split folds. The notebook:

- Loads the `.txt` folds from `data/training/` and `data/testing/`.
- Builds sliding window datasets for sequence modeling.
- Trains baselines and attention-based models (including a TLOB-style classifier).
- Reports accuracy, macro F1, and confusion matrices.
- Produces comparison plots across folds and models.

### Prerequisites

- Decompress the dataset with `bash scripts/unxz_data.sh` from the project root.
- Install the Python dependencies listed in `README.md`.
- Use Jupyter Lab or Notebook.

### Data expectations

- Fold files:
  - `data/training/Train_Dst_NoAuction_ZScore_CF_{fold}.txt`
  - `data/testing/Test_Dst_NoAuction_ZScore_CF_{fold}.txt`
- Files are whitespace-separated blocks of shape `(rows, timesteps)`.
- Features are the first `num_features` rows.
- Labels are taken from the horizon row and shifted from `(1, 2, 3)` to `(0, 1, 2)`.
- Sliding window labels align to the last timestep in each window.

### Tensor conventions

- Raw block `data` is loaded via `np.loadtxt` with shape `(R, T)`.
- Each sample is a sliding window shaped `(num_features, seq_size)`.
- Conv1d-style models consume batches shaped `(batch, num_features, seq_size)`;
  sequence models reshape as needed.
- Labels are integer class indices in `[0, 2]`.

### Device selection

The notebook picks `cuda` when available, otherwise `mps`, otherwise `cpu`, and sets
`PYTORCH_ENABLE_MPS_FALLBACK=1` for Apple Silicon compatibility.

### Run

```bash
jupyter lab notebooks/train.ipynb
```

### Key parameters

| Parameter | Meaning | Default in notebook |
| --- | --- | --- |
| `seq_size` | Sliding window length (timesteps per sample) | `10` |
| `num_features` | Number of feature rows to extract | `144` |
| `horizon` | Label horizon index (see mapping below) | `5` |
| `batch_size` | Batch size for loaders | `128` |
| `val_ratio` | Fraction of training data for validation | `0.1` |
| `epochs` | Training epochs per fold | `20` |
| `num_folds` | Walk-forward folds to evaluate | `8` |
| `test_horizon_folds` | Future folds used for testing | `1` |

Horizon mapping (used in `HORIZON_TO_TICKS`):

- `1 -> 100` ticks
- `2 -> 50` ticks
- `3 -> 30` ticks
- `4 -> 20` ticks
- `5 -> 10` ticks

### Outputs

- Per-fold metrics (loss, accuracy, macro F1) and predictions.
- Summary table with mean and std for accuracy and macro F1.
- Plots: walk-forward curves, mean/std bars, metric distributions, heatmaps, and
  confusion matrices.
- Optional attention summaries for TABL and TLOB models.

### Method reference (train.ipynb)

Data and loaders:

- `Dataset`: Sliding window dataset that returns `(features, label)` with features
  shaped for `Conv1d` as `(num_features, seq_size)`.
- `_load_block(path)`: Load a whitespace-separated `.txt` block into a NumPy array.
- `_make_Xy_from_block(data, horizon, seq_size, num_features)`: Build features and
  aligned labels from a raw block.
- `_build_concat_dataset(folds, dir_path, prefix, ...)`: Create a `ConcatDataset`
  across multiple folds, skipping empty windows.
- `_time_ordered_split(dataset, val_ratio)`: Time-ordered train/val split to avoid
  leakage.
- `_extract_labels(dataset)`: Extract labels for class-weight computation.
- `make_loaders_for_fold(...)`: Build train/val/test loaders for an expanding
  window fold and return labels for weighting.
- `HORIZON_TO_TICKS`: Horizon index to tick mapping used for labeling.

Training and evaluation:

- `set_seed(seed)`: Seed Python, NumPy, and PyTorch RNGs.
- `compute_class_weights(labels, num_classes, scale)`: Inverse-frequency class
  weights (normalized in the CV loop).
- `train_epoch(model, loader, optimizer, criterion)`: One training epoch with loss
  and accuracy tracking.
- `eval_epoch(model, loader, criterion, return_preds)`: Evaluate loss, accuracy,
  macro F1, and optional predictions.
- `train_one_epoch(model, loader, optimizer, criterion)`: Minimal training helper
  (not used in the walk-forward loop).
- `run_walk_forward_cv(...)`: Main training loop across folds with optional
  attention tracking and best-model selection by validation F1.
- `_should_collect_attention(track_attention, attention_collector, epoch, ...)`:
  Gate attention collection by epoch.
- `_print_cv_summary(model_name, fold_results)`: Print mean/std for accuracy and F1.

Models:

All models take inputs shaped `(batch, num_features, seq_size)` unless noted.

- `MLPBaseline`: Flattens input to `(num_features * seq_size)` and applies fully
  connected layers (1024, 512, 256) with LeakyReLU and dropout (0.3, then 0.2),
  followed by a linear classifier to `num_classes`.
- `CNNTimeBaseline`: Two `Conv1d` layers over time (kernel 3, padding 1) with
  LeakyReLU and dropout, then global average pooling across time and an MLP head
  (Linear -> LeakyReLU -> Dropout -> Linear) to `num_classes`.
- `LSTMClassifier`: LSTM over time (`batch_first=True`) with optional stacking and
  dropout (disabled for a single layer), using the final hidden state and a
  two-layer MLP head (Linear -> ReLU -> Dropout -> Linear).
- `TCNBlock`: Two dilated `Conv1d` layers with padding to preserve length, ReLU
  activations, dropout, and a residual connection (1x1 conv if channels change).
- `TCNClassifier`: Stack of `TCNBlock`s with dilation `2^i`, global average pooling
  over time, and an MLP head to `num_classes`.
- `TABLLayer`: Temporal attention-augmented bilinear layer with learnable feature
  transform (`W1`), time attention (`W` with fixed diagonal), time projection (`W2`),
  and a learned blend between attended and original features.
- `TABLClassifier`: `TABLLayer` feature extractor followed by flattening and an MLP
  head (Dropout -> Linear -> ReLU -> Dropout -> Linear) to `num_classes`; can return
  attention weights.
- `BilinearNormalization`: Learnable normalization along time and feature axes with
  separate gamma/beta parameters and nonnegative weights that blend the two views.
- `SinusoidalPositionalEncoding`: Fixed sin/cos time encoding added to the sequence,
  cached per device and dtype.
- `MLPLOBMixer`: MLP-Mixer style block with time mixing (LayerNorm over time,
  Linear T -> mlp_time -> T) and feature mixing (LayerNorm over features,
  Linear C -> mlp_feat -> C), both with GELU and dropout in residual form.
- `DualAttentionBlock`: Time self-attention (`MultiheadAttention`) in model space,
  feature attention in a projected feature space (T -> d_feat_attn and back),
  followed by `MLPLOBMixer`; can return time and feature attention.
- `TLOBClassifier`: Optional `BilinearNormalization`, optional input projection,
  sinusoidal positional encoding, a stack of `DualAttentionBlock`s, LayerNorm,
  configurable pooling (`last` or `mean`), and an MLP head (Dropout -> Linear ->
  GELU -> Dropout -> Linear) to `num_classes`; can return attention stacks.

Attention analysis:

- `collect_avg_tabl_attention_per_class(...)`: Average TABL attention per class.
- `collect_avg_time_attention_per_class(...)`: Average temporal attention per class
  for TLOB, using last or mean layer.
- `plot_average_attention_history(...)`: Plot attention evolution across epochs.

Reporting and plotting:

- `summarize_cv(fold_results, model_name)`: Per-fold DataFrame and summary stats.
- `set_modern_mpl_style()`: Matplotlib style configuration used for plots.
- `plot_walk_forward(results_dict, metric, ...)`: Line plot per fold.
- `bar_mean_std(results_dict, metric, ...)`: Bar chart with mean and std.
- `plot_metric_distribution(results_dict, metric, ...)`: Box plot of fold metrics.
- `plot_performance_heatmap(results_dict, metric, ...)`: Heatmap of fold metrics.
- `plot_confusion_matrix(results, ...)`: Aggregated confusion matrix (raw or
  normalized).
