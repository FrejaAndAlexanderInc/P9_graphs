from MimicDataExtractor import MimicDataExtractor

def main():
    mde = MimicDataExtractor()
    df = mde.extract(mde.labevents)
    print(df.head())

if __name__ == '__main__':
    main()