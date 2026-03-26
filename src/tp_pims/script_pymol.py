from pymol import cmd
import pymol
from tp_pims.config import TP_PATH

pymol.finish_launching(['pymol', '-q'])

cmd.load(TP_PATH / "data" / "AF-Q8U442-F1-model_v6.pdb")
cmd.select("helix_alpha", "resi 32-44")
cmd.color("cyan", "helix_alpha")

cmd.select("beta_sheet", "resi 2-11")
cmd.color("red", "beta_sheet")
cmd.deselect()
cmd.set("seq_view", 1)