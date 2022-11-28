import random
from faker import Faker
from datetime import timedelta, datetime as dt
import numpy as np

# As per assessment details
status_list = ["Open","Closed","Resolved","Waiting for Customer","Waiting for Third Party","Pending"]

# Properties as per freshdesk website
# https://support.freshdesk.com/en/support/solutions/articles/226460-export-ticket-activities-from-your-helpdesk

activity_note_types = {0:"Reply",
                       1:"Forward",
                       2:"Reply_to_forward",
                       3:"Private_note",
                       4:"Public_note",
                       5:"Phone_note",
                       6:"Broadcast_note"}

activity_sources = {1:"Email",
                    2:"Portal",
                    3:"Phone",
                    4:"Forums",
                    5:"Twitter",
                    6:"Facebook",
                    7:"Chat",
                    8:"Mobihelp",
                    9:"Feedback widget",
                    10:"Outbound email",
                    11:"E-commerce",
                    12: "Bot"  }

activity_priorities = {1:"Low",
                       2:"Medium",
                       3:"High",
                       4:"Urgent"}

products = {
            'phone':['mobile','landline phone'],
            'tablets':['Apple','Samsung'],
            'computer': ['laptop','desktop PC'],
            'headphones': ['earphones','headphones']
}

issue_types = {
                "Pre_Sale_Question": ['question'],
                "Order_Question": ['question'],
                "Return": ['refund', "store credit", "exchange"],
                "Shipping": ['missing', 'delivery delay'],
                "Vendor": ['stock', 'price'],
                "Accounts": ['payment','address','login','registration'],
                "Product_Availability": ['low','not available']
                }
activity_priorities = [1,1,2,4,4,3,1]
performer_ids = np.arange(149015,149020) # assumer there are 5 agents
# requesters = np.arange(1,n+1)
