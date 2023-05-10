import os, time
from seleniumpagefactory.Pagefactory import PageFactory

class BasePage():
    jj_baseURL = 'http://qah5.jjplaygo.com'
    jj_urls = {
        'home': f'{jj_baseURL}',
        'register': f'{jj_baseURL}/register',
        'login': f'{jj_baseURL}/login',
        'forgot-password': f'{jj_baseURL}/forgot-password',
        'wallet': f'{jj_baseURL}/wallet',
        'transactions': f'{jj_baseURL}/transactions',
        'add-card': f'{jj_baseURL}/add-card',
        'add-address': f'{jj_baseURL}/add-address',
        'withdrawal-methods': f'{jj_baseURL}/withdrawal-methods',
        'withdraw': f'{jj_baseURL}/withdraw',
        'deposit': f'{jj_baseURL}/deposit',
        'history': f'{jj_baseURL}/history',
        'profile': f'{jj_baseURL}/profile',
        'settings': f'{jj_baseURL}/settings',
        'nickname': f'{jj_baseURL}/nickname',
        'fullname': f'{jj_baseURL}/fullname',
        'phone': f'{jj_baseURL}/phone',
        'password': f'{jj_baseURL}/password',
        'language': f'{jj_baseURL}/language',
        'tasks': f'{jj_baseURL}/tasks',
        'promo': f'{jj_baseURL}/promo',
        'notifications': f'{jj_baseURL}/notifications',
        'games': f'{jj_baseURL}/games',
        'referral': f'{jj_baseURL}/referral',
        'share': f'{jj_baseURL}/share',
        'agent': f'{jj_baseURL}/agent',
        'help': f'{jj_baseURL}/help',
        'about': f'{jj_baseURL}/about',
    }

    cms_baseURL = 'http://20.24.16.242:8002'
    cms_urls = {
        'customers': f'{cms_baseURL}/customers/search',
        'mobileverificationcode': f'{cms_baseURL}/mobileverificationcode/search'
    }

    def __init__(self, driver):
        self.driver = driver