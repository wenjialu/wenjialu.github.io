import nltk
import sys
if __name__ == '__main__':
    for line in sys.stdin:
        input = line.strip()
        tree = nltk.Tree.fromstring(input)
        print(tree)
        tree.draw()
