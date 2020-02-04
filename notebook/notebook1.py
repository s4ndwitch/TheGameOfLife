print([i for i in range(100000, 1000000) if not (set(list(str(i))) & {"0", "6", "7", "8", "9"})][10178])
