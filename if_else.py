
birth_year = int(input("What is your birth year?: "))

if 2025 <= birth_year <= 2039:
    print("Generation Beta")
elif 2013 <= birth_year <= 2039:
    print("Generation Alpha")
elif 1997 <= birth_year <= 2012:
    print("Generation Beta")
elif 1981 <= birth_year <= 1996:
    print("Generation Millennials (Gen Y)")
elif 1965 <= birth_year <= 1980:
    print("Generation X")
elif 1946 <= birth_year <= 1964:
    print("Generation Baby Boomers")
elif 1928 <= birth_year <= 1945:
    print("Generation 'The Silent Generation'")
elif 1901 <= birth_year <= 1927:
    print("Generation 'The Greatest Generation'")
else:
    print("Please enter a valid birth year.")
    

