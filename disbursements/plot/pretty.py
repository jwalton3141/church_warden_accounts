"""Standardise plot size and style."""

import matplotlib.pyplot as plt
import os
import os.path as path

plt.rcParams['text.usetex'] = False

# If running under windows use times new roman font
if os.name == 'nt':
    plt.rcParams["font.family"] = "Times New Roman"


def make_fig_ax():
    """Create figure and axes instances to plot on."""
    return plt.subplots(1, 1, figsize=[10, 6.18])


def savefig(fig, plot_base, parish, entry=None, **kwargs):
    """Convenience function for saving plots."""
    save_dir = 'output'

    if entry:
        # Directory to save plots to
        save_dir = path.join(save_dir, 'custom', entry)
    else:
        save_dir = path.join(save_dir, 'standards')

    # Create output directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Construct file name of plot
    file_name = os.path.join(save_dir,
                             '{}_{}.png'.format(plot_base, parish))

    fig.tight_layout()
    fig.savefig(file_name, format='png', **kwargs)
    plt.close('all')
