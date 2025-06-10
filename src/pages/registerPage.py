from seleniumpagefactory.Pagefactory import PageFactory

class RegisterPage(PageFactory):
    locators = {
        'phone_input': ('XPATH', '//div[@class="base-input phone-input"]/input'),
        'uapp_link': ('CLASS_NAME', 'rules-desc-link'),
        'login_link': ('XPATH', '//a[@href="/login"]'),
        'close_btn': ('XPATH', '//a[@href="/"]'),
        'nextStep_btn': ('CLASS_NAME', 'next-button'),
        'verificationCode_input': ('XPATH', '//div[@class="base-verification"]/input'),
        'resend_btn': ('CLASS_NAME', 'verification-code-button code-input-button'),
        'checkVerificationCode_btn': ('CLASS_NAME', 'sheet-button'),
        'username_input': ('ID', '帐号'),
        'password_input': ('ID', '密码'),
        'confirmPassword_input': ('ID', '确认密码'),
        'referralBy_input': ('ID', '推荐码(选填)'),
        'register_btn': ('XPATH', '//button[.="注 册"]'),
    }

    def __init__(self, driver):
        self.driver = driver
    
    def enter_phone_number(self, phone):
        self.phone_input.set_text(phone)

    def click_nextStep_button(self):
        self.nextStep_btn.click_button()

    def enter_phone_verification_code(self, code):
        self.verificationCode_input.set_text(code)

    def resend_phone_verification_code(self):
        self.resend_btn.click_button()

    def check_phone_verification_code(self):
        self.checkVerificationCode_btn.click_button()

    def enter_username(self, username):
        self.username_input.set_text(username)

    def enter_password(self, password):
        self.password_input.set_text(password)

    def enter_confirm_password(self, confirmPassword):
        self.confirmPassword_input.set_text(confirmPassword)
    
    def enter_referral_by(self, refferralBy):
        self.referralBy_input.set_text(refferralBy)

    def submit_registerInfo(self):
        self.register_btn.click_button()

