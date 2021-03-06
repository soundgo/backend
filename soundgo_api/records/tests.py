from django.test import TestCase

from rest_framework.test import APIRequestFactory

import json

from records.models import Category
from configuration.models import Configuration

from accounts.models import UserAccount, Actor, CreditCard
from accounts.views import get_token

from .views import (audio_create, audio_delete_get_update, audio_site_category_get, audio_listen, report_create,
                    like_create, advertisement_create, advertisement_update_get, advertisement_listen,
                    audio_site_create)

from sites.views import site_update_delete_get, site_create

from managers.cloudinary_manager import upload_record, get_record_duration, remove_record


class CloudinaryTest(TestCase):

    """
    Test for the Cloudinary functions used in the Records module.
    """

    def get_record(self):
        record = ("data:audio/ogg;base64,T2dnUwACAAAAAAAAAAA+HAAAAAAAAGyawCEBQGZpc2hlYWQAAwAAAAAAAAAAAAAA6AMAAAAAAAAAAA"
                  "AAAAAAAOgDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABPZ2dTAAIAAAAAAAAAAINDAAAAAAAA9LkergEeAXZvcmJpcwAAAAACRK"
                  "wAAAAAAAAA7gIAAAAAALgBT2dnUwAAAAAAAAAAAAA+HAAAAQAAAPvOJxcBUGZpc2JvbmUALAAAAINDAAADAAAARKwAAAAAAAABAA"
                  "AAAAAAAAAAAAAAAAAAAgAAAAAAAABDb250ZW50LVR5cGU6IGF1ZGlvL3ZvcmJpcw0KT2dnUwAAAAAAAAAAAACDQwAAAQAAAGLSAC"
                  "4Qdv//////////////////cQN2b3JiaXMdAAAAWGlwaC5PcmcgbGliVm9yYmlzIEkgMjAwOTA3MDkCAAAAIwAAAEVOQ09ERVI9Zm"
                  "ZtcGVnMnRoZW9yYS0wLjI2K3N2bjE2OTI0HgAAAFNPVVJDRV9PU0hBU0g9ODExM2FhYWI5YzFiNjhhNwEFdm9yYmlzK0JDVgEACA"
                  "AAADFMIMWA0JBVAAAQAABgJCkOk2ZJKaWUoSh5mJRISSmllMUwiZiUicUYY4wxxhhjjDHGGGOMIDRkFQAABACAKAmOo+ZJas45Zx"
                  "gnjnKgOWlOOKcgB4pR4DkJwvUmY26mtKZrbs4pJQgNWQUAAAIAQEghhRRSSCGFFGKIIYYYYoghhxxyyCGnnHIKKqigggoyyCCDTD"
                  "LppJNOOumoo4466ii00EILLbTSSkwx1VZjrr0GXXxzzjnnnHPOOeecc84JQkNWAQAgAAAEQgYZZBBCCCGFFFKIKaaYcgoyyIDQkF"
                  "UAACAAgAAAAABHkRRJsRTLsRzN0SRP8ixREzXRM0VTVE1VVVVVdV1XdmXXdnXXdn1ZmIVbuH1ZuIVb2IVd94VhGIZhGIZhGIZh+H"
                  "3f933f930gNGQVACABAKAjOZbjKaIiGqLiOaIDhIasAgBkAAAEACAJkiIpkqNJpmZqrmmbtmirtm3LsizLsgyEhqwCAAABAAQAAA"
                  "AAAKBpmqZpmqZpmqZpmqZpmqZpmqZpmmZZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZlmVZQGjIKgBAAgBAx3Ecx3"
                  "EkRVIkx3IsBwgNWQUAyAAACABAUizFcjRHczTHczzHczxHdETJlEzN9EwPCA1ZBQAAAgAIAAAAAABAMRzFcRzJ0SRPUi3TcjVXcz"
                  "3Xc03XdV1XVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVYHQkFUAAAQAACGdZpZqgAgzkGEgNGQVAIAAAAAYoQhDDA"
                  "gNWQUAAAQAAIih5CCa0JrzzTkOmuWgqRSb08GJVJsnuamYm3POOeecbM4Z45xzzinKmcWgmdCac85JDJqloJnQmnPOeRKbB62p0p"
                  "pzzhnnnA7GGWGcc85p0poHqdlYm3POWdCa5qi5FJtzzomUmye1uVSbc84555xzzjnnnHPOqV6czsE54Zxzzonam2u5CV2cc875ZJ"
                  "zuzQnhnHPOOeecc84555xzzglCQ1YBAEAAAARh2BjGnYIgfY4GYhQhpiGTHnSPDpOgMcgppB6NjkZKqYNQUhknpXSC0JBVAAAgAA"
                  "CEEFJIIYUUUkghhRRSSCGGGGKIIaeccgoqqKSSiirKKLPMMssss8wyy6zDzjrrsMMQQwwxtNJKLDXVVmONteaec645SGultdZaK6"
                  "WUUkoppSA0ZBUAAAIAQCBkkEEGGYUUUkghhphyyimnoIIKCA1ZBQAAAgAIAAAA8CTPER3RER3RER3RER3RER3P8RxREiVREiXRMi"
                  "1TMz1VVFVXdm1Zl3Xbt4Vd2HXf133f141fF4ZlWZZlWZZlWZZlWZZlWZZlCUJDVgEAIAAAAEIIIYQUUkghhZRijDHHnINOQgmB0J"
                  "BVAAAgAIAAAAAAR3EUx5EcyZEkS7IkTdIszfI0T/M00RNFUTRNUxVd0RV10xZlUzZd0zVl01Vl1XZl2bZlW7d9WbZ93/d93/d93/"
                  "d93/d939d1IDRkFQAgAQCgIzmSIimSIjmO40iSBISGrAIAZAAABACgKI7iOI4jSZIkWZImeZZniZqpmZ7pqaIKhIasAgAAAQAEAA"
                  "AAAACgaIqnmIqniIrniI4oiZZpiZqquaJsyq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7ruq7rukBoyCoAQAIAQEdyJE"
                  "dyJEVSJEVyJAcIDVkFAMgAAAgAwDEcQ1Ikx7IsTfM0T/M00RM90TM9VXRFFwgNWQUAAAIACAAAAAAAwJAMS7EczdEkUVIt1VI11V"
                  "ItVVQ9VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV1TRN0zSB0JCVAAAZAAACKcWahFCSQU5K7EVpxiAHrQblKYQYk9"
                  "iL6ZhCyFFQKmQMGeRAydQxhhDzYmOnFELMi/Glc4xBL8a4UkIowQhCQ1YEAFEAAAZJIkkkSfI0okj0JM0jijwRgCR6PI/nSZ7I83"
                  "geAEkUeR7Pk0SR5/E8AQAAAQ4AAAEWQqEhKwKAOAEAiyR5HknyPJLkeTRNFCGKkqaJIs8zTZ5mikxTVaGqkqaJIs8zTZonmkxTVa"
                  "GqniiqKlV1XarpumTbtmHLniiqKlV1XabqumzZtiHbAAAAJE9TTZpmmjTNNImiakJVJc0zVZpmmjTNNImiqUJVPVN0XabpukzTdb"
                  "muLEOWPdF0XaapukzTdbmuLEOWAQAASJ6nqjTNNGmaaRJFU4VqSp6nqjTNNGmaaRJFVYWpeqbpukzTdZmm63JlWYYte6bpukzTdZ"
                  "mm65JdWYYsAwAA0EzTlomi7BJF12WargvX1UxTtomiKxNF12WargvXFVXVlqmmLVNVWea6sgxZFlVVtpmqbFNVWea6sgxZBgAAAA"
                  "AAAAAAgKiqtk1VZZlqyjLXlWXIsqiqtk1VZZmpyjLXtWXIsgAAgAEHAIAAE8pAoSErAYAoAACH4liWpokix7EsTRNNjmNZmmaKJE"
                  "nTPM80oVmeZ5rQNFFUVWiaKKoqAAACAAAKHAAAAmzQlFgcoNCQlQBASACAw3EsS9M8z/NEUTRNk+NYlueJoiiapmmqKsexLM8TRV"
                  "E0TdNUVZalaZ4niqJomqqqqtA0zxNFUTRNVVVVaJoomqZpqqqqui40TRRN0zRVVVVdF5rmeaJomqrquq4LPE8UTVNVXdd1AQAAAA"
                  "AAAAAAAAAAAAAAAAAEAAAcOAAABBhBJxlVFmGjCRcegEJDVgQAUQAAgDGIMcWYUQpCKSU0SkEJJZQKQmmppJRJSK211jIpqbXWWi"
                  "WltJZay6Ck1lprmYTWWmutAACwAwcAsAMLodCQlQBAHgAAgoxSjDnnHDVGKcacc44aoxRjzjlHlVLKOecgpJQqxZxzDlJKGXPOOe"
                  "copYw555xzlFLnnHPOOUqplM455xylVErnnHOOUiolY845JwAAqMABACDARpHNCUaCCg1ZCQCkAgAYHMeyPM/zTNE0LUnSNFEURd"
                  "NUVUuSNE0UTVE1VZVlaZoomqaqui5N0zRRNE1VdV2q6nmmqaqu67pUV/RMU1VdV5YBAAAAAAAAAAAAAQDgCQ4AQAU2rI5wUjQWWG"
                  "jISgAgAwAAMQYhZAxCyBiEFEIIKaUQEgAAMOAAABBgQhkoNGQlAJAKAAAYo5RzzklJpUKIMecglNJShRBjzkEopaWoMcYglJJSa1"
                  "FjjEEoJaXWomshlJJSSq1F10IoJaXWWotSqlRKaq3FGKVUqZTWWosxSqlzSq3FGGOUUveUWoux1iildDLGGGOtzTnnZIwxxloLAE"
                  "BocAAAO7BhdYSTorHAQkNWAgB5AAAIQkoxxhhjECGlGGPMMYeQUowxxhhUijHGHGMOQsgYY4wxByFkjDHnnIMQMsYYY85BCJ1zjj"
                  "HnIITQOceYcxBC55xjzDkIoXOMMeacAACgAgcAgAAbRTYnGAkqNGQlABAOAAAYw5hzjDkGnYQKIecgdA5CKqlUCDkHoXMQSkmpeA"
                  "46KSGUUkoqxXMQSgmhlJRaKy6GUkoopaTUUpExhFJKKSWl1ooxpoSQUkqptVaMMaGEVFJKKbZijI2lpNRaa60VY2wsJZXWWmutGG"
                  "OMaym1FmOsxRhjXEuppRhrLMYY43tqLcZYYzHGGJ9baimmXAsAMHlwAIBKsHGGlaSzwtHgQkNWAgC5AQAIQkoxxphjzjnnnHPOSa"
                  "UYc8455yCEEEIIIZRKMeacc85BByGEEEIoGXPOOQchhBBCCCGEUFLqmHMOQgghhBBCCCGl1DnnIIQQQgghhBBCSqlzzkEIIYQQQg"
                  "ghhJRSCCGEEEIIIYQQQggppZRCCCGEEEIIIZQSUkophRBCCCWEEkoIJaSUUgohhBBCKaWEUkJJKaUUQgillFBKKaGUkFJKKaUQQi"
                  "illFBKKSWllFJKJZRSSikllFBKSimllEoooZRQSimllJRSSimVUkopJZRSSgkppZRSSqmUUkoppZRSUkoppZRSKaWUUkoppaSUUk"
                  "oppVJKKaWUEkpJKaWUUkqllFBKKaWUUlJKKaWUSgqllFJKKaUAAKADBwCAACMqLcROM648AkcUMkxAhYasBABSAQAAQiillFJKKT"
                  "WMUUoppZRSihyklFJKKaWUUkoppZRSSimVUkoppZRSSimllFJKKaWUUkoppZRSSimllFJKKaWUUkoppZRSSimllFJKKaWUUkoppZ"
                  "RSSimllFJKKaWUUkoppZRSSimllFJKAcDdFw6APhM2rI5wUjQWWGjISgAgFQAAMIYxxphyzjmllHPOOQadlEgp5yB0TkopPYQQQg"
                  "idhJR6ByGEEEIpKfUYQyghlJRS67GGTjoIpbTUaw8hhJRaaqn3HjKoKKWSUu89tVBSainG3ntLJbPSWmu9595LKinG2nrvObeSUk"
                  "wtFgBgEuEAgLhgw+oIJ0VjgYWGrAIAYgAACEMMQkgppZRSSinGGGOMMcYYY4wxxhhjjDHGGGOMMQEAgAkOAAABVrArs7Rqo7ipk7"
                  "zog8AndMRmZMilVMzkRNAjNdRiJdihFdzgBWChISsBADIAAMRRrDXGXitiGISSaiwNQYxBibllxijlJObWKaWUk1hTyJRSzFmKJX"
                  "RMKUYpphJCxpSkGGOMKXTSWs49t1RKCwAAgCAAwECEzAQCBVBgIAMADhASpACAwgJDx3AREJBLyCgwKBwTzkmnDQBAECIzRCJiMU"
                  "hMqAaKiukAYHGBIR8AMjQ20i4uoMsAF3Rx14EQghCEIBYHUEACDk644Yk3POEGJ+gUlToQAAAAAAAIAHgAAEg2gIhoZuY4Ojw+QE"
                  "JERkhKTE5QUlQEAAAAAAAQAD4AAJIVICKamTmODo8PkBCREZISkxOUFJUAAEAAAQAAAAAQQAACAgIAAAAAAAEAAAACAk9nZ1MABA"
                  "AAAAAAAAAAPhwAAAIAAADItsciAQBPZ2dTAABAKgAAAAAAAINDAAACAAAAi/k29xgB/4b/av9h/0j/Wv9g/1r/UP9l/1//Wv8A2j"
                  "Wsrb6NXUc1CJ0sSdewtPbGlo1NaJI8UVTVUGRZipC555WVlSnnZVlZWVlZljm1c+zimE1lYRMrAAAAAEGChIyc4DjOGcNecpzj3e"
                  "5eskWraU5OsZ1ma2tra+/QoUNbkyPMXUZO1Skw1yh8+fLly+84juMURSFhhhyPx1EDqAmLBR0xchzH8XgcYYYknU5HIoc//F1uAO"
                  "a6rplb8brWAjo6AuBaCWnBu1yRw+9I6HTe9bomx3Ecj8eHR7jhpx2EJSwhwxKWDtHpSA/hd+Q6Q/XNZeIut1JxXdd1FzPAbGI6ky"
                  "Ym6HQcNmEJi07r6Ojo6OjQ6XQdhMWCTscBwEd2xARjIprIJiYmJiYyf2KCACDkOB6Px+O3AKDQkNscN32A7tIn3tm+wPdQiK1gI2"
                  "FpTbSPWkfP39+nb29vT9+3/Y+8NdEAfA+OmQ6zRtfR0dHR8ahTR0fH4+PjY0dHx2ynx8dHgB8U/i6fLaUnx1wT25MmJiYmJqYDAC"
                  "DTYdbodB2EQ+9aRwD+Nkw+hfQxSPHBdvQ2TD5FpJFBCCtwtLsEMYc15nbtXNNdkgqHYiKRlIwAAABAlCZiYkIIiThNSRKhE8KqUr"
                  "nsJ2hxoZt4CRurX076XaZaxJetiVOHTp0a+PgINiJWq8VwfLk+cITkeOQ14Y4rvOkFV5gNbxGwcVJTDea6zsoAASCExwDXWK1chO"
                  "N6pdVirqN3roR6RupwgcQ1uTLXI+HyOoth7KQkYR7fAFOJv3TclGuuX2CS60rmmwgoZRIFU8icwlwDSea3MKrOGxMM1XtqaLgmDc"
                  "CLYEbscM8PuoIEXYE9Qj08y62k5aQRDimNrAslDCa0CL3XGSYaTW0Q2etDMZyiS435NgHG4HACkQxzYNnYqtvRwqPLDKAT1fRDd5"
                  "KIJ45cOoeyA1FHC455K8BYpAAAZ2gMqDAOQPcz9/v3uTNAASBXhW/+wqevLAUrnjUnS7YzOs8s+bpwXYrKdoXXGjBgp10SlQ8A3j"
                  "b0scTwUeAFrmtD70uMfSS4gJeZlUhIlNsKco2uXVeY2VWl6JRDSAhW4jYAQCYAAJCXD9bEGgGxF1Oz2UgEAhOlC0q5pjzL3fxjlQ"
                  "cAAACAjx8bmMEYnbAb1U4nzBE2MsOHLwGuHz8oUi2qnhqYoTAuZWUNo0sfSn2HJJcA1xVleDATYEDmjGsqfYuV1VW3dhdQ11Yrko"
                  "0xrJHM6qZIpxW2qPLKAiBzakFdDasdLWtAzpUaGbaUXhZzReGzLuS71zqMZIhap91418WyG4stA5xvC5AWfdPC0KFnhug9EJ6h0y"
                  "AGfs54rQNMjP2JYPT0RkeosWCnkZ1GGYvGLCMRrhdEj8Ch8OOUvsYFzIyKCO+MNsuxBAyvGFnp9QwEhcblgg5xA7gRNLmyHjMwEA"
                  "Wu57SEt2AIXIbqDRCqICCh7QEAvBIAAACSrVYG45afyShwcSuuNzIo4AUK/1ZvfgUABf42jCVGeVhwqQpxQ99SBB86rGrhPqKsDI"
                  "mUIoPYFTmNXd0Vlks7U8FRjYAEAACYOUpUk8RSEAkCIWK0JOXukmSu2R1+iWGIWLBM+mt0Up2tqni9YR6/b6aK70i+IV0EAzUMs4"
                  "ZAYRQJwvNSInBWKJtFAgS9MiFgEEYDmIOZMK8E4h5xAegwErEGYWbSzKJ0E5mz+AozI2QYjutAsEbhzsrxtoHkIjxIZo4Ho/RpMM"
                  "DTvsug986rhaceoIQiQucUUCJPKaOJwDKa0Y2kiRhjDxOG6EGJEyEhATLXC0j4qKckgkeEugjRA8B1MY8D3sIBr0kOVsvFwQTfLb"
                  "j3ABCIMrHSLyQ4qbOdjCEK8gghdCNG3wyjgskAAICiE8D3VkkAYPyxpQAAwPXlW2HA/I/NAfx2KQA+3q4MBYDE/X+cAACyJJGwfp"
                  "ZxAP42TMkH+0AOLxIzb8MUfZQRHR7AkSHICOeGMHdG55ULc3qMjEjSBwO0SAEAAAgZYhCWUSyoKAVKKKsQL5v0RJaFKF0iIp4A4u"
                  "42AYA9HEIPhlrCoWNiOrlxU6OmOcVsXyAWNWWyYvEg1fLKMHi1MRcAqZ6qsKKPcJIoAfWgjkIjWXkBzZLBQ2X0djWBHvsi6aIQ6r"
                  "QmZ50vcrgEuGNleEwUBA1WpKJiZkbhShja5TrjZ8uHdL4p6sJpn0748t/4Ky401MB4FwAw6vRWc8BMAjnySEYJoc5+VpmHtCG962"
                  "2e9msJozQgHQ18GB16oycX3odS6siozeCNd2g8ow/jDOloAgg3GK9JhkfU4FAwCLci2kD8KNGqMLrinHR6yujhyHcCArjgYYwpic"
                  "BMtEILRJRmAK8ncHC0MBHPNnh8fASAue68jrwrIuG/vZnupwGA/v5t2CyABGSAA942LF5E8x+NWB4kPtqGxYto9scgpxdJx11V1A"
                  "BBREREEsTMk6t0u1QyNV3MRCIdAgAA4C6ZGSzQBMyUmAhNpRgtYEkrCYlUtqSPpYbpbf2LmAYxxcEodhZD1DDVNE1z4VabMg0MUz"
                  "ksaBW5vkWD45q5luFKQ4xDl6XhA0w4GGKQyRZwjQbX8Y1Q1y10x21clDHA4EPjADidlLiWSmXCUjIzk18yZHjkFeGU5hOwsjSXKm"
                  "a1g2NpIJmVsRIyHQb04fcMMljQLC4eVrUpAsBbR2P80rIFh7xkaD+qQRJAhCF6amxRZzQLYCgAwGHk4tTxhp46UZ1GR01UxokEw3"
                  "RgDR8aYLLBhBVWdRfXkdlKNjRIntIN5WpsAhOGYW3WNE6ychBocusS6He+3SoISm3RZ/ity3SkcDrh1O3GnqUWeMII2FsBAACOXK"
                  "+ZAayOaQAAAMDr9fgQAAAQpgyQURIsAD43bNUE+YGaVgonZW7YqgtmBDX1FCdVPNoASzrC7pwh6GrXnSTOhZliQkJITZQjAQAAEB"
                  "ayiEAASkSEEhUnAlqMIl4iEBUvFwr9KaKiwRKlIixCWBS0QJTtFQwxraBqER3lw4O5wsxcLRbgeBwXM5WRLq6EXAII0SuonlAqIj"
                  "sEkPAiYT5wvA6YhOuYQ5AkIsK4nA7DuAjJhDkrtwWLUBWrcSQhFlOglSQ3XXBN6sIjyXFczCTkSo5X5hpGyJJ7MtDTHSJLkPBbpM"
                  "By2F1Er3PU7qKM5yMsFhDGeEooCKVk4zwFE9pNnPoeCBgAYsJ9JsGHiYDTHHEpzKldb3scr1fvvJRLdLrQPhYwq7FljfBg/R6eNR"
                  "ZEBhQGYVX9QEdsDeG6qA6OAGjMBADgO6AIdQEAlaUfAAAAEM/wQZz6AQAoK06aAAAAAGTherz+MgAAAMAHlAX1Uy0qAL42LNpFsx"
                  "8HpWdH0LVh0T4i/zhIHWskPTKhHTrYuWpKV5KkjEUnpIYIJAEAAIhAIBSI0aIlSlQoChGhUKQQioEWUqJCUYeEmB98T5k2E/+DL3"
                  "t1UQNjJmHEFP+mrQyEabFWhEmubBFIrmAMZaYgjrBwHIfFMHkdTzDRuXSQqUP1KAKoAGJv6IC8ddTpGcyxIIyMNkIHYlVoMSLCOp"
                  "cBXBAKSR4Z5iJSHo/h+sSn1w1zcL2+t+vggs6EoRb1YfQRvRtEfcwboET1ohMO0JBOF4wuclcSqndFBhgiPPWeAT6CUAZAZwylLt"
                  "L7MC6YNRgRVn1YnQwIRYTuUl3EIdFbu47ru3l9uMJcud4JcxHQ6RSD7hqATRcNGv0Q6EIJPAUwANBRKPxWAYAIcjoAAADwMf0lHq"
                  "Cej/n7+9sAAAsWFtSVSDhHPrjcDBlFPWb95RQZfjds3cfIH5Ae5KTOd8PeYkz2Q8BDwXYfeeK0w1i5SQTt1sByrhw9LiVZHOVBEg"
                  "EAAKDECjFxMWamy8tFabpcQBMlLIwymhKDW/motIQ8H8rNy3MJzBhFOsIQ0gAhTIG23swQ9rJa+Vo1kgrfbpgarwknpUFFUXhkAZ"
                  "nUyFzo9nYLTpTQKNarPtd46sfSmS7CSgl1VkzAxOFWowvyqwiyQM9Io9rMVtMNIw0N6duZoR3zWRYFWWQhVKbjuF7WnVTZYY8CY4"
                  "e4jCT93sfJJACJBRpY1l6NSQDEmmzDBPqhSdNmLPURTE4SPg9PiIuMSJ5SGvOh8fQAYFSRR2T4XYMZETqDnihEsuKtxoSvzEQOhh"
                  "XKl2oCK1LfMJe11t/NvT/EuCdvlaj1JXsG+sLnIEHNJtDRjXHAGhudngIATJQBHPC5X0dy8cgAwAAAnP3s8A77BoAGigofEvUvt"
                  "SQzzckL3lz5SgA+N2xVxqYfiG2hQDRxw5p0TP7RUFYed2WZkTJkEIIMG+ax2rmxQ086qaIcOihPIgEAQAgBQniAcIAZEPPwclRAK"
                  "FomKe7hVnULf3/PrQ43ubI48InJ1po2TLadA0rEUDVUsVMxwBjVmBC0w250lKGkDmEFeevFhBnCXCZDGDrECQYkgQebcT2OKzNKQ"
                  "DKHqgnDSkN6oiMCsInFdb1GjTwpqw4J2QmJpC4LKoDrLwrHbc/zI95E+Ki0iHd+wOuhI5EXB7E4UwUkRwKwRFLVul6uHiATCy54a"
                  "CgNFdC7/pjGcUyYMJw4OrgMxutRSL3lRBFhhNE7tAhCI0BJWCOb1aJpVEbyCMmnhOosy5XrmptCmDLAOhf11KO/3ahqxOhRJZwP1"
                  "/AEZkTAcQBMVwwAAu8E9KzWgEiZCJPhBQAAMJcCAHp1D6QSAAAAzKfbAVCHthYLAAAAlQI8macAIFQ+AD43bFXEXvzAuvFRN2xdx"
                  "24/FOvOfNzVZYRMMqQMOWHNBpJ27Ry92YXHdDyJgHJYAAAAPxIzmSBiki6amEBSVBYqBTFapoRCodBcQooSE4rQEqQLIYHXj79ce"
                  "axwo/D71/JVcaMMtwDAHFyFJLmS6+hmgeso9zEQShTggBx3gco4QjLABeTBMDMltQ8Brgk7g1kxLtIOwrwCEwhsUeMKC7rG5ArX5"
                  "HgNfDrOIsfjlFavcc2EnBx3IoaOFs0aHKEuK26Jo1oGKpcKCVPHpO3dn7yJ0X8xXC73Lnd26CXLjgMtCjN5hCFThAQ2oSFtOqOVG"
                  "SDuE32hhYk4jsTlovpQozGwRbDa4UortUhDwkUAGGOR6jFYw2wXFJWsYBDy4MgWAXCbVTMEAABQEJ9LgCwH3xYAAIBMa6ZNaQCgA"
                  "cBTJ/x3AOj3+wDAcLwer2MAAAAy2ACgwXf8bXKBCjY2xMkkMx+KLi9G1SRfQ+pkrPnA2nUmeyDHu80EQVKEELbtjomYPTNESOfau"
                  "aokPSZJA0UIkQAAYM42+guCLGQ+ns1y+KgSupXRApdXJEpi4pSLDJJKRcndw82tg0wkAgPrVMAMn+iQ3W/huqg/Dn51VgoLfPn9g"
                  "VTIoESUeFyxOCk/hSsDF5NZW70MrmNVrOoWZlo5bmhxTDLHOHTC3u/ymKjiOlaAEIzU6EcUCYPLmDnmVK1esZjWOPXKWdXtVr01Y"
                  "JGhu4TiVoJMBjheB9dxCXLovTEEhRLGaUp2Y+m+rAscdQDonFbotozWUeP0Lop2ZioVzASyLqcOHV0lOE9nZ1MAAUBTAAAAAAAAg"
                  "0MAAAMAAABNPAGzHHBCSXWA/4hFeXd4eHD/Tf9a/0z/RP9T/1T/VP80TOZAm1Nx5OLKuqg4gORtwnDFBzFFjQzs0XZdrDdKYSDmS"
                  "jid4LQfDhKi5+h240ACA0CNW3cUDABUawBGbEDXTQBrAQCVA+gxJAeAooIVRYmfpDQ/ADDPAJiZPJ4CKL0VwmKNDgAAABB4wcksg"
                  "AwAnP100SFYKhzvrKcPFkH6ob/mUaXIRDBTcgHEGFi5xJcO3laj2nwCDrhVGxPvuosRTqeLwWlAfYSrIzNoeauADicEfPVoAlDqQ"
                  "aRFq+snciCkfCHS4qa8or0MBDMmF1j6cY1Cm4iGhjfGaeO3aieOGe5NDbGwDjMMcczOSPXRFkE9H8+2tivg+AwTAGQNEQxiLnIqu"
                  "GjWEMUgZgkKXsxZc5FSaqfd3Uw1z81sIB8+X5WJ4h5VVZ9m4+6i1buron8SP34vySmxQ7qLMCG0QEz0/dT7XwCo2VZgmg6XM5ywW"
                  "qdMz5QJ8fsMtqXl9ASTOGbvISIWw86dzoFrOPK5YYp0AJQNE0WyW7gQLT5gX0YMCEhLFyIFZx7T9tdYUcZB0VtJu6JumJQl5fBOS"
                  "LhW37S5VXs34jK1Jk6VT/x83HsZZHFaDLQov1dP9gNAMvmItMzF99N26+QM0xzGyd1NG3vx7cvGMQe2Flvf/nbSajF9W32brvVMk"
                  "+7b9uwetObQFh8AUjYUlVb4B2Kq5oLCGBuKhIP8byZy6k0Fy/P7VLTPiCKAqKtn1I4yy4MRVYUi94hYM9q163TiXMVijoCQBlgBI"
                  "AEAAGyfygLXGCzgsKJUvzv9XsNFCjlU+yZdS4D2WD4dm8oyL0+5TdC9AAAAAOSQ49//kCTDIgMwAI6dPc3tnLUcLWWKMTh3gAtGu"
                  "RBrX8HcVR2OmbiORPgtuEJZSZiw4OIuJlOhrDgCWNqTvazq8R1kGqXJdTJxtXJKFMGgpws9wcyEk9FRCbfVYK7HpfDKt6iRl2yPW"
                  "3hTVjWw8HljZcsxBrKd+rDCSQCAGKtxnRWOVybT4lpXTXidEUdPVgF4UL9swRV23u0ZD+F0MRKXIawEFIB1ekIgDYGbwsMKU+0oz"
                  "Ko9Z2TkC0c3gMxmkYQbJsxQOzYjDyQkIuv7bsFeisuWiRwzYCSRqHXOjQg98QZbtYEYxjGcQcARkID2pQDgwPm9ngRunDrVrqxYy"
                  "YraKzL4/nJO3t3aACCBuWOB5ax1sNREyTiHA2wFfRZkaS4gkWMr6LMg2DOhYKapgsoCSDNCBtw9OxjKFWDCykgduoxFYqpga3WXZ"
                  "EJdsKgHsYBJTARBmHkdFKsAQCmnXnwROSE7Hv6llTQVfDiNLyIjZBf2/ksraS74cBrfqkTCRD5PUtVGNNMKXBQCXNlcVlBc3JeFF"
                  "aQQFSmXY1K0woOGWAXocnERodAlpA6qrJyaaTkB4Jizva1jptWWCYvjdk79BZjTT5tmqsXOxhCQCDJiPlKf74sLJSRcEWkl5I7tv"
                  "9mpYBrTuCLSSsgd27/ZqWCapv0HIOTKyCpCDKk6j0huPhQVAAtocQIRWkiGIAYtJsnw9BAjYl4xuuSLUnHcx2tjuUQyZhTkDACHj"
                  "sQhFltHamcRO8SwkekNAZhRrXYOp5uxrLd4XtEwbb8z73zWNpwRWZbbM239xM8kh+uMyLLcnj0cip8LZsytqkYyyYqoriqQu5FSj"
                  "1dkFaJAQSnL43E4lBKlTCgqQknRouwQXhEVEbg7NHGEdOWrR9X0wRWbhOXu4rUZu3p+8FtsDIsThmlnNTCMKQ4thuOOKKuNZUbFx"
                  "BOPz3vyLzwRKSzpbvMJu4IBp56ICCKJx9zGrmDDqbOGUiFCT7KTkUeojozcJkSBhIijQiLK54mJE4GIKAsFkCwT8yUwIelyMU2EI"
                  "AJRP8Vo0dPebkqGaBR4ylMQA3+cdMJiYz7r7wm1Mez8OGaorRXUNFVncCyO9y+tTnwJTwwRNQtG5BcKZh5BQ70FA/IHBTPXWRUpU"
                  "nQexLSqkClyVlENHAqLYQOXD15ITCgkhBDxMhE3DxaKif+YkFkgIqZ4SgmQMW2qv3wdmTb2rsVGrGpx6LhDJ2wcc4TF3saBL6Gd+"
                  "vhJLbZdxG7+Z25+jQzaNYQuBh1BDYutlYCuIXQx6Aiq1aqVkFstWUNWFBEioowYI7tudxub1uSo3FXFSbHERiQSAgIAAJAymXQJK"
                  "SDADKEYiBhdQYsKPMVBM0UkxcSYEqFEpJDaskhhOmY6sBhiqCm2YmIRU7Cghi9bQQwceq3qcWAxCjlmZiH6YF0HALHFRchc/IWBh"
                  "RpjMYxFxrA4wLQKomKVxEB1ozEEOBlBjDOceDHHXZlryEFrZOCVme9uTSOkpQbDgxAsBoQ6dBjBwWrXj4MpbNqgByzqAzrwgIMhA"
                  "GSRUAI4ImPoj+4YhtEJ450rTr3Te+oKQ0EdEh0AuLwvoUgAWPT6ibwjn2ZyAcMQETA6C9hhQkdsorFi0RUGeqCkDB1Dd4A28ScCM"
                  "QJwuxH6QfQ/yMCNHCVggaJ1aR0BADDzeh0BwEQEwFyvuyQAAODD7zgA4LJkAL4G9D5GmqVR02oJnHPAa0DvY6RZGjUtlsA5B3Rn1"
                  "hAyRSpTRUo7mDuT66pYUiZ62NwCAxIAAACNtZcoBlgINkBEZhUtSYASZ1pICE0IAehCyA7TQgCCvQOL2OG46YRjoqO964AUEUVtM"
                  "dWiMpMcF3OEHHwIyRNOXSSFFzOi1+tdFlz6MJEIiHfoFEGsBWqK2llRk+NFMszjmrkOYygQDQIEGAA+HOSYuSZcnIoDMgcTuGgKb"
                  "4MccORxwXUwMNM5NAQ+jEtmJnk8GAgTGCOIAaGRvV5HqNPpDSamPgLUZYEEhXR53c0QJzo6dJE7ZC1BLTrDgLgQUV0Y1ZPI8bg60"
                  "YUL6iMCM8fjQ0JCwjg9wzJDSCeIN5aeRgETm7ShW7pNB2jdSQAA1YwA0I0Y3ZIcAgAA76QMFAAnAgAAoe4uy6WEMgFavwv68IdhA"
                  "BANMmTIIwAAAAA2XwkkAD43TD0Fe0BLqzkJe6wblp6CPaCl1ZSEPR4R0mKQdrfEUNXOo1NjxXQ2M5EiggQAAKgQTLsoYbmoUISmW"
                  "BTJoFKcEitjFhGyQCgmQigBDQjFBZ4QZYPjTsiOMNVioDY+dqjHBzjITDKZHBoZrnA6iiCYOUJgwqFq+mDEu24kxORIYLjm+PR65"
                  "PUKYWASXsmhngAEHkhMCHx4ZAgAmbmSkb5JI4ZhgHh2YtpgAvN4XMOQmTMRjA6aHkCH+jA6FVDEAWqKgjhHlD9ZS4bOogVPLEZQB"
                  "j2SnvQEZxim+mvvsK7dgCUswSOc9JLIBK6oCaPbNTkHBedS9YS4cPG65rQAudgwO6bHoKsJYTTAMMK4AANmHVxjTJ7Q6QEdEKZ7k"
                  "puib8EQLZAqQIkrdnQAGCnS4ojg7a1FusboazG0MBFHAGiOI6/H2pEcTw7goALeNkzFJ3EoxLSYAkePbcNUfBKHQk6LKVD0eNdQE"
                  "YqElJIghn03CFyXqw6RHi66whQTcEMAAADsJRmSWJKEhBABRQi7i3sIRDxERcFEIE6J00wooiZWgLI6sqqoaaImA+AdUsJsHFq5e"
                  "AwXHDQG1CCPzECqbQSSuXI9EjRqkAnfqWtrj2u6Y38kvY8UZgIRAAA9gwTCcT0OQgBi8JqZ4zokjJNENj7UEZiDVyYzBMiQObjpN"
                  "XAMqKGRYaiDoaEGQAgBHUEGgBAe0gRASDCOv8NijCH5HbiKapzzQjhouA6MQFLiGN2g85EoRSdULj4MpRwDF0XuDnXc2ccYPjlmj"
                  "uEBMwSjdvQRSBM69k4wgteORhhoAuA7ZAMAoGH0pwAAKjI5AfAMBEZERr9LRwdR/f/WBm+EjcfMXDOQBGAec8FkAsD/AD4HLClF2"
                  "mYmMaxmckRzw5pKSIdJDqsJz0ecGC0J59zOuW5Oko7MwuxAAgAAiAgkxSBKiREWijMlLi6kaAERZYoCU2IQiGH1rfZGI+Y0W78s/"
                  "lhtUBVDXdPJ0QA8ZxyJAOSovfLiMcBwMFwRSeciPbgYDXgEeBzcdBDURwTpIjNAHpnhYuYguTKg3unQCUwgGeARIgDDzMxc4XEcT"
                  "y23Ta6LzCOv15VPDK/MXBnpOulLtVsXBVEAxmithYNQOPXElRBBXLggBE6XkyI0JMwyYBWGMgJ6q9BkKNxjaz1K1TsDIoyDzmvPY"
                  "KiekGJIEE67I4w5XhwXAANwweMUkuGCQRwqtQSNAIgJWVdWnOzt0Z73R6kl6IqhpHsKQi20iNlJYKzVeep1jEBkLAHjLRq/UnJQI"
                  "QC0AXjipN3gQHy1Bl5P4B0CMsRhT7d3VQAEcgya72QAvgY0MUVpGiE98OhpDWiijxBNIXiQwwLyXWNlLSkJRJkI5pi5UlTXSULsy"
                  "MwiIgAAACAhhBASEoKFEC4uToiQFkIImoYERQpM7JzusG7HVhTTnGaL1ZaZDDK4tqNimK5HPlyfXuGYK5lrGByZSHqmoJCghDFsJ"
                  "CSBHqEkssICuV7MlSHDpYuwyHgD4CnRASEjTEoCBEN8gwr0npGEhhokDMcVLq6oulqoGphjJoGEXHPku2pJQZM6zuIt3uC7hCC6C"
                  "BCqj0U4dfoOA9BhlLln1LEUBsTodNAZpm5GSuBRjpJ+R5Ek3R4mHnEpz/woPkxaVjIZVmODUztO1TAhxmg8DmYgD7CYCYOzn0EaE"
                  "hI3AgAQI7XSEZoyRajTAI3kO0Dr0EmcDwBtiE5koAsZFh2DbidOjEjVWTcA72J0RKGoGj76McwC3UjFxPOcEMipPa7jejAXHjcs0"
                  "QdzQcovE8YYN0zJB/lAyR8mjOEuq0UkyCICO4Spq9o1McwpI4rXhEUzgwAAAECCGVJIZgmWaCICIi6ghOIULUoEQhCA6RKI+oEC7"
                  "IVD7Oysin0xzEStE6bM1rjSClwzOYtrjuHTzMxr5i7CvI6LyeQY5piDQF4Mrwk51tqiBrCgMwfXNWTmOI7HXIrwWSwhShx5b+Ii1"
                  "xxZywAw5EiYRxgwNJIFRw6Ba3LAcaAiL64jny6u1yTMEI5h4Jh5EVCXHiZidw8ByIsUYNY6nYnwnrh0YRwaCjh1jND6IoN+e8D4S"
                  "OgefGSnBRCdK+KC+hVLp40uMkAoHI1PHK8Mw0UgALCo07kiQpd1YEHEOLMMAxOMQM0igWcEwKcPiOP5aGVv1DEGeD041V0twoN6i"
                  "yaCSnJjqzbkmg9D5s02YTJgmh1GAABAJF1E6GIVBYcAABIAPjesNQUzQkMCPHqaG5aWgrnQlAyPHBnsGoyI2J1YxnYulVRiRRQPz"
                  "USSQAAAAOICIkIJxRjulBjTIqJu4hRhEeKQ9BB4sCgoIikBdwJxmhIQEVERePaOrBbUFKsFq9Via8xoMdRixUQUMdH7kA4dmdBkm"
                  "MnwIExawKglHDM5mAcLxjNur2OQcJDU8jgezKGMoTTCSSjIcISEH/DAZSzCSRGZhkZQFzWOzHzIPI55kVeyaJyOLOjDeMB4x32ET"
                  "hqElRiLbu4hSagB4JPVGX106CQwFxlezAwL1AmnI2OgJ95FTYTXUWJCHXogYjiJ9zeAQk+MMzz6qVPvGfo6OkJ3T2dnUwABQIMAA"
                  "AAAAACDQwAABAAAAIrNerQYWv9V/0//Xf9p/2H/ef9p/2X/Yf9Q/1b/BEzE2jK0NDQQNcgJ14gIsT+BVgws0GAgojdE9hi06B0ut"
                  "k6OBEYZxNa/YWB1IIIaiC3o9ycQrxHPWQR2Beo57/Q8dRMQZxfcCgCgLFSCVcrkbAMF1KpCqhQAnjY0MQb5gPRhjae0oYk+yA9IH"
                  "9Z4vmUNKSIyKUUp2G7NVa66kjgVnUUcZ1EOBAAAIIiYWLIJMjJIQolT7uJM00SMFhFj2FnNqfaGWu0x7MVi8SNjYScCA2AY4ksuM"
                  "pMZDi6yzpho1rAWIcMx8IKBa+IZaoHVE4SPIiKyR1iEDMnFqYXM41L4r2C4C2auQrtpqFOnM5JMmHkkHMeRIeF1vOYxyafjejxej"
                  "xzDF+B6cEJaoEZP9HoSwUAZLvROGEM8OINxkgiqB0LJCojXQ98rMUTnbyQgCKKskRBKoYPTAI6RpU8JdfOn9Bj92A+xhdANvOATJ"
                  "ADQqojR7XLp+uW0OQjWYCAD4hiDETvevXUkAjpgjECjdaxVgTpi7BgQBghIvwmmQweKgROAYQAnxdyfDyZVwGwGHRx6WToDAiaKI"
                  "gB0n3G26RFiNDNjZQ4AABbyfsJZF7429M5FZh8N7ZfZo6e2YfQuMhtpGJ9mT56PdjGbaAfz5LpdV+gcuhHFY8dAAAAAUMYUGOJgS"
                  "kSCAoGAQkH7NEkIxQUUoWgBamtnqDoQx8wwzLa4VuxtRcQwxM6imGqnKQgBNWW0tiGP43gquIHMiPBMTgaPsCI8ZgZqRyCZFwfDX"
                  "MfMwIthOI4QjtGYuYgAwPBipck181o4BlCAhBIGF2aOubgG8uDBHDMz4WKGPHhxVXExgRmmiiZqE1MnGAB6Z0gaGuHOQEANIaCVQ"
                  "V8tAuHgAOBFZmI3honY1a0m+v2+jzxGOAidEZ46gShAZwqN14ePmBfHCnAAAsHotmG8h8swmg5oTWjInYPwm4BSGAA0Qz8WEOK0M"
                  "KkB6L0BHLkmVidRw/CXKQaiJhRE56mXHICVMMNHIt8dVwAAAADQYAoA9IyMjJ7oqQTSj5kFKAA+N0wtxmQPSB+szA1jTSF7QPgEj"
                  "i6TiF1WMldVeoorFzqdKN4sa+xAICQkRAIAAIZUUE6xD1SQ9LIn8SmvZ8kzWFRMVAhJmWEhSJAyL4MrQAABCCGEfYoqBwVfvvLUr"
                  "U/4c2L1xM7OVuzTDlVwzGqjVrEI8prXcU0y88plIvltLPrw60Py4gQ40ylhApdQi5FAHcwDkosPFzB9RBhi2eV9xrjA6HRKoY9s4"
                  "zLPO6ZcHEoCcDGvYTLDPI/PbC+uHFExMNQWcxog2GKZ5jpUTZBGGcM2sX2mQCLtBWzc9M5oBKIhr2nVZDJEvSJUA+bQsEDzom5Y7"
                  "CBDnBL20EigLuFgAMG9AkZhqAXooQNcJrRGBoQkwGOCCf0JQICKmBWByTq0iKlp+hN3YnvaOAbIg5khYARg0RrITBhYACXbggyTa"
                  "w4uJi84xkxEBhVUAAAATK6zqrqO9dNIgA+4ABn+NuzexMcPq+gTqae3YYsmmn248EvZQ0C6y6xWikQZGWFyJ9ZmmaCqXU/0xDlHO"
                  "c08ToQAgQQAACQxCyoKXMYUlIiAeJhQKkm7OrF0BwRSl9Qzyq+naTefUI6H1/G6XhfX6qqwlu8+DWR+cCiM0qKDbrp2C04Lrjmua"
                  "ZEHM1dUC60NP6HujMTM9SCbkDmuHEeu+QETMqpjoWG7hHjqCZiQU2DmIg8qhDnIMY/rSrWjQTUvLdbUWsHpYRhQmVBVRamO7zK3T"
                  "KPOlFoV1xChAZB7O8K0/17piAkJSr3pA5yUM91WPSEOzTCRBYmgoSE7UhOkc+j0AGASjpYbGQLWggCQDLoB/EqPIhdqU3C5wu9BF"
                  "hSl5AjAcPBYWnE1mQsAAADhxRjzGPI0AGACAACEOgkoEXAjXOTQg6ja2k2ozdSZmEgougvGG6nOAqNiqqCGKkxTGXF9GFQdEgAQW"
                  "U8AACxYFD9ZTwBcHAD+NizJxdgf4BeePL0NUzTB/EAIH3jy/K7MDEAicmDsIKnqdq7MQiw6UcSxCUFAYAAAAAYOS8EFAeHGuBwX8"
                  "vRSBSUAMxGIOSZgEXEBYUp5UkCRGU6IomKqrW8MFWPsE+p4BKLiSo5cWxwy6i2aCIvGlVzkQZhhqre1vk9GIfwduyysMYfp6kqSH"
                  "OQRAIWFrTlamUtRVOsCi4ASxy2Xp8bxI6UeNLl0JOylIcm8KoEFTxgd0SGyjzADxwVh5p2qbG7NoLBCFj0NvaP21M25Z0CihupMa"
                  "GN0YHS6fEgnRjQmpm83Ol/jVmSZIsJTR4674wtdQXMxTPU4YYl55a1SW+nKRe3FFAlAmAhGIcmscRzzms0MoAVaoI95esuyDgBoT"
                  "DDNfS8gTmABgIQQkH4R8cepiMUvv8YxDR+M3lgy6zpakJmQK0dy8SHhs3CtwLJn7gACzghHACADVAAk4JUSb0tKfjb0UobsAelFT"
                  "vZ4NnTSRNMDygtPnu/qsiIRAoGNNZ25q+PSqThXbDzNxIIAAAAihw8RwCQFFUtKRCjmFa3wFAiFFWIV5V4RB/aAb4d+jW3v1Ll3h"
                  "OFnwiIRzm1rGKhPc3yaHNfBNY9j4PW4UCBz3NIMKRb/Yo7Zgi3mhEMIHYwD9BaCSHPCGeE1DxXXzMxpB8z1mEzRc1bhNy7PUAIsI"
                  "HwGl7vCGhk6Y7wXmGvO4pK+lbRF1hPoXU6dtybCUH349R7h4KmaiyFcmTA3qJCNGVzAkTN2GcUle/mWDIKhu76tydqwxRWyU3KxD"
                  "UNIu59GGQwRZDu7naQbpjp7QCTjgcxcM6zwF4E5Oq0eoRG0o6+3hCHJ0l8UhguOJFHBYmTcfN4aYJ10jKBL7xEZRcAIaxUQw59h3"
                  "ALQQJ1wU/pIYPpbVNRfRiBtMpLXDDNMLDGMhsCo2hgOWsIyvao0kQAAgRgAQAPLaiUAXBzCv5fAVKXAdwUBAGRZAl43LF0nmR8b+"
                  "TdyHHXDNOpY+2MjPvg8HhPD5OZY7Oy621URi7stBMTJI6Qoh0AkAACgRGUm4oQC7aVExEUQLBAFERX47hSBQKWOqROGjZ3VoVVU7"
                  "GRyl1E27YQKri81sQoR4Yeehgy4+0R0LUBtGnOVfneARcIAs/bIqpLUhiHKQFpM4F0ZjIQrVgjMZLmkwEQVhFaMIWozuVYbnAauQ"
                  "IQXmKtKmBVApYiiqBSFL/NFWWAZvstNhHESPTJXWnpxhDmszIoF0OzhMNHRotGHmZkRViFoQvXSjkfR5jgqXPNU5yPBSWjtElhAA"
                  "RBjYLXHXDCEqZYhx/BY4WCuWQmktTxgkp+6MDxGQRE1jaGRSdjOKJxwYlrOrE1EEAA9AZV0UwB+SdMZDfoRAACAUfrDY7euoerjy"
                  "7nMmgTkQxIIJG8Xql1h7lLtxbdXHcFpAAAAoCZPi1BjyeQAAEDcvM4MAFxwRLKT+VIFAB43jMmF7EMR8yeXuGFMJjL7UIifPO6qo"
                  "oqQMkhEMGbu6nhjkrhYRNwsgZmQIpBIAABAGYiYBZiIIJmwkGkRES5RolwhpMUBQaBgYZnA933QqL3VcVcmdTKMmboWrGdB1er50"
                  "kSGFKPaMT/mePHi0xWF3xwXcyQXmcAjheOaGqx0pDDw0LkYoZYZMseDyfEIrwEmF5lc5LJl1wU5dNFLCAlpTHjoHAxhmLPCkIliC"
                  "mIFmc6G0QZ71bSoKBgYmIjkDJu/IJRR54TLhyRwMXrDIhj0YW51qHNBRYJDEdbIAPRhyDAMC2pAEZkAPkJPXKBwMl5yEWyF4QqXk"
                  "8JTuxwXx8XMHWeFOfpIFp36ZVZnREf7pe8jT7pIFKErIuL5806oVQGAulqAwEwAQBQFA9hKQzAAwGQSGHjAXBfDHGGuDzk4nRKiU"
                  "mplyvR2CNPZAwAAAIZh2idUVVUB4YAA3AXkmytQOFQO/jYsSSalkUYOFznb49swJZksjcxCeZCTuryriiyFFCECllZOnTHtXBLXx"
                  "tLYhCAMAAAASAgJyYIlS5IshGJCQiAqFIgJxZl9j/333W7fpr05MZp24cSkeH2tSnMsFKXMW9qaikylHLmuSXU4lCgLP05DdRTO3"
                  "rc7GW11BpMW1kY0WI0IKGm0kx5qjFZjIpiivDq3YqSMulB1Ce/f4dTnLa+O2IKtrKH2mnnSRpi8uE6bvx0rESWgBr6HEKpYWSJNh"
                  "uqSdKnDhXeh6MSWruKu6hyZM0pIGDjELxUMwkfCygCHDg3Vha6jhITx+UIAnnjjw+oylIFs7gYnnGElegYIR8hw5Bg+hDkGCCPhd"
                  "lFHjUvhRwBAFvB6i3CGt80JIf/eAE8RviQdBRYacEIEQRAijEDrmjDFbopMWMVTUQzf7fUeI5iGHsD8pfkrfjOnUgAAAECvF0P7e"
                  "aABAEBk1zsCAF43bFFH88dEXg0/6oYt6oj8MQl5Nfy4a8iSSCIRDjYnzE3veOwqsYrYTG4CCQAAwCBmEEkhJQtJtBhExUVExQQCC"
                  "MXFxIgBTkxvbxo6xfAvFov/GfBvljmtJ0T8a1m0dl0zw+u6AjM55vVYFWEIA3NcMMPkw0FeCR1DdyIiyY95XI8p5C3kT3nlAJ4C1"
                  "6gRnoRkRBgPPa1hi+xICJTmMUPITAG1mlZ7MAwbw9VO0Pp9i66wIjSy3hGB0zDC6wx5wIvhNQwBeJAwcDF0TmNRZ6GvkokIwm8hm"
                  "NM4Q/VY0Vk0jozLWlAXIgwjP3aag9GR3qUG9hhtuoh82CAPhrnmEwuu6yhGhILBFYlQQp0UodRTCUALsQ/CRAtBEE2YuEWKMOBAZ"
                  "EAPCBm3AwBqSZcC4BeYmABMAMBYkACOxyMAAABUHLMaUgAA2BqfXgMAANQLHjcsSUcOI1AfPA9xw5J0TP5A7B6GHndFdRIZMqEUH"
                  "LN2EIzV7ZxLLC5sinMeAUkCAAAJKUgykSBmgCgxUTBDhIlAnA6AhpAWEOJXiCahabB1mnjOpaZaDBUMg6lYBAXMAUPUdc3AECmyI"
                  "4DMZF6PjbxicKPLSuf1kYQAczHD63qQXLcAVbRu4BgmeZGLgLQwDMzMHD8yoJH1HbhohKH05QjAdXEcjFBH1Bs9o8d1zQOODEAgA"
                  "hERxsBFJrklKxcDTyRjvJPAGLtbWAm8xRHNaEgYi05XJJ2nLjiBvgiHThJpY6P1o4lBLEYihlBCdQRhaHeQ1IHR"
                  "GO+UHK/JNZMUZdUIdTGA6OBDwhgE6ToiBgCAUADXFJLZRegIIYQoijAitBpBAYB0mAfamTgAAMkqChSAihVZmAAAoCMFMlhXBQAA"
                  "QKXfX1ZIgOk/hyXbVQAAfAAuAAf+NozRRI4/NiVcwNswRhM5/NgkF3DXrFYBRMiIyNOM3Vpg2lW6E2NqlUI"
                  "XnUAEIQEAgJNUJSAFRcFgZqFATOApLVScEtKAmDhNu4kLKHF2l8sUdJljntIH5tPxOCSuKl7MKvh0zTFIJ4YaqsLwIONWlytkqK4"
                  "B4Qay8MgE6kzDcVwXgXmRRb2erGJHdpmQFiLadToZYXxknY4YSzNHOKWwiuPDI7kyc+V4C78TrkyOx+T6CpO"
                  "BqTS8Xj+OzDFkFmE8jajuDNSEtGiNnsEbwOkYSMDFXAFvQPQK+ohQo2XDs8hfHcVMZG+cej0BjCdmMwERRMUU1CL2qFzHHA9eV9R"
                  "PZ2dTAAEArQAAAAAAAINDAAAFAAAAVx6YmR9Y/2H/V/9m/2H/WP9Z/3VORkpMSk58cGtuam5nZ2tqCCObwnf0"
                  "LmQeXJnfa+BIPtTG5UaNjfA6/XTYrl1Li5wcMDBMyyEBAF4AAABUOFPjubFDzrqMwarPAKjxugADIIHebgW63cx9egLIFsQMGgku"
                  "PwwAFbhABp421M7EjP9ohbCwHc6G0piw+UcKuCR0nV41SQCASbETOXdcdVVFrlJ0c4QJJCMAAADPcA5xIzxW"
                  "A8M6xnl8N9fwkEppIgEPyXI3oSjtWYZYTHtnDH/Z7mKZTNdfNJ74Fp3eFECMtjGQhfnA9UYpJ/1YvXJYOTJjany7DRgsABTFaIsr"
                  "EaAurw8LkbAxmeNrAQQr05IYJkEtMEgE9W+PA3LlOF7HhKtFKadthaM1K5xauaZ9l2vmygFMF1ZJqI6V4pUB"
                  "IDOBmyw6DXHrSMHFUMWvchozIGwb0TA6EO/yEQB0PhIsIBkT/RZH60dad4vrPXQTKg9UoU0grXHkSLlIuGTg8ehSXBchQwkIM3Va"
                  "sAXXhY8n0g36Ic8XYiWlQQty6B0tXAROgEgwWAHzCgAAAPezppotW0BBAOCrZgzA9ZIAbrfLxAToYGdTAAAw"
                  "JlYqgErGhYwDFBfYYEPg7h84CgC+BkxRJo1LIaeFgiLTBkxFJxsW5LQQKPKqSkhAwCJkbLnspE5VuyqLa7pJKULKAQAAAC+VM14Y"
                  "jpC4cagMhwhyKWMIadCdl4iKeFaQ8umy6RmFTzy9AlpMBGJer+FT8iBH5nqQyUG2wAjvysAMw1y5VtnmhH"
                  "S6Iul8+KkzguhJqEXqgoS8siog00U4CTajcR2vOTIhZCA9jeS0gY5a4Zr5cF2Pa5iAwadjOK4EJtfNnlwgDE7zGAGAKc2R1zFpZA"
                  "Ygw1Dohu8LhgvVmdqchRXCFiw6zuI9hYwa0n8F1dGaMeAawS6RgGF06b2OOkicjlG9t4KZHADwuI5T8Zi"
                  "hdnE8husDr3nwSUgmkE0oTLIEc/EYZh9t0hS9h8uEpMAf6MIv/X/RFyLUMrp4HJEHAG8R8B0BAABxCQBw8TB7JwdsAICKjT0CAKL"
                  "W6Cx4QDLX9fp0DfnwVQDeNqzFx+YHKBeePLcNWzFJ+QPKQk42xndRAYJMQSdlrrmqXSplrsvCLKUAAAAAC"
                  "7COyxK+gDiOLYwwEihIqTcioqJiLooSnzad5t+XI0uovdXHMqONWu1trehoTigttn5GYxgHG8NkOF7XrY0L9PqG8IxsjhZYcNZ2L"
                  "Q0LBYlEXYwl4VWCmQCEa4WbVrf5ckEGxLIEdx5WXWHh0h7AAEdZEniGHUFCRgpmTRgSYXSOC401a4Qh87Z"
                  "YdDoVkcJurIvWXwpjFF2RnKYI6iwwE5UUojSIgvCdauUWic5Jik642t86i2NiZAeZEMbo9DqjFwgc3dI1QlOla7G0pQzDkLlLrGq"
                  "yF0BmjlzJ8XSMs77qyLUbDQ95sTx2hEVzhs7PbdbWAT2rl4TFaQEI+D7KBRgTjiQAMLBEOZHA5R4JAELo6Jn"
                  "16Rh7Ygwshn5kljY5WKeDdAGAIQBuAlQtDFxcAIxFvZ46HQSeNozOxc1Dk9OFJw9rw+RdhHkYclkNPBnDq45JAGDkEHO77q6E45q"
                  "lROYgAACAd7s4eePywOcolC/CqoxMsaiwAiIlUUI8iJP+svEx+2QbbYpv9TO1J7H1a6oxTcxBWgfTROPK5"
                  "IqK8+JhfYfXcWWOuRXMMYiwBWZnV4UXB3PClYAWAbiL+fAQ4UjpD1cJok3mLICBex2oogaEeRjDHLW4YbrlB5mZYQaLg7nWTulBJ"
                  "nM0huPIMR/mEmVyRnVK4iPTIAvdTkcuh/2BCAaHr9EOEIuk2NVw7iAl/bqH56EwAkMkSIdiBdAZvUt/d"
                  "dH6ZCx6Qr1BEyARBNdw0azorHiMIbngNbOAdrLwOhamZSgiIrQ3Y5i0sPQUNtb5FifoEdtmD6RbgBsb6O+VlBWA0CNsBtuLG4V7I"
                  "Dw4UhUelkBk94g+/WKK6YV11wYAoDduA4B7z1+6Lr2XymIDAACQYEnIPgcsKSbSAj6YKwjQHLBEn7INhBd4"
                  "fleUGQAyxJHL5NyZ0pUUOyeW6CZHAgAAgMcIhByNclkurFTAJ6Ll4uoVifIQgAgrxMqn+Ip0ZFOu+mBrGr5lMid90mIxp472/h0n"
                  "d3h8F65wXOGlXkxIaVWNMDNXKcF+XWbyxBk1dBIPP6qBiMpUAyk6MXBNBqgqicXujEyd1JGBMa6QIBSNwMwr"
                  "18DcXoMrWenWtU9zHcPjw1yZBA7ChMUXOmkEwh9q0TgRBH2HUggSegw4QUI3ABdsJl62hemlSmOaFWRIAgu3MMEuD3H0e3RHJA4J"
                  "Ay2SxQaaTjfDgFxTUa5cGWDABtb1HhdBq9pox5U1RTkOvXr73dZtaG01Ebq6Tn3EhQsAgU/oNpFRIgYDVYtO"
                  "rlF1qXhqryu5JjoinVEAzovr0NEmAmmijwwTu7EjrkABJFseTe0sAIC5XjcDAB439CWWNo2azpJW55jpHokbuhpj7YdOX1bnmOmV"
                  "uavKIgmZskwZx4plgyWamrXzBBljFucSRaQnAgEAAMDNwYGJSDxRWeEpLvBShHKoaGgrMYREkqgIXGLihBBHjI"
                  "Wevu8pJAQEAChnMfPpE8x1MGiva5JHjszM9YJrCWbgel1jcW906QAgsipqWic7DN82mBrhoCM6AIbAkPBf6IgFn5zeMeNJWDx8KE"
                  "Goy5HBSoTj4WyAmmIYgqoxNSwRjA4GufTGBUd6KwcFnATQ1y4XgEOAEmix6dkdRq9bahQaIN1+iK2FyY1BI+"
                  "sIjbZGR1zUQnK6vLHIIEHTNddrhms0TqZnCEkNSBjXzKwCciCFRabeI9qEQRQoqAc1FkAcp3A6S1QoAGDryQi0GOjDGwCWhRcUAB"
                  "AGLhv4IIR+v98HAMhIAPDppHj2hkWVUlFR2Quwt4tuJIMDuMAHFjYkhSzy/L8ZsuVnkSupZMresCEhRDEM"
                  "/83E+rPKlVQyUfdHWVGkQIgyiCJFWYQKZWQxNdVNvQGScooeYtPZmEpKYhIAAHCFggYx8hmGFTMyw6XkLgFRCEILqUX4oJUQBrvA"
                  "vUjJfibTT6cOHNjFTHG87DxduU7Vh1wXTK7hOK7VXhOurRyPXMOkXHD8VhbhdxsEhiGS8OKgRfGlrbZqqHa"
                  "vXmdA4FQYQgIwL1AO1J+p9k6nmV6iJngxIQxLwwDMABxzw2++ASgxOXL8MvPI9zEAkMkcx+MgE8hkAikBLf7alVlCnYIwbGfGzNq"
                  "CVVuZbUbbzCE969R0OpDQkBYIQQ+GOGKZBm3P5IkRZYC5kDiu65dJEtJipop3Fi9mhhkSgwpHDsAKOQpwg3"
                  "FnuhicFPXBW8vpSlEFWAEAd6w8ecSZhJ6bwBva91t3Avs1S7b8yQ8yYqiiowpTDXokAFBEALgsFJz7CeCaU3JRPVysbc4KAPABPA"
                  "V3W0MRxvdyBAX/NBUV3OUMRRi/nyNEch+cSQ2VpTKTNyM0IErFMTvMa4a5MpPhQS5XZL1D6KOyvLBW74Q+"
                  "/LZQzerw1OCbEgBoYNcAlAULDSuNVA8UfG7aMmChYqWR+gUFvxvTmmpGGXhTFQAawExCsAe1iDDHBw5GF1LvNJsxFm1CGgYLtMU4"
                  "GJj5ziFCfRjzAmQBdxiQcF6kggXbPLaC5Q2wuD6kggXbNPk8kQApvRGEYqj3IW7UlXAthj2gJnE5JPiQ60g"
                  "y4RHM1ZBeEI7wIsIAnjgESCiQYNgZpAW9nBhHsr5Ach+YWgt6ODGOZP6A5H5QfwF4cwRTlAHf6yIWknkMlIDhADBRk/k0pFCnwxs"
                  "jESZ3GmFcMnA9Ul8YE+JlBAHyP6UWANQBCyM4JH8kgZHkfsg6YGEEt8SHzERyL6ijogqQ5j1TUFErK+Szx"
                  "PUKcwtIRPgdgWuG11w+OtTpLVDDZF4zx6knBlUAhwDICmQALCKB08VwOgaSu6apRiR0jpu3QyC5zziNs7JaCAqQZFQwMNc5uY3QL"
                  "bMSrgmNzxINUxl7OyYslrwoYTSW5hsgvtFBQqEPnf1YBIBj6z8BXDpDN7Ff+Wx9MUF2jU5VgT/1w1Es"
                  "0H+1J1qEFCsX5TGX0IZvTtN9S5llTiNyVKec5rJmvh6CYjGTi9Bn4tLhaREGlmcL5nBu+KDZnq2Kiol8RH9qfpfQf6ZSVK0dP/e/"
                  "nvvUaGuZNm3KVN++ZbvTOpOdjzawOi+O9yoXAHQ+0RXo8vzCWFyz9/lEVuAzf2EuPvO/sjx0WR0hcqc5"
                  "I4MaznYaOVWEsijZZpWBique7CZhMbGQZfEyWVyG0LMCYp4Oza4KUjZViMiSQg/JWxerNC3JT/767BP/xVSfXYYZZ5wwxSqfPgto"
                  "4LprbSdcLtEVXI/fo3THu1TCFeTTKaXN2VbNrK4qg85GO2bFWkWILNyZbK/KP1NAdz0CADFN8i4ltJAIS"
                  "gLi0X9a2ynottztoFPoZvWfneL3HKV90HsypJK7Z4GTo+rlc5fjyjLaOUypO8x83scuACw2qQ7qtd7EAgV+5BJXoPs91L7p3TgWR"
                  "SQRmxcH564OZydzCfU0SV57KRj4ToRDUoFkPXZKTjVV3okKiaruMtXOiJvA0/zjx//HqlnfY8n74+l7Hv"
                  "eURKJzFxWIUOel4rq+e5dTPPUjM/23WFUCjErBCfplfdjiwjcqhRcQp/qYYjPcVVZEYmJ2CVlVIYnssMHUPUuHciRXDLCaCJMScv"
                  "jseLhRLq8nNuOopQoxmYiKv4i4lWhPUcrfRaso7b1OeIiPC09dSCl4giLiB5UKKWZX6D2OAPgkAGQ+qQO"
                  "s25VQbOBdQtEVaCs90Di9V11URiLaIeY5Y8x+s01mCsGpqjlRM0w5kbtfAbg2X7Y5ooTqyNL1iX234M3noeyJB8rDzTbe/NOZnDU"
                  "SdBctE3OXWHOV0Hru/z8zXbkYTn+tVnNvilOx1wIAjE7FAfSov5nimu1oVZtB7Pk3U7xm/4zKyoR2Zhumj"
                  "fs8c1oUMI8ngKhITnHK41EyJeLu3qyMogICupCAL8aiNMUQp0VFiFBUPJj4EzN25n8O7Wc6Go4cOdiN+LLFwUwc+AAVvvxKAJxS4"
                  "QD9dn1JxTFeKhXPoF7uDxSL2dtlecgRKUQVisiLrMpA6ggbRs0jjnKEfgOgpdrGJEmCSIha0HPVlKMFk4Qi"
                  "E4JF1+bDDBGaRT0YxK13A0tkcaGKi4iAYFT+/W2YfgarKWpoBQCMUsmKtB5iEFZcwyutkg2cSxwhWlzjv1ElEmfMLMrRNnpJm5k5"
                  "p0iVFcoR4QYAaqZoCY7B2Ht3D9GSj5UqYu5SuApSXjaqRFGWFWVX7g1JNJIsdMVGBnXsrEM17v79bbU6mtJ+"
                  "1MbHl20AAFRavZMB3cRI3ALd8C+tnmHEN3GkbvHDtpvihMRpzsEZGciKmJYo5h63sigOZkVZBsqSekW2KwFcl6qEF+YzIkKKQcty"
                  "eZlBtNogIMHzUTQ571WEF0+a8GJSCLgRqQb+Ga5LgvTOmLssAABPZ2dTAADA1wAAAAAAAINDAAAGAAAAssrB"
                  "0Bhy/5H/Yv9Z/0j/Wf92/0r/Vv9N/17/VP9sOrUDVEK81OJAtxnVTcDvIWrbbP+qRVGJOCSJg2sRZVYUgzhr8q+OySJtSwRgYVvW"
                  "vMClNgVxqmmBq7XQR4pyuSiRllAhTU/J80pq59H9GYf2dEFIWTNjavbxba7fe+OzU2w2vu0F347gu3zb2vq"
                  "6AQBaJx0+LCWy/w6fDJKL0EZwnXRoeIwP/z18GjtrPSVoJb4DAJBZWQaiMiPZj7TIXiTY8nimN0md5gjdTTmENAAJAAAAoAIUURw"
                  "BLHQ+h8sTCIWiPLNMeQmDxdwkmdC+CLzUAdMyBAIPBUlZIkwN7fnb+9uSwtRWkmuyyocmOYtBEel1Hmpe"
                  "TJ1EVLFOb0lEnO0AXMdjMseLD1Mp8wDCL2uEL0vATRNAZypa49olwNrQqAJwT3iAkFusfXgdw8VZCVX8WMGwTjUUFEPpfgfmOncd"
                  "+rHhdRSxWu3EBExD0NS2mRys5YNvKavYqwyfMhfAhNCeup1HCj7GrEZVA7mODVjh+BT+9PvuptHu3jSigQFX1zBEmbaGaD"
                  "b2JQaCVRhGwwoyevNdOw9O15QrnybH5LqurGVP20xayn4QQBFRLNMQF1QHHcxIBM6wdmFYKUG3AQBwGjQAAAOnZf1Ub/e9v37rOD"
                  "2YuEfcx5PCbDSLZCYAAKCX25caq19ul9qapX61+lIDABAZSVxfXy8QCQBYc3MAHjkFVsyd/TfmSw7VR2o/O0"
                  "v5UYpsnz37D/Mhh+wjsZ/V4v2goqyEoiJRoSzJogx4HDqDIpEqE6EqJWUi14uAo+4E4GnIM6qbRCCmFwAAAABEA+qwXTLOUhBj28"
                  "gygOcTCBhaGosRLslN8EpBjMajIMEsUkAQkyAGBEIBE1AQJ2AKYAGLEBqgKIqimTCID0NNSEaLLkYDnQvEN1"
                  "8VGb45rkw4rqOnYaV6GJ2YACioYLGzmqZFrQ7FFAciIOiIIzQAAF4XqrYWe4vVBsVQUUGGOSbXcX14JZmdaYqKKIiCoa1NBDF0zS"
                  "OW7AEDTIwyGBNWY8ImffuJWy/n9DB6AMBHPXz4HIbqDEUEtccwTauqOKLOMMbD5ZrjmhnC9ciHmWlnscFiF"
                  "SyY2IsDPPLpyHUw4TpYALQIILSubgSg3+/3+/1+v98Pow83Ajh3lCBkrhyPYzJCnQIAAMgovA6uh9EJAABeKZVWTb/60V7qPRw9u"
                  "5P3C16lVFo1/epHe+nu4ejZnbxfsP4ga4RCkllZkYEAOTnnefRqj3JmH9iZ6QAhtWtTGgAAAAAAwhLwGSFHC"
                  "B6XRMWUR1nKslxCGD5DweeAwIEwXKCZoigIBdNuXW+u6XmVQBqiHoQyTBsxHNkLpmlrZ6uG48Prxeu6Zo7jw4cPQ/hDnTowOvIY5"
                  "pjhOq7rypEF4vTGQlhZ3fSY2+AgDOHWUYPHMMxFEsRQFDUNMVA7Hz7l4nhdwPAgwKFaUbW3qGCxcb1CZsJ"
                  "M8kpAaJjj9bgCwwBRmPCFMYS4rlcmBwPMkWFyXJnMdXDMCz5NJvMhMGGA2ohpOCbqmDghiE8PAAAAAAAAYq9qMbFxYIppZ2M6hmN"
                  "itXfwIddxvSbD9WEAo402Vgdq65jjamPrUAXEsLERAPV6TcJIAOBooXUEAADAsb5Pql+mBQAAAN4J9ZZPu/"
                  "wP45f1bp5ZsmuFdUK96tMu/0P7Zb2bZ5bsWmEPRHV1EDUkqbKiSFFUhCiCuV06Xs1G9VyLiZQHAAAAACCClHTIhfTAEMK3JKnVdm"
                  "IjsNo6ZtoYYmOjIlgdM0yrKXaYNqjVDodWPB6QA8K8rpnJQcJ1zeuagzkWqKckjAW9g+s14fUaOI4HUEYXI"
                  "TpqIkAM1Tu9jut4TciVMITJ8HodCWQ4YfQADOANoUR/A6NjXnPk9SKBgymYKphqWGzAYudxQK6LGQAA3kSYCJcdDm0xTNMiiAiqq"
                  "oIhYie2IoYQfkcA4ClghIT+Bpe3CDXtBNSRaasI9qbjmjm4Ei6OeRFM03DQo4cAiLFIunWAd11M5hWuOQ4Gw"
                  "hUgD8jBNXNdV3jNwQDAmEBHABgTEWBCWgCgowMAAACu49OHa7GxcYQDHAQoAP74JDM9PfvDL92dfFUybqQ9Osmwp2V/+KW7+apk3"
                  "Ih7oIaKDBUQUmRZGRlRU0QRe1pQ3VN5Q1SKidQKkXuiGAAAAAAIAsFdEIKLZMmAkwlyuWHBXaYIxWJioCA"
                  "UsIhLfKqKWkVMwKq2Zntcx8wxuRVpwpV3EW/RRyZeM2FWCsOEa3g9ZmbIMLQY5qwMc1zr0sFAGCMMTGskbXXMFAO1mmJgimGu5HY"
                  "FwJLEawIzENapAwBQFsf1Vjzy3QFzHZk7BTENW7W0VRxa1Cr2zGCrPVpMAQDAIGH1DomxGKG2aoM64TDT12CL"
                  "4rolxwGE0UN39IchwOvxOraYx+t4bwBdhE5ADTUxHNjZ22LYuD7NZF6v1e31zcx6zrEAKfTQU5eHAcLoXQwAANBiX0heAwAAoxl9"
                  "XQLY2gCw6koAAAAAwJi5JflldKc4cDAPu7NKAQAAANB9/7YUAAAA3vjE1hG/eISH7tv5rFmwJWx8UnWP"
                  "Xj186Hb2SbcVu6ZUSwQ11CIzK5AZqMgQaTcwymUaDxMWgKQ8nxgowoTvGRllZlE2ByJDep1kiMCIE+UBAAAAgIDwJjjo5aaInToq"
                  "ytXNJkNBGrxRElEWdZgihGYwiJBLAiKeyfS0hGkuioJQhMoSuMzrifT3D1OQMmGwWLh5ywBRCMhQ8o93"
                  "apqvqaryMorpq5x0LBQTAAEph2La2hoGlmn2FityDMLrGO1k2HS4PjSsrjAd6pDRJdE1kmsZxyOv445hcjDHcb1FHbp5aFF/dXoE"
                  "86GG6AwGkxNWEHOQAIxqxY/AcAxnFJmGJ1YBFRcA7xhC/zvtjPnm7M3up1AAMMTMAHIwn5W15st2SgAAABB"
                  "HAABDVEAEI6aaXWD0AYQcpaGbD1/DiJwhDDNMAgAoSgC6Edx44wDgdcETADRHRn+/9/ern6+ur+1+2d2c9XF1M/y93QAAAABz5/u"
                  "fBgAAAB7pNMoRs33saBnTJ2D0uEU6jXLEbB87Wsb0CRg9btdEVZFU1ZRRkYQkKjJkcBKGoBBZGYkIVLmatj"
                  "Wrg/II0wm7yQghJiWSBAAAABGzZJAgIkjJLOEKWVDK4/AJhyEMiIBQzKJMWCBOUQxJLCQJAksWzJQIREDTIjSIOAhhATgIPCYzx2"
                  "WROHU0DBGOBI6EeXDMos5pMQyj8SAW9RHUMOLINUNgMpPXI59myDDAFfDEIqN3MZhqbzHEECVwRwQAAOSa"
                  "DzyOJHMk4fjAY2axsTPV1lAbAYAf+k3sDkTFztRSiwmmIWAegetg6XowdKMwEQEAiqiomFaHtjaMkWgoBYC1NYDMdQxvCiZWB7Zi"
                  "b2JabEdz5HVdHPPiAbwMFgyIk+giEwDAWPSOdMDoBwCgG1aLAKD3/S0AsGO+VNLeqaW8tpS3+UVmUQAu3sj"
                  "U/B47Pgb1zr4gS7ISNzI1v8eOj0F9Zl+QA1npfEjVZYYaa0rVRNRQGWrImlA4ZjEcgHY9LcA4EAkwZjAbgKO7qkiEGCWRAAAAAAv"
                  "BEJJYNCIpWBKxZLBkKSUTxFmEAk0LAEdKEzEhBSZCmmJCiwsYDEIAZjBFgWkBTZiIQxxCBpimCBgOM2jQB"
                  "G6SLpaiysW0izAYAAC5wkCGB1y5BnIM5FNmCF0k6Bn0kYBPB5kjgWuYORKO12hXCAfAvBhIgCnUYicihokCqgKTSRIyk9cUTId2Y"
                  "kFSAwAAwGKk0vGFVPi8tTC54HhNcj1eTwVkwIi0LkXKBHXgARgOrgw8hmMekwECQ2YE1OkkobwNQBYRJnl"
                  "ri2G1SA2AEuCMFBHhtOCQGFAAiKOBiTjV7/e7fToicLYBgA8/I0JEbe2tpioigHcsJAMsiZ8AgAuwcgG2EoACIAP+6CzKkpRfTI9"
                  "7tbNDya/RmZQ5Kb+YHvdqZ4ew/zWFWguhfSWqoCpTlAWE3diQ2hvp0wIkujNXNRLCeKIYAAAAAMCBv2Zuo0s"
                  "BJbg8DkTw+MIwCAPKZUDoEgUWEfeCkoAQFJgmTEGUov0iCe1pGvYq9oaihtqiYo4DrjDhFcIV4IKZV2CuMEwyTBheDFNs7VUEBdR"
                  "UwFTAHMGBaSthCCwAXucxF9fxIddjvjsOVqc6EPc6mGLYMgmoAAiYgfC6yDHXAcOiFsfUsJiqVjF9yBwEAACA"
                  "pje6qBEmAvI7gAkvXjmOxzsdeQKAAQBUUNbBysytJu3F1ohFdRXJMVcAAGC7PGFxhSQkBPJYgAKeXkcIMqqNlemmODCwEdsIO7Bc"
                  "FggFgw4oIuzQE4QadIjBymC0xnhEg5BQBVsDh6JWC6oC5pYeM69hmNeBEQAAAB4JrdaYSBfbx+ys5DS/SGi"
                  "x57TsYPvYPTnN75qozqCqOlNZERTVJUqIPCezIGsMImlqDbVXjk54G8BQMRM3y4BiAAAAAJBgiuzGvaSw2COcUPAsKgwQtVLFCAX"
                  "MjE5kisGCZIk4oKgqJGEATADaK+JGBBRFi1B0EFqu6zGZD5yK7w5uMW46gNdkroOZTDjINWPlOCJ8jJ7ICHT"
                  "17Ywa4pepioEgZozVBLVrVvUp6wihFEbP0BZBDaymyjQRIY4Wp6b5bo4ClmwhM8OlruXD5FvIACRHyKeT3e6EEYKKhoTgnO3b67h"
                  "OKQIAAPir3b0QhhICAL2E4x1zzGxcR0ZmBTL9qCxGrjFhjGgCiH2YOhgDKmJ1YtJy"
                  "8xUAANWeUkgZSecbRxsRUxXt4/QEAOR4cVzHpw8fzDoAAADb26LUAxeXWn2M4NKBCQDoUMcAINMAGPK2yQOAifAxxggAAAA+KZ3V"
                  "Gs8Opl93kpyTI2xSuqg1nl9MnzetLicOuR+KTFRDGWR1VZCgOI+IyqoIMjIydNfoqBUj7I2ORdytWZAA"
                  "AAAAwGcIFVIOy7IChku5BIQGoDEORyB5hHg+SUkMFpICMXcoMEXTghIlQ"
                  "iAUo4itMX/FEAJfOFaddCzcisxAVuDI5C/BAaNwbWSGqmY1Wuqa6qt1FdYsDuaCmYGZFZiZH9fr0GEiFBWq4Sm2NmJVe9c1lSEBF"
                  "Lg52NV2TDBO43HCj2fCdUyAE2rRWyCAs4Au9QQnccwQqfhskEkGAAC8ziIQui0wGgJE2NKnM8J13MkY5nxqwUfou6OV0d0LMDwVw"
                  "LTgyyL+Ej+GKz80AAAAoBgiiJNi6+xj8W2q1alYxUCsgqc9uAg10OkoJT6yU6oYCBAAYHRFEAAAdAHQIgEUYbVPMI/NmPmU6jRQD"
                  "KvLdYsxZgD+2FxCl2VHjIAbORGNzjnjs7IRze9PTPwQEyALiQoUlQGC2M8D6B4a2gDjkw8gOmOPvoGFmN5NSqwAZwIAAAAARqNG0"
                  "ysYsTgPzUCEQgGPbxDyNMKwoAJQCIViREDcKiihCO3uEyIAGJRKChwPdciTpAyT6ODP5QiJiyJgGrSQVUsByq8mQcmUBD1LHlFhQ"
                  "rpERCgFAACgKRYpwNNkVKyGgGFYZTINPA7y4rThFo4ZOKTMgxkVJwwTmEy8gKIrjtdR1fV7UYEUARIDI0fx7TONAC3kxOjfGM6Ym"
                  "ExpYh+EtSpleWO+1p6ziSjXSooCmAZA/okWJjoAAAAAjsdJSrFPZ2dTAAHABwEAAAAAAINDAAAHAAAASEashxh0/2H/Tf9Q/1z/a"
                  "/9J/0P/Uf9f/1v/T/9ThxSNkAfKZZHcwvT9bk446gQtnFQwGkw88zQxMEa6wgUAkqSiKb0lYqgtKiLTxMTADHOsbcEDZm1ioq8n6"
                  "17fHM16LwAAGP0g1wOAGQAAAIBgyvQuAVIIB8Cnu8LjCWrwOJgd1o8nEhcDDFVkEmKq86YqAF7ZPEBJ42J7xIdyju+ubB4gpYuL6"
                  "ZUfSrWo+4esKqACKgURiahItg1YTZ3oE9W51Bx6RJw2sAAAAAAAh4LH03mEcIUcygFEWZbH53A5ABEh0qSIuCPOvgrZEaGFspgYA"
                  "AAA8apAKteLn8K1JdekzFHpUjEH8HoG8EqmugZMOSBPYoTVU4suGL2ipYZOnSLCKJigBghq4LU5Mc2XyVgEBoYJxFL1LmksY7X1I"
                  "6CYFsMYVG0NW8Pega4AACMRJkZG6KAzYbN1aDvZDk9YDRMQJDKBcxkAAABeBJiTtSISAuEL3V2/caEUAD3l/cT1UdBtEd47CaATY"
                  "AAA5l8C3vtLABCAOegkFk9j6hlTdRQagUCMdE2NlwJDRyUrsY6VUHkxOWWUhXnGcZ1uNPgARFboAyz0Xm8AEUyIY6K5L2MLIawsN"
                  "gACDIT5kTIdGGJYLU5FRI2c7lWkCSTXhZfVygAAAAAe6dxyPkcfmstFTnVHOrecz9GL5mElJ3s/kEUNkIGKskpQBEUlpuoa6ctkB"
                  "+iJpjI24ngAYQEAAAAAIGDBYSgFjxIenwFLkJKEFFKyEmDhiEpApsXZAcUEDAbNgJQI3URYnAaHVAaDmQEAAKyObK1iUWeLTF92D"
                  "m38+BTCiyuP42LIMQ8CxzFzXMwTRh8B43Q5NIQ8eAWFwMzj4G2Ti8ZFcgAEJhetHNcZCRYI9QDUtFinU7EiqhgCwKm3aABex8yDY"
                  "zL7oYU4RkCNMhGxYrEaVos9FQGYAQCA4WR0qAfgdDoB6FmMw4gIZyQLFdCFYdQDGP1+H0YYQQwdpqmK2IGlTAUwFzfkYODIhw/HN"
                  "ddjVWCxlDDXfeBI/VySEdFdiNTCAJSg6qC44iIrRUYLeidggE6tgQgAEAgXKCqLYm/YCDbiC1UrkEshOoDBAB7ZvIlUHHNQXOVBq"
                  "CSyeRUlS140a3sRGvlAZk0yRAnVWVGKjAxRGUzdSXmhh92Qk3iciCQAAADAY20asg7iCcEXgFCGAOpMEJBSMZtMMcUik45mOjVLZ"
                  "pwwcSFLOR6PB5DhjluXmVVDXg9mDnjADBNpgFl4XFytJEGCT8fkejw+JaNkARjcrYwzDoRHgk0Yh0RHKWW0ajhjznLYjSUxDK/Md"
                  "8cFM0MXKMZBXYdrsGEGRFJXrfBtHac4g2oqhNWgTPAUAABOoSKElcjjIqkQADrgzYrqMop5YWcni7RSJtA6qrWegui9kxuENayEO"
                  "C42dzyLXDABFtPO1NJABa37q0EHjB+yz5cgQ/QIT4ALk0ObCELMcSJEXRGM6/ZtpQi9AOPujcpbFJfpDR"
                  "H/TgwthqkIhpMtGMZQUIlGULX6rZiuB/B6DADAIwBpEgCSVQgA3mi8+5gyE3Tt01gRGbNovLqUliao7dMwvEGNVYlItLlhmdt1UT"
                  "2uMFGReNyARQjKAQAAAMQQ8GnrgM5huDEOGK4nLWBIuMItWURSVFZCEUI4DQBUXybOjpw6tBF7U896yhwn2j2K0c/EgAVcKxNWMI"
                  "8Z3LqejHpVW1Eb5kjIA1NpqN7orXSMevC6HpNVSNFhAkmOMDnmw2sq/UVhZipwcYDSb2AIQtRV7rgNoFy3SCwwA6ZDahcFYXG347"
                  "lwE/NVTKjELdYuy5eJm3qY4l8FBQH4JFyAGYWuKFcxn3INwMw1jBOGATpa1nunK8q03an3RC90jib0w40xMEZYUetcOt3odtA6Ot"
                  "IxwIXEzPyZogjSHCN2uJztxPSq73YIGD0cIjJhCG2ioxVogIUJjda0ACgkxuyQamJrb7EROxsdVbUs9UwGyVu81z48Kq00ACCyi"
                  "wAGQRgALGu8AwBeB+w0ZdKMjF9KFMjobjjSlMWkVHwqYRG+oagRRJK5xqaZ3l3eVElV6CyZESIkAAAAaDTKHTwifEIjQpuFoBBjM"
                  "RFSEhWyoNz3CkWsM6Tt1AkrFnvfzn7sygxqu08G9nYWBQtuLSEwxwXXaya6/RhaA/NiEvJ6VMqR6zoyrDbXU8UM2jHXY2vSp8w8"
                  "HkcZWbTHTCYH/CZbYyBXjqpmwJbGhCGsXDPXZ/geTrtyUIbRJq2maeN/YnoDtYjFWuJARAXTAiscRzIzM6mUokaLBpWDa1QSA2z"
                  "ZdBksXOgD8CBBjihLH3ywlp4YFqqHd1owTlDjlIMArNJpSxgLKzw1Xo+B40U2ZqOcUSIKymQZqsdydKjwiaw40pmcRVqGTWEFl"
                  "cIcGdYbQy/I3e4JY7MvDI1R2IuCTRVAt2uUAWLLjEhdpgurtZEItvq6sXWj03snCRNW2g/NADYxQIRnpQAp2w8sFGEJ2WP0SjsJA"
                  "N43nH1J4wAW8NA3nH1JcQCLAjwcmQuCgKkyttcuKZeoiSASUiMIAAAAZDERUQoolxNikjQtzhCnQIEIBJRoOaGIf3vTfgYnJqzTW"
                  "WY6zUSsjYOvKuD1sXiMqslr0rhIOK7jRlgkVGcYsTos+LAwC+qMAByG9kcbIojamYKhIipOY3yEt3gAxzETJvmUueY1AwDXNeSYy"
                  "dGCa5hDy+uqvSlKG6jYmIYVcwSO48U8hmSYyZGRHhdk4y2ZYCJRIsfoaYQHAyMeiAQ9nKsI8oY4kxOIEILQlVBQY0BAAoD2m4uIb"
                  "sWRIxc8gWu0myBaGsUowfXXk9BX+4kLKYIBTgM4hYGO6p2WDgEkxlCnjkSve+O4tAkAABL/7dSQZsbc+VZbCbmdQasaeBENAOj3G"
                  "RMZALlKJByPAADUxM5qihoKQGInJgBgbHkCKAB+N2wpBh7I6TIXTuZu2FIM4oEcLnOBZI7MYJGnNDFVjZWuVFwkZopbDBIAAEBE"
                  "TFzoQVOgaBYRCIWUqDglIhCIiFIUEaXERYmIOrCooPZWbB1Xi+t6cOV6HC8CIS9mQEyhbhzjPWOooTC5Ji+YmUxYh4aCBgzRGwp"
                  "WmaoAouDPdxlEGEON+e4gmXBdjFoEQgIkTl1yhVpFckb2CEl0Ou/IHOERyAwh1wWZDwckTKQEIKz0pgQAAhMbGQowUgZiBkm+dz"
                  "0ACaxoLwLBIfVO/fUyIlhWARrJjayiTyIkXIDOM8K4/GFyE1ZgVqblQ11wSfg4M55AR51jYoTpcXIMUb91xI7QoQdMJPrHBGijj"
                  "3C08L3YETVl0OeA/F0BAGAYHAEAsxkwjwtmZgmAFo/rMdasMTEBZ0xMoOi9gMjhpwBIhfUCnjccaw1yguphjce84VhrkBNUD2s8"
                  "7WbS2rmqq9vJ2BWHZcYNAgAAAECcmaJEaZpFxIlQTCwOsbU4YWOxmo7ZGAaO4RA7MR1XHKhptcWwE1OcUDHFVDFU8ChcXMSYTIS"
                  "xqEdEZFuFhLxORS4UKnBhdFFQPYWbkvl0XJnM5DrgMTArTLgCB7wyAJMJCwUiNtGFARwcBObT8ZjAXKBdOebT43Vdr8eHTy9gyA"
                  "UXGeb1AgLXxKHTh791tTphShMRY6VnND8VJ6I2gWmE5vXS2IRGRA7G6Pplchz9iRiatbSjQw/o9RG0BOPhJt+EXHNrC6QCXPMCI"
                  "EOYERci0McYOkaI8f8OROg4CHSghUEXiAC1VNB7E0rHWXV0GBecjhRMgPYsPZ+tXz8AAORpKHpnRgT4PxUCg"
                  "daFLn1bfpig8MvGGe4AAICpXi8pT3291qQDAAAJPjeckw9mQbUYEjKGueGYYpATxLywPV+qRESUEBkZ01Rd7ZVLrBNmEzsAAABA"
                  "MpGQzAxIFpItToiNvYkVi42TDsWBGuKEwDgMtoZjlolJG9/leqTFu/hYLbhrsDUFi+2gE4PqNFSm66oco14twjpVYgIJx4MrJ4J"
                  "c64CLFRzHXMnA6whruS7CDNerpnTwllKYBMhkOkAfHdGKQDgOXoRg3UuvCqomZ82ka2hluODUte/mQC3fQSZMRKaKIioGQ2O1q"
                  "NbYwNDtG3YREyAASUQxmggzACoi6IUk74JHXC4n0XlE1ofNBcawXB/jNOd76rjxMMSt30R2vaduv/TDcquhxZXaMUwyR3gRYoUA"
                  "R0fpACapOgZjAMCCkyAl47SOQlQX9UbPrclh/sCJYACWn7Vu7Pf71cnkAQDERfpnLAC3RVrsh0GH98kRxlNG/F1AN2RXSareh0"
                  "aDAAwvaVKAkwA+B2zFB9EghsWC5zlgKz7QQFjA87EHkLpzR+7Estuuq7vCLnSOscwcAAAAQNFCSYHAJaDFaUlKICYQgxBi4mJiA"
                  "C1K0SIQZZoWJQIxlEOMiNC13a7A8I+NjcWwtZRD0/HpuI5MjvCaYxg4dBhVTIVN77SlMy69/gbXoF5YyVxpkRz5hYHAXCThINdx"
                  "MDwSLua4huR1JJCoMxiknUEnYOUAhrXVOLi45jWTj7HFNWGOPGocAzOxMrN0DWQCQxi4eB3HxQHizLNywJKAOo0nkdKAcek9a+t"
                  "tYcQ2wQI3wwAAxngnwSoMHDMzxytkDIWprhvO99dwNHc6vccsXRczx8wcr3VjHLH1O0rtnxB63sscGhAXHdCDtHtPCXQMhFAn0Q"
                  "GI7FSPk6M2dPvdgVupidB5eFdkq9M3Af3YoJt6QJKOEHCyp4ABq0sII8C1Q+oi6RwPj0SuwCfI9SIAHjcsqQazIHoY4SluWFILdg"
                  "Je4OmYEAgOMxwGCEBXJ00nhuOkkokbJAAAgLioCE3R4hRhSgChi4iIikiKijBFCcULJhCKCsWZiHCFuyjEiZAZbpQog1BgIiqk"
                  "aQrPKryGa8gVjrwIk4thgCRzzU1UbWxsmocJkPBccekpoJQfUUgIrCJK1yk9gMl1RXL6MHoD4hkVjHNFYYWBImpdNILVUdANYb"
                  "GI+S4P2CBj5PV4MNdk5mBkIDBoTLOmTfR/pze6Rpu4rWPwyMAMMFGnii7jVkOCYBUlMpGNNxPDCEx3UUfOMMzxmg6xYM4viYQWQ"
                  "ykoCaVMMWuMD+l9GL8jtYx0wEVIS4uhGUJP1gZCCIOOoEVYDRgyr5mZURKJDkIGPkPr/shgABdMKPorPG8xRIFWCmF7ROs1NMAw"
                  "wbswp35SMgl5wpgBw3y5frcAAO5RAZ42TC7GyEOjj5elNLKHtGF0MYgJurhaF03q8a7OShARqchMZ86cOU81OVd0V6mYjB6K5RG"
                  "QAAAAgCQ0MEsI6sIFKXDJkiIiQtGKifLpycL/qdOjOVkOjLR3Nm3sdq2qatnFV4pTUdT00l86gWIRFNTE9QjDjIIwSbByTQ4Yrhz"
                  "13GmBQxfhFARxAkVQVBW5rr8Q5mJWt0LlxBSWFpSZXMegNPNiDoChel1lNACvYZjjmgDHXA+g0ooMHEamoYDxMsdMFsKnUEPH3D"
                  "bR6PXRFLpI5gAqkWRQwcBwyjh4FJjjQ0NGWCyRO43sAacOQ7ikYB1UbzLJKxNGI1zXdjAwsE9nZ1MAAYA1AQAAAAAAg0MAAAgAA"
                  "ABdaUsxHF7/aP9I/1T/Zf9o/2VCaGv/Yf9P/2xFSERse/9GhzM8e5fRoM+b5OAGfAv2HQqqOog9JsfCj3TjREdf7JhGeAIAhCGA"
                  "s/3wAwAMjwBAC7pdHQBPIwHifACATdHdiX4sBayk0G+19VdyEWOOLXK8AdCFWC0f5wAAFOAfPgesvcRQqFgV4CluWGoKTKAt4Ol"
                  "up2ZJIMvISBlWHnO50fWUcDoWmck5igUAAHBjumQpndi5qSAu+2RKnKK5XMzEtEIg06kf66Tfx4ZMz1Q3nfoNprOHC5h+kTtLFa"
                  "UxhFFYm89qYmLZhKF+h0YQywuvFabB5JphZqURU8W0hjYqiF4fhyuXnXqXdRZMigCBCwaGzNaIAWzlgAsmxxwhU1H1uOPC4qUa"
                  "PWDxURWwBwS/g0sFv5AE6KC6KF8Anowg3yMtWjA6qg8HygEwOinpdrtjYsJgSEGGwEiqi3IwZ4lsKElRsRDvAsYKwBXmtBk2tb"
                  "C0ZY1ZXUuPMGGCqMuHp1XHDX3UoC+UX9zoGRB19Demu"
                  "hXgYyIYihW3GykLE9z3UsNEbUEMd2aKFXC69HrP5n+s3moUYlwUXA9esFLvXI+v7UVde0fwAADUYjKA2KsJGswMFQ6tBX4CAIDM"
                  "l1N4z1MAAAAqGQCeNvSuBCZgBU9pQ29KYAJW8HTXUsoUGSgzDWbMXKnQADGacdErikwJSAAAACmYiEERUkZJEKmgIFrG8BYsrgI"
                  "qQQkpiNIQgoWEOCLKMNX0b2NvYzdV1M6Yzr8gIogDm9ZCTfOJmZCo5RaToSEpnI50Do0jQ4mLuCwweuqE3iPz5Ua1UONIruPhD"
                  "fWhHowMniJMJIs+r"
                  "Nc+UjRohCNPrtYiRLGxmphYta2KPYNxwqnz3BAfSR8+r5vo6BH7ITRKPJgMw55pYxAjtzXdYUtYOUlsOwEPjisZOGZGwknTpdBI"
                  "FnEBgxW45kCnII+JFgUAnjHMZcoLGIfUpWMggzitIVayXObeOyO49pfWMeKET0sAIgghvjs5ZCDUqW+gI3QB/jrBrcgBIbaerbW"
                  "Y0DEmnJkAACsA6Q2wJcNud1FAB+MQ2PmwhiVkBQD+NuwxBjlBVy+j7elt2GIKLKj1Mm3PhwmwYs6ws1cd1+biUjKOMTcBAAAARE"
                  "XFKFEWEQhFaTFaBJSYQCgUF6NoAYQiFSIQMQ2xsdpYbKyG6ZitgTqy2hoDajVtNXyZExYfJhjcFq4Lo/YiBlAwCmXUtWSuDFcmj"
                  "xkh3iCUEHPG47pIAklUBSbXQym55pSOaBgbYtG7XNUnRN7O7SOot4ekOJjHycaH45rJ9el6TUKMIRfMNa9j7UEIugkBwgdrlTE"
                  "JYRh3hgQCD4C8DjJkVrjgyFqiixylBs4ImGVZRFhpqC6Kl5cybwTJ9CQi4zJOajqANYToGaqJAyAMYQv4ZU64M3TrKELHDYHpi"
                  "dhtgTtWIXgAIGtHONjqd2vVRwIAxlAAoETnLWCKxCC6BXQ6AiD0RyBIkQkCFgCEsoTQB6ByY2wrkAmgTSbzumo8bcity2wT4AC"
                  "+NmwiBbtMOg9jeF4DFuGDaSY1Xmw7gN4VKgAiIImU2zEBU1XprrhOwmYsdiAAAAAwRvhcDpfyKBVwuVyGAEIxoZtvQjdJAcTFB"
                  "OI+EXeVSm5lLkogpKUeVnjkuq4Xx3XMmfD6cByzWonS8RjBIqCjq7DAgCNhMoEc36xgMsRFIsLKKPABCwEADqUu0oP3cKhH+Ax"
                  "A7IjucHffIRFg4FKYTBgeUo5LzMp8un6P4+DDIzMcV+b6njKB2nfHGmABk0G6XlgwAHYKHxFdz/fSgoOFxpQsgHJPDqlT364nH"
                  "BXXEhvHAVOlBMObCAfXJsNEW8VNDAHgCtVHTXsYoyNh9EQPco1I16PfOos28UYwlLBMdP7qnBTAba2w25wMGRTd9jxoW/0LD8AQ"
                  "qtcXKXDqIYsjEgAgwm+MIGhxJJ1HG0DH6KIA2l5GaCOGjt+N4E7qRgZAqCsiwrsQmRFAyDNdM8DlOOZeAF4HXLwLphj0eSFne64"
                  "DTjFFZSLq46XIYvB0V0RVCaQoInfFkLNLOVeVuE4sZjIHEgAAgJmVkBAkHRwAgZhAjJZKQGZHjBrIgPHZFvNMi8W08cHq7tooZ1"
                  "/bnTplsEyvk2IyOF4CJZFLDV+EEnDwpfTQqs3eexZGggtd4arG4ZXxXqLMWaquTbRJGLJIb4YBdM5L6XJGxOkrcoVDLqaKnKmDH"
                  "FHHLfYMDEjmhCAXr1TKkXkC1Bi0F5CwRsd0gHoU2T6dggaYyJ0ALvh+3QpjABFwHKuw3wDovfPSTREWXBdhIe6UxALG+62jzGeQ"
                  "04qVOSgC5EyahRCl+cENZIZrYG6lHFm03BczCsVIO1pS9"
                  "MNEh81Dp2s3pv/aE7kJo25ZBeT4pml0gTAuF5abHe19EskfAfg+TDuffRgA0NuiuNGEEfjlebmjrE5hN/cBZ0I8SQ9wOket640+F"
                  "iaiT859USQNpVU8JMgANjZ0ySTjIuACT2NDF10wIxAe4OmuqqEylFkZFVlGWZWZu4c4t1gptZWpvK6EUyUWkdlBJAAAkMYshYwa"
                  "HkcRRTlLGAIx2lOCEiyniUAgaW6iss8SZevVSrr1uvIalYvhV+H6XY/5I0tvxe+4vskAmWsh9R3utFYXWR+yB+K9uTrjhI3Oul6"
                  "dRKRkRhSxyOgsOYim6ruDEAioHRctK3dGQkYZjRPLZiPqbsZ316ha6WtSm0mL82GyBnN3TMBMVDHJwJEhOWK1MnARAw4K89uYGQD"
                  "EI5TonZ5SXRgAOgpG4TLE0kk9YJHApSNw9jA9nTBSHL4Sa/TBpHTpQupIdUSoM3JIT6NvLJm0AteV/JgrQ2wAHWGSQLgVkDAMlPb"
                  "qcuQyI5oG1LsXYDxvADWwilwj7ST6RgPMyhMDFAJcSDO8Y4LuqbU6XS7ekbjouHmmAwCEugMAAIy/DQA89rVFBlDIcLKVgAVc+UQ"
                  "CDBfOqdq7+gkMSOAcdf9k1ZIZEcwrIRkwtMikFa8WOYBv3mUY9FGF9KsIEDiMDnUkmd2DmqD1wTAcH/LhFQCs+STkJIWbf+i1noR"
                  "Uk8LNa4RaNStrliIy7ZmnJZ6KioqqiuB2ZkveACC5lSARpEUIHQGhRMBlROiLPgrqdPjogN2JQIRiBgD4pYZpa2+KQ78cs9rMZCZ"
                  "TzafreLRabNW0cYBiiMDvAXwBBb2KvZavEyjk+wIKepX0LF8nqJBv1ayhrChFxNjsdKRpGaG6jIzMVEZlDWUEIA3SdddcSYkTWjQ"
                  "FFAsYTACQKMZO1oqYJ2Tbmf3GdFJMw960FYemjWlBDQeOY1htBFARwV4cDQTZkZIIGjYUGgX/A/21UBF4jsKEUhJBf2C5eioYLxB"
                  "6aqyuijIjK7I6iojILMuK6pBFBuw74jgO7aoq9BbPbaS4GiAwEgAAkGBJxEzEIEkEFoIhIKWQDAh3SuiC0KHdxMTFhAIxOLJV1wQ"
                  "MW8PE1vTl9eEZxxxhrmMbrx/MS0UeK9xSwuXSMUXQbhgycx0Mp3Tw4ZUwD2ASItldCUp1C2ktjhwrXjxkUcoMBh08CsMStQIZnQD"
                  "IizFhKHXoMJJDBhc8JcQT4vVOC2F1PQgHGRYmpBsjY2hA5nER5rjCVEuuFwGYXKPfDyEIWsTohzgCHVjWMyIk478QRFHTYme1mKY"
                  "gFluL1dZG1c6hYczUsDHf5dN1VmsPXhcHr2EeA5ODQBYpwngdgH4bQXdo3T66QMAEwshJAACEwyJ1Obi+zPXg03G8clwLdelg6Z2"
                  "hrgBcj5UOXvn06XHleAsAAIAMAEkAdyjABX42lE6HPoLaZ1POlTwbGidCjaD2kZwr+Q4VkQA4ogN7WiemLlehh56ejBAssocIkyQ"
                  "AAICQb4yDR8GCoeAR0CK0UITQRETANGFRyG7sC9xlSkTSjRIQERG1ADaIvxETVfXU8GMKID6iYpp4BMIlKmBQuH4TQBuSNXhFbSC"
                  "TSTLkwyMQwszMgo54Z0R0hpQ0AZ0OnuIiw29a8ABmGNJkDg4e4YTeqbNokeh0xmnC5y0gpJ5Bj1BvPs11ZEmzJMbz0G0v3YFhwK"
                  "JTTyIc6kOJq+d5GOFVDZiECVpHgA7oATQoo97QCBCXHhkmB0wy5NMxJK8Pr+QKcxw1bQzDtLG3KFZMBXkNC5lkEljwgBMUGFoAAM"
                  "YagAkmIqDbIQCEgF8Ljhzp0RE2AwAAbSa/ZIXJfHMB83oRAAAAafi2AExM4JxtN/DESd8CtKpCoqoscAA2BjReBHlA7Dr+HNEY0H"
                  "gZmCD2ncGXE7prqIrKSFkZkRk1tW2cs2HvdjbD0cRyrq2T6rCxiakgAQAABKQRJAlmkkJAKBAVF5cKZFFxSkwoTmgxIRGAZjEKtC"
                  "glJipmY2uLrWKI/WiYtn7Zy+tWveCVuSbHdTBz5XjNdT2GZpl8RujoCNPweHEwMGGYzMzxLEshzDGZLImB15OIsBEYhvB5gsDME"
                  "eAHiGJoD07S7dBLmNetmMcpkSOvJGRmuOA1gdKPvI4jMzw+HT2BsUB1ZqLRRh6A4eARZq6FAN8SsJ4ajPLrBOBC54kTicW7LXMg"
                  "sZANqjM90+ucyIQE+H1DFQcMemZmH4mh9q0wc7wmU+kDx5UXMQVggMzpNHovTChAe/EA6feMuge9d3rJlADvHSxK6Mpo0EYgjT+"
                  "lN4DLlZ4t1YUZJwBdgogOevvB"
                  "Vmv29EsXHcYEAIb4qOJcu5TvtVOAaYiBALGE0ykWcDNs+VALJFMcp9F1Fk+wwJmi2BpdTNSsUUrBItgBxJ6CAOCx8ID52yQZjpn"
                  "XdV0cwlCG2DCmqaY9hnRcJ6cWSr8wmTurPgl89cRIzKBFcO739eUTHFGDJuXU77q8qhII6hA6APgEAp6Qo7xFV495hVEj1zVWI5K"
                  "LtbUbJY/jlQdd0/cyGKjgGIbvhVNcCwBs+VDDUEANE7nG1o6SDAnUMLFTeVERQTLhCAcQMpQPwmGZLNoaoa4IXSj0kbpjcmOkR7g"
                  "gzG8dydAbPgixyHjNx8yaACT9fEbDNTnZ7ZPPa0FWTGfW00NVR9TbZtbUtiluzGZGAQTQv7AkEoSmiIebhzhAIABlEHq60XRvRY"
                  "QoY0q0EDOtDqfMqPamA79tpsPWCccc88ehQ6ti2Nk4cGTnt8UUtbWO9j5WHEdmHh+7C9wIRcbudjS9CXjM7kaocWm3CfsmIKfZp"
                  "vtHUVaURZ6uy8pxxLmzR5SEHNsXspeo+DDzw4x9MaFSHm6tIyWiFempO9P2dtOMiWnTObTzx19O+Msvi/htb6NqsZ/O3s7eMiJW"
                  "j9dTFq5AEM9w6Lh/X076mm6aA9sCSIoJAHo13PxwXzBABvcU8c/u7iQHUUTgzNM0Wo1dlmJRzDKZSAAAAAAwJwLO5a/4yl+5v++H"
                  "209u/94v13Pn59nDcvtSL21xLUpndfvy7VA5//w4f27LOL795PYo+f7974+SXupFFhk591zTOL79eH98nts4eItR07Oe9axnPeuZ"
                  "E0CZ27tPW1u3OzOKit91rOe+1K7jFmVbZRyPx0AxaDGNyYnJp/7+eXL7yaB/9H/Pku1wvejpgenJsPvz+/+mrSgjkevxerzVlbPI"
                  "moxrYbKeY8BJsnrRY89KMmG12IoUvs3b7eanpycFiVHdouYWg8lsNmt1FS+33+9zIiFVOq5jbU9nZ1MABYA2AQAAAAAAg0MAAAkA"
                  "AACfd/skAWoWAKqz3++H+/T0pGA6hrVD9XUrrc4zc3Nzc/r9sOZyIGq6bDnpYwKensDQ9y/K37+cAFtbW3TudhWOtwZzlstb/X5/"
                  "a6vf72/x5+fm5nB6slBlZ3Fcha363d5ut7u3ni1rLoPf728l3KcK")

        return record

    def test_upload_duration_and_remove_record(self):
        url = upload_record(self.get_record())
        self.assertTrue(url != "")

        duration = get_record_duration(url)
        self.assertTrue(duration == 1)

        res = remove_record(url)
        self.assertTrue(res)


class RecordsTest(TestCase):

    # Tests set up and tear down
    def setUp(self):

        category1 = Category.objects.create(name='Leisure', maxTimeRecord=60, minDurationMap=259200)
        category1.save()

        category2 = Category.objects.create(name='Experience', maxTimeRecord=60, minDurationMap=259200)
        category2.save()

        category3 = Category.objects.create(name='Tourism', maxTimeRecord=60, minDurationMap=259200)
        category3.save()

        config = Configuration.objects.create(maximum_radius=20000, minimum_radius=20, time_listen_advertisement=3,
                                              minimum_reports_ban=10, time_extend_audio=3600)
        config.save()

        user_account_us = UserAccount.objects.create_user_account('manuel', 'Manuel123.', is_active=True)
        actor_us = Actor.objects.create(user_account=user_account_us, email='soundgoapp3@gmail.com')
        actor_us.save()

        credit_card = CreditCard.objects.create(holderName='Carlos', brandName='MASTERCARD',
                                                number='5364212315362996', expirationMonth=7, expirationYear=21,
                                                cvvCode=841, isDelete=False)
        user_account_ad = UserAccount.objects.create_user_account('carlos', 'Carlos123.', is_active=True)
        actor_ad = Actor.objects.create(user_account=user_account_ad, email='soundgoapp2@gmail.com',
                                        credit_card=credit_card)
        actor_ad.save()

    def tearDown(self):

        Category.objects.all().delete()
        Configuration.objects.all().delete()
        UserAccount.objects.all().delete()

    # Test cases
    def test_crud_advertisement(self):

        # Create advertisement
        advertisement = self.create_advertisement({"base64": CloudinaryTest.get_record(self),
                                                   "maxPriceToPay": 500,
                                                   "longitude": 35.23,
                                                   "latitude": -5.34,
                                                   "radius": 100}, 201)

        # Update advertisement
        self.update_advertisement({"maxPriceToPay": 600,
                                   "isDelete": False}, 200, advertisement['id'])

        # Update advertisement delete
        self.update_advertisement({"maxPriceToPay": 400,
                                   "isDelete": True}, 200, advertisement['id'])

        # Get advertisement
        self.get_advertisement(200, advertisement['id'])

        # Update listen advertisement
        self.update_listen_advertisement(200, advertisement['id'])

    def test_crud_audio(self):
        # Create site
        base64Value = CloudinaryTest.get_record(self)
        audio = self.create_audio(
            {"latitude": 123, "longitude": 221,
             "base64": base64Value, "category": "Leisure"}, 201)

        # Update site
        self.update_audio({"category": "Experience", "tags": []}, 200, audio['id'])

        # Get site
        self.get_audio(200, audio['id'])

        # Delete site
        self.delete_audio(204, audio['id'])

        # Site deleted can not get again
        self.get_audio(404, audio['id'])

        # Site deleted can not delete again
        self.delete_audio(404, audio['id'])

        # Site deleted can not update again
        self.update_audio(
            {"category": "Experience"},
            404, audio['id'])

        # Create site
        site = self.create_site(
            {"name": "Escuela informática", "description": "Aprende informática en tu lugar  favorito",
             "longitude": 35.23, "latitude": -5.34}, 201)

        # Create audio in a site
        audio_site = self.create_audio(
            {"latitude": 123, "longitude": 221,
             "base64": base64Value, "category": "Leisure"}, 201, site['id'])

        # Delete audio in a site
        self.delete_audio(204, audio_site['id'])

        # Delete site
        self.delete_site(204, site['id'])

    def test_audios_site(self):
        # Create site
        site = self.create_site(
            {"name": "Escuela informática", "description": "Aprende informática en tu lugar  favorito",
             "longitude": 35.23, "latitude": -5.34}, 201)

        # Get site
        self.get_audio_sites(200, site['id'])

        # Delete audio in a site
        self.delete_site(204, site['id'])

        # Get audios to a deleted site
        self.get_audio_sites(404, site['id'])

    def test_like_report_listen_audio(self):
        # Create site
        base64Value = CloudinaryTest.get_record(self)
        audio = self.create_audio(
            {"latitude": 123, "longitude": 221,
             "base64": base64Value, "category": "Leisure"}, 201)

        # Create like
        self.create_like(201, audio['id'])

        # Create report
        self.create_report(201, audio['id'])

        # Listen
        self.audio_listen(204, audio['id'])

        # Delete audio in a site
        self.delete_audio(204, audio['id'])

        # Create like in audio deleted
        self.create_like(400, audio['id'])

        # Create report in audio deleted
        self.create_report(400, audio['id'])

        # Listen in audio deleted
        self.audio_listen(404, audio['id'])

    # Auxiliary methods
    def create_site(self, object, code):

        token = self.get_token("carlos", "Carlos123.")

        body = json.dumps(object)

        factory = APIRequestFactory()

        request = factory.post('/site/', body,  content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer ' + token)

        response = site_create(request)
        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def create_audio(self, object, code, site_id=None):

        token = self.get_token("manuel", "Manuel123.")

        body = json.dumps(object)

        factory = APIRequestFactory()

        if site_id is None:
            request = factory.post('/audio/', body, content_type='application/json',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
            response = audio_create(request)
        else:
            request = factory.post('/audio/site/' + str(site_id) + "/", body, content_type='application/json',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
            response = audio_site_create(request, site_id)

        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def update_audio(self, object, code, id):

        token = self.get_token("manuel", "Manuel123.")

        body = json.dumps(object)

        factory = APIRequestFactory()

        request = factory.put('/audio/' + str(id) + "/", body,  content_type='application/json',
                              HTTP_AUTHORIZATION='Bearer ' + token)

        response = audio_delete_get_update(request, id)
        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def delete_audio(self, code, id):

        token = self.get_token("manuel", "Manuel123.")

        factory = APIRequestFactory()

        request = factory.delete('/audio/' + str(id) + "/",  content_type='application/json',
                                 HTTP_AUTHORIZATION='Bearer ' + token)

        response = audio_delete_get_update(request, id)
        response_body = response.getvalue().decode()

        self.assertTrue(response.status_code == code)

    def get_audio(self, code, id):

        factory = APIRequestFactory()

        request = factory.get('/audio/' + str(id) + "/",  content_type='application/json')

        response = audio_delete_get_update(request, id)
        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def get_audio_sites(self, code, id):

        factory = APIRequestFactory()

        request = factory.get('/audio/site/categories/' + str(id) + "/?categories=Leisure",
                              content_type='application/json')

        response = audio_site_category_get(request, id)
        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def delete_site(self, code, id):

        token = self.get_token("carlos", "Carlos123.")

        factory = APIRequestFactory()

        request = factory.delete('/sites/site/' + str(id) + "/", content_type='application/json',
                                 HTTP_AUTHORIZATION='Bearer ' + token)

        response = site_update_delete_get(request, id)
        response_body = response.getvalue().decode()

        self.assertTrue(response.status_code == code)
        self.assertTrue(response_body == "")

    def create_like(self, code, id):

        token = self.get_token("manuel", "Manuel123.")

        factory = APIRequestFactory()

        request = factory.post('/audio/like/' + str(id) + '/', content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer ' + token)

        response = like_create(request, id)
        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def create_report(self, code, id):

        token = self.get_token("manuel", "Manuel123.")

        factory = APIRequestFactory()

        request = factory.post('/audio/report/' + str(id) + '/', content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer ' + token)

        response = report_create(request, id)
        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def audio_listen(self, code, id):

        token = self.get_token("manuel", "Manuel123.")

        factory = APIRequestFactory()

        request = factory.put('/audio/listen/' + str(id) + "/", content_type='application/json',
                              HTTP_AUTHORIZATION='Bearer ' + token)

        response = audio_listen(request, id)

        self.assertTrue(response.status_code == code)

    def create_advertisement(self, object, code):

        token = self.get_token("carlos", "Carlos123.")

        body = json.dumps(object)

        factory = APIRequestFactory()

        request = factory.post('/advertisement/', body, content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer ' + token)

        response = advertisement_create(request)
        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def update_advertisement(self, object, code, id):

        token = self.get_token("carlos", "Carlos123.")

        body = json.dumps(object)

        factory = APIRequestFactory()

        request = factory.put('/advertisement/' + str(id) + '/', body, content_type='application/json',
                              HTTP_AUTHORIZATION='Bearer ' + token)

        response = advertisement_update_get(request, id)
        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def update_listen_advertisement(self, code, id):

        token = self.get_token("carlos", "Carlos123.")

        factory = APIRequestFactory()

        request = factory.put('/advertisement/listen/' + str(id) + '/', content_type='application/json',
                              HTTP_AUTHORIZATION='Bearer ' + token)

        response = advertisement_listen(request, id)
        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response.status_code == code)

        return response_value

    def get_advertisement(self, code, id):

        factory = APIRequestFactory()

        request = factory.get('/advertisement/' + str(id) + "/", content_type='application/json')

        response = advertisement_update_get(request, id)

        response_value = json.loads(response.getvalue().decode())

        self.assertTrue(response_value is not None)
        self.assertTrue(response.status_code == code)

        return response_value

    def get_token(self, username, password):

        factory = APIRequestFactory()

        request = factory.post('/api-token-auth/', json.dumps({"nickname": username, "password": password}),
                               content_type='application/json')

        response = get_token(request)
        response_value = json.loads(response.getvalue().decode())

        return response_value['token']
