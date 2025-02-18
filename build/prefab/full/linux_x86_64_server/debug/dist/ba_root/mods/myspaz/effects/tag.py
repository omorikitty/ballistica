import babase
import bascenev1 as bs
from typing import Sequence

icons = {
    '\\d': ('\ue048'),
    '\\c': ('\ue043'),
    '\\h': ('\ue049'),
    '\\s': ('\ue046'),
    '\\n': ('\ue04b'),
    '\\f': ('\ue04f'),
    '\\g': ('\ue027'),
    '\\i': ('\ue03a'),
    '\\m': ('\ue04d'),
    '\\t': ('\ue01f'),
    '\\bs': ('\ue01e'),
    '\\j': ('\ue010'),
    '\\e': ('\ue045'),
    '\\l': ('\ue047'),
    '\\a': ('\ue020'),
    '\\b': ('\ue00c'),
}

class CustomTag(object):
    def __init__(self, 
                 owner=None, 
                 tag="somthing", 
                 col=(1, 1, 1),
                 animate: bool = False,
                 animate_array: dict[float, tuple[float, float, float]] = {}
        ):
        self.node = owner

        mnode = bs.newnode('math',
                           owner=self.node,
                           attrs={
                               'input1': (0, 1.5, 0),
                               'operation': 'add'
                           })
        self.node.connectattr('torso_position', mnode, 'input2')

        for prefix, code in icons.items():
            if '\\' in tag:
                tag = tag.replace(prefix, code)
                break

        self.tag_text = bs.newnode('text',
                                   owner=self.node,
                                   attrs={
                                       'text': tag,
                                       'in_world': True,
                                       'shadow': 1.0,
                                       'flatness': 1.0,
                                       'color': tuple(col),
                                       'scale': 0.01,
                                       'h_align': 'center'
                                   })
        mnode.connectattr('output', self.tag_text, 'position')
        if animate:
            bs.animate_array(node=self.tag_text, attr='color', size=3, keys=animate_array, loop=True)