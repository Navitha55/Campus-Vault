import bcrypt

def pass_hash(input_pass):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(input_pass.encode('utf-8'),salt).decode('utf-8')

def check_pw(input_pass,db_pass):
    return bcrypt.checkpw(input_pass.encode('utf-8'),db_pass.encode('utf-8'))