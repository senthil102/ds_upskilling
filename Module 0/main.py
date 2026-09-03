name="senthil"
age=30
mark=100

print("Name:", name)
print("Age:", age)
print("Mark:", mark)  


def calculate_experience(start_year, current_year):
    experience = current_year - start_year
    return experience

print("Experience:", calculate_experience(2010, 2026), "years")


def add(a, b):
    c=a+b
    return c

result=add(10,20)
print("Addition:", result)


list=[
"senthil",
"age"
]

for i in list:
    print(i)


dic ={

    "name": "kumar",
    "age": 30
}
for key,value in dic.items():
    print(key,":",value)

print("Name:", dic["name"])
print("Age:", dic["age"]);