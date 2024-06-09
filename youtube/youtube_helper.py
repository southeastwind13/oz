from pytube import YouTube

class YoutubeHelper():
    '''
    Download mp4 file from the Youtube link

    :param str link: The url of the Youtube link.
    :param str filepath: The path to save the file.
    :param str filename: The name of the file.
    '''
    @staticmethod
    def save_file(link:str, filepath:str, filename:str):
        yt = YouTube(link)
        yt = yt.streams.get_highest_resolution()
        try:
            file = yt.streams.filter(progressive=True, file_extension="mp4").first()
            file.download(output_path=filepath, filename=f'{filename}.mp4')
        except Exception as e: 
            print(f"Error: {e}")