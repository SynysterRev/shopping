import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

month_dict = {
    "Jan": 0,
    "Feb": 1,
    "Mar": 2,
    "Apr": 3,
    "May": 4,
    "June": 5,
    "Jul": 6,
    "Aug": 7,
    "Sep": 8,
    "Oct": 9,
    "Nov": 10,
    "Dec": 11
}


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    try:
        with open(filename) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            evidence_lists = []
            labels = []
            for row in csv_reader:
                month = month_dict.get(row["Month"])
                returning = 0 if row['VisitorType'] == 'New_Visitor' else 1
                weekend = 1 if row['Weekend'] == 'TRUE' else 0
                evidence = [int(row['Administrative']),
                            float(row['Administrative_Duration']),
                            int(row['Informational']), float(row['Informational_Duration']),
                            int(row['ProductRelated']),
                            float(row['ProductRelated_Duration']),
                            float(row['BounceRates']), float(row['ExitRates']),
                            float(row['PageValues']), float(row['SpecialDay']), month,
                            int(row['OperatingSystems']), int(row['Browser']),
                            int(row['Region']),
                            int(row['TrafficType']), returning, weekend]
                evidence_lists.append(evidence)
                labels.append(1 if row['Revenue'] == 'TRUE' else 0)
            return evidence_lists, labels
    except FileNotFoundError:
        sys.exit("File not found")


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive = sum(1 for label in labels if label == 1)
    negative = len(labels) - positive
    sensitivity = sum(1 for label, prediction in zip(labels, predictions) if label ==
                      1 and prediction == 1) / positive
    specificity = sum(1 for label, prediction in zip(labels, predictions) if label ==
                      0 and prediction == 0) / negative
    return sensitivity, specificity


if __name__ == "__main__":
    main()
