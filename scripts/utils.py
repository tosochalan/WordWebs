import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from scipy import stats


def samples_to_probability(samples):
    """
    Takes samples, returns X, Y, where X is array of sorted unique samples and Y[i] is the probability of choosing sample X[i] at random.
    """

    sample_counts = Counter(samples)
    unique_sorted_samples = sorted(set(samples))

    num_of_samples = len(samples)
    probability = np.array([sample_counts[sample] / num_of_samples for sample in unique_sorted_samples])

    return unique_sorted_samples, probability


def log_bin(X, Y, num_bins=50):
    """
    Takes X, Y and applies log binning. Returns bX where bX[i] is center of the i-th bin, and bY, where bY[i] is the average value in the i-th bin.
    """
    X = np.array(X)
    Y = np.array(Y)

    bins = np.logspace(np.log10(X.min()), np.log10(X.max()), num_bins)

    indices = np.digitize(X, bins, right=True)

    bx = []
    by = []

    for i in range(1, len(bins)):
        mask = indices == i
        if np.any(mask):
            bx.append(np.sqrt(bins[i]*bins[i-1]))
            by.append(np.sum(Y[mask]) / (bins[i] - bins[i-1]))

    return np.array(bx), np.array(by)


def to_log_log(X, Y):
    X_log = []
    Y_log = []
    for x in X:
        X_log.append(np.log10(x))
    for y in Y:
        Y_log.append(np.log10(y))
    return X_log, Y_log


def plot_multi_regime_degree_distribution(title, points_X, points_Y, slope_small, intercept_small, slope_large, intercept_large):
    if title:
        title = f"{title}: Multirežimová distribúcia stupňa uzlov"
    else:
        title = "Multirežimová distribúcia stupňa uzlov"

    intersection_x = 10 ** ((intercept_small - intercept_large) / (slope_large - slope_small))

    line1_X = [points_X[0], intersection_x]
    line1_Y = [
        10 ** intercept_small * line1_X[0] ** slope_small,
        10 ** intercept_small * line1_X[1] ** slope_small
    ]

    line2_X = [intersection_x, points_X[-1]]
    line2_Y = [
        10 ** intercept_large * line2_X[0] ** slope_large,
        10 ** intercept_large * line2_X[1] ** slope_large
    ]

    plt.scatter(points_X, points_Y, color='#34495E', alpha=0.6, s=15, zorder=1)
    plt.plot(line1_X, line1_Y, color='#E67E22', linestyle='--', linewidth=2.5, label="$\gamma_1 = " + f"{-slope_small:.2f}" + "$")
    plt.plot(line2_X, line2_Y, color="#27C246", linestyle='--', linewidth=2.5, label="$\gamma_2 = " + f"{-slope_large:.2f}" + "$")
    plt.grid(True, linestyle=':', alpha=0.3)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("k")
    plt.ylabel("P(k)")
    plt.title(title)
    plt.legend()
    plt.show()


def from_middle(length_of_array, step):
    """
    Returns left and right indices of an array if iterating from the
    middle while adding two elements at each step.

    Also returns length of elements iterated over given steps.
    """
    n = 2
    mid = length_of_array // 2
    left = mid - 1
    right = mid

    if length_of_array % 2:
        # if odd number of points, start with only one middle point
        n = 1
        left = mid

    left -= step
    right += step
    n += step * 2

    if left < 0 or right > length_of_array - 1:
        raise ValueError("Indices out of bounds. Step is too large for given array length.")

    return (left, right + 1, n)


def linear_regression(X, Y, trim_statistics=True, R2_difference_threshold=0.015):
    """
    Estimates the slope of power-law line in log-log space.

    If trims_statistics is True, then the slope is computed from the middle of the data
    avoiding tails until the determination coefficient starts dropping rapidly (effectibvely
    trimming noisy tails).

    Returns:
    - start index of trimmed data
    - end index of trimmed data
    - slope
    - intercept
    - coefficient of determination
    - margin of error
    """
    log_X, log_Y = to_log_log(X, Y)

    if not trim_statistics:
        slope, intercept, r, p, se = stats.linregress(log_X, log_Y)
        return 0, len(log_X), slope, intercept, r * r, se

    last_slope = None
    slope = None
    last_R2 = 0
    R2 = 0

    length = len(log_X)
    left, right, n = from_middle(length, 2)

    X_subset = log_X[left:right]
    Y_subset = log_Y[left:right]

    right -= 1  # because noninclusive array slices

    alpha = 0.05

    slope, intercept, r, p, se = stats.linregress(log_X, log_Y)
    t_crit = stats.t.ppf(1 - alpha / 2, n - 2)

    while left > 0 and last_R2 - R2 < R2_difference_threshold:
        left -= 1
        right += 1
        n += 2

        X_subset.append(log_X[left])
        X_subset.append(log_X[right])
        Y_subset.append(log_Y[left])
        Y_subset.append(log_Y[right])

        last_slope = slope
        last_se = se
        last_intercept = intercept
        last_R2 = R2
        last_t_crit = t_crit

        slope, intercept, r, p, se = stats.linregress(X_subset, Y_subset)
        t_crit = stats.t.ppf(1 - alpha / 2, n - 2)
        R2 = r * r

    confidence = last_t_crit * last_se
    return left + 1, right, last_slope, last_intercept, last_R2, confidence


def strip_word(word: str) -> tuple[str, bool]:
    """
    Strips word off of interpunctions and other unwanted symbols.

    Returns the stripped word and flag if the word is ending a sentence.

    For example, ...Don't!! -> ("don't", True).

    :param word: Word for tokenization
    :type word: str
    :return: Stripped word, is_end_of_sentence
    :rtype: tuple[str, bool]
    """
    is_end_of_sentence = False
    end_of_sentence = set(".!?")
    if len(word) > 0 and word[-1] in end_of_sentence:
        is_end_of_sentence = True
    _, core_word = get_tokens_and_core_word(word)
    return core_word, is_end_of_sentence


def split_word(word: str) -> list[str]:
    """
    Splits word into interpunction and the core word.

    For example, ...Don't!! -> [".", ".", ".", "don't", "!", "!"].

    :param word: Word for tokenization
    :type word: str
    :return: List of tokens
    :rtype: list[str]
    """
    if word.count(" ") > 0:
        raise ValueError("Input word should not contain spaces")

    tokens, _ = get_tokens_and_core_word(word)
    return tokens


def get_tokens_and_core_word(word):
    tokens = []
    punctuation = []
    core_word = ""
    reading_prefix_punctuation = True
    for char in word:
        if char.isalnum():
            reading_prefix_punctuation = False
            if punctuation:
                core_word += "".join(punctuation)
                punctuation = []
            core_word += char.lower()

        elif reading_prefix_punctuation:
            tokens.append(char.lower())
        else:
            punctuation.append(char.lower())

    if core_word:
        tokens.append(core_word)
    if punctuation:
        tokens.extend(punctuation)

    return tokens, core_word


def test_plot_multi_regime_degree_dsitribution():
    """
    Visual testing plot_multi_regimeDegree_distribution with two regimes (gamma1 = 1.5, gamma2 = 3)
    The plot should show two regimes with a steeper right side.
    """
    X1 = []
    Y1 = []
    gamma_1 = -1.5
    for exponent in range(10):
        X1.append(10 ** exponent)
        Y1.append(X1[-1] ** gamma_1)

    gamma_2 = -3
    X2 = [10 ** 10]
    Y2 = [Y1[-1] * 10 ** gamma_2]
    for exponent in range(11, 19):
        X2.append(10 ** exponent)
        Y2.append(Y2[-1] * 10 ** gamma_2)

    _, _, slope1, intercept1, r2, confidence1 = linear_regression(X1, Y1, False)
    _, _, slope2, intercept2, r2, confidence2 = linear_regression(X2, Y2, False)

    assert confidence1 == 0
    assert confidence2 == 0
    assert abs(slope1 - gamma_1) < 0.001
    assert abs(slope2 - gamma_2) < 0.001

    # should see nice plot with steeper right side (gamma1 = 1.5, gamma2 = 3)
    plot_multi_regime_degree_distribution("Umelé dáta", X1 + X2, Y1 + Y2, slope1, intercept1, slope2, intercept2)


if __name__ == "__main__":
    test_plot_multi_regime_degree_dsitribution()
