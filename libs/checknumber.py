def evenedorodded(number):
    if(number % 2 == 0):
        if(number != 0):
            return 'bilangan genap'
        else:
            return 'bilangan netral'
    else:
        return 'bilangan ganjil'

def isPrime(number):
    if number > 1:
        for x in range(2, number):
            if number % x == 0:
                return 'bukan bilangan prima'
                break
        else:
            return 'bilangan prima'
    else:
        return 'bukan bilangan prima'