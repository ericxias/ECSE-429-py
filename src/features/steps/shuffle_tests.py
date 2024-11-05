import random
import sys

# to run tests in random order -> python shuffle_tests.py

# import behave runner package files
from behave.__main__ import Configuration, run_behave, Runner


# overrides the feature_locations() function in behave/runner.py that typically returns the features in sequential order
class ShuffleRunner(Runner):
    # collect feature file names in a list, shuffle them, and return the randomized list
    def feature_locations(self):
        locations = super().feature_locations()
        random.shuffle(locations)
        return locations

# call run_behave function with the shuffled feature order in the runner_class parameter
def main():
    config = Configuration()
    return run_behave(config, runner_class=ShuffleRunner)


if __name__ == '__main__':
    sys.exit(main())