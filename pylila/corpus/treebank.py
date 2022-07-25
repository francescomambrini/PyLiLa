from pylila.resources import LiLaRes


class DependencyRel(LiLaRes):

    @property
    def head(self):
        pass

    @property
    def dependent(self):
        pass

    def as_triple(self):
        pass

    def __str__(self):
        pass


class WebAnnotation(LiLaRes):
    pass
