from typing import List

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


def show_descriptive_stats(dataset: pd.DataFrame, feature_names: List[str], y_name: str, classes: List[str]):
    """
    Show three graphs per feature:
      - a boxplot
      - a histogramm
      - a repartition function
    :param dataset: dataset
    :param feature_names: features names to analyze
    :param y_name: name of the column that correspond to the lables
    :param classes: distinct values of labels
    :return: None
    """

    colors = px.colors.qualitative.Pastel

    if len(classes) > len(colors):
        print(f"We can show only {len(colors)} classes")
        return

    for feature in feature_names:
        fig = make_subplots(rows=1, cols=3)
        for i, cl in enumerate(classes):
            mask = (dataset[y_name] == cl) & (dataset[feature] != 9999) & (dataset[feature] != -9999)

            feature_values = dataset.loc[mask, feature].sort_values()
            feature_density = np.array(range(len(feature_values))) / float(len(feature_values))

            fig.append_trace(
                go.Box(
                    y=feature_values,
                    name=cl,
                    # boxpoints='outliers',
                    boxpoints=False,
                    #boxmean='sd',
                    jitter=0.5,
                    whiskerwidth=0.1,
                    fillcolor=colors[i],
                    marker_color=colors[i],
                    marker_size=2,
                    line_width=1
                ),
                row=1,
                col=1
            )

            fig.append_trace(
                go.Histogram(
                    x=feature_values,
                    name=cl,
                    marker_color=colors[i],
                    # marker=dict(color=colors[i]),
                    opacity=0.6,
                    histnorm='probability density',
                    autobinx=True,
                    showlegend=False,
                    nbinsx=200
                ),
                row=1,
                col=2
            )

            fig.append_trace(
                go.Scatter(
                    x=feature_values,
                    y=feature_density,
                    marker_color=colors[i],
                    showlegend=False
                ),
                row=1,
                col=3
            )
        fig.update_layout(title_text=f"Feature name: {feature}")
        fig.show()

        return


def plot_correlation_matrix(dataset: pd.DataFrame, cols: List[str]):
    """
    Plot the correlation matrix for all features listed in the cols param
    :param dataset: dataset
    :param cols: features to show
    :return: None
    """
    fig = px.imshow(dataset[cols].corr())
    fig.update_layout(
        autosize=False,
        width=900,
        height=1000)
    fig.show()
    return
