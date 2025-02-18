import numpy as np
import pandas as pd

# Configuration object for paths and constants
class Config:
    DEFAULT_QFILE = 'q_200.txt'
    SCALE_OFFSET = 0.001
    HIGHQ_MEAN_RANGE = 20  # Last 20 values used for mean calculation

def load_csv_as_dataframe(filepath):
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(filepath)

def load_spec(filepath, q_column):
    """Loads and transforms spectrum data from a CSV file."""
    df = load_csv_as_dataframe(filepath)
    return np.log10(np.array(df[q_column]) + 1.0)

def load_params(filepath, colnames):
    """Loads parameter data from a CSV file into a dictionary."""
    df = load_csv_as_dataframe(filepath)
    return {col: np.array(df[col]) if col in df.columns else np.zeros(len(df)) for col in colnames}

def scale(spec, maxval):
    """Scales spectrum data by adjusting each row based on the first value."""
    return spec - spec[:, 0][:, np.newaxis] + maxval

def scale_highq(spec):
    """Adjusts high-q spectrum data by normalizing with the mean of the last few values."""
    return spec - np.mean(spec[:, -Config.HIGHQ_MEAN_RANGE:], axis=1, keepdims=True) + Config.SCALE_OFFSET

def shuffle_data(spec, params):
    """Shuffles spectrum data and associated parameters consistently."""
    shuffled_spec, shuffled_params = {}, {}
    for target in spec:
        indices = np.arange(spec[target].shape[0])
        np.random.shuffle(indices)
        shuffled_spec[target] = spec[target][indices]
        shuffled_params[target] = {p: params[target][p][indices] for p in params[target]}
    return shuffled_spec, shuffled_params

def load_q(datadir, qfile=Config.DEFAULT_QFILE):
    """Loads q-values from a file."""
    return np.loadtxt(f'{datadir}/{qfile}', dtype=str, delimiter=',')

def load_all_spec(targets, q_column, datadir, dataset, prefix='train'):
    """Loads spectrum data for all targets."""
    all_spec, maxval = {}, 0
    for target in targets:
        filepath = f'{datadir}/{dataset}/{prefix}_{target}_{dataset}.csv'
        spec = load_spec(filepath, q_column)
        maxval = max(maxval, np.max(spec[:, 0]))
        all_spec[target] = spec
    return all_spec  # Apply scaling if needed: {t: scale(s, maxval) for t, s in all_spec.items()}

def unravel_dict(spec_dict):
    """Unravels a dictionary of spectra into a single array with labels and index mapping."""
    targets = list(spec_dict.keys())
    spec_list, label_list, index_list = [], [], []
    for i, target in enumerate(targets):
        spec_list.append(spec_dict[target])
        label_list.append(i * np.ones(spec_dict[target].shape[0]))
        index_list.append(np.arange(spec_dict[target].shape[0]))
    return np.concatenate(spec_list), np.concatenate(label_list), np.concatenate(index_list)

def concatenate_spec(spec_dict):
    """Concatenates spectra from multiple targets into a single array."""
    spec_list, labels = [], []
    for key, (i, spec) in enumerate(spec_dict.items()):
        spec_list.append(spec)
        labels.append(i * np.ones(spec.shape[0]))
    return np.concatenate(spec_list), np.concatenate(labels)

def load_all_params(targets, param_list, datadir, dataset, prefix='train'):
    """Loads parameter data for all targets."""
    return {
        target: load_params(f'{datadir}/{dataset}/{prefix}_{target}_{dataset}.csv', param_list)
        for target in targets
    }
