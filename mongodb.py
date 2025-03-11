from pymongo import MongoClient
import os
import hashlib

# ---------------------------------
# Connect to MongoDB
mongo_client = MongoClient(os.getenv('MONGO_DB_URI'))
db = mongo_client["chatbot_db"]
problem_sets_col = db["problem_sets"]
admins_col = db["admins"]

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

# ---------------------------------
# Ensure admin credentials exist (for starters: username "abc", password "123")
def ensure_admin_exists():
    if admins_col.count_documents({"username": "abc"}) == 0:
        admins_col.insert_one({"username": "abc", "password": encrypt_string("123")})

def add_admin(username, password):
    if admins_col.count_documents({"username": username}) == 0:
        admins_col.insert_one({"username": username, "password": encrypt_string(password)})

# ---------------------------------
# Authenticate an admin user
def authenticate_admin(username, password):
    admin = admins_col.find_one({"username": username})
    return admin and admin["password"] == encrypt_string(password)

# ---------------------------------
# Store a problem set in MongoDB
def save_problem_set(pset_name, problems):
    problem_sets_col.update_one(
        {"set_name": pset_name},
        {"$set": {"problems": problems}},
        upsert=True
    )

# ---------------------------------
# Retrieve all problem sets from MongoDB
def load_problem_sets():
    problem_sets = {}
    for pset in problem_sets_col.find():
        problem_sets[pset["set_name"]] = pset["problems"]
    return problem_sets
