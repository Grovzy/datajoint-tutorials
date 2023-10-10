# %%
import datajoint as dj

# %%
schema = dj.Schema('app1')

# %%
@schema
class UserAccount(dj.Manual):
    definition = """
    phone      : bigint unsigned 
    ---
    first_name : varchar(40)
    last_name : varchar(40)

"""

# %%
@schema
class CreditCard(dj.Manual):
    definition = """
    card_number :  bigint unsigned 
    ---
    exp_date : date 
    cvc      : smallint unsigned
    zipcode  : int unsigned       
    -> UserAccount
    """

# %%
dj.Diagram(schema)

# %%
from faker import Faker
fake = Faker()

# %%
@schema
class AddOn(dj.Lookup):
    definition = """
    addon_id : int
    ---
    addon_name : varchar(40)
    price : decimal(5, 2) unsigned
    """

    contents = ((1, "Track & Field", 13.99), (2, "Marathon", 26.2), (3, "Sprint", 100.00))

# %%
AddOn()

# %%
@schema
class Purchase(dj.Manual):
    definition = """
   -> UserAccount
   -> AddOn
   ---
   -> CreditCard
   """

# %%
CreditCard()

# %%
dj.Diagram(schema)

# %%
UserAccount.insert(dict(
    phone=fake.random_int(1_000_000_0000, 9_999_999_9999),
    first_name=fake.first_name(),
    last_name=fake.last_name()) for _ in range (1000))

# %%
UserAccount()

# %%
CreditCard()

# %%
keys = UserAccount.fetch('KEY')

# %%
import random

# %%
fake.credit_card_number()

# %%
CreditCard.insert(
    dict(random.choice(keys), 
         zipcode=random.randint(10000,99999), 
         card_number=int(fake.credit_card_number()),
         cvc=random.randint(1, 999), 
         exp_date=fake.future_date()) for _ in range(15000))

# %%
CreditCard()

# %%
dj.Diagram(schema)


