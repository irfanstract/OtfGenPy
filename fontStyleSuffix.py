
import collections












#

from otfSpecConstants1 import OTF_ENGLISH




def fontstylesuffix_str(weight: int, italic: bool ) -> str :
  return "".join(fss(weight = weight, italic = italic ) )
#

def fss(weight: int, italic: bool ) :
  yield ""

  if weight == 100 : yield " Thin"
  if weight == 200 : yield " ExtraLight"
  if weight == 300 : yield " Light"
  if weight == 400 : pass
  if weight == 500 : yield " Medium"
  if weight == 600 : yield " SemiBold"
  if weight == 700 : yield " Bold"
  if weight == 800 : yield " ExtraBold"
  if weight == 900 : yield " Black"

  if italic : yield " Italic"

#




class FontFsSelection(collections.namedtuple("FontFsSelection", ("weight", "italic") ) ) :
  #
  
  @property
  def suffix_str(this ) -> str :
    """ Suffix To Form The Full Name """
    return fontstylesuffix_str(weight= this.weight, italic= this.italic)
    
  @property
  def sb_str(this ) -> str :
    """ PS Intra-Family Sub-Name """
    
    c = this.suffix_str
    
    if c == "" :
      return ("Regular")
    else :
      return c[1:]
    
  @property
  def fnss(this ) :
    """ for OS/2 """

    c = this.sb_str

    defaultFamilyName = "My Type"

    if c == "Regular" or c == "Italic" or c == "Bold" or c == "Bold Itallic" :
      return ((defaultFamilyName, ""), c )
    else :
      return ((defaultFamilyName, " " + c) , "Regular" )
  #

  def __str__(this ) -> str :
    return "FontFsSelection(suffix_str=({suffix}) ; fnss={fnss} )".format(suffix=this.suffix_str, fnss=this.fnss )
  #

  def ffgeOtfNameTuplesFor(this, familyNm, / ) :
    ((_1, o1), o2) = this.fnss
    return (
      (0x0, 0x01, familyNm + o1 ) ,
      (0x0, 0x02, o2 ) ,
      (0x0, 0x04, familyNm + this.suffix_str ) ,
      (0x0, 0x10, familyNm ) ,
      (0x0, 0x11, this.sb_str ) ,
    )

  pass
#










