from statistics import quantiles
from PIL import Image

class ImageHelper():

    @staticmethod
    def save_image_with_quality(image_path:str, image_quality:int, save_directory:str, file_name:str):
        image_file = Image.open(image_path)
        save_path = f'{save_directory}/{file_name}.jpg'

        image_file.save(save_path, quality=image_quality)

image_dir = '/Users/watcharapongwongrattanasirikul/Documents/Git/MyUtils/Asimov/lib/Image/original/'
image_name = 'DSCF1121'
image_path = image_dir + image_name + '.jpg'
directory_path = '/Users/watcharapongwongrattanasirikul/Documents/Git/MyUtils/Asimov/lib/Image/reduce'

ImageHelper.save_image_with_quality(image_path, 10, directory_path, image_name+'_reduce')