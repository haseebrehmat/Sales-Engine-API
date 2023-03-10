from difflib import SequenceMatcher
import jellyfish

print("Using JellyFish => ", jellyfish.jaro_distance("Hi how are you ", "hello how is doing"))
