
from ezodf import Sheet, opendoc
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import re
import os
from sendmsgs import send_messages
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

FILE_DATA_PATH = os.getenv('FILE_DATA_PATH')
FILE_USERS_PATH = os.getenv('FILE_USERS_PATH')
TEXT_1 = os.getenv('TEXT_1')
TEXT_2 = os.getenv('TEXT_2')


DEFAULT_INITIAL_ROW = 3
ROW_OFFSET = 9

IMAGES_INITIAL_RECT = (7, 3, 9, 10)
IMAGES_RECT_X_SIZE = IMAGES_INITIAL_RECT[2] - IMAGES_INITIAL_RECT[0]
IMAGES_RECT_Y_SIZE = IMAGES_INITIAL_RECT[3] - IMAGES_INITIAL_RECT[1]
IMAGES_Y_OFFSET = 7

INITIAL_ROW = DEFAULT_INITIAL_ROW + ROW_OFFSET



    
    
def create_image(names: list[str],date, i) -> str:
            canvas = (400, 200)
            # init canvas
            im = Image.new('RGBA', canvas, (255, 255, 255, 255))
            draw = ImageDraw.Draw(im)
            
            x = 30
            y = 110
            offset_y = 25
            font_size = 15
            font = ImageFont.truetype('./assets/arial.ttf',font_size)
            
            for name in names:
                draw.text((x, y), name, fill=(0, 0, 0, 255), font=font)
                y += offset_y
                

            size_text1 = font.getlength(TEXT_1)

            draw.text(((canvas[0] - size_text1) / 2, 30), TEXT_1,fill=(0, 0, 0, 255), font=font)
            draw.text((270, 150), TEXT_2,fill=(0, 0, 0, 255), font=font)


            date_object = datetime.strptime(date, '%Y-%m-%d')
            date = date_object.strftime('%d/%m/%Y')

            size_date = font.getlength(date)
            draw.text(((canvas[0] - size_date) / 2, 60), date, fill=(0, 0, 0, 255), font=font)
            # save image
            path = f'output_{i}.png'
            im.save(path)
            
            return path
    
    
    

def trim_phone(phone):
    phone = re.sub('\.0|\'', '', phone)  # remove .0 and ' from phone
    return phone

def create_messages(file_path: str = "data.ods", users: list = []) -> list[any]:
    """Create a message for each row in the file, returns a list of dictionaries with the following structure:
    [
        {
            'image_path': 'path/to/image',
            'names': ['name1', 'name2',...]
        }
    ]"""
    
    doc = opendoc(file_path)
    
    n_names = 3
  
    sheet: Sheet
    sheet = doc.sheets[0]  # get the first sheet

    data = []
    for i, row in enumerate(sheet.rows()):
        if (i < INITIAL_ROW ):
            continue
        
        row_data: dict[str, str|list[str]] = {'image_path': '', 'phones': []}
        date = row[0].value
        if not date:
            break
        
        names = []
        
        for j, cell in enumerate(row):
            if 0 <  j < n_names + 1 and cell.value != None:
                name = cell.value
                names.append(name)
                phone = name_to_phone(name, users)
                if (phone == None): 
                    print(f"User {name} in date {date} not found")
                else:
                    row_data["phones"].append(phone)
        
        
        image_path = create_image(names, date, i)
        row_data["image_path"] = image_path
        
        data.append(row_data)
              

    return data
 
def get_users(file_path: str = "users.ods") -> list:
    doc = opendoc(file_path)
    
    sheet: Sheet
    sheet = doc.sheets[0]  # get the first sheet
    
    user_data = {}
    for i, row in enumerate(sheet.rows()):
        if (i == 0):
            continue
            
        name = row[1].value
        phone = trim_phone(str(row[2].value))
        
        user_data[name] = phone
               
    
    return user_data


def name_to_phone(name, users: dict[str, str]) -> list[dict[str,str | list[str]]]:
    return users.get(name)


def main():
    users = get_users(FILE_USERS_PATH)
    messages = create_messages(FILE_DATA_PATH, users)
    
    send_messages(messages)
    os.system("rm *.png")
    

if __name__ == "__main__":
    main()
