import datetime

year, month, day = map(int, input().split())
per, flex = int(input()), 0
shit = list(map(float, input().split()))
while shit[0] > shit[1]:
    shit[0] = shit[0] / 2
    flex += per
print(*map(int, str(datetime.date(year, month, day)
      + datetime.timedelta(days=flex)).split("-")))

