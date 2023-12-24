import string
import spotify

dict = {
    #what words need to be recognised : command to execute
        "play" : "play",
        "pause" : "spotify.pause",
        "resume" : "spotify.play",
        "go back" : "spotify.previous_track",
        "last" : "spotify.previous_track",
        "next" : "spotify.next_track",
        }


list1 = []
position1 = []

def play():

    string_list = list1
    index = position1

    if string_list and not string_list[-1] == 'play':

        song = ""
        artist = None
        string_list.pop(int(index))

        #removes on spotify if its said at the end
        if len(string_list) > 2:
            if string_list[-2] == 'on' and string_list[-1] == 'spotify':
                string_list = string_list[:-2]

        if string_list[0] == "play":
            string_list.pop(0)
        song_list = string_list

        #parses song and artists title/names around the word "by" (if it exsists)
        if "by" in string_list:
            index1 = string_list.index("by")
            song_list = string_list[:index1]
            artist_list = string_list[index1:]
            index3 = artist_list.index("by")
            artist_list.pop(index3)
            artist = " ".join(artist_list)
            song = " ".join(song_list)
            print("song:" + song)
            print("artist:" + artist)
            spotify.search_play([song, artist])
            return

        song = " ".join(song_list)
        print("query:"+song)
        spotify.search_play([song, None])

    else:
        spotify.play()

def remove_punctuation(input_string):
    # to remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    result_string = input_string.translate(translator)
    return result_string
def run_integrator(string_test, callword):
    string_list = (remove_punctuation(string_test).lower()).split()
    #removes punctuatiuon from text string, makes it all lowercase and puts it into a list

    if callword in string_list:
        position = string_list.index(callword)
        if position + 1 < len(string_list):
            key = string_list[position + 1]
            if key in dict:
                command = dict.get(key)+"()" #gets the command associated with the keyword

                global list1
                global position1
                list1 = string_list
                position1 = position

                eval(command)

                # tells main that a keyword has been found and integrator is executing command
                return 1

            # tells main that no keyword is found but should push text to llm
            return 2

    # tells main text does not contain callword
    return 3