from airbnb.save import save_to_file
from airbnb.airbnb_selenium import get_accommodations
from airbnb.airbnb_selenium import remove_tag
import csv

accommodations = get_accommodations()

# save_to_file(accommodations)
