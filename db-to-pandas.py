import pandas as pd
import pickle
from trie import Trie

dict = pd.read_csv("ids.txt")

with open("ids.pickle", "rb") as file:
    nuestrasids = pickle.load(file)


if(nuestrasids.search("7IDGJCWEC5FOJGT4RUN2CCBNLQ")):
    print("existe")
else:
    print("no existe")
