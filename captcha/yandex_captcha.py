import os

from dotenv import load_dotenv

from anticaptchaofficial.imagecaptcha import *


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

api_key = os.environ.get("SECRET_KEY")

def img_captcha():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)

    solver.set_soft_id(0)

    captcha_text = solver.solve_and_return_solution("img/captcha.jpeg")

    if captcha_text != 0:
        print("captcha text " + captcha_text) 
        return True
    else:
        print("task finished with error " + solver.error_code)
        return False