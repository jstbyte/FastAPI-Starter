import os
from dotenv import load_dotenv

if load_dotenv('.env.dev'):  # 'DEV'|'PRD'
    os.environ['MODE'] = 'DEV'
