from global_objects import root
import build_interface
from utils import recalculate


root.title("Фракталы")
root.iconbitmap("icon.ico")

root.update()
recalculate()


root.mainloop()
