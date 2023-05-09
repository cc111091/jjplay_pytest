import os, time
import modules.funcs as funcs
# from selenium.webdriver.common.by import By
from seleniumpagefactory.Pagefactory import PageFactory


class BasePage(PageFactory):
    baseURL = 'http://qah5.jjplaygo.com'
    urls = {
        'home': f'{baseURL}',
        'register': f'{baseURL}/register',
        'login': f'{baseURL}/login',
        'forgot-password': f'{baseURL}/forgot-password',
        'wallet': f'{baseURL}/wallet',
        'transactions': f'{baseURL}/transactions',
        'add-card': f'{baseURL}/add-card',
        'add-address': f'{baseURL}/add-address',
        'withdrawal-methods': f'{baseURL}/withdrawal-methods',
        'withdraw': f'{baseURL}/withdraw',
        'deposit': f'{baseURL}/deposit',
        'history': f'{baseURL}/history',
        'profile': f'{baseURL}/profile',
        'settings': f'{baseURL}/settings',
        'nickname': f'{baseURL}/nickname',
        'fullname': f'{baseURL}/fullname',
        'phone': f'{baseURL}/phone',
        'password': f'{baseURL}/password',
        'language': f'{baseURL}/language',
        'tasks': f'{baseURL}/tasks',
        'promo': f'{baseURL}/promo',
        'notifications': f'{baseURL}/notifications',
        'games': f'{baseURL}/games',
        'referral': f'{baseURL}/referral',
        'share': f'{baseURL}/share',
        'agent': f'{baseURL}/agent',
        'help': f'{baseURL}/help',
        'about': f'{baseURL}/about',
    }

    def __init__(self, driver):
        self.driver = driver