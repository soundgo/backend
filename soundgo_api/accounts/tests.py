from django.test import TestCase

from managers.cloudinary_manager import upload_photo, remove_photo

import requests
import json
from accounts.models import Actor, CreditCard


class AccountsTest(TestCase):



    def get_host(self):
        return "http://127.0.0.1:8000"
        #return "https://soundgo-api-v2.herokuapp.com"

    """
    Test for the Cloudinary functions used in the Accounts module.
    """

    def test_upload_and_remove_photo(self):

        photo = ("data:image/jpeg;base64,/9j/4QAYRXhpZgAASUkqAAgAAAAAAAAAAAAAAP/sABFEdWNreQABAAQAAABQAAD/"
                 "7gAmQWRvYmUAZMAAAAABAwAVBAMGCg0AAAZfAAAJVwAADj0AABIN/9sAhAACAgICAgICAgICAwICAgMEAwICAwQ"
                 "FBAQEBAQFBgUFBQUFBQYGBwcIBwcGCQkKCgkJDAwMDAwMDAwMDAwMDAwMAQMDAwUEBQkGBgkNCwkLDQ8ODg4ODw"
                 "8MDAwMDA8PDAwMDAwMDwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wgARCAEsASwDAREAAhEBAxEB/8QA0"
                 "AABAQEAAgMBAAAAAAAAAAAAAAcGAwQBAgUIAQEAAAAAAAAAAAAAAAAAAAAAEAABBAEDAwMDBQEAAAAAAAADAQIE"
                 "BUAAMBMREhQgMSMQoAZQcCEiNBURAAIBAAQKBQkGBwEAAAAAAAECAwBAEQQwITFBUWGREiIyccFCUiMggdHhYhM"
                 "zUxSx8XKCskMQUHChktJjcxIBAAAAAAAAAAAAAAAAAAAAoBMBAAECBQQBBQACAwAAAAAAAREhMQBAQVFhMHGBka"
                 "Eg8LHB0VCgcOHx/9oADAMBAAIRAxEAAAH9/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                 "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Hg9gAAAAAAAAAAAAAAAehkTHGfOgeDun3zXGzOUAAAAAAAAAAAAAz"
                 "ZJz5IAAAPoFUNcAAAAAAAAAAAAYMlZ6gAAAAFGKYAAAAAAAAAAAYskIAAAAAAKaUUAAAAAAAAAA+cQU4AAAAAAA"
                 "excz7oAAAAAAAAAJMYYAAAAAAAGnLWAAAAAAAAAcB+eTiAAAAAAAAL8fUAAAAAAAABlCMAAAAAAAAAq5uwAAAAA"
                 "AAATwmAAAAAAAAAN+VMAAAAAAAAE0JwAAAAAAAADbFcAAAAAAAABOyYgAAAAAAAA3pVQAAAAAAAAZEjYAAAAAAA"
                 "AKmb8AAAAAAAAHVPz0egAAAAAAABej7AAAAAAAAABHzGgAAAAAAA0JcQAAAAAAAAAfJIOcYAAAAAABbjSAAAAAA"
                 "AAAAGAJYAAAAAAChFQAAAAAAAAAAAJqTcAAAAAG4KwewAAAAAAAAAAAMcSs6QAAAOwU43Z5AAAAAAAAAAAAPQx5"
                 "KzqAAA5inm4OUAAAAAAAAAAAHAT8wJ0gAAAAdk3RRDtgAAAAAAAAAGTJQdAAAAAAAHaKibcAAAAAAAAHgmROwAA"
                 "AAAAAAbcq5yAAAAAAAHgkxhwAAAAAAAAAaoshyAAAAAAAmJOwAAAAAAAAAAbQrp5AAAAABkiNAAAAAAAAAAAAqp"
                 "vQAAAADrkDOiAAAAAAAAAAADmL2fRAAAABNCcAAAAAAAAAAAAA2xXAAAADgPz6dYAAAAAAAAAAAAHsX8+iAAADE"
                 "EkAAAAAAAAAAAAABSikAAAAjJkwAAAAAAAAAAAAAfcLsAAAeD87nWAAAAAAAAAAAAAB5P0OdoAAHyyAgAAAAAAA"
                 "AAAAAAAtxpAAAZwiAAAAAAAAAAAAAAAK+bMA//9oACAEBAAEFAv2r69f0FVRqSLqKLRbuY/T5comvf6MkyB6Fcz"
                 "R6j3kcmmPYRuXNsgw9SpsiWuxHlHiug2wpWVZ2vDpVVV26y2yLaw8Zm9T2PdjSpDYoCEeV+8iq1a+WkyPiXknkN"
                 "gVMnx5WGV6CGR6kfgwzeRFwrknHBwqEndHwvyB3x4VA75sL8g98Kh/2YX5A3+mFQN+fCuh98LCoB9A4RhoYLmqx"
                 "2DAD48TDuo3FJwKyN5MvEmxUlx3Ncx2/WQ/Ej4txX8ib1PX9y49nU7tbVKfSIiJkT6kcnR45oz9gQiGfBpmiy1V"
                 "GpLtK/tM4Tn+pisR0KzrmNY9hEyCEGJsq90aSeQu0IxQrFvXJoJxSG4s61FF1IkmlO3hGKB8G4GfEsbhVw662cD"
                 "TXNe3AtLRTriVtk6I5rmvbvXFj1XGqrHx3btrO8UWRTTuVu2UjQjknfJNkDI4T4shsoG1eyv5yqSVxH2SEaIZiu"
                 "MXKRVasU6SY+xeH442ZQH2bkvJNzK03DN9ftoz+UuaEnKH1TX8cTOqX98D1W3X/AJ+dRdfC+v8A/9oACAECAAEF"
                 "AvtpP//aAAgBAwABBQL7aT//2gAIAQICBj8CNJ//2gAIAQMCBj8CNJ//2gAIAQEBBj8C/pXi/kJLGwDKTQiO2dt"
                 "WJdtODdhGoWn+9OO8SNq3j/HgnkXoY04mWUe0PRZSyZTAdOVaBkYOpyMMdc3fiTZox10tlfhzRjlGB3oXK6RmPS"
                 "KCOTwpswzHorTXe7G2XI8nd9dCSbScpwi3e9NqjmP2Gse4iPjyDGe6MOLpMcf7L9VWeZuzyjSdFGkc2u5tJw4IN"
                 "hGMGiv+4uKUa6qLup4Yeb8RqKgnw5uB+qqPI2SNSx81Hkbmcknz1KGXOy8XSMRqbj5rBOvqqcsXy3tHQ33VO7Jp"
                 "Zjs++pzppQHYfXU7r+fqqcn/AIn9S1O7NoLDbZ6KnO2hLNp9VTLfKYN1ddTnl77bv+P31OSI5JFK0ZWxMpsIqUM"
                 "Z5rLW6TjqnvhyXjH+bPUUBHhx8cnmqrxHmyxtoajIwsZTYwqA3h40vFJ1CrfVQrxr8VdI04cXuYcK/BXSdNYa8X"
                 "VdckI+0YVZ7wLIeyne9VLBiAyCsmSGyKbPobppuTIUObX0YEJEhdjmFBLerJHzR9kemt2sQoGUmhjYfVeyBaNtC"
                 "YYjEvcLb3lgyKXXOoNlBGsf0nmtG2m8jB1PaGOsl5HCKM5oVuiW/wDVuoUtmlZ9RybMHvRSNGdVAt6TfHzVy7Kb"
                 "8Lh11VYxp4s/dzDppvzPvaBmHRh9+JyjaRQR3iyKXM3ZPoqjQXQ2DI8/+tTEN4JeHM+daBlO8rYwRUTBAbIRzv3"
                 "vVVfdycV3bKO7rFAyneVsYIw5ukDYh8dx+mr+4mPgPkPdOG93GfHl5dQ01n6WU+JGPCOldHmwjyubFQWmjzPlbI"
                 "NA0VlZENjIbVNEmXtcw0HPg1uin2peoVs3djwT8v4sE8jcqC0+akkrc0htNbDA2EYwaRTDtjiGvPgVhGWc4+ha7"
                 "Ndjm40+w4FlzQgL1muwNmLbrfmxYC2kknzGLba9FJ8xQ23y7w2iM2V+H2bV2Hy7xZ7P6hXzb8w2bB5H/9oACAEB"
                 "AwE/If8AipQJWDdwCpCbn+BOKaVQBy4orf3H+hxPm2/mJfjFgDdB6mMKqVl3cClSjvjRp0AepxDArSt7kwoPP3k"
                 "qesXA5GD5M4fq7q3L0xZYOn8H96Mhr38QkEeklfl+nNDsBduB9owiZ0pVXqKVIeC5f37zC0HQevr3dMXq9ZKvJW"
                 "1DX+stVnh3W2QT+E4Z4K4lnChT1fr5vld1z5h+j95F42h7jf4cp8N0AnCcyt8qcjapRMV7kn3jUycYMIXuXxk05"
                 "MviD+rJwf8AQmGTRf8Amkyb4/8AhmJNo/Xlk02lP1HJouK+HcnSYWx2E5Nrrg2kv4wUUltko5KN0CP5XqYylOdZ"
                 "wP2vkXmzsEWHlysWR4Qt/MOieTcS/XvQqtjFqEHD/DLM8w6Wl+R+Ou9faX+yGmYaZYf2g/rqtIHVqP8AP5YAAAg"
                 "LBmZdLr+kLPOFGtJsN1Z6NnIxfcYegGp17m7475t5WkqA84pXdRS90HkwmR2oHmB+smL3X5hwuGV5kPJlfOANvC"
                 "g9mZutmeDAnCNP7d/WJBHRKO1h093orie++NjYs+Vj4jAXWpuOEuZajktD7/6xLW+32GnXNHfk4TXFc5pqv7ZNQ"
                 "FWAu42E0XeP69YvVyWj0b39zADwXYRyCgKsBdwi9UB9/wCsqGRduq+yTBjxFmR6+xRah2fv1l2OtK+tr2dffWt4"
                 "FF7/AOczdbUOl+X4dupPyZ+2Lrj+EHbMxfs5hinPDstnTlooiPf7n1m+6FNDb2U9dJg4X2xOLiZ4p08Zuc0wWiW"
                 "xeC7IaD30Zzx+bn5jOyidl9vHRjlkr3/7M7UmPGv0TPQUCmAquFXv7ZOdFERhLOCJ/jJ+vQdkuUg+XP1jed5I+P"
                 "r8Ql2qZ/gXr/0+j//aAAgBAgMBPyH/AFpP/9oACAEDAwE/If8AWk//2gAMAwEAAhEDEQAAEAAAAAAAAAAAAAAAA"
                 "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAI"
                 "JBIIAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAJAAAAAAAAAAABIAAAAAAIAAAAAAAAAAIAAAAAAABAAAAA"
                 "AAAAAAAAAAAAABAAAAAAAAAAIAAAAAAABIAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAA"
                 "AAAIAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAIAAAAAAAAAIAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAA"
                 "AAAAAAAAAAJAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAABIAAAAAAAAAAABAAAAABAAAAAAAAAAAABAAAABAA"
                 "AAAAAAAAAAABAAAAAIAAAAAAAAAAAJAAAAAAABAAAAAAAAABIAAAAAAAABAAAAAAAAAAAAAAAAAABIAAAAAABAA"
                 "AAAAAAAAABAAAAAAJAAAAAAAAAAABAAAAAAIAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAIAAAAIAAAAAAAAAAAAAJ"
                 "AAAAAAAAAAAAAAAAAABAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAABAAAAAAAAAAAAAAAAAAAAAAAAAA"
                 "AAAAAAAAAAP/9oACAEBAwE/EP8AipEIrpAecFaFSCfH+BVp4QJdSAMNjo8uB5BnuDCLVUhwcx55Bh1nl7l2IHrD"
                 "xTXSX24QEQqCiYiY2gjzZEHFvBo9HvOWcQTqItbkD4nOBTbJfZImcc0kkYrKVMeIl2iuEq6yZtInV5k89EC8Iyw"
                 "TRKP5NExGu9Plqy9zZc0gCE1RddN3Nu6z4BPqDKq1VemKIjCWcIpuEJdAq5s7cKmXIVQKrRQ29QrthVKKrKt16x"
                 "NDZtSXnUPSm05WliilhpC7t9iXDvmn6robAUDQ66XjjhCQSyOCJISUgLTY0eTTKrPR0rSnzh3cilOMDYb5WJ2XK"
                 "WVodVCDljHLE1mL5ciKhFEiURMTjAi7ny2TSXEheGF5QyaQkJbUJ7GTeco4c5NjyVHDtZMnDpT7zk8qNqmTFh6g"
                 "eSPyyaQNWPJmTPKnLpFftk3gCWutSOJeTjkFyrJg8lcKVRq60PCZJYJlVx0Xu9GUQ44LFoYfh3LtkZBVFSpxXxk"
                 "bTtlaEClaFn2ZVwuKBNCE4D2TrgoBRAVVcCKsC3p+G15XLWVS+o6ELiV37K9aBXEG1rHU8mulcuKqAVU1C01fTb"
                 "qunQnodRdeS+ilcAvIAACAAoAZlSYJYhvYNh3HFaEkEk0Mh2ejqB/pjdbA1Whih71WN5bY2iHtgAACAsZo/wAcC"
                 "NuqAwkOlBxoZ+xLh2z1Adi9xe/1vNGZDxtzsYoRicYmeuSYum2s9kTM22V5JoE3XQKuGzWTBTuoLwowi6TNYOKP"
                 "EdMHSiXoaAoOEwsVRQh80/sBw9PQIqtZcJwhlouhQ1jw6myu8YWgq6DdBp+TrPXpTtkoN1IOETCVEpmNNVubNHR"
                 "0yYJjqjABdXDKIyjGipoe77KqUVWVbrkkKQnSSxye1zTbBgqrAyREuOQBMdUYALq4QORmFlwft2ZXVYTkmo7ey5"
                 "W6LpmkaRE366xYyxauhoe7wZyzmadtHatG8HukRBGRs9WICKDW1wOnKumFVVVVlXXMONUCagqnULb9zqbs5wiwD"
                 "VWgb4cOJ8khU4gpzfMpZHDRJruNk1MQOUcstIvZtuQ9N6HstdXOxWZskY2ioSz/ANj0ki7/AKyEHLFMJzIZMkkg"
                 "4FDjNtip4lUo5ExHwAQt8RBjjotYERel7n886ks0OdGAOJn5ei8Iuy0yTvMXtnUajW3rHhDw6BkhqrAVXEq8hHS"
                 "eHic6iZYhREsmLQ0IaIo8L9blsJ2n/GZ9XqS8Nj4fXy/7DbZ/7V+X8vo//9oACAECAwE/EP8AWk//2gAIAQMDAT"
                 "8Q/wBaT//Z")

        url = upload_photo(photo)

        self.assertFalse(url == "")

        res = remove_photo(url)

        self.assertTrue(res)


    #Test cases
    def test_crud_account(self):

        #Create account
        account= self.create_account({"nickname": "manolo345", "password": "ventana76", "email": "manolo@gmail.com"}, 201)

        #Update account
        self.update_account({"nickname": "manolo346", "password": "ventana76"}, 200, "manolo345", "ventana76", True)

        self.update_account({"base64": "data:image/jpeg;base64,/9j/4QAYRXhpZgAASUkqAAgAAAAAAAAAAAAAAP/sABFEdWNreQABAAQAAABQAAD/"
                 "7gAmQWRvYmUAZMAAAAABAwAVBAMGCg0AAAZfAAAJVwAADj0AABIN/9sAhAACAgICAgICAgICAwICAgMEAwICAwQ"
                 "FBAQEBAQFBgUFBQUFBQYGBwcIBwcGCQkKCgkJDAwMDAwMDAwMDAwMDAwMAQMDAwUEBQkGBgkNCwkLDQ8ODg4ODw"
                 "8MDAwMDA8PDAwMDAwMDwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wgARCAEsASwDAREAAhEBAxEB/8QA0"
                 "AABAQEAAgMBAAAAAAAAAAAAAAcGAwQBAgUIAQEAAAAAAAAAAAAAAAAAAAAAEAABBAEDAwMDBQEAAAAAAAADAQIE"
                 "BUAAMBMREhQgMSMQoAZQcCEiNBURAAIBAAQKBQkGBwEAAAAAAAECAwBAEQQwITFBUWGREiIyccFCUiMggdHhYhM"
                 "zUxSx8XKCskMQUHChktJjcxIBAAAAAAAAAAAAAAAAAAAAoBMBAAECBQQBBQACAwAAAAAAAREhMQBAQVFhMHGBka"
                 "Eg8LHB0VCgcOHx/9oADAMBAAIRAxEAAAH9/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                 "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Hg9gAAAAAAAAAAAAAAAehkTHGfOgeDun3zXGzOUAAAAAAAAAAAAAz"
                 "ZJz5IAAAPoFUNcAAAAAAAAAAAAYMlZ6gAAAAFGKYAAAAAAAAAAAYskIAAAAAAKaUUAAAAAAAAAA+cQU4AAAAAAA"
                 "excz7oAAAAAAAAAJMYYAAAAAAAGnLWAAAAAAAAAcB+eTiAAAAAAAAL8fUAAAAAAAABlCMAAAAAAAAAq5uwAAAAA"
                 "AAATwmAAAAAAAAAN+VMAAAAAAAAE0JwAAAAAAAADbFcAAAAAAAABOyYgAAAAAAAA3pVQAAAAAAAAZEjYAAAAAAA"
                 "AKmb8AAAAAAAAHVPz0egAAAAAAABej7AAAAAAAAABHzGgAAAAAAA0JcQAAAAAAAAAfJIOcYAAAAAABbjSAAAAAA"
                 "AAAAGAJYAAAAAAChFQAAAAAAAAAAAJqTcAAAAAG4KwewAAAAAAAAAAAMcSs6QAAAOwU43Z5AAAAAAAAAAAAPQx5"
                 "KzqAAA5inm4OUAAAAAAAAAAAHAT8wJ0gAAAAdk3RRDtgAAAAAAAAAGTJQdAAAAAAAHaKibcAAAAAAAAHgmROwAA"
                 "AAAAAAbcq5yAAAAAAAHgkxhwAAAAAAAAAaoshyAAAAAAAmJOwAAAAAAAAAAbQrp5AAAAABkiNAAAAAAAAAAAAqp"
                 "vQAAAADrkDOiAAAAAAAAAAADmL2fRAAAABNCcAAAAAAAAAAAAA2xXAAAADgPz6dYAAAAAAAAAAAAHsX8+iAAADE"
                 "EkAAAAAAAAAAAAABSikAAAAjJkwAAAAAAAAAAAAAfcLsAAAeD87nWAAAAAAAAAAAAAB5P0OdoAAHyyAgAAAAAAA"
                 "AAAAAAAtxpAAAZwiAAAAAAAAAAAAAAAK+bMA//9oACAEBAAEFAv2r69f0FVRqSLqKLRbuY/T5comvf6MkyB6Fcz"
                 "R6j3kcmmPYRuXNsgw9SpsiWuxHlHiug2wpWVZ2vDpVVV26y2yLaw8Zm9T2PdjSpDYoCEeV+8iq1a+WkyPiXknkN"
                 "gVMnx5WGV6CGR6kfgwzeRFwrknHBwqEndHwvyB3x4VA75sL8g98Kh/2YX5A3+mFQN+fCuh98LCoB9A4RhoYLmqx"
                 "2DAD48TDuo3FJwKyN5MvEmxUlx3Ncx2/WQ/Ej4txX8ib1PX9y49nU7tbVKfSIiJkT6kcnR45oz9gQiGfBpmiy1V"
                 "GpLtK/tM4Tn+pisR0KzrmNY9hEyCEGJsq90aSeQu0IxQrFvXJoJxSG4s61FF1IkmlO3hGKB8G4GfEsbhVw662cD"
                 "TXNe3AtLRTriVtk6I5rmvbvXFj1XGqrHx3btrO8UWRTTuVu2UjQjknfJNkDI4T4shsoG1eyv5yqSVxH2SEaIZiu"
                 "MXKRVasU6SY+xeH442ZQH2bkvJNzK03DN9ftoz+UuaEnKH1TX8cTOqX98D1W3X/AJ+dRdfC+v8A/9oACAECAAEF"
                 "AvtpP//aAAgBAwABBQL7aT//2gAIAQICBj8CNJ//2gAIAQMCBj8CNJ//2gAIAQEBBj8C/pXi/kJLGwDKTQiO2dt"
                 "WJdtODdhGoWn+9OO8SNq3j/HgnkXoY04mWUe0PRZSyZTAdOVaBkYOpyMMdc3fiTZox10tlfhzRjlGB3oXK6RmPS"
                 "KCOTwpswzHorTXe7G2XI8nd9dCSbScpwi3e9NqjmP2Gse4iPjyDGe6MOLpMcf7L9VWeZuzyjSdFGkc2u5tJw4IN"
                 "hGMGiv+4uKUa6qLup4Yeb8RqKgnw5uB+qqPI2SNSx81Hkbmcknz1KGXOy8XSMRqbj5rBOvqqcsXy3tHQ33VO7Jp"
                 "Zjs++pzppQHYfXU7r+fqqcn/AIn9S1O7NoLDbZ6KnO2hLNp9VTLfKYN1ddTnl77bv+P31OSI5JFK0ZWxMpsIqUM"
                 "Z5rLW6TjqnvhyXjH+bPUUBHhx8cnmqrxHmyxtoajIwsZTYwqA3h40vFJ1CrfVQrxr8VdI04cXuYcK/BXSdNYa8X"
                 "VdckI+0YVZ7wLIeyne9VLBiAyCsmSGyKbPobppuTIUObX0YEJEhdjmFBLerJHzR9kemt2sQoGUmhjYfVeyBaNtC"
                 "YYjEvcLb3lgyKXXOoNlBGsf0nmtG2m8jB1PaGOsl5HCKM5oVuiW/wDVuoUtmlZ9RybMHvRSNGdVAt6TfHzVy7Kb"
                 "8Lh11VYxp4s/dzDppvzPvaBmHRh9+JyjaRQR3iyKXM3ZPoqjQXQ2DI8/+tTEN4JeHM+daBlO8rYwRUTBAbIRzv3"
                 "vVVfdycV3bKO7rFAyneVsYIw5ukDYh8dx+mr+4mPgPkPdOG93GfHl5dQ01n6WU+JGPCOldHmwjyubFQWmjzPlbI"
                 "NA0VlZENjIbVNEmXtcw0HPg1uin2peoVs3djwT8v4sE8jcqC0+akkrc0htNbDA2EYwaRTDtjiGvPgVhGWc4+ha7"
                 "Ndjm40+w4FlzQgL1muwNmLbrfmxYC2kknzGLba9FJ8xQ23y7w2iM2V+H2bV2Hy7xZ7P6hXzb8w2bB5H/9oACAEB"
                 "AwE/If8AipQJWDdwCpCbn+BOKaVQBy4orf3H+hxPm2/mJfjFgDdB6mMKqVl3cClSjvjRp0AepxDArSt7kwoPP3k"
                 "qesXA5GD5M4fq7q3L0xZYOn8H96Mhr38QkEeklfl+nNDsBduB9owiZ0pVXqKVIeC5f37zC0HQevr3dMXq9ZKvJW"
                 "1DX+stVnh3W2QT+E4Z4K4lnChT1fr5vld1z5h+j95F42h7jf4cp8N0AnCcyt8qcjapRMV7kn3jUycYMIXuXxk05"
                 "MviD+rJwf8AQmGTRf8Amkyb4/8AhmJNo/Xlk02lP1HJouK+HcnSYWx2E5Nrrg2kv4wUUltko5KN0CP5XqYylOdZ"
                 "wP2vkXmzsEWHlysWR4Qt/MOieTcS/XvQqtjFqEHD/DLM8w6Wl+R+Ou9faX+yGmYaZYf2g/rqtIHVqP8AP5YAAAg"
                 "LBmZdLr+kLPOFGtJsN1Z6NnIxfcYegGp17m7475t5WkqA84pXdRS90HkwmR2oHmB+smL3X5hwuGV5kPJlfOANvC"
                 "g9mZutmeDAnCNP7d/WJBHRKO1h093orie++NjYs+Vj4jAXWpuOEuZajktD7/6xLW+32GnXNHfk4TXFc5pqv7ZNQ"
                 "FWAu42E0XeP69YvVyWj0b39zADwXYRyCgKsBdwi9UB9/wCsqGRduq+yTBjxFmR6+xRah2fv1l2OtK+tr2dffWt4"
                 "FF7/AOczdbUOl+X4dupPyZ+2Lrj+EHbMxfs5hinPDstnTlooiPf7n1m+6FNDb2U9dJg4X2xOLiZ4p08Zuc0wWiW"
                 "xeC7IaD30Zzx+bn5jOyidl9vHRjlkr3/7M7UmPGv0TPQUCmAquFXv7ZOdFERhLOCJ/jJ+vQdkuUg+XP1jed5I+P"
                 "r8Ql2qZ/gXr/0+j//aAAgBAgMBPyH/AFpP/9oACAEDAwE/If8AWk//2gAMAwEAAhEDEQAAEAAAAAAAAAAAAAAAA"
                 "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAI"
                 "JBIIAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAJAAAAAAAAAAABIAAAAAAIAAAAAAAAAAIAAAAAAABAAAAA"
                 "AAAAAAAAAAAAABAAAAAAAAAAIAAAAAAABIAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAA"
                 "AAAIAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAIAAAAAAAAAIAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAA"
                 "AAAAAAAAAAJAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAABIAAAAAAAAAAABAAAAABAAAAAAAAAAAABAAAABAA"
                 "AAAAAAAAAAABAAAAAIAAAAAAAAAAAJAAAAAAABAAAAAAAAABIAAAAAAAABAAAAAAAAAAAAAAAAAABIAAAAAABAA"
                 "AAAAAAAAABAAAAAAJAAAAAAAAAAABAAAAAAIAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAIAAAAIAAAAAAAAAAAAAJ"
                 "AAAAAAAAAAAAAAAAAABAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAABAAAAAAAAAAAAAAAAAAAAAAAAAA"
                 "AAAAAAAAAAP/9oACAEBAwE/EP8AipEIrpAecFaFSCfH+BVp4QJdSAMNjo8uB5BnuDCLVUhwcx55Bh1nl7l2IHrD"
                 "xTXSX24QEQqCiYiY2gjzZEHFvBo9HvOWcQTqItbkD4nOBTbJfZImcc0kkYrKVMeIl2iuEq6yZtInV5k89EC8Iyw"
                 "TRKP5NExGu9Plqy9zZc0gCE1RddN3Nu6z4BPqDKq1VemKIjCWcIpuEJdAq5s7cKmXIVQKrRQ29QrthVKKrKt16x"
                 "NDZtSXnUPSm05WliilhpC7t9iXDvmn6robAUDQ66XjjhCQSyOCJISUgLTY0eTTKrPR0rSnzh3cilOMDYb5WJ2XK"
                 "WVodVCDljHLE1mL5ciKhFEiURMTjAi7ny2TSXEheGF5QyaQkJbUJ7GTeco4c5NjyVHDtZMnDpT7zk8qNqmTFh6g"
                 "eSPyyaQNWPJmTPKnLpFftk3gCWutSOJeTjkFyrJg8lcKVRq60PCZJYJlVx0Xu9GUQ44LFoYfh3LtkZBVFSpxXxk"
                 "bTtlaEClaFn2ZVwuKBNCE4D2TrgoBRAVVcCKsC3p+G15XLWVS+o6ELiV37K9aBXEG1rHU8mulcuKqAVU1C01fTb"
                 "qunQnodRdeS+ilcAvIAACAAoAZlSYJYhvYNh3HFaEkEk0Mh2ejqB/pjdbA1Whih71WN5bY2iHtgAACAsZo/wAcC"
                 "NuqAwkOlBxoZ+xLh2z1Adi9xe/1vNGZDxtzsYoRicYmeuSYum2s9kTM22V5JoE3XQKuGzWTBTuoLwowi6TNYOKP"
                 "EdMHSiXoaAoOEwsVRQh80/sBw9PQIqtZcJwhlouhQ1jw6myu8YWgq6DdBp+TrPXpTtkoN1IOETCVEpmNNVubNHR"
                 "0yYJjqjABdXDKIyjGipoe77KqUVWVbrkkKQnSSxye1zTbBgqrAyREuOQBMdUYALq4QORmFlwft2ZXVYTkmo7ey5"
                 "W6LpmkaRE366xYyxauhoe7wZyzmadtHatG8HukRBGRs9WICKDW1wOnKumFVVVVlXXMONUCagqnULb9zqbs5wiwD"
                 "VWgb4cOJ8khU4gpzfMpZHDRJruNk1MQOUcstIvZtuQ9N6HstdXOxWZskY2ioSz/ANj0ki7/AKyEHLFMJzIZMkkg"
                 "4FDjNtip4lUo5ExHwAQt8RBjjotYERel7n886ks0OdGAOJn5ei8Iuy0yTvMXtnUajW3rHhDw6BkhqrAVXEq8hHS"
                 "eHic6iZYhREsmLQ0IaIo8L9blsJ2n/GZ9XqS8Nj4fXy/7DbZ/7V+X8vo//9oACAECAwE/EP8AWk//2gAIAQMDAT"
                 "8Q/wBaT//Z"}, 200, "manolo346", "ventana76", True)

        #Get account
        self.get_account(200, "manolo346", "ventana76", True)

        #Delete account
        self.delete_account(204, "manolo346", "ventana76", True)

        #account deleted can not get again
        self.get_account(400, "manolo346", "ventana76", False)

        #account deleted can not delete again
        self.delete_account(400, "manolo346", "ventana76", False)

        #account deleted can not update again
        self.update_account({"nickname": "manolo346", "password": "ventana76"}, 400, "manolo346", "ventana76", False)

    #########


    #Auxiliary methods
    def create_account(self, object, code):

        headers = {'content-type': 'application/json'}
        body = json.dumps(object)

        r = requests.post(self.get_host() + '/accounts/actor/', data=body, headers=headers)


        self.assertTrue(r.status_code == code)

        return r.json()


    def update_account(self, object, code, username, password, useToken):

        if useToken:
            token = self.get_token(username,password)

            headers = {'content-type': 'application/json', 'Authorization': "Bearer " + token}
        else:
            headers = {'content-type': 'application/json'}

        body = json.dumps(object)

        r = requests.put(self.get_host() + '/accounts/actor/'+str(username)+"/", data=body, headers=headers)



        self.assertTrue(r.status_code == code)


        return r.json()


    def delete_account(self, code, username, password, useToken):

        if useToken:
            token = self.get_token(username, password)

            headers = {'content-type': 'application/json', 'Authorization': "Bearer " + token}
        else:
            headers = {'content-type': 'application/json'}

        r = requests.delete(self.get_host() + '/accounts/actor/'+str(username)+"/", headers=headers)


        self.assertTrue(r.status_code == code)


    def get_account(self, code, username, password, useToken):

        if useToken:
            token = self.get_token(username, password)

            headers = {'content-type': 'application/json', 'Authorization': "Bearer " + token}
        else:
            headers = {'content-type': 'application/json'}

        r = requests.get(self.get_host() + '/accounts/actor/' + str(username) + "/", headers=headers)


        self.assertTrue(r.status_code == code)


    # Test cases
    def test_crud_credit_card(self):

        account = self.create_account({"nickname": "manolo345", "password": "ventana76", "email": "manolo@gmail.com"},
                                      201)

        # Create credit card
        creditCard = self.create_credit_card({"number": "4194196013034073", "brandName": "unknown", "holderName": "Efrain Smith", "expirationMonth": 12, "expirationYear":22, "cvvCode":277},
                                      201, "manolo345", "ventana76")

        # Update credit card
        self.update_credit_card({"number": "4194196013034073", "brandName": "unknown", "holderName": "Carlos Mallado", "expirationMonth": 12, "expirationYear":22, "cvvCode":277}, 200, "manolo345", "ventana76", creditCard['id'])

        # Get credit_card
        self.get_credit_card(200, "manolo345", "ventana76", creditCard['id'])

        # Update credit card
        self.update_credit_card({"number": "4194196013034073", "brandName": "unknown", "holderName": "Efrain Smith", "expirationMonth": 12, "expirationYear":22, "cvvCode":277, "isDelete": True}, 200, "manolo345", "ventana76", creditCard['id'])


        # credit_card deleted can not update again
        self.update_credit_card({"number": "4194196013034073", "brandName": "unknown", "holderName": "Carlos Mallado",
                                 "expirationMonth": 12, "expirationYear": 22, "cvvCode": 277}, 200, "manolo345", "ventana76", creditCard['id'])

        # Delete account
        self.delete_account(204, "manolo345", "ventana76", True)

    def get_credit_card(self, code, username, password, id):


        token = self.get_token(username, password)

        headers = {'content-type': 'application/json', 'Authorization': "Bearer " + token}

        r = requests.get(self.get_host() + '/accounts/creditcard/' + str(id) + "/", headers=headers)


        self.assertTrue(r.status_code == code)


    def create_credit_card(self, object, code, username, password):

        token = self.get_token(username, password)

        headers = {'content-type': 'application/json', 'Authorization': "Bearer " + token}
        body = json.dumps(object)

        r = requests.post(self.get_host() + '/accounts/creditcard/', data=body, headers=headers)


        self.assertTrue(r.status_code == code)

        return r.json()


    def update_credit_card(self, object, code, username, password, id):


        token = self.get_token(username,password)

        headers = {'content-type': 'application/json', 'Authorization': "Bearer " + token}


        body = json.dumps(object)

        r = requests.put(self.get_host() + '/accounts/creditcard/'+str(id)+"/", data=body, headers=headers)


        self.assertTrue(r.status_code == code)


        return r.json()




    def get_token(self, username, password):
        headers = {'content-type': 'application/json'}
        body = json.dumps({"nickname": username, "password": password})

        r = requests.post(self.get_host() + '/api-token-auth/', data=body, headers=headers)

        return r.json()['token']

