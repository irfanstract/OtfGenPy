import fontforge

import time

import os



from fontStyleSuffix import fontstylesuffix_str, FontFsSelection



if __name__ == "__main__" :
  #


  dts = round(time.time() * 1000 )


  ffName = "Type{dts}".format(dts = dts)


  class fs() :
    #

    def __iter__(this) :
      for (sW, sI) in ((sW, sI) for sI in (False, True,) for sW in (200, 300, 400, 600, 700, 800, ) ) :
        yield this.singlet_init(fontforge.font(), iWeight = sW, shallBeItalic= sI )
    #

    def singlet_init_notdefglyph(this, f: fontforge.font, /) :
      #
    
      glyphSk = f.createChar(-1, ".notdef" )
      glyphSk.clear()

      pen = glyphSk.glyphPen()
      pen.moveTo((100,100))                 # draw a square
      pen.lineTo((100,200))
      pen.lineTo((200,200))
      pen.closePath()
      pen.moveTo((100,100))
      pen.lineTo((100,800))
      pen.lineTo((105,800))
      pen.lineTo((105,-350))
      pen.closePath()
      pen = None

      return glyphSk

    def singlet_init(this, f: fontforge.font, /, *, iWeight: int, shallBeItalic: bool) -> fontforge.font :
        """
        init-es the given `fontforge.font()`.
        """

        # f.fontname = (
        f.familyname = (
          ffName
        )
        f.fullname = ffName + fontstylesuffix_str(weight= iWeight, italic= shallBeItalic )
        f.fontname = ffName + fontstylesuffix_str(weight= iWeight, italic= shallBeItalic ).replace(" ", "")

        fsD = FontFsSelection(weight=iWeight, italic=shallBeItalic)

        xHeight = 512
        descent = 356
        ascent = xHeight + descent

        f.ascent  = ascent
        f.descent = descent
        # f.em = 1024
        
        this.singlet_enlog_semiverbose(f)

        this.singlet_init_notdefglyph(f)

        # f.selection[84 ] = True
        # raise (fontforge.logWarning(str(tuple(f.selection) ) ) , TypeError() )[1]
        # f.selection[84 ] = False

        if False :
          for charI in range(29, 512) :
            #

            glyphSk = f.createChar(charI )
            #
            glyphSk.clear()

            height = ascent

            pen = glyphSk.glyphPen()
            pen.moveTo((100,100))                 # draw a square
            pen.lineTo((500,height))
            pen.lineTo((iWeight,height))
            pen.lineTo((iWeight,100))
            pen.closePath()
            pen = None

            if shallBeItalic :
              # f.selection = (charI, )
              f.selection[charI ] = True
              f.italicize(italic_angle=15 )
              f.stroke("circular", 29 )
              f.selection[charI ] = False

          #
        #

        # SPACE
        for cp in (0x20, 0xA0, ) :
          glyphSk = f.createChar(cp )
          glyphSk.clear()
          glyphSk.width = descent
        #

        # COMBINING DOT ABOVE
        strokeWidth = round(0.55 * iWeight)
        glyphSk = f.createChar(0x307 )
        glyphSk.clear()
        glyphSk.width = 2
        pen = glyphSk.glyphPen()
        pen.moveTo((            0, ascent  ))                 # draw a square
        pen.lineTo((            0, round(ascent + -min((ascent - xHeight) / 2 , strokeWidth ) ) ))
        pen = None
        # glyphSk.stroke("elliptical", width = strokeWidth, minor_width = 1 , )
        # glyphSk.stroke("circular", width = strokeWidth, )
        glyphSk.stroke("circular", width = strokeWidth, cap="butt" )

        # DOTLESS U
        strokeWidth = round(0.45 * iWeight)
        # the counter width - the distance between the two main stems of 'n'.
        eaw = round(500 )
        advanceWidth = eaw

        for (cc, loopCount, inset, inlineEndSideInset, nHeight) in (
          # 
          (icls + cci, loopCount, inset, inlineEndSideInset, nHeightImpl )

          for (icls, (inset, inlineEndSideInset, nHeightImpl), ) in (
            (0x40, (100, 90, round(1.5 * xHeight)) ),
            (0x60, (100, 275,             xHeight) ),
          )
          for (cci, loopCount ) in (
            (21, 1, ) ,
            (13, 2, ) , 
          )
        ) :
          #
          
          eaw = round(600 - inlineEndSideInset )
          advanceWidth = inset + (loopCount * eaw) + inlineEndSideInset

          glyphSk: fontforge.glyph = f.createChar(cc )
          glyphSk.clear()

          glyphSk.width = advanceWidth
          # cannot `contour.draw` ATM.
          ct = fontforge.contour()
          class ss() :
            def __iter__(this) :
              #
              cw = (eaw - inset)

              # the relevant Py API reference page was not very clear -
              # had to reach for the docs for the GUI-based itc, https://fontforge.org/docs/ui/mainviews/charview.html 
              for i in range(0, loopCount + 1) :
                #  
                if i == 0 :
                  yield (inset + (i * eaw)       , nHeight + 3, fontforge.spiroOpen , 0 )
                yield (inset + (i * eaw)         , nHeight, fontforge.spiroCorner , 0 )
                if loopCount <= i :
                  yield (inset + (i * eaw)         ,       0, fontforge.spiroCorner     , 0 )
                  break
                yield (round(inset + (i * eaw)                )   ,       20, fontforge.spiroRight , 0 )
                yield (round(inset + (i * eaw) + (50       )  )    ,      10, fontforge.spiroG2     , 0 )
                yield (round(inset + (i * eaw) + (0.5 * eaw) )     ,      80, fontforge.spiroG2     , 0 )
                pass
              pass
          #
          # print("spiro M !")
          ct.spiros = tuple(ss() )
          ct.closed = False
          # print("ct fi !")
          glyphSk.foreground += ct
          # print("ct transform !")
          # glyphSk.transform((1.008, 0, 0, 1, 0, 0, ) )
          # print("ct stroking !")
          glyphSk.stroke("circular", width = strokeWidth, cap="butt" )

        #

        f.selection[0x60 + 21 ] = True
        f.copy()
        f.selection = ()
        f.selection[0x60 + 14 ] = True
        f.paste()
        f.selection = ()

        # I AND J
        #
        # instead of directly dealing with the ASCII-specified dotted variants,
        # we work with the dotless ones, and later call "Build Pre-Composed"
        strokeWidth = round(0.5 * iWeight)
        x = 100
        advanceWidth = round(2 * x )

        for (cc, upperY, lowerY, ) in (
          (0x40 +  9, ascent - 100 , 0, ),
          (0x40 + 10, ascent - 100 , -descent, ),
          (0x131, xHeight, 0, ),
          (0x237, xHeight, -descent, ),
        ) :
          #
          
          glyphSk: fontforge.glyph = f.createChar(cc )
          glyphSk.clear()

          glyphSk.width = advanceWidth
          pen = glyphSk.glyphPen()
          pen.moveTo((x                , lowerY))
          pen.lineTo((x                , upperY))
          pen = None
          glyphSk.stroke("circular", width = strokeWidth, cap="butt" )
          # work-around the spurious reset of `width`
          glyphSk.width = advanceWidth

          glyphSk.transform((1.75, 0, 0, 1, 0, 0, ) )

        pass

        glyphSk = f.createChar(0x60 + 9 )
        glyphSk.clear()
        # pen = glyphSk.glyphPen()
        # pen = None
        glyphSk.build()

        glyphSk = f.createChar(0x60 + 10 )
        glyphSk.clear()
        glyphSk.build()

        #

        if False : fontforge.logWarning("Font:" + str(fsD) )

        f.weight = str(iWeight )
        if False : f.os2_weight = iWeight
        if False : f.sfnt_names = fsD.ffgeOtfNameTuplesFor(ffName )

        if False : fontforge.logWarning("Font: {0}, {1} ;".format(fsD, fsD.ffgeOtfNameTuplesFor(ffName ) ) )

        this.singlet_on_completed_enlog(f)

        return f
    #

    def singlet_on_completed_enlog(this, f: fontforge.font, / ) :
      #
      
      # this.singlet_enlog_semiverbose(f)

      pass

    def singlet_enlog_semiverbose(this, f: fontforge.font, / ) :
      #
      
      fontforge.logWarning(str(f.activeLayer) )

      fontforge.logWarning("Font Family Name: '{0}'".format(f.familyname ) )
      fontforge.logWarning("Font Weight: '{0}'".format(f.weight ) )
      fontforge.logWarning("Font Name: '{0}'".format(f.fontname ) )
      fontforge.logWarning("Font FullName: '{0}'".format(f.fullname ) )

      if False : fontforge.logWarning("Font Layers: '{0}'".format(tuple(f.layers) ) )
      fontforge.logWarning("Font Errors: '{0}'".format(hex(f.validate(1) ) ) )

    #

  #
  fs = tuple(fs() )

  destFName = "fontforged_out_{0}.otf".format(dts )




  # fs[0].generate(destFName )
  fs[0].generateTtc(destFName, fs[1:], layer="Fore" ) # needs to make `layer` explicit, otherwise the export would fail

  if False : fs[0].save(destFName + ".sfd")




  fontforge.logWarning("done, please check file {0}".format("{0} ({1} )".format(destFName, os.path.abspath(destFName ), "" ) ) )


