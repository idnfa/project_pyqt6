from PyQt6.QtGui import QPalette, QColor

light_palette = QPalette()
light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))

green_palette = QPalette()
green_palette.setColor(QPalette.ColorRole.Window, QColor(148, 179, 121))
green_palette.setColor(QPalette.ColorRole.Base, QColor(194, 212, 184))
green_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))

yellow_palette = QPalette()
yellow_palette.setColor(QPalette.ColorRole.Window, QColor(252, 234, 167))
yellow_palette.setColor(QPalette.ColorRole.Base, QColor(255, 247, 217))
yellow_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))

red_palette = QPalette()
red_palette.setColor(QPalette.ColorRole.Window, QColor(247, 216, 205))
red_palette.setColor(QPalette.ColorRole.Base, QColor(250, 219, 200))
red_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))

dark_palette = QPalette()
dark_palette.setColor(QPalette.ColorRole.Window, QColor(90, 90, 90))
dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
dark_palette.setColor(QPalette.ColorRole.Base, QColor(141, 150, 161))
dark_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))


PALETTES = {'light': light_palette, 'green': green_palette, 'yellow': yellow_palette, 'red': red_palette,
            'dark': dark_palette}
