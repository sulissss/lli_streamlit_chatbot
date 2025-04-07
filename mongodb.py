from dotenv import load_dotenv
from pymongo import MongoClient
import os
import hashlib

load_dotenv('.env')

# ---------------------------------
# Connect to MongoDB
# mongo_client = MongoClient(os.getenv('MONGO_DB_URI'))
# print(os.getenv('MONGO_DB_URI'))

mongo_client = MongoClient(os.getenv('MONGO_DB_URI'))
db = mongo_client["LLI_Chatbot"]
problem_sets_col = db["Problem_Sets"]

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

# ---------------------------------
# Store a problem set in MongoDB
def save_problem_set(pset_name):
    problems = {}
    for problem_name in sorted(os.listdir(f'problem_sets/{pset_name}')):
        with open(f"problem_sets/{pset_name}/{problem_name}", "r") as file:
            problem_content = file.read()
        problems[problem_name[:-4]] = problem_content
    # os.listdir('problem_sets/Continuity')
    problem_sets_col.update_one(
        {"problem_set_name": pset_name},
        {"$set": {"problems": problems}},
        upsert=True
    )

    print(problems)

# ---------------------------------
# Retrieve all problem sets from MongoDB
def load_problem_sets():
    problem_sets = {}
    for pset in problem_sets_col.find():
        problem_sets[pset["problem_set_name"]] = pset["problems"]
    return problem_sets


# ensure_admin_exists()

# print(os.listdir('problem_sets/Continuity')[0][:-4])
# save_problem_set("Continuity")
# print(load_problem_sets())
# save_problem_set("Derivatives")