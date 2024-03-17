from hijridate import Hijri, Gregorian
from flask import Blueprint, render_template, request
import re
from datetime import datetime
import unicodedata

date_converter_bp = Blueprint('date_converter', __name__, url_prefix='/date_converter_bp')


@date_converter_bp.route('/', methods=['GET', 'POST'])
def handle_conversion():
    if request.method == 'POST':
        input_date = request.form['input_date']
        conversion_type = request.form['conversion_type']
        converted_date = convert_date(input_date, conversion_type)
        return render_template('date_converter/date_converter.html', converted_date=converted_date)
    else:
        return render_template('date_converter/date_converter.html', active_link='date_converter')


def convert_date(date, conversion_type):

    date = date.strip()
    print(date)
    date = convert_arabic_to_english_numerals(date)
    print(date)
    year, month, day = check_and_flip_date(date)
    print(date)

    try:
        if conversion_type == 'auto':
            if (year < 1500):
                converted_date = Hijri(year, month, day).to_gregorian()
            else:
                converted_date = Gregorian(year, month, day).to_hijri()

        elif conversion_type == 'ad_to_hijri':
            converted_date = Gregorian(year, month, day).to_hijri()

        elif conversion_type == 'hijri_to_ad':
            converted_date = Gregorian(year, month, day).to_hijri()

        converted_date_components = str(converted_date).split("-")
        converted_date = "/".join(converted_date_components)
        return converted_date
    except Exception as e:
        return str(e)


def check_and_flip_date(date):

    if "/" in date:
        components = date.split("/")

    else:
        components = date.split("-")

    if len(components) == 3:

        # Check if the first component has 4 digits, indicating it is a year
        if len(components[0]) == 4:

            return int(components[0]) , int(components[1]), int(components[2])
        else:
            # The date is in the day/month/year format, so flip it
            return int(components[2]), int(components[1]), int(components[0])

        # return formatted_date
    else:
        print("Invalid date format")
        return False

def convert_arabic_to_english_numerals(arabic_numerals):
    arabic_to_english = {
        '٠': '0',
        '١': '1',
        '٢': '2',
        '٣': '3',
        '٤': '4',
        '٥': '5',
        '٦': '6',
        '٧': '7',
        '٨': '8',
        '٩': '9'
    }

    english_numerals = ''
    for numeral in arabic_numerals:
        if numeral in arabic_to_english:
            english_numerals += arabic_to_english[numeral]
        else:
            english_numerals += numeral
    # Normalize the string to remove any invisible characters or formatting elements
    normalized_string = unicodedata.normalize('NFKD', english_numerals)
    ascii_string = normalized_string.encode('ascii', 'ignore').decode('ascii')
    return ascii_string

        
@date_converter_bp.route('/numbers_converter', methods=['GET', 'POST'])
def numbers_converter():
    if request.method == 'POST':
        input_numbers = request.form['input_numbers']
        converted_numbers = convert_arabic_to_english_numerals(input_numbers)
        return render_template('date_converter/numbers_converter.html', converted_numbers=converted_numbers, active_link='numbers_converter')
    else:
        return render_template('date_converter/numbers_converter.html', active_link='numbers_converter')