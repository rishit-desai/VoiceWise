import streamlit as st
import matplotlib.pyplot as plt # type: ignore
import matplotlib.patches as patches # type: ignore


def plot_call_timeline(
    call_id, utterances, silence_intervals, overtalk_intervals, total_duration, silence_percentage, overtalk_percentage
):
    """
    Generates a timeline visualization of the call.

    Args:
        call_id (str): The ID of the call.
        utterances (list): The list of utterance dictionaries.
        silence_intervals (list of tuples): Silence intervals.
        overtalk_intervals (list of tuples): Overtalk intervals.
        total_duration (float): The total duration of the call.
    """
    fig_timeline, ax = plt.subplots(figsize=(12, 4))
    y_agent = 1
    y_customer = 0
    bar_height = 0.8

    # Plot agent utterances
    for utt in [u for u in utterances if u["speaker"] == "Agent"]:
        rect = patches.Rectangle(
            (utt["stime"], y_agent - bar_height / 2),
            utt["etime"] - utt["stime"],
            bar_height,
            linewidth=1,
            edgecolor="black",
            facecolor="skyblue",
            alpha=0.7,
            label=(
                "Agent"
                if not any(rect.get_label() == "Agent" for rect in ax.patches)
                else ""
            ),
        )
        ax.add_patch(rect)

    # Plot customer utterances
    for utt in [u for u in utterances if u["speaker"] == "Customer"]:
        rect = patches.Rectangle(
            (utt["stime"], y_customer - bar_height / 2),
            utt["etime"] - utt["stime"],
            bar_height,
            linewidth=1,
            edgecolor="black",
            facecolor="lightcoral",
            alpha=0.7,
            label=(
                "Customer"
                if not any(rect.get_label() == "Customer" for rect in ax.patches)
                else ""
            ),
        )
        ax.add_patch(rect)

    # Plot silence intervals
    for start, end in silence_intervals:
        rect = patches.Rectangle(
            (start, -1),
            end - start,
            0.4,
            linewidth=1,
            edgecolor="gray",
            facecolor="lightgray",
            alpha=0.6,
            label=(
                "Silence"
                if not any(rect.get_label() == "Silence" for rect in ax.patches)
                else ""
            ),
        )
        ax.add_patch(rect)

    # Plot overtalk intervals
    for start, end in overtalk_intervals:
        rect = patches.Rectangle(
            (start, 1.5),
            end - start,
            0.4,
            linewidth=1,
            edgecolor="orange",
            facecolor="orange",
            alpha=0.6,
            label=(
                "Overtalk"
                if not any(rect.get_label() == "Overtalk" for rect in ax.patches)
                else ""
            ),
        )
        ax.add_patch(rect)

    ax.set_xlabel("Time (seconds)")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Customer", "Agent"])
    ax.set_title(f"Call ID: {call_id} - Utterance Timeline with Silence and Overtalk")
    ax.set_xlim(0, total_duration)
    ax.set_ylim(-1.5, 2)
    ax.legend(bbox_to_anchor=(0, 1))

    fig_silence_overtalk, axs = plt.subplots(figsize=(12, 5))
    # 1. Bar chart for a single call's metrics
    labels = ["Overtalk", "Silence"]
    percentages = [overtalk_percentage, silence_percentage]
    colors = ["skyblue", "lightcoral"]

    axs.bar(labels, percentages, color=colors)
    axs.set_ylabel("Percentage (%)")
    axs.set_title(f"Call ID: {call_id} - Overtalk and Silence")
    axs.set_ylim(0, 100)  # Adjust y-axis limits for better visualization
    for i, v in enumerate(percentages):
        axs.text(i, v + 0.5, f"{v:.1f}%", ha="center")

    return fig_timeline, fig_silence_overtalk


def analyze_call_timeline(utterances, total_duration=None):
    """
    Analyzes a list of utterances to identify silence and overtalk intervals.

    Args:
        utterances (list): A list of dictionaries, where each dictionary
                           has 'speaker', 'stime', and 'etime'.
        total_duration (float, optional): The total duration of the call.
                                         If None, it will be inferred from the
                                         latest utterance end time.

    Returns:
        tuple: A tuple containing:
               - silence_intervals (list of tuples): (start_time, end_time) of silence.
               - overtalk_intervals (list of tuples): (start_time, end_time) of overtalk.
               - max_time (float): The maximum time in the call.
               - silence_percentage (float): Percentage of silence in the call.
               - overtalk_percentage (float): Percentage of overtalk in the call.
    """
    silence_intervals = []
    overtalk_intervals = []
    sorted_utterances = sorted(utterances, key=lambda x: x["stime"])
    max_time = 0

    for utt in sorted_utterances:
        max_time = max(max_time, utt["etime"])

    if total_duration is None:
        total_duration = max_time

    # Calculate silence
    if sorted_utterances:
        if sorted_utterances[0]["stime"] > 0:
            silence_intervals.append((0, sorted_utterances[0]["stime"]))
        for i in range(len(sorted_utterances) - 1):
            if sorted_utterances[i + 1]["stime"] > sorted_utterances[i]["etime"]:
                silence_intervals.append(
                    (sorted_utterances[i]["etime"], sorted_utterances[i + 1]["stime"])
                )
        if sorted_utterances[-1]["etime"] < total_duration:
            silence_intervals.append((sorted_utterances[-1]["etime"], total_duration))
    elif total_duration > 0:
        silence_intervals.append((0, total_duration))

    # Calculate overtalk
    for i in range(len(sorted_utterances)):
        for j in range(i + 1, len(sorted_utterances)):
            utt1 = sorted_utterances[i]
            utt2 = sorted_utterances[j]
            if utt1["speaker"] != utt2["speaker"]:
                overlap_start = max(utt1["stime"], utt2["stime"])
                overlap_end = min(utt1["etime"], utt2["etime"])
                if overlap_start < overlap_end:
                    overtalk_intervals.append((overlap_start, overlap_end))

    silence_percentage = (
        sum(end - start for start, end in silence_intervals) / total_duration * 100
    )
    overtalk_percentage = (
        sum(end - start for start, end in overtalk_intervals) / total_duration * 100
    )

    return silence_intervals, overtalk_intervals, total_duration, silence_percentage, overtalk_percentage
