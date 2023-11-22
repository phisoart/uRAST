from .ImageProcessing import ImageProcessing as qmapIP
from .Reporting import Reporting as report

beads = {
    0: {"x": None, "y": None, "r": None, "brightness": None, "ID": None}
}


def qmap(_src, _dst):
    print('start QmapID')
    img_bf = _src + '/Qmap_BF.png'
    img_pe = _src + '/Qmap_PE.png'

    qmapIP.circle_detection(img_bf, beads, _dst)
    qmapIP.extract_bead_brightness(img_pe, beads)
    qmapIP.bead_decoding(img_bf, beads, _dst)
    report.qmap_reporting(beads, _dst)
