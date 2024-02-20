import matplotlib.pyplot as plt

def plot_price(filename, snapshots):
    plt.plot([s.date for s in snapshots], [s.avg_price for s in snapshots], )
    plt.xlabel("Date")
    plt.ylabel("Prices")
    plt.savefig(filename)
    return filename
