from urllib.parse import urlparse
import os

def is_valid_img_url(url):
    try:
        result = urlparse(url) # break up URL string into componenets
        is_valid = all([result.scheme, result.netloc]) #returns true if all items in the list are true, scheme is the https, netlock is the www.youtube.com

        # Check if the URL path has an image extension
        file_extension = os.path.splitext(result.path)[1] #splitting the path at the period  [1] accesses the 
        is_image = file_extension.lower() in ['.png', '.jpg', '.jpeg', '.gif']

        return is_valid and is_image
    except ValueError:
        return False

# URL to test
url_to_test = 'https://www.youtube.com/'

# Test the function
is_valid_and_image = is_valid_img_url(url_to_test)

# Print the result
print(f"The URL points to an image: {is_valid_and_image}")


