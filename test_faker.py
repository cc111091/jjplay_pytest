import random, string
from faker import Faker

faker = Faker(locale='zh_CN')

def bbanGenerator():
    for i in range(50):
        randomLength = random.randint(2, 7)
        randomString = ''.join(random.choices(string.digits, k=randomLength))
        bban = faker.bban()
        print(f'{bban[-14:]}{randomString}')

def usdtAddressGenerator(usdtType: str, n=50):
    if usdtType in 'trc20':
        header = 'T'
        length=34-len(header)
    elif usdtType in 'erc20':
        header = '0x'
        length=42-len(header)

    for i in range(n):
        randomAddress = ''.join(random.choices(string.ascii_letters+string.digits, k=length))
        print(f'{header}{randomAddress}')

usdtAddressGenerator('erc20')