import pandas as pd

df = pd.read_csv('data.csv')

#print(df.to_string()) 
#print(pd.options.display.max_rows) 
#print(df.head(20))
#print(df.tail(20))
#print(df.info())

new_df = df.dropna()

print(new_df.to_string())

#df.dropna(inplace=True)
df["Calories"].fillna("NOT",inplace=True)
print(df.to_string())
'''
###
mydataset = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}

myvar = pd.DataFrame(mydataset)

print(f"{myvar}\n")

###
a = [1, 7, 2]

myvar = pd.Series(a,index=["x","y","z"])

print(f"{myvar}\n")

###
calories = {"day1": 420, "day2": 380, "day3": 390}

myvar = pd.Series(calories,index=["day1","day2","day3","day4"])

print(f"{myvar}\n")

###
data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}

myvar = pd.DataFrame(data,index=["A","B","C"])

print(myvar.loc[["A","B"]])
print(f"{myvar}\n")
'''