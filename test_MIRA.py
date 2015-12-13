from MIRA import MIRA
def main():
    data = [[0, 0, 0, 0],
	    [1, 1, 1, 1],
	    [.5, .5, .5, 0],
	    [2, 2, 2, 1]]
    test_data = [[0, 0, 0],
	    [1, 1, 1],
	    [.5, .5, .5],
	    [2, 2, 2]]
    mira = MIRA(data, 2, test_data)
    mira.preprocess()
    mira.train_model()
    print mira.test_model()

main()
