import itertools

def compute_wer(predictions_dict, ground_truth_dict, split_words=False):
    wer = 0
    for fname, prediction in predictions_dict.items():
        prediction = _strip_extra_chars(prediction)
        ground_truth = _strip_extra_chars(ground_truth_dict[fname])

        if split_words is True:
            prediction = ''.join(prediction).split()
            ground_truth = ''.join(ground_truth).split()

        wer += levenshtein(ground_truth, prediction) / float(len(ground_truth))

    return wer / float(len(predictions_dict))


def levenshtein(ground_truth, prediction):
    r"""
    Calculates the Levenshtein distance between ground_truth and prediction.
    """
    n, m = len(ground_truth), len(prediction)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        ground_truth, prediction = prediction, ground_truth
        n, m = m, n

    current = list(range(n+1))
    for i in range(1, m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1, n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if ground_truth[j - 1] != prediction[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def _strip_extra_chars(prediction):
    return [value for value in prediction if value not in ('EOS', 'END', 'MASK')]


def write_sequences_to_labelfile(sequence_dict, fname):
    items = []
    for (k, v) in sequence_dict.items():
        label_str = ''.join(_strip_extra_chars(v)) + '\n'
        items.append(' '.join([k, label_str]))

    with open(fname, 'w') as f:
        f.writelines(items)

    del items

def flatten(list):
    if isinstance(list, str): return [list]  
    return list(itertools.chain.from_iterable([list]))