

import matplotlib.pyplot as plt
import seaborn as sns


# Project color palette
ZONE_COLORS = [
    "#60A5FA",
    "#34D399",
    "#FBBF24",
    "#FB923C",
    "#F87171"
]


def set_chart_style():
    """
    Set common chart styling.
    """

    sns.set_theme(style="darkgrid")

    plt.rcParams["figure.facecolor"] = "#111827"
    plt.rcParams["axes.facecolor"] = "#111827"
    plt.rcParams["axes.labelcolor"] = "#E5E7EB"
    plt.rcParams["text.color"] = "#E5E7EB"
    plt.rcParams["xtick.color"] = "#9CA3AF"
    plt.rcParams["ytick.color"] = "#9CA3AF"


def heart_rate_line_chart(df, zone_limits):
    
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        df["Timestamp"],
        df["Heart_Rate"],
        color="#38bdf8",
        linewidth=2.5,
        marker="o",
        markersize=4,
        label="Heart Rate"
    )

    ax.fill_between(
        df["Timestamp"],
        df["Heart_Rate"],
        alpha=0.12,
        color="#38bdf8"
    )

    ax.set_title(
        "Heart Rate During Workout",
        fontsize=16,
        fontweight="bold",
        color="white",
        pad=15
    )

    ax.set_xlabel("Time", color="white", fontsize=11)
    ax.set_ylabel("Heart Rate (BPM)", color="white", fontsize=11)

    ax.tick_params(colors="white")

    ax.grid(
        True,
        linestyle="--",
        alpha=0.25
    )

    ax.set_facecolor("#111827")
    fig.patch.set_facecolor("#111827")

    for spine in ax.spines.values():
        spine.set_color("#334155")

    fig.autofmt_xdate()

    plt.tight_layout()

    return fig

def zone_bar_chart(zone_time):
    """
    Create zone duration bar chart.
    """

    set_chart_style()

    fig, ax = plt.subplots(figsize=(9, 4))

    sns.barplot(
        x=zone_time.index,
        y=zone_time.values / 60,
        hue=zone_time.index,
        palette=ZONE_COLORS,
        legend=False,
        ax=ax
    )

    ax.set_title("Time Spent in Heart Rate Zones")
    ax.set_xlabel("Heart Rate Zone")
    ax.set_ylabel("Time (Minutes)")

    fig.tight_layout()

    return fig


def zone_donut_chart(zone_time):
    """
    Create zone distribution donut chart.
    """

    set_chart_style()

    fig, ax = plt.subplots(figsize=(7, 5))

    values = zone_time.values

    if values.sum() == 0:
        ax.text(
            0.5, 0.5,
            "No zone data available",
            ha="center",
            va="center"
        )
        ax.axis("off")
        return fig

    ax.pie(
        values,
        labels=zone_time.index,
        colors=ZONE_COLORS,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={
            "width": 0.42,
            "edgecolor": "#111827"
        }
    )

    ax.set_title("Heart Rate Zone Distribution")

    fig.tight_layout()

    return fig


def heart_rate_histogram(df):
    """
    Show heart rate frequency distribution.
    """

    set_chart_style()

    fig, ax = plt.subplots(figsize=(9, 4))

    sns.histplot(
        data=df,
        x="Heart_Rate",
        bins=12,
        kde=True,
        color="#22D3EE",
        ax=ax
    )

    ax.set_title("Heart Rate Distribution")
    ax.set_xlabel("Heart Rate (BPM)")
    ax.set_ylabel("Frequency")

    fig.tight_layout()

    return fig
