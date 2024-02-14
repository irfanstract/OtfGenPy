import fontforge

import time




if __name__ == "__main__" :
  #
  
  # "J:\Dev\fontforged_out_1707698135603.ttf"

  f = fontforge.open("J:\\Dev\\NotoSans-Bold.ttf")
  
  dts = round(time.time() * 1000 )

  destFName = "fontforged_out_{0}.otf".format(dts )

  f.save(destFName + ".sfd")



